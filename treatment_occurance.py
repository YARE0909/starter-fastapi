import pandas as pd
from ast import literal_eval

def clean_treatments(treatments_str):
    try:
        return literal_eval(treatments_str)
    except (ValueError, SyntaxError):
        return []

# Load data from CSV file
file_path = './mockData/patientDetails.csv'
patients_data = pd.read_csv(file_path)

# Clean 'medicalHistory.treatments' column
patients_data['medicalHistory.treatments'] = patients_data['medicalHistory.treatments'].apply(clean_treatments)

# Flatten the list of treatments into a single list
all_treatments = sum(patients_data['medicalHistory.treatments'], [])

# Count the occurrences of each treatment
treatment_counts = pd.Series(all_treatments).value_counts()

# Convert treatment counts to the required format for Mantine UI
result = [{"date": "Mock Date", treatment: treatment_counts.get(treatment, 0)} for treatment in treatment_counts.index]

print(result)
