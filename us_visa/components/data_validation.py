import json
import sys
import pandas as pd
from pandas import DataFrame
from evidently.report import Report
from evidently.metric_preset import DataDriftPreset

from us_visa.exception import USvisaException
from us_visa.logger import logging
from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
from us_visa.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifact
from us_visa.entity.config_entity import DataValidationConfig
from us_visa.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, data_validation_config: DataValidationConfig):
        """
        :param data_ingestion_artifact: Output reference of data ingestion artifact stage
        :param data_validation_config: configuration for data validation
        """
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
        except Exception as e:
            raise USvisaException(e, sys)

    def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
        try:
            status = len(dataframe.columns) == len(self._schema_config["columns"])
            logging.info(f"Is required column present: [{status}]")
            return status
        except Exception as e:
            raise USvisaException(e, sys)

    def is_column_exist(self, df: DataFrame) -> bool:
        try:
            dataframe_columns = df.columns
            missing_numerical_columns = []
            missing_categorical_columns = []

            for column in self._schema_config["numerical_columns"]:
                if column not in dataframe_columns:
                    missing_numerical_columns.append(column)

            if missing_numerical_columns:
                logging.info(f"Missing numerical columns: {missing_numerical_columns}")

            for column in self._schema_config["categorical_columns"]:
                if column not in dataframe_columns:
                    missing_categorical_columns.append(column)

            if missing_categorical_columns:
                logging.info(f"Missing categorical columns: {missing_categorical_columns}")

            return not (missing_numerical_columns or missing_categorical_columns)
        except Exception as e:
            raise USvisaException(e, sys)

    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise USvisaException(e, sys)

    def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
        """
        Method Name :   detect_dataset_drift
        Description :   This method validates if drift is detected
        """
        try:
            report = Report(metrics=[DataDriftPreset()])
            report.run(reference_data=reference_df, current_data=current_df)

            report_data = report.as_dict()

            write_yaml_file(
                file_path=self.data_validation_config.drift_report_file_path,
                content=report_data
            )

            n_features = report_data["metrics"][0]["result"]["number_of_columns"]
            n_drifted = report_data["metrics"][0]["result"]["number_of_drifted_columns"]
            dataset_drift = report_data["metrics"][0]["result"]["dataset_drift"]

            logging.info(f"{n_drifted}/{n_features} features drifted. Drift status: {dataset_drift}")
            return dataset_drift
        except Exception as e:
            raise USvisaException(e, sys) from e

    def initiate_data_validation(self) -> DataValidationArtifact:
        """
        Method Name :   initiate_data_validation
        Description :   This method initiates the data validation component for the pipeline
        """
        try:
            validation_error_msg = ""
            logging.info("Starting data validation")

            train_df = self.read_data(file_path=self.data_ingestion_artifact.trained_file_path)
            test_df = self.read_data(file_path=self.data_ingestion_artifact.test_file_path)

            if not self.validate_number_of_columns(train_df):
                validation_error_msg += "Columns are missing in training dataframe. "

            if not self.validate_number_of_columns(test_df):
                validation_error_msg += "Columns are missing in test dataframe. "

            if not self.is_column_exist(train_df):
                validation_error_msg += "Some required columns are missing in training dataframe. "

            if not self.is_column_exist(test_df):
                validation_error_msg += "Some required columns are missing in test dataframe. "

            validation_status = len(validation_error_msg.strip()) == 0

            if validation_status:
                drift_status = self.detect_dataset_drift(train_df, test_df)
                if drift_status:
                    validation_error_msg = "Drift detected"
                    logging.info("⚠️ Drift detected in dataset.")
                else:
                    validation_error_msg = "Drift not detected"
                    logging.info("✅ No drift detected in dataset.")
            else:
                logging.info(f"Validation errors: {validation_error_msg}")

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg.strip(),
                drift_report_file_path=self.data_validation_config.drift_report_file_path
            )

            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise USvisaException(e, sys) from e


# import json
# import sys
# import pandas as pd
# import os 

# # ✅ UPDATED IMPORTS FOR EVIDENTLY 0.3.x+
# from evidently.report import Report
# from evidently.metric_preset import DataDriftPreset
# from evidently.pipeline.column_mapping import ColumnMapping

