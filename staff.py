# -*- coding: utf-8 -*-
"""
Synthetic Procurement Dataset for Loca Gruppen (Restaurants + Canteens)
Author: Marta (prepared by your AI coach)
Purpose: Generate realistic, constraint-aware procurement data
Outputs:
  - products_catalog.xlsx
  - suppliers.xlsx
  - procurement_lines.xlsx
"""

import numpy as np
import pandas as pd
from datetime import date, timedelta
import random

np.random.seed(42)
random.seed(42)

# ---------------------------
# 0) CONFIG & MASTER DATA
# ---------------------------

# Business units (8 total): 5 restaurants + 3 canteens
RESTAURANTS = ["Almanak i Operaen", "Almanak i Kilden", "Radio", "Format", "Posthallen"]
CANTEENS   = ["Langelinie Kantine", "Bankdata Kantine", "Carlsberg Kantine"]
UNITS = RESTAURANTS + CANTEENS

UNIT_TYPE = {u: ("Restaurant" if u in RESTAURANTS else "Canteen") for u in UNITS}

# Date range (quarter)
START = date(2025, 1, 1)
END   = date(2025, 3, 31)
DATES = pd.date_range(START, END, freq="D")

# Target portfolio constraints (by WEIGHT share unless noted)
TARGETS = {
    "plant_share": 0.748,       # incl. drinks
    "plant_tol": 0.02,
    "organic_share": 0.65,      # organic degree overall
    "organic_tol": 0.03,
    "animal_welfare_min": 0.50, # min; aim 0.78
    "animal_welfare_target": 0.78,
    "fish_better_methods": 0.75, # line/snurre
    "fao27_near_share": 0.50     # sub-areas near Denmark
}

# Product taxonomy: 7 main categories for CO2
# Each product row will carry: category, is_animal, unit ("kg"/"L"), base_co2_per_unit
PRODUCTS = [
    # Fruits & Veg (plant-based)
    ("Carrots",            "F&V",    False, "kg", 0.15),
    ("Potatoes",           "F&V",    False, "kg", 0.20),
    ("Tomatoes",           "F&V",    False, "kg", 0.40),
    ("Leafy Greens",       "F&V",    False, "kg", 0.25),
    ("Apples",             "F&V",    False, "kg", 0.30),
    # Dairy (animal-based)
    ("Milk",               "Dairy",  True,  "L",  1.20),
    ("Butter",             "Dairy",  True,  "kg", 8.00),
    ("Cheese",             "Dairy",  True,  "kg", 6.00),
    ("Yogurt",             "Dairy",  True,  "kg", 1.80),
    # Meat & Poultry (animal-based)
    ("Pork",               "Meat&Poultry", True, "kg", 6.00),
    ("Chicken",            "Meat&Poultry", True, "kg", 4.50),
    ("Beef",               "Meat&Poultry", True, "kg", 27.0),
    ("Veal",               "Meat&Poultry", True, "kg", 22.0),
    # Fish (animal-based) – CO2 varies but lower than beef
    ("White Fish",         "Fish",   True,  "kg", 3.50),
    ("Salmon",             "Fish",   True,  "kg", 5.00),
    # Beverages (plant-based; affects plant share)
    ("Soft Drinks",        "Beverages", False, "L", 0.50),
    ("Beer",               "Beverages", False, "L", 0.70),
    ("Juice",              "Beverages", False, "L", 0.60),
    ("Coffee Beans",       "Beverages", False, "kg", 4.00),
    # Non-food (for CO2 tracking attention; no animal/plant)
    ("Cleaning Chemicals", "Non-Food", None,  "L", 1.50),
    ("Paper Products",     "Non-Food", None,  "kg", 1.00)
]

PRODUCTS_DF = pd.DataFrame(PRODUCTS, columns=["Product","Category","Is_Animal","Unit","Base_CO2_per_unit"])

