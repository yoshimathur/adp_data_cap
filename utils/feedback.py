from utils.loader import FEEDBACK
import utils.col_refs as REF

# get employee benefits usage feedback 
# parameter employeeID and benefitID compound key
# return database series 

def get_feedback(employeeID, benefitID): 
    grouped = FEEDBACK.groupby([REF.employeeID, REF.benefitID], as_index=True)
    result = grouped[grouped[REF.employeeID] == employeeID and grouped[REF.benefitID] == benefitID]
    return result