# from pandas import DataFrame
# from us_visa.exception import USvisaException
# from us_visa.logger import logging
# from us_visa.utils.main_utils import read_yaml_file, write_yaml_file
# from us_visa.entity.artifact_entity import DataIngestionArtifacts, DataValidationArtifact
# from us_visa.entity.config_entity import DataValidationConfig
# from us_visa.constants import SCHEMA_FILE_PATH
# from us_visa.entity.artifact_entity import DataValidationArtifact
# from us_visa.entity.artifact_entity import DataValidationArtifact  # Make sure this is imported



# class DataValidation:
#     def __init__(self, data_ingestion_artifact: DataIngestionArtifacts, data_validation_config: DataValidationConfig):
#         try:
#             self.data_ingestion_artifact = data_ingestion_artifact
#             self.data_validation_config = data_validation_config
#             self._schema_config = read_yaml_file(file_path=SCHEMA_FILE_PATH)
#         except Exception as e:
#             raise USvisaException(e, sys)
# class DataValidation:
#     def __init__(self, data_validation_config, data_ingestion_artifact):
#         self.data_validation_config = data_validation_config
#         self.data_ingestion_artifact = data_ingestion_artifact

#     def validate_number_of_columns(self, dataframe: DataFrame) -> bool:
#         try:
#             status = len(dataframe.columns) == len(self._schema_config["columns"])
#             logging.info(f"Is required column present: [{status}]")
#             return status
#         except Exception as e:
#             raise USvisaException(e, sys)

#     def is_column_exist(self, df: DataFrame) -> bool:
#         try:
#             dataframe_columns = df.columns
#             missing_numerical_columns = []
#             missing_categorical_columns = []
#             for column in self._schema_config["numerical_columns"]:
#                 if column not in dataframe_columns:
#                     missing_numerical_columns.append(column)

#             if len(missing_numerical_columns) > 0:
#                 logging.info(f"Missing numerical column: {missing_numerical_columns}")

#             for column in self._schema_config["categorical_columns"]:
#                 if column not in dataframe_columns:
#                     missing_categorical_columns.append(column)

#             if len(missing_categorical_columns) > 0:
#                 logging.info(f"Missing categorical column: {missing_categorical_columns}")

#             return False if missing_categorical_columns or missing_numerical_columns else True
#         except Exception as e:
#             raise USvisaException(e, sys) from e

#     @staticmethod
#     def read_data(file_path) -> DataFrame:
#         try:
#             return pd.read_csv(file_path)
#         except Exception as e:
#             raise USvisaException(e, sys)

    # def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
    #     try:
    #         report = Report(metrics=[DataDriftPreset()])
    #         report.run(reference_data=reference_df, current_data=current_df)
    #         report_json = report.as_dict()
    #         write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=report_json)

    #         # ❌ OLD CODE (ERROR — causes KeyError if 'metrics' not present)
    #         # n_features = report_json["metrics"][0]["result"]["metrics"]["n_features"]

    #         # ✅ NEW FIXED CODE BLOCK
    #         metrics_list = report_json.get("metrics", [])
    #         if not metrics_list:
    #             logging.error("❌ 'metrics' key missing or empty in report_json.")
    #             logging.debug(f"Full report_json: {json.dumps(report_json, indent=2)}")
    #             raise Exception("❌ 'metrics' key missing in Evidently report. Check your data or report generation.")

    #         metrics_data = metrics_list[0].get("result", {}).get("metrics", {})
    #         n_features = metrics_data.get("n_features")
    #         n_drifted_features = metrics_data.get("n_drifted_features")
    #         drift_status = metrics_data.get("dataset_drift")

    #         if n_features is None or n_drifted_features is None or drift_status is None:
    #             logging.error("❌ Some expected keys are missing in metrics.")
    #             logging.debug(f"metrics_data: {json.dumps(metrics_data, indent=2)}")
    #             raise Exception("❌ Incomplete metrics data in Evidently report.")

    #         logging.info(f"✅ Drift detected in {n_drifted_features}/{n_features} features.")
    #         return drift_status
    #     except Exception as e:
    #         raise USvisaException(e, sys) from e


    
# def detect_dataset_drift(self, reference_df: DataFrame, current_df: DataFrame) -> bool:
#     try:
#         # 🟩 Validate input DataFrames
#         if reference_df.empty or current_df.empty:
#             raise Exception("❌ Reference or current DataFrame is empty.")

