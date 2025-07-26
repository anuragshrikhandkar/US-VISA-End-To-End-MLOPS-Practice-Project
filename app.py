from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import numpy as np
from starlette.responses import HTMLResponse
from uvicorn import run as app_run
from typing import Optional

from us_visa.constants import APP_HOST, APP_PORT
from us_visa.pipline.prediction_pipeline import USvisaData, USvisaClassifier
from us_visa.pipline.training_pipeline import TrainPipeline

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory='templates')

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Form data class
class DataForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.continent: Optional[str] = None
        self.education_of_employee: Optional[str] = None
        self.has_job_experience: Optional[str] = None
        self.requires_job_training: Optional[str] = None
        self.no_of_employees: Optional[str] = None
        self.company_age: Optional[str] = None
        self.region_of_employment: Optional[str] = None
        self.prevailing_wage: Optional[str] = None
        self.unit_of_wage: Optional[str] = None
        self.full_time_position: Optional[str] = None

    async def get_usvisa_data(self):
        form = await self.request.form()
        self.continent = form.get("continent")
        self.education_of_employee = form.get("education_of_employee")
        self.has_job_experience = form.get("has_job_experience")
        self.requires_job_training = form.get("requires_job_training")
        self.no_of_employees = form.get("no_of_employees")
        self.company_age = form.get("company_age")
        self.region_of_employment = form.get("region_of_employment")
        self.prevailing_wage = form.get("prevailing_wage")
        self.unit_of_wage = form.get("unit_of_wage")
        self.full_time_position = form.get("full_time_position")

# Home route
@app.get("/", tags=["authentication"])
async def index(request: Request):
    return templates.TemplateResponse("usvisa.html", {"request": request, "context": "Rendering"})

# Train route
@app.get("/train")
async def trainRouteClient():
    try:
        train_pipeline = TrainPipeline()
        train_pipeline.run_pipeline()
        return Response("Training successful !!")
    except Exception as e:
        return Response(f"Error Occurred! {e}")

# Predict route
@app.post("/")
async def predictRouteClient(request: Request):
    try:
        form = DataForm(request)
        await form.get_usvisa_data()

        usvisa_data = USvisaData(
            continent=form.continent,
            education_of_employee=form.education_of_employee,
            has_job_experience=form.has_job_experience,
            requires_job_training=form.requires_job_training,
            no_of_employees=form.no_of_employees,
            company_age=form.company_age,
            region_of_employment=form.region_of_employment,
            prevailing_wage=form.prevailing_wage,
            unit_of_wage=form.unit_of_wage,
            full_time_position=form.full_time_position,
        )

        usvisa_df = usvisa_data.get_usvisa_input_data_frame()
        print("Input DataFrame:\n", usvisa_df)

        model_predictor = USvisaClassifier()
        prediction = model_predictor.predict(dataframe=usvisa_df)
        print("Model Raw Prediction:", prediction)

        # 🔁 UPDATED: Handle raw string or numeric predictions
        prediction_value = prediction[0] if isinstance(prediction, (np.ndarray, list)) else prediction

        if isinstance(prediction_value, str):
            result = prediction_value
        elif prediction_value == 1:
            result = "Visa Approved ✅"
        elif prediction_value == 0:
            result = "Visa Not-Approved ❌"
        else:
            raise ValueError(f"Unexpected prediction value: {prediction_value}")

        print("Visa Prediction Result:", result)

        return templates.TemplateResponse(
            "usvisa.html",
            {"request": request, "context": result},
        )

    except Exception as e:
        print(f"Prediction Error: {e}")
        return {"status": False, "error": str(e)}

# Run app
if __name__ == "__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)


# from fastapi import FastAPI,Request,Form
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse
# import pandas as pd 
# import numpy as np
# from us_visa.pipline.prediction_pipeline import USvisaClassifier
# from us_visa.utils.main_utils import load_object

# app = FastAPI()
# templates = Jinja2Templates(directory="templates")

# # Load your trained model
# model = USvisaClassifier()  # <- use actual model path

# @app.get("/", response_class=HTMLResponse)
# async def home(request: Request):
#     return templates.TemplateResponse("index.html", {"request": request, "result": None})

# @app.post("/", response_class=HTMLResponse)
# async def predict(request: Request):
#     form = await request.form()

#     # Collect form data
#     input_data = {
#         "continent": [form.get("continent")],
#         "education_of_employee": [form.get("education_of_employee")],
#         "has_job_experience": [form.get("has_job_experience")],
#         "requires_job_training": [form.get("requires_job_training")],
#         "no_of_employees": [form.get("no_of_employees")],
#         "region_of_employment": [form.get("region_of_employment")],
#         "prevailing_wage": [float(form.get("prevailing_wage"))],
#         "unit_of_wage": [form.get("unit_of_wage")],
#         "full_time_position": [form.get("full_time_position")],
#         "company_age": [int(form.get("company_age"))]
#     }

#     input_df = pd.DataFrame.from_dict(input_data)
#     prediction = model.predict(input_df)

#     # Correct interpretation of result
#     result = "Visa Approved" if int(prediction[0]) == 1 else "Visa Not Approved"

#     return templates.TemplateResponse("index.html", {"request": request, "result": result})



  # print("Model Raw Prediction:", prediction)  # ✅ DEBUG: log model prediction

        # if (prediction) == 1:  # ✅ FIXED: ensure prediction is int not string
        #     status = "Visa Approved ✅"
        # else:
        #     status = "Visa Not-Approved ❌"

        # prediction = model.predict(dataframe=input_df)
