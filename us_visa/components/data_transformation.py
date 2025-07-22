import sys
import numpy as np
import pandas as pd
from imblearn.combine import SMOTEENN
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder, OrdinalEncoder, PowerTransformer, LabelEncoder
from sklearn.compose import ColumnTransformer

from us_visa.constants import TARGET_COLUMN, SCHEMA_FILE_PATH, CURRENT_YEAR
from us_visa.entity.config_entity import DataTransformationConfig
from us_visa.entity.artifact_entity import DataTransformationArtifact, DataIngestionArtifacts, DataValidationArtifact
from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import save_object, save_numpy_array_data, read_yaml_file, drop_columns
from us_visa.entity.estimator import TargetValueMapping


class DataTransformation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts,
                 data_transformation_config: DataTransformationConfig,
                 data_validation_artifact: DataValidationArtifact):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_transformation_config = data_transformation_config
            self.data_validation_artifact = data_validation_artifact
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)

    def get_data_transformer_object(self) -> Pipeline:
        logging.info("Entered get_data_transformer_object method of DataTransformation class")
        try:
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder()
            ordinal_encoder = OrdinalEncoder()

            oh_columns = self._schema_config['oh_columns']
            or_columns = self._schema_config['or_columns']
            transform_columns = self._schema_config['transform_columns']
            num_features = self._schema_config['num_features']

            transform_pipe = Pipeline(steps=[
                ('transformer', PowerTransformer(method='yeo-johnson'))
            ])

            preprocessor = ColumnTransformer([
                ("OneHotEncoder", oh_transformer, oh_columns),
                ("Ordinal_Encoder", ordinal_encoder, or_columns),
                ("Transformer", transform_pipe, transform_columns),
                ("StandardScaler", numeric_transformer, num_features)
            ])

            logging.info("Created preprocessor object from ColumnTransformer")
            logging.info("Exited get_data_transformer_object method of DataTransformation class")
            return preprocessor

        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            if not self.data_validation_artifact.validation_status:
                raise Exception(self.data_validation_artifact.message)

            logging.info("Starting data transformation")
            preprocessor = self.get_data_transformer_object()

            train_df = self.read_data(self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(self.data_ingestion_artifact.test_file_path)

            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]

            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]

            logging.info("Got train and test features")

            # Add company_age
            input_feature_train_df['company_age'] = CURRENT_YEAR - input_feature_train_df['yr_of_estab']
            input_feature_test_df['company_age'] = CURRENT_YEAR - input_feature_test_df['yr_of_estab']

            # Drop unwanted columns
            drop_cols = self._schema_config['drop_columns']
            input_feature_train_df = drop_columns(input_feature_train_df, drop_cols)
            input_feature_test_df = drop_columns(input_feature_test_df, drop_cols)

            logging.info("Dropped columns and added company_age")

            # Map target column using TargetValueMapping
            try:
                # Normalize labels (remove extra spaces, fix casing)
                target_feature_train_df = target_feature_train_df.str.strip().str.capitalize()
                target_feature_test_df = target_feature_test_df.str.strip().str.capitalize()

                # Map Certified -> 1, Denied -> 0
                mapping = TargetValueMapping()._asdict()
                logging.info(f"Target mapping used: {mapping}")
                target_feature_train_df = target_feature_train_df.replace(mapping).astype(int)
                target_feature_test_df = target_feature_test_df.replace(mapping).astype(int)

            except Exception as e:
                logging.warning(f"Target mapping failed: {e}, falling back to LabelEncoder")

                label_encoder = LabelEncoder()
                target_feature_train_df = label_encoder.fit_transform(target_feature_train_df)
                target_feature_test_df = label_encoder.transform(target_feature_test_df)

            # Transform features
            logging.info("Applying preprocessing object on train/test features")
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            # Apply SMOTEENN
            logging.info("Applying SMOTEENN to balance classes")
            smt = SMOTEENN(sampling_strategy="minority")

            input_feature_train_final, target_feature_train_final = smt.fit_resample(
                input_feature_train_arr, target_feature_train_df)

            input_feature_test_final, target_feature_test_final = smt.fit_resample(
                input_feature_test_arr, target_feature_test_df)

            # Combine inputs + targets
            train_arr = np.c_[input_feature_train_final, target_feature_train_final]
            test_arr = np.c_[input_feature_test_final, target_feature_test_final]

            # Save transformed objects and arrays
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor)
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, train_arr)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, test_arr)

            logging.info("Saved transformed arrays and preprocessor successfully")

            return DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

        except Exception as e:
            raise USvisaException(e, sys) from e