#         if set(reference_df.columns) != set(current_df.columns):  # 🟩 Safer column check
#             raise Exception("❌ Train and Test DataFrames have mismatched columns.")

#         report = Report(metrics=[DataDriftPreset()])
#         report.run(reference_data=reference_df, current_data=current_df)
#         report_json = report.as_dict()

#         # 🟩 Ensure the directory exists before saving files
#         drift_report_html_path = self.data_validation_config.drift_report_file_path.replace('.yaml', '.html')
#         os.makedirs(os.path.dirname(drift_report_html_path), exist_ok=True)  # ✅ ✅ CREATE FOLDER IF MISSING

#         # 🟩 Save HTML for visual debug
#         report.save_html(drift_report_html_path)

#         # 🟩 Save YAML output
#         write_yaml_file(file_path=self.data_validation_config.drift_report_file_path, content=report_json)

#         # 🟩 Handle missing metrics
#         metrics_list = report_json.get("metrics", [])
#         if not metrics_list:
#             raise Exception("❌ 'metrics' missing from Evidently report.")

#         metrics_data = metrics_list[0].get("result", {}).get("metrics", {})
#         n_features = metrics_data.get("n_features")
#         n_drifted_features = metrics_data.get("n_drifted_features")
#         drift_status = metrics_data.get("dataset_drift")

#         # 🟩 Validate all fields exist
#         if None in (n_features, n_drifted_features, drift_status):
#             raise Exception("❌ Incomplete metrics data in Evidently report.")

#         logging.info(f"✅ Drift detected in {n_drifted_features}/{n_features} features.")
#         return drift_status

#     except Exception as e:
#         raise USvisaException(e, sys)

    
# def initiate_data_validation(self) -> DataValidationArtifact:
#         """
#         Method Name :   initiate_data_validation
#         Description :   This method initiates the data validation component for the pipeline
        
#         Output      :   Returns bool value based on validation results
#         On Failure  :   Write an exception log and then raise an exception
#         """

#         try:
#             validation_error_msg = ""
#             logging.info("Starting data validation")
#             train_df, test_df = (DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
#                                  DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))

#             status = self.validate_number_of_columns(dataframe=train_df)
#             logging.info(f"All required columns present in training dataframe: {status}")
#             if not status:
#                 validation_error_msg += f"Columns are missing in training dataframe."
#             status = self.validate_number_of_columns(dataframe=test_df)

#             logging.info(f"All required columns present in testing dataframe: {status}")
#             if not status:
#                 validation_error_msg += f"Columns are missing in test dataframe."

#             status = self.is_column_exist(df=train_df)

#             if not status:
#                 validation_error_msg += f"Columns are missing in training dataframe."
#             status = self.is_column_exist(df=test_df)

#             if not status:
#                 validation_error_msg += f"columns are missing in test dataframe."

#             validation_status = len(validation_error_msg) == 0

#             if validation_status:
#                 drift_status = self.detect_dataset_drift(train_df, test_df)
#                 if drift_status:
#                     logging.info(f"Drift detected.")
#                     validation_error_msg = "Drift detected"
#                 else:
#                     validation_error_msg = "Drift not detected"
#             else:
#                 logging.info(f"Validation_error: {validation_error_msg}")
                

#             data_validation_artifact = DataValidationArtifact(
#                 validation_status=validation_status,
#                 message=validation_error_msg,
#                 drift_report_file_path=self.data_validation_config.drift_report_file_path
#             )

#             logging.info(f"Data validation artifact: {data_validation_artifact}")
#             return data_validation_artifact
#         except Exception as e:
#             raise USvisaException(e, sys) from e

# def initiate_data_validation(self) -> DataValidationArtifact:
#     print("✅ initiate_data_validation() called")

#     # Example logic — replace with actual validation logic
#     schema_path = self.data_validation_config.schema_file_path
#     report_path = self.data_validation_config.report_file_path
#     report_page_path = self.data_validation_config.report_page_file_path

#         # Create and return a dummy artifact for now
#     return DataValidationArtifact(
#         schema_file_path=schema_path,
#         report_file_path=report_path,
#         report_page_file_path=report_page_path
#     )