# Suppliers (some Danish, some foreign; some provide Swan-labeled cleaning products)
SUPPLIERS = [
    ("Aarstiderne",        "DK", True,  True),  # fresh F&V, Danish, can do organic
    ("Hørkram",            "DK", True,  False), # broadline Danish
    ("Carlsberg",          "DK", False, False), # beverages, Danish HQ
    ("Arla",               "DK", True,  True),  # dairy, DK
    ("Danish Crown",       "DK", True,  False), # meat, DK
    ("MSC Nordics",        "DK", False, False), # fish distributor (MSC capability external)
    ("EuroFoods GmbH",     "DE", False, False),
    ("Nordic Clean A/S",   "DK", False, True),  # cleaning supplies, Swan-labeled
    ("Italia Import Srl",  "IT", False, False),
    ("AquaSea",            "NO", False, False)   # fish supplier (Norway)
]
SUP_DF = pd.DataFrame(SUPPLIERS, columns=["Supplier","Country","Danish_Cert","Swan_Label_Able"])

# Fish metadata
FISH_METHODS_BETTER = ["Line", "Snurrevod"]
FISH_METHODS_LESS   = ["Trawl"]
FAO27_NEAR = ["27.3a", "27.3b", "27.4b"]
FAO27_OTHER = ["27.4a", "27.2a", "27.2b"]

# Employee spread (not used directly in procurement lines but useful to keep context)
EMP_PER_UNIT = {u: random.randint(10,14) for u in UNITS}

# ---------------------------
# 1) HELPERS
# ---------------------------

def pick_supplier_for_product(prod):
    """Simple rule-of-thumb mapping to realistic suppliers."""
    cat = PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Category"].values[0]
    if cat == "F&V":
        cands = ["Aarstiderne","Hørkram","EuroFoods GmbH"]
    elif cat == "Dairy":
        cands = ["Arla","Hørkram"]
    elif cat == "Meat&Poultry":
        cands = ["Danish Crown","Hørkram","EuroFoods GmbH"]
    elif cat == "Fish":
        cands = ["MSC Nordics","AquaSea"]
    elif cat == "Beverages":
        cands = ["Carlsberg","EuroFoods GmbH","Italia Import Srl"]
    elif cat == "Non-Food":
        cands = ["Nordic Clean A/S","Hørkram"]
    else:
        cands = list(SUP_DF["Supplier"])
    return random.choice(cands)

def draw_volume(unit, product):
    """Draw a plausible volume per line (kg/L) depending on unit type & category."""
    cat = PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==product, "Category"].values[0]
    typ = UNIT_TYPE[unit]
    base = 0
    if cat in ["F&V", "Meat&Poultry", "Fish", "Dairy", "Beverages"]:
        base = np.random.uniform(40, 200) if typ=="Restaurant" else np.random.uniform(25, 120)
    elif cat == "Non-Food":
        base = np.random.uniform(10, 60) if typ=="Restaurant" else np.random.uniform(8, 40)
    return round(base, 2)

def is_danish(prod, supplier):
    """Probability an item is Danish; varies by category."""
    cat = PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Category"].values[0]
    sup_row = SUP_DF.loc[SUP_DF["Supplier"]==supplier].iloc[0]
    prob = 0.6 if sup_row["Country"]=="DK" else 0.1
    if cat == "F&V":
        prob += 0.15
    if cat in ["Meat&Poultry","Dairy"]:
        prob += 0.10
    return np.random.rand() < min(prob, 0.95)

def is_organic(prod, supplier):
    """Probability of organic flag based on category/supplier capability."""
    cat = PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Category"].values[0]
    sup_row = SUP_DF.loc[SUP_DF["Supplier"]==supplier].iloc[0]
    base = 0.55
    if sup_row["Danish_Cert"]:
        base += 0.10
    if cat in ["F&V","Dairy"]:
        base += 0.10
    if cat == "Meat&Poultry":
        base -= 0.05
    if cat == "Non-Food":
        base -= 0.30
    return np.random.rand() < max(min(base, 0.95), 0.10)

def animal_welfare_flags(prod):
    """Return welfare categories for animal products (pork/chicken/beef/veal)."""
    if prod not in ["Pork","Chicken","Beef","Veal"]:
        return {"Welfare_Flag": None, "Welfare_Type": None}
    # Base chance; will tune later to meet 78% target overall
    chance = 0.65
    typ = None
    if prod == "Pork":
        typ = "Svinekød"
        chance += 0.05
    elif prod == "Chicken":
        typ = "Kylling"
        chance += 0.00
    elif prod in ["Beef","Veal"]:
        typ = "Kalve/Oksekød"
        chance -= 0.05
    ok = np.random.rand() < max(min(chance, 0.9), 0.4)
    return {"Welfare_Flag": bool(ok), "Welfare_Type": typ}

