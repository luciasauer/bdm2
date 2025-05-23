"""
Entry point script to run MongoDB data modeling pipelines for Model1, Model2, and Model3.

Workflow:
1. Connects to MongoDB.
2. Generates the same synthetic companies and persons datasets.
3. Iterates over all models:
    - Clears collections.
    - Inserts data.
    - Runs queries Q1 to Q4.
4. Prints progress and timing info.
"""
import copy
from pymongo import MongoClient
from data_generator import generate_companies, generate_persons
from models.model1 import Model1
from models.model2 import Model2
from models.model3 import Model3

def run_model(model_class, db, persons, companies):
    """
    Helper function to execute full pipeline for a given model class.
    """
    model_name = model_class.__name__
    print(f"\nRunning {model_name}...")
    
    model = model_class(db)
    model.clear_collections()
    model.insert_data(persons, companies)
    
    # Run queries in order
    for i in range(1, 5):
        query_func = getattr(model, f"query{i}")
        query_func()

def main():
    # MongoDB connection string and DB name
    client = MongoClient("mongodb://localhost:27017/")

    NUM_COMPANIES = 50_000
    NUM_PERSONS = 1_000_000

    # Generate datasets once
    print("Generating datasets...")
    companies_data = generate_companies(NUM_COMPANIES)
    persons_data = generate_persons(NUM_PERSONS, companies_data)

    # List of all model classes to run and their corresponding DB
    model_classes = [(Model1, client.model1), (Model2, client.model2), (Model3, client.model3)]

    for model_class, db_model in model_classes:
        # Deep copy to prevent mutation from affecting other models
        run_model(model_class, db_model, copy.deepcopy(persons_data), copy.deepcopy(companies_data))

if __name__ == "__main__":
    main()
