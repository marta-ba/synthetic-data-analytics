# -*- coding: utf-8 -*-
"""
Synthetic Staff / HR / Training Dataset for Loca Gruppen
Author: Marta Blanco (with AI support)
Exports: staff_data.xlsx
"""

import pandas as pd
import numpy as np
import random
from faker import Faker
from datetime import date, timedelta

# Initialize
fake = Faker("da_DK")
np.random.seed(42)
random.seed(42)

# -------------------------------
# 1. COMPANY STRUCTURE
# -------------------------------

RESTAURANTS = ["Almanak i Operaen", "Almanak i Kilden", "Radio", "Format", "Posthallen"]
CANTEENS = ["Langelinie Kantine", "Bankdata Kantine", "Carlsberg Kantine"]
UNITS = RESTAURANTS + CANTEENS
UNIT_TYPE = {u: ("Restaurant" if u in RESTAURANTS else "Canteen") for u in UNITS}

DEPARTMENTS = ["Kitchen", "Service", "Admin", "Procurement"]
ROLES = {
    "Kitchen": ["Chef", "Sous Chef", "Kitchen Assistant"],
    "Service": ["Waiter", "Cashier", "Barista"],
    "Admin": ["HR Assistant", "Accountant", "Receptionist"],
    "Procurement": ["Procurement Officer", "Warehouse Assistant"]
}

EMP_COUNT = 100  # total employees across all units

# -------------------------------
# 2. HELPER FUNCTIONS
# -------------------------------

def random_role(dept):
    return random.choice(ROLES[dept])

def training_hours_required(role):
    if role in ["Chef", "Sous Chef", "Procurement Officer"]:
        return 10
    elif role in ["Waiter", "Cashier", "Barista"]:
        return 8
    elif role in ["HR Assistant", "Accountant", "Receptionist"]:
        return 6
    else:
        return 5

def salary_by_role(role):
    base = {
        "Chef": 35000, "Sous Chef": 32000, "Kitchen Assistant": 27000,
        "Waiter": 28000, "Cashier": 26000, "Barista": 27000,
        "HR Assistant": 30000, "Accountant": 32000, "Receptionist": 29000,
        "Procurement Officer": 33000, "Warehouse Assistant": 28000
    }.get(role, 28000)
    return round(np.random.normal(base, 1500), 0)

def turnover_risk(training_completion, satisfaction):
    if training_completion < 0.5 or satisfaction < 6:
        return "High"
    elif training_completion < 0.8 or satisfaction < 7:
        return "Medium"
    else:
        return "Low"

# -------------------------------
# 3. GENERATE EMPLOYEE DATA
# -------------------------------

employees = []

for i in range(1, EMP_COUNT + 1):
    emp_id = f"E{i:03d}"
    name = fake.name()
    gender = random.choice(["M", "F"])
    age = np.random.randint(18, 60)
    business_unit = random.choice(UNITS)
    dept = random.choice(DEPARTMENTS)
    role = random_role(dept)
    hire_date = fake.date_between(start_date="-3y", end_date="today")
    tenure_months = max(1, (date.today().year - hire_date.year) * 12 + (date.today().month - hire_date.month))
    employment_type = random.choices(["Full-time", "Part-time"], weights=[0.75, 0.25])[0]

    # Hours and salary
    monthly_hours = 160 if employment_type == "Full-time" else 80
    hours_worked = round(np.random.normal(monthly_hours * 0.95, 5), 0)
    salary = salary_by_role(role)

    # Training info
    required_training = training_hours_required(role)
    # Newer employees tend to have less training
    if tenure_months < 6:
        completed_training = np.random.uniform(0, required_training * 0.5)
    else:
        completed_training = np.random.uniform(required_training * 0.4, required_training)
    training_completion = round(completed_training / required_training, 2)

    # Mentorship and satisfaction logic
    mentor_assigned = random.choices([True, False], weights=[0.6, 0.4])[0]
    if mentor_assigned:
        satisfaction = np.random.normal(7.5, 1)
    else:
        satisfaction = np.random.normal(6.5, 1.2)
    satisfaction = max(1, min(round(satisfaction, 1), 10))

    # Risk and performance
    risk = turnover_risk(training_completion, satisfaction)
    performance = round(np.random.normal(3.5 + (training_completion * 1.5), 0.7), 1)
    performance = min(max(performance, 1), 5)

    last_training_date = hire_date + timedelta(days=np.random.randint(30, 400))
    if last_training_date > date.today():
        last_training_date = None

    employees.append({
        "Employee_ID": emp_id,
        "Name": name,
        "Gender": gender,
        "Age": age,
        "Business_Unit": business_unit,
        "Type": UNIT_TYPE[business_unit],
        "Department": dept,
        "Role": role,
        "Employment_Type": employment_type,
        "Hire_Date": hire_date,
        "Tenure_Months": tenure_months,
        "Monthly_Hours": monthly_hours,
        "Hours_Worked": hours_worked,
        "Salary_DKK": salary,
        "Training_Hours_Completed": round(completed_training, 1),
        "Required_Training_Hours": required_training,
        "Training_Completion_%": round(training_completion * 100, 1),
        "Mentor_Assigned": mentor_assigned,
        "Satisfaction_Score": satisfaction,
        "Turnover_Risk": risk,
        "Last_Training_Date": last_training_date,
        "Performance_Score": performance
    })

df = pd.DataFrame(employees)

# -------------------------------
# 4. EXPORT TO EXCEL
# -------------------------------

df.to_excel("staff_data.xlsx", index=False)
print("✅ staff_data.xlsx created successfully!")
print(df.head(5))
