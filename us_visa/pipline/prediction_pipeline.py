import os
import sys
import pickle
import pandas as pd
from pandas import DataFrame
from us_visa.exception import USvisaException
from us_visa.logger import logging

# ---------- USvisaData Class ----------
class USvisaData:
    def __init__(self,
                 continent,
                 education_of_employee,
                 has_job_experience,
                 requires_job_training,
                 no_of_employees,
                 region_of_employment,
                 prevailing_wage,
                 unit_of_wage,
                 full_time_position,
                 company_age):
        try:
            self.continent = continent
            self.education_of_employee = education_of_employee
            self.has_job_experience = has_job_experience
            self.requires_job_training = requires_job_training
            self.no_of_employees = no_of_employees
            self.region_of_employment = region_of_employment
            self.prevailing_wage = prevailing_wage
            self.unit_of_wage = unit_of_wage
            self.full_time_position = full_time_position
            self.company_age = company_age
        except Exception as e:
            raise USvisaException(e, sys) from e

    def get_usvisa_data_as_dict(self):
        try:
            input_data = {
                "continent": [self.continent],
                "education_of_employee": [self.education_of_employee],
                "has_job_experience": [self.has_job_experience],
                "requires_job_training": [self.requires_job_training],
                "no_of_employees": [self.no_of_employees],
                "region_of_employment": [self.region_of_employment],
                "prevailing_wage": [self.prevailing_wage],
                "unit_of_wage": [self.unit_of_wage],
                "full_time_position": [self.full_time_position],
                "company_age": [self.company_age],
            }
            return input_data
        except Exception as e:
            raise USvisaException(e, sys) from e

    def get_usvisa_input_data_frame(self) -> DataFrame:
        try:
            data_dict = self.get_usvisa_data_as_dict()
            return DataFrame(data_dict)
        except Exception as e:
            raise USvisaException(e, sys) from e

# artifact/07_26_2025_16_33_46/model_trainer/trained_model/model.pkl
# ---------- USvisaClassifier Class ----------
class USvisaClassifier:
    def __init__(self, model_path: str = "artifact/07_26_2025_16_33_46/model_trainer/trained_model/model.pkl") -> None:
        try:
            self.model_path = model_path
            if not os.path.exists(self.model_path):
                raise FileNotFoundError(f"Model file not found at {self.model_path}")
            with open(self.model_path, "rb") as f:
                self.model = pickle.load(f)
        except Exception as e:
            raise USvisaException(e, sys) from e
##prediction output 
    def predict(self, input_df: pd.DataFrame = None, dataframe: pd.DataFrame = None) -> str:
        try:
            logging.info("Entered predict method of USvisaClassifier class")

            # Accept either input_df or dataframe
            if dataframe is not None:
                input_df = dataframe

            if input_df is None:
                raise ValueError("No input DataFrame provided for prediction.")

            # Fill missing values
            input_df["continent"] = input_df["continent"].fillna("Asia")
            input_df["education_of_employee"] = input_df["education_of_employee"].fillna("Bachelor's")
            input_df["has_job_experience"] = input_df["has_job_experience"].fillna("YES")
            input_df["requires_job_training"] = input_df["requires_job_training"].fillna("NO")
            input_df["no_of_employees"] = input_df["no_of_employees"].fillna("51-200")
            input_df["region_of_employment"] = input_df["region_of_employment"].fillna("Northeast")
            input_df["prevailing_wage"] = input_df["prevailing_wage"].fillna(50000)
            input_df["unit_of_wage"] = input_df["unit_of_wage"].fillna("Year")
            input_df["full_time_position"] = input_df["full_time_position"].fillna("Y")
            input_df["company_age"] = input_df["company_age"].fillna(10)

            # Debug (optional)
            print("Input DataFrame:\n", input_df)

            # Prediction
            prediction = self.model.predict(input_df)
            print("Model Raw Prediction:", prediction)

            # return "Visa Approved ✅" if prediction[0] == 1 else "Visa Not Approved ❌"
            return "Visa Approved ✅" if int(round(prediction[0])) == 1 else "Visa Not Approved ❌"
        except Exception as e:
            raise USvisaException(e, sys) from e



    







           # def predict(self, dataframe) -> str:
#     #     """
#     #     Predict visa approval status.
#     #     """
#     #     try:
#     #         logging.info("Entered predict method of USvisaClassifier class")
#     #         prediction = self.model.predict(dataframe)

#     #         return "Approved" if prediction[0] == 1 else "Rejected"

#     #     except Exception as e:
#     #         raise USvisaException(e, sys)

        
#     # def predict(self, dataframe) -> str:
#     #     try:
#     #          logging.info("Entered predict method of USvisaClassifier class")
        
#     #     # Avoid unknown categories crash
#     #          dataframe.fillna("Unknown", inplace=True)

#     #          prediction = self.model.predict(dataframe)
#     #          return "Visa Approved ✅" if prediction[0] == 1 else "Visa Not Approved ❌"

#     #     except Exception as e:
#     #         raise USvisaException(e, sys)


##Testing code not for Production 

