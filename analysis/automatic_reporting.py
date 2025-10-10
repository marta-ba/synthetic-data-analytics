import pandas as pd
from ydata_profiling import ProfileReport
import sweetviz as sv


# --- Operations report
ops = pd.read_excel("data/loca_operations_2025.xlsx")
ProfileReport(ops, title="Loca Gruppen – Operations Profiling").to_file("docs/reports/operations_report.html")

# --- Procurement report
proc = pd.read_excel("data/procurement_lines.xlsx")
ProfileReport(proc, title="Loca Gruppen – Procurement Profiling").to_file("docs/reports/procurement_report.html")

# --- Staff report (ydata-profiling version)
staff = pd.read_excel("data/staff_data.xlsx")
ProfileReport(staff, title="Loca Gruppen – Staff Profiling", explorative=True).to_file("docs/reports/staff_report.html")
