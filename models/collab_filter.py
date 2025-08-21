import numpy as np
import tqdm
from utils.loader import BENEFITS, EMPLOYEES_BENEFITS_USAGE
import utils.col_refs as REF
from sklearn.metrics.pairwise import cosine_similarity as sim 

LIMIT = 10
MAX_USAGE_COST = np.max(BENEFITS[REF.benefit_cost])
# benefit id = idx + 1
BENEFITS_VECTORIZER = BENEFITS[REF.benefitID].tolist()
DEPARTMENT_VECTORIZER = EMPLOYEES_BENEFITS_USAGE[REF.deparment].unique().tolist()

def create_vector(employee): 
    try: 
        benefits = EMPLOYEES_BENEFITS_USAGE.groupby(REF.employeeID).get_group(employee).reset_index()
    except KeyError: 
        raise KeyError(f"Collaborative filter: Employee {employee} not found.")
    finally: 
        vector = [0] * len(BENEFITS_VECTORIZER)

    # count operation (assign value at idx in vector)
    for _, benefit in benefits.iterrows(): 
        idx = benefit[REF.benefitID] - 1
        if benefit[REF.usage_freq] == 0: 
            usage_cost = 0
        else:
            usage_cost = (benefit[REF.benefit_cost] / benefit[REF.usage_freq])
        vector[idx] += usage_cost / MAX_USAGE_COST

    # append metadata
    vector.append(benefits[REF.age].to_list()[0])
    vector.append(benefits[REF.tenure].to_list()[0])
    vector.append(DEPARTMENT_VECTORIZER.index(benefits[REF.deparment].to_list()[0]))

    return vector

def create_embeddings(): 
    employees = EMPLOYEES_BENEFITS_USAGE[REF.employeeID].unique().tolist()
    embeddings = {}
    for employee in employees: 
        employee_vector = create_vector(employee)
        embeddings[employee] = employee_vector

    return embeddings
    
def get_collab_recommendations(target_employee, embeddings): 
    target_vector = create_vector(target_employee)

    if all(v == 0 for v in target_vector): 
        print(f"Collaborative Filter: Employee {target_employee} has no benefits.")

    employee_recs = list()
    max_distance = 1
    delta_vector = [list()] * len(BENEFITS_VECTORIZER)

    for _, employee in enumerate(EMPLOYEES_BENEFITS_USAGE[REF.employeeID].unique()):
        if employee == target_employee:
            continue

        employee_vector = embeddings[employee]
        if not employee_vector:
            raise ValueError(f"Collaborative Filter: Employee {employee} not found.")
        
        similarity = sim([target_vector], [employee_vector])[0][0]
        
        if similarity > max_distance: 
            max_distance = similarity

        employee_recs.append((employee, similarity))
    
    # find symmetric difference between top 3 employee recommendations and target employee
    employee_recs = sorted(employee_recs, key=lambda x: x[1], reverse=True)[:LIMIT]
    for employee, score in employee_recs: 
        employee_vector = embeddings[employee]
        sym_diff = [(employee_vector[i] - target_vector[i]) for i in range(len(BENEFITS_VECTORIZER))]

        # update recs list with symmetric difference * similarity score
        for j in range(len(BENEFITS_VECTORIZER)): 
            delta = float(sym_diff[j]) 
            # delta /= (score * max_distance)
            if not delta_vector[j]: 
                delta_vector[j] = [delta]
            else: 
                delta_vector[j].append(delta)

    # aggregate employee similarity scores by rec 
    for i, delta in enumerate(delta_vector): 
        sum_delta = np.array(delta).sum() / LIMIT * MAX_USAGE_COST
        delta_vector[i] = sum_delta
    
    return delta_vector
