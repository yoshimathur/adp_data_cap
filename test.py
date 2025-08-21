from utils.loader import EMPLOYEES_BENEFITS_USAGE
import utils.col_refs as REF
from models.collab_filter import get_collab_recommendations, create_embeddings, BENEFITS_VECTORIZER

employees = EMPLOYEES_BENEFITS_USAGE[REF.employeeID].unique().tolist()
embeddings = create_embeddings()

delta = get_collab_recommendations(employees[1], embeddings)

for i, benefit_delta in enumerate(delta): 
    print(BENEFITS_VECTORIZER[i], benefit_delta)