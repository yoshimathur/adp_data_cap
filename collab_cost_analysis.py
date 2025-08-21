import numpy as np
import pandas as pd
from tqdm import tqdm
from utils.loader import EMPLOYEES_BENEFITS_USAGE
import utils.col_refs as REF
from models.collab_filter import get_collab_recommendations, create_embeddings, BENEFITS_VECTORIZER

employees = EMPLOYEES_BENEFITS_USAGE[REF.employeeID].unique().tolist()
embeddings = create_embeddings()

delta = np.empty(len(BENEFITS_VECTORIZER))
delta_counts = np.empty(len(BENEFITS_VECTORIZER))
for employee in tqdm(employees, desc="Processing employees"): 
    employee_delta = get_collab_recommendations(employee, embeddings)
    delta += np.array(employee_delta)

    delta_count = [1.0 if d != 0.0 else 0.0 for d in employee_delta]
    delta_counts += np.array(delta_count)

for i in range(len(BENEFITS_VECTORIZER)): 
    if delta_counts[i] == 0: 
        delta[i] = 0
    else: 
        delta[i] /= delta_counts[i]

pd.DataFrame({REF.benefitID: BENEFITS_VECTORIZER, "UsageCostDelta": delta}).to_csv('data/delta_cosine.csv', index=False)