def fish_metadata(prod):
    """Return fish method + area if fish, else None."""
    if PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Category"].values[0] != "Fish":
        return {"Fish_Method": None, "FAO_Area": None}
    better = np.random.rand() < TARGETS["fish_better_methods"]
    method = random.choice(FISH_METHODS_BETTER if better else FISH_METHODS_LESS)
    near = np.random.rand() < TARGETS["fao27_near_share"]
    area = random.choice(FAO27_NEAR if near else FAO27_OTHER)
    return {"Fish_Method": method, "FAO_Area": f"FAO {area}"}

def egg_policy(prod):
    """Eggs nearly 100% organic — here eggs are not a separate line item; if you add 'Eggs', force organic."""
    return

def co2_for_line(prod, vol):
    """Compute CO2e = base factor * volume (kg or L)."""
    base = PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Base_CO2_per_unit"].values[0]
    return round(base * vol, 3)

def price_per_unit(prod, organic):
    """Simple price model: organic is pricier; meat/dairy pricier; beverages mid; F&V lower."""
    cat = PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Category"].values[0]
    base = {
        "F&V": 18, "Dairy": 28, "Meat&Poultry": 70, "Fish": 55, "Beverages": 22, "Non-Food": 20
    }.get(cat, 25)
    if organic:
        base *= 1.15
    return round(np.random.normal(base, base*0.08), 2)

# ---------------------------
# 2) GENERATE BASE LINES
# ---------------------------

lines = []
for d in DATES:
    for unit in UNITS:
        # per-day variety of purchase lines (3–8)
        n_lines = np.random.randint(3, 9)
        # ensure mix includes both plant & animal across period
        sampled_products = random.choices(PRODUCTS_DF["Product"].tolist(), k=n_lines)
        for prod in sampled_products:
            supplier = pick_supplier_for_product(prod)
            vol = draw_volume(unit, prod)  # kg/L
            # Flags
            danish = is_danish(prod, supplier)
            organic = is_organic(prod, supplier)
            # Animal welfare (only for animal meats)
            w = animal_welfare_flags(prod)
            # Fish metadata
            fish = fish_metadata(prod)
            # Pricing & CO2
            ppu = price_per_unit(prod, organic)
            cost = round(ppu * vol, 2)
            co2 = co2_for_line(prod, vol)

            lines.append({
                "Date": d,
                "Business_Unit": unit,
                "Type": UNIT_TYPE[unit],
                "Product": prod,
                "Category": PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Category"].values[0],
                "Is_Animal": PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Is_Animal"].values[0],
                "Unit": PRODUCTS_DF.loc[PRODUCTS_DF["Product"]==prod, "Unit"].values[0],
                "Supplier": supplier,
                "Supplier_Country": SUP_DF.loc[SUP_DF["Supplier"]==supplier, "Country"].values[0],
                "Supplier_Danish_Cert": bool(SUP_DF.loc[SUP_DF["Supplier"]==supplier, "Danish_Cert"].values[0]),
                "Organic": bool(organic),
                "Danish": bool(danish),
                "Welfare_Flag": w["Welfare_Flag"],
                "Welfare_Type": w["Welfare_Type"],
                "Fish_Method": fish["Fish_Method"],
                "FAO_Area": fish["FAO_Area"],
                "Volume_kg_L": vol,
                "Price_per_Unit_DKK": ppu,
                "Cost_DKK": cost,
                "CO2e_kg": co2
            })

df = pd.DataFrame(lines)

# ---------------------------
# 3) PORTFOLIO TUNING (meet targets)
# ---------------------------

def plant_share(df):
    plant_mask = (df["Is_Animal"] == False) | (df["Category"].isin(["Beverages"]))  # plant & beverages
    return df.loc[plant_mask, "Volume_kg_L"].sum() / df["Volume_kg_L"].sum()