# import pandas as pd
# import joblib

# class USvisaData:
#     def __init__(
#         self,
#         continent,
#         education_of_employee,
#         has_job_experience,
#         requires_job_training,
#         no_of_employees,
#         region_of_employment,
#         prevailing_wage,
#         unit_of_wage,
#         full_time_position,
#         company_age,
#     ):
#         self.continent = continent
#         self.education_of_employee = education_of_employee
#         self.has_job_experience = has_job_experience
#         self.requires_job_training = requires_job_training
#         self.no_of_employees = no_of_employees
#         self.region_of_employment = region_of_employment
#         self.prevailing_wage = prevailing_wage
#         self.unit_of_wage = unit_of_wage
#         self.full_time_position = full_time_position
#         self.company_age = company_age

#     def to_dataframe(self):
#         return pd.DataFrame([{
#             "continent": self.continent,
#             "education_of_employee": self.education_of_employee,
#             "has_job_experience": self.has_job_experience,
#             "requires_job_training": self.requires_job_training,
#             "no_of_employees": self.no_of_employees,
#             "region_of_employment": self.region_of_employment,
#             "prevailing_wage": self.prevailing_wage,
#             "unit_of_wage": self.unit_of_wage,
#             "full_time_position": self.full_time_position,
#             "company_age": self.company_age,
#         }])

#     def get_usvisa_input_data_frame(self):
#         return self.to_dataframe()

# class USvisaClassifier:
#     def __init__(self, model_path: str = "artifact/07_25_2025_14_52_42/model_trainer/trained_model/model.pkl"):
#         self.model = joblib.load(model_path)

#     def predict(self, input_df: pd.DataFrame) -> str:
#         prediction = self.model.predict(input_df)
#         return "Visa Approved ✅" if prediction[0] == 1 else "Visa Not Approved ❌"

# # Example usage
# if __name__ == "__main__":
#     input_data = USvisaData(
#         continent="Asia",
#         education_of_employee="Bachelor's",
#         has_job_experience="YES",
#         requires_job_training="NO",
#         no_of_employees="51-200",
#         region_of_employment="Northeast",
#         prevailing_wage=60000,
#         unit_of_wage="Year",
#         full_time_position="Y",
#         company_age=10
#     )

#     input_df = input_data.to_dataframe()
#     classifier = USvisaClassifier()  # Uses the full model path you provided
#     result = classifier.predict(input_df)
#     print("Visa Prediction Result:", result)



##Testing code not for production

# import pandas as pd
# import joblib

# class USvisaData:
#     def __init__(
#         self,
#         continent,
#         education_of_employee,
#         has_job_experience,
#         requires_job_training,
#         no_of_employees,
#         region_of_employment,
#         prevailing_wage,
#         unit_of_wage,
#         full_time_position,
#         company_age,
#     ):
#         self.continent = continent
#         self.education_of_employee = education_of_employee
#         self.has_job_experience = has_job_experience
#         self.requires_job_training = requires_job_training
#         self.no_of_employees = no_of_employees
#         self.region_of_employment = region_of_employment
#         self.prevailing_wage = prevailing_wage
#         self.unit_of_wage = unit_of_wage
#         self.full_time_position = full_time_position
#         self.company_age = company_age

#     def to_dataframe(self):
#         return pd.DataFrame([{
#             "continent": self.continent,
#             "education_of_employee": self.education_of_employee,
#             "has_job_experience": self.has_job_experience,
#             "requires_job_training": self.requires_job_training,
#             "no_of_employees": self.no_of_employees,
#             "region_of_employment": self.region_of_employment,
#             "prevailing_wage": self.prevailing_wage,
#             "unit_of_wage": self.unit_of_wage,
#             "full_time_position": self.full_time_position,
#             "company_age": self.company_age,
#         }])

#     def get_usvisa_input_data_frame(self):
#         return self.to_dataframe()  # For compatibility if old code uses this


# class USvisaClassifier:
#     def __init__(self, model_path: str = "artifact/07_25_2025_14_52_42/model_trainer/trained_model/model.pkl"):
#         self.model = joblib.load(model_path)

#     def predict(self, input_df: pd.DataFrame) -> str:
#         input_df.fillna(method="ffill", inplace=True)  # Fill missing if any
#         prediction = self.model.predict(input_df)
#         return "Visa Approved ✅" if prediction[0] == 1 else "Visa Not Approved ❌"


# # Example usage
# if __name__ == "__main__":
#     input_data = USvisaData(
#         continent="Asia",
#         education_of_employee="Bachelor's",
#         has_job_experience="YES",
#         requires_job_training="NO",
#         no_of_employees="51-200",
#         region_of_employment="Northeast",
#         prevailing_wage=85000,
#         unit_of_wage="Year",
#         full_time_position="Y",
#         company_age=15
#     )

#     input_df = input_data.get_usvisa_input_data_frame()  # You can also use .to_dataframe()
#     classifier = USvisaClassifier()
#     result = classifier.predict(input_df=input_df)
#   # ✅ fixed here
#     print("Visa Prediction Result:", result)