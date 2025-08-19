import pandas as pd 

# merge csv files to one dataframe on benefitID -> employeeID

DATA = None

benefits_df = pd.read_csv('data/benefits_data.csv')
employee_df = pd.read_csv('data/employee_data.csv')
feedback_df = pd.read_csv('data/feedback_data.csv')
usage_df = pd.read_csv('data/usage_data.csv')

# merge benefits metadata onto usage
merge1_df = pd.merge(usage_df, benefits_df, on="BenefitID", how="left")
print(len(merge1_df))

# merge feedback onto previously merged usage
# merge2_df = pd.merge(merge1_df, feedback_df, on=["EmployeeID", "BenefitID"], how="outer")
# print(len(merge2_df))

# merge complete benefit data onto employee
final_df = pd.merge(employee_df, merge1_df, on="EmployeeID", how="left")
print(len(final_df))


DATA = final_df