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
    db = client.mongo_lab

    NUM_COMPANIES = 10
    NUM_PERSONS = 100

    # Generate datasets once
    companies = generate_companies(NUM_COMPANIES)
    persons = generate_persons(NUM_PERSONS, companies)

    # List of all model classes to run
    model_classes = [Model1, Model2, Model3]

    for model_class in model_classes:
        run_model(model_class, db, persons, companies)

if __name__ == "__main__":
    main()
