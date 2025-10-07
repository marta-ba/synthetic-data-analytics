import pandas as pd
import numpy as np
import random
from datetime import timedelta, date

# Parameters
np.random.seed(42)
random.seed(42)

# Business units
restaurants = ["Almanak i Operaen", "Almanak i Kilden", "Radio", "Format", "Posthallen"]
canteens = ["Langelinie Kantine", "Bankdata Kantine", "Carlsberg Kantine"]
units = restaurants + canteens

unit_type = {u: "Restaurant" for u in restaurants}
unit_type.update({u: "Canteen" for u in canteens})

cities = {
    "Almanak i Operaen": "Copenhagen",
    "Almanak i Kilden": "Hellerup",
    "Radio": "Copenhagen",
    "Format": "Copenhagen",
    "Posthallen": "Copenhagen",
    "Langelinie Kantine": "Copenhagen",
    "Bankdata Kantine": "Fredericia",
    "Carlsberg Kantine": "Valby"
}

# Date range
start_date = date(2025, 1, 1)
end_date = date(2025, 3, 31)
dates = pd.date_range(start=start_date, end=end_date)

records = []

for d in dates:
    for unit in units:
        is_restaurant = unit_type[unit] == "Restaurant"
        
        # Base revenue ranges
        revenue = np.random.uniform(40000, 70000) if is_restaurant else np.random.uniform(15000, 30000)
        guests = np.random.randint(180, 320) if is_restaurant else np.random.randint(80, 160)
        
        organic_pct = np.random.uniform(70, 90) if is_restaurant else np.random.uniform(60, 80)
        local_sup = np.random.uniform(60, 85) if is_restaurant else np.random.uniform(50, 75)
        
        cost_factor = np.random.uniform(0.6, 0.8)
        if organic_pct > 85:
            cost_factor += 0.02  # higher organic = higher cost
        costs = revenue * cost_factor
        
        waste = np.random.normal(0.08 * guests, 2)  # about 80g waste per guest
        hours = np.random.normal(150, 15) if is_restaurant else np.random.normal(110, 10)
        employees = np.random.randint(10, 15)
        
        records.append({
            "Date": d,
            "Business_Unit": unit,
            "Type": unit_type[unit],
            "City": cities[unit],
            "Revenue_DKK": round(revenue, 2),
            "Costs_DKK": round(costs, 2),
            "Guests": guests,
            "Waste_kg": round(waste, 2),
            "Hours_Worked": round(hours, 1),
            "Organic_Percentage": round(organic_pct, 1),
            "Local_Supplier_%": round(local_sup, 1),
            "Employee_Count": employees
        })

df = pd.DataFrame(records)
df["Profit_DKK"] = df["Revenue_DKK"] - df["Costs_DKK"]
df["Profit_Margin_%"] = round((df["Profit_DKK"] / df["Revenue_DKK"]) * 100, 2)
df["Waste_per_Guest_kg"] = round(df["Waste_kg"] / df["Guests"], 3)
df["Revenue_per_Hour"] = round(df["Revenue_DKK"] / df["Hours_Worked"], 2)

df.to_excel("local_operations_2025.xlsx", index=False)
print("✅ Synthetic dataset generated:", df.shape)
df.head(5)


###📊 6. What This Dataset Enables You to Do in Power BI

# Revenue per unit (restaurants vs canteens)

# Organic vs Cost correlation (scatter plot)

# Waste per Guest (environmental performance)

# Profit Margin trend (financial performance)

# Local Supplier % by unit (social/sustainability impact)

# Plus, you can group the 8 businesses to show their unified progress toward sustainability — just like in the real sustainability report.