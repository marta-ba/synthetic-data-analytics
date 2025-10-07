# -----------------------------------------------------
# Restaurant Operations Synthetic Dataset Generator
# Author: Marta Blanco

import pandas as pd
import numpy as np
from faker import Faker
import random

# Initialize Faker and seed
fake = Faker()
np.random.seed(42)
random.seed(42)

# Parameters
restaurants = ["Almanak", "Operaen", "Kilden", "Posthallen"]
locations = ["Copenhagen", "Hellerup", "Frederiksberg", "Lyngby"]
categories = ["Fine Dining", "Bistro", "Casual", "Gourmet"]

# Generate daily data for 3 months (Jan–Mar 2025)
dates = pd.date_range(start="2025-01-01", end="2025-03-31")

data = []

for date in dates:
    for r in restaurants:
        # Base random metrics
        revenue = round(np.random.normal(50000, 8000), 2)
        guests = max(50, int(np.random.normal(250, 40)))
        costs = round(revenue * np.random.uniform(0.55, 0.75), 2)
        waste = round(np.random.normal(20, 5), 2)
        hours = round(np.random.normal(150, 20), 2)

        data.append({
            "Date": date,
            "Restaurant": r,
            "Location": random.choice(locations),
            "Category": random.choice(categories),
            "Revenue_DKK": revenue,
            "Guests": guests,
            "Costs_DKK": costs,
            "Waste_kg": waste,
            "Hours_Worked": hours
        })

# Create DataFrame
df = pd.DataFrame(data)

# Derived metrics (optional pre-calculation)
df["Profit_DKK"] = df["Revenue_DKK"] - df["Costs_DKK"]
df["Profit_Margin_%"] = round((df["Profit_DKK"] / df["Revenue_DKK"]) * 100, 2)
df["Avg_Ticket_DKK"] = round(df["Revenue_DKK"] / df["Guests"], 2)
df["Waste_per_Guest_kg"] = round(df["Waste_kg"] / df["Guests"], 3)
df["Revenue_per_Hour"] = round(df["Revenue_DKK"] / df["Hours_Worked"], 2)

# Save to CSV
df.to_excel("loca_restaurant_data.csv", index=False)

print("✅ Dataset generated successfully! Rows:", len(df))
print(df.head(5))
