
# 📘 Loca Gruppen Synthetic Data Model Documentation

Author: Marta Blanco
Purpose: Demonstration of data integration and BI reporting architecture simulating Loca Gruppen’s operations, procurement, and HR systems.
Date: 2025

# 🌍 Overview

Loca Gruppen operates eight food service units (restaurants and canteens) with around 100 employees, all sharing unified sustainability and operational goals.

This synthetic dataset simulates the company’s three main data sources:

    - Restaurant Operations Data
    - Procurement & Sustainability Data
    - Staff & Training Data

Together, they form a realistic data ecosystem for Business Intelligence, sustainability tracking, and strategic workforce management.

🏪 1. Restaurant Operations Database

File: loca_operations_2025.csv
Rows: ≈ 720 (8 units × 90 days)

    🎯 Purpose
        To monitor daily operational performance of restaurants and canteens — including        
        financial, efficiency, and sustainability KPIs. Provides the foundation for Plecto or 
        Power BI dashboards to visualize business performance and identify best practices across 
        units.


📊 Key Metrics
Metric	Description	KPI Example
Revenue_DKK	Daily income from restaurant sales	Total revenue by restaurant
Costs_DKK	Operating costs (food, staff, utilities)	Cost ratio = Costs / Revenue
Profit_Margin_%	Profitability measure	Financial efficiency
Guests	Number of daily customers	Guest trends
Waste_kg	Daily food waste	Waste per guest
Organic_Percentage	Share of organic ingredients used	Sustainability goal tracking
Local_Supplier_%	Local sourcing percentage	Danish product share
Hours_Worked	Staff hours logged per day	Staff productivity
Revenue_per_Hour	Output per labor hour	Labor efficiency
🧩 How It’s Used

Baseline for all operational dashboards.

Links to Procurement via shared Business_Unit.

Links to Staff data to analyze productivity, training, and performance.

🌿 2. Procurement & Sustainability Database

Files:

procurement_lines.csv

products_catalog.csv

suppliers.csv
Rows: ≈ 10,000 procurement lines

🎯 Purpose

To simulate Loca Gruppen’s purchasing system, enabling detailed analysis of Scope 3 CO₂ emissions, organic sourcing, animal welfare, and supplier performance.

📦 procurement_lines.csv — Fact Table
Column	Description
Date	Purchase date
Business_Unit	Restaurant / canteen
Product, Category	Purchased item and food group
Volume_kg_L	Amount purchased (in kg/L)
Cost_DKK	Purchase cost
Organic	Organic certification flag
Danish	Danish origin flag
Is_Animal	Animal vs plant-based
Welfare_Flag / Welfare_Type	Animal welfare status
Fish_Method / FAO_Area	Sustainable fishing classification
CO2e_kg	CO₂ equivalents (Scope 3 impact)
Non_Food	Cleaning or packaging purchases
Swan_Labeled	Swan-eco-certified products
📘 Key Sustainability Goals Simulated
Goal	Target	Representation
Organic Degree (Økologi)	≥ 65%	Organic flag by volume
Plant-based Share	≈ 75%	Is_Animal=False ratio
Animal Welfare	≥ 50% (actual ~78%)	Welfare_Flag
Fish Methods	≥ 75% “Better”	Fish_Method
Local (Danish) Sourcing	≥ 60% for main groups	Danish=True
FAO 27 Origin	100%	FAO_Area codes
📦 suppliers.csv — Dimension Table

Supplier name, country, Danish certification, Swan-label capability.

📦 products_catalog.csv — Dimension Table

Product name, category, animal/plant type, unit, CO₂ emission factor.

🔗 How It Integrates

Joins to loca_operations_2025.csv via Business_Unit (to compare procurement vs. performance).

Feeds Scope 3 CO₂ and sustainability reporting dashboards.

👩‍🍳 3. Staff & Training Database

File: staff_data.xlsx
Rows: ≈ 100 employees

🎯 Purpose

To simulate Loca Gruppen’s workforce structure and training challenges.
Supports HR and management dashboards for training completion, satisfaction, and turnover risk — addressing real issues mentioned by Michael (difficulty training new staff).

👥 Core Columns
Column	Description
Employee_ID	Unique employee code
Name, Gender, Age	Employee profile
Business_Unit, Department, Role	Organizational structure
Hire_Date, Tenure_Months	Employment duration
Employment_Type	Full-time / Part-time
Monthly_Hours, Hours_Worked	Labor metrics
Salary_DKK	Monthly salary
Training_Hours_Completed, Required_Training_Hours	Training progress
Training_Completion_%	Completion ratio
Mentor_Assigned	Whether mentor assigned
Satisfaction_Score	Survey feedback (1–10)
Turnover_Risk	Low / Medium / High
Performance_Score	1–5 KPI score
📊 Key HR Insights
KPI	Formula	Insight
Training Completion Rate	AVG(Training_Completion_%)	Training progress
New Staff Completion (<6mo)	Filtered measure	Onboarding effectiveness
Mentorship Coverage	% with Mentor_Assigned	Training support
Satisfaction vs. Risk	Correlation	Predict turnover
Performance vs. Training	Correlation	Training ROI
💡 How It Solves the Training Problem

Tracks onboarding progress through Training_Completion_% and Mentor_Assigned.

Flags departments with high Turnover_Risk or low satisfaction.

Enables predictive models to identify where mentoring or retraining could reduce churn.

🔗 4. Data Model Integration (Power BI / Plecto)
Business_Unit
│
├── loca_operations_2025.csv   (Operational Metrics)
├── procurement_lines.csv       (Sustainability & Purchasing)
└── staff_data.xlsx             (HR & Training)

Relationships

Business_Unit → joins all three datasets.

Date → time series alignment (Operations & Procurement).

Department → HR segmentation.

Unified Analysis Themes
Area	Combined Insight Example
Operational Efficiency	Compare revenue/hour vs. staff training & turnover
Sustainability Impact	Link organic sourcing with waste reduction & CO₂ per DKK revenue
Workforce Optimization	Identify units with low productivity & low training completion
Leadership Decisions	Prioritize investments in training, local sourcing, or equipment
📈 5. Dashboard Opportunities
Dashboard	Description	Data Source(s)
Executive Overview	Revenue, Costs, Margin, Waste, CO₂	Operations + Procurement
Sustainability Performance	Organic %, Local sourcing, Welfare %, CO₂e trend	Procurement
HR & Training Tracker	Completion %, Mentor coverage, Risk	Staff
Integrated Performance	Training vs. Profit Margin, CO₂ vs. Revenue	All 3 datasets
✅ 6. Deliverables Summary
File	Description	Format
loca_operations_2025.csv	Daily restaurant & canteen operations	CSV
procurement_lines.csv	Detailed procurement records	CSV
products_catalog.csv	Product taxonomy	CSV
suppliers.csv	Supplier metadata	CSV
staff_data.xlsx	HR & Training dataset	Excel
💬 Author’s Note

This synthetic data model demonstrates how an integrated Data & Analytics system can unify Loca Gruppen’s core activities — operations, procurement, and workforce — under one reporting structure.

It supports sustainability reporting, financial oversight, and workforce development, directly reflecting the company’s values of “Love Before Cash”, sustainability, and care for people.