from typing import Union
from age_distribution_module import get_age_distribution
from gender_distribution_module import get_gender_distribution
from medical_condition_frequency import plot_categorical_frequency
from MIA.tumour_detect import predict_tumor
from fastapi import FastAPI, File, UploadFile, HTTPException
import base64
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (not recommended for production)
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


@app.get("/ageDistribution")
def read_root():
    result = get_age_distribution("./mockData/patientDetails.csv")
    return result

@app.get("/genderDistribution")
def read_root():
    result = get_gender_distribution("./mockData/patientDetails.csv")
    return result

@app.get("/medicalConditionFreq")
def read_root():
    result = plot_categorical_frequency("./mockData/patientDetails.csv", 'medicalHistory.condition')
    return result
  
@app.post("/MIA")
async def read_root(file: UploadFile = File(...)):
    contents = await file.read()

    base64_image = base64.b64encode(contents).decode("utf-8")

    try:
        response = predict_tumor(base64_image)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))