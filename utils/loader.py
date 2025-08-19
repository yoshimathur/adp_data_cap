import pandas as pd 
import utils.col_refs as REF

# merge emkployee csv files to one dataframe
# benefits -> usage -> employees

BENEFITS = pd.read_csv('data/benefits_data.csv')
EMPLOYEES = pd.read_csv('data/employee_data.csv')
FEEDBACK = pd.read_csv('data/feedback_data.csv')
USAGE = pd.read_csv('data/usage_data.csv')

# merge benefits metadata onto usage
BENEFITS_USAGE = pd.merge(USAGE, BENEFITS, on=REF.benefitID, how="left")
print(f"Loaded {len(BENEFITS_USAGE)} benefits usage data!")

# merge feedback onto previously merged usage
# --> don't merge feedback too many resulting nulls
# merge2_df = pd.merge(merge1_df, feedback_df, on=["EmployeeID", "BenefitID"], how="outer")
# print(len(merge2_df))

# merge complete benefit data onto employee
EMPLOYEES_BENEFITS_USAGE = pd.merge(EMPLOYEES, BENEFITS_USAGE, on=REF.employeeID, how="left")
print(f"Loaded {len(EMPLOYEES_BENEFITS_USAGE)} employees benefits usage data!")

print(EMPLOYEES_BENEFITS_USAGE.columns, FEEDBACK.columns)