def organic_share(df):
    return df.loc[df["Organic"]==True, "Volume_kg_L"].sum() / df["Volume_kg_L"].sum()

def animal_welfare_share(df):
    animal_mask = (df["Is_Animal"] == True)
    if df.loc[animal_mask, "Volume_kg_L"].sum() == 0:
        return 0.0
    return df.loc[(animal_mask) & (df["Welfare_Flag"]==True), "Volume_kg_L"].sum() / df.loc[animal_mask, "Volume_kg_L"].sum()

# Adjust organic rate slightly towards target by flipping some flags within plausible categories
def nudge_organic(df, target, tol):
    current = organic_share(df)
    if abs(current - target) <= tol:
        return df
    need_increase = current < target
    candidates = df[df["Category"].isin(["F&V","Dairy","Beverages"])]  # plausible to flip
    idx = candidates.sample(frac=0.1, random_state=np.random.randint(0, 99999)).index
    df.loc[idx, "Organic"] = True if need_increase else False
    return df

# Nudge welfare on animal categories
def nudge_welfare(df, target):
    current = animal_welfare_share(df)
    if current >= target:
        return df
    candidates = df[(df["Is_Animal"]==True) & (df["Category"].isin(["Meat&Poultry","Dairy","Fish"])) ]
    idx = candidates.sample(frac=0.15, random_state=np.random.randint(0, 99999)).index
    df.loc[idx, "Welfare_Flag"] = True
    return df

# Run nudges iteratively (few passes)
for _ in range(4):
    df = nudge_organic(df, TARGETS["organic_share"], TARGETS["organic_tol"])
for _ in range(3):
    df = nudge_welfare(df, TARGETS["animal_welfare_target"])

# Ensure fish method & FAO near ratios roughly match (re-sample subset if off)
def enforce_fish_targets(df):
    fish_mask = (df["Category"]=="Fish")
    if fish_mask.sum()==0:
        return df
    # Better methods
    cur_better = (df.loc[fish_mask, "Fish_Method"].isin(FISH_METHODS_BETTER)).mean()
    if cur_better < TARGETS["fish_better_methods"]:
        to_flip = df.loc[fish_mask & df["Fish_Method"].isin(FISH_METHODS_LESS)].sample(frac=0.3, random_state=1).index
        df.loc[to_flip, "Fish_Method"] = np.random.choice(FISH_METHODS_BETTER, size=len(to_flip))
    # FAO near
    cur_near = (df.loc[fish_mask, "FAO_Area"].isin([f"FAO {a}" for a in FAO27_NEAR])).mean()
    if cur_near < TARGETS["fao27_near_share"]:
        to_flip = df.loc[fish_mask & ~df["FAO_Area"].isin([f"FAO {a}" for a in FAO27_NEAR])].sample(frac=0.3, random_state=2).index
        df.loc[to_flip, "FAO_Area"] = np.random.choice([f"FAO {a}" for a in FAO27_NEAR], size=len(to_flip))
    return df

df = enforce_fish_targets(df)

# Recompute some portfolio ratios to log (optional)
plant_ratio = plant_share(df)
org_ratio = organic_share(df)
welfare_ratio = animal_welfare_share(df)

# ---------------------------
# 4) NON-FOOD & SWAN LABEL SHARE (info for reporting)
# ---------------------------

# Mark non-food & Swan-labeled availability
df["Non_Food"] = df["Category"].eq("Non-Food")
df["Swan_Labeled"] = False
mask_nf = df["Non_Food"] & df["Supplier"].eq("Nordic Clean A/S")
df.loc[mask_nf, "Swan_Labeled"] = True

# ---------------------------
# 5) EXPORT
# ---------------------------

PRODUCTS_DF.to_excel("products_catalog.xlsx", index=False)
SUP_DF.to_excel("suppliers.xlsx", index=False)
df.to_excel("procurement_lines.xlsx", index=False)

print("✅ Generated rows:", len(df))
print(f"Plant-based share (by weight): {plant_ratio:.3f}")
print(f"Organic degree (by weight):   {org_ratio:.3f}")
print(f"Animal welfare share:         {welfare_ratio:.3f}")
print("Files written: products_catalog.xlsx, suppliers.xlsx, procurement_lines.xlsx")
