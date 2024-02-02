import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

def calculate_age(dob):
    dob_date = datetime.strptime(dob, "%m/%d/%Y")
    today = datetime.now()
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return age

def create_age_distribution(ages):
    age_distribution = {}
    for age in ages:
        age_range = str((age // 10) * 10)  # Group ages in a 10-year range
        age_distribution[age_range] = age_distribution.get(age_range, 0) + 1

    return age_distribution

def get_age_distribution(file_path):
    # Load data from CSV file
    df = pd.read_csv(file_path)

    # Calculate age for each patient
    df['age'] = df['dateOfBirth'].apply(calculate_age)

    # Create age distribution
    age_distribution = create_age_distribution(df['age'])

    # Convert age distribution to the required format for Mantine UI
    max_age = max(map(int, age_distribution.keys()))
    result = [{"age": str(age), "count": age_distribution.get(str(age), 0)} for age in range(0, max_age + 1, 10)]

    return result

def get_gender_distribution(file_path):
    # Load data from CSV file
    df = pd.read_csv(file_path)

    # Get data in array of objects format
    gender_distribution = df['gender'].value_counts().reset_index()
    gender_distribution.columns = ['gender', 'count']
    data_array = gender_distribution.to_dict(orient='records')

    # Return the data array
    return data_array
