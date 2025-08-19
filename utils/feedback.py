from utils.loader import FEEDBACK
import utils.col_refs as REF

# get employee benefits usage feedback 
# parameter employeeID and benefitID compound key
# return database series 

def get_feedback(employeeID, benefitID): 
    # filter for employee match then benefit match 
    result = FEEDBACK[FEEDBACK[REF.employeeID] == employeeID]
    result = result[result[REF.benefitID] == benefitID]
    return result