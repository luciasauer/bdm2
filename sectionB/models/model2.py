"""
This script implements Model 2 for MongoDB data modeling.
In Model 2, only a `persons` collection is used, and the `company` details
are embedded within each person document.

Pipeline Steps Implemented in this File:
Step 1: Clear previous data from the collection (`clear_collections`)
Step 2: Insert person data with embedded company objects (`insert_data`)
Step 3: Run and time the required queries:
    - Q1: For each person, retrieve their full name and embedded company name
    - Q2: Count number of employees per company using aggregation
    - Q3: Set age = 30 for all persons born before 1988
    - Q4: Append the word "Company" to all embedded company names
"""

from utils import timed_query

class Model2:
    def __init__(self, db):
        """
        Constructor: Initializes the model with a reference to the persons collection.
        """
        self.db = db
        self.persons = db.persons

    def clear_collections(self):
        """
        Step 1: Drop the collection to start from a clean state.
        """
        self.persons.drop()

    def insert_data(self, persons_data, companies_data):
        """
        Step 2: Insert data into the persons collection, embedding company info inside each person.
        - For each person, the `company` field is added as a nested document.
        """
        self.persons.insert_many(persons_data)

    @timed_query
    def query1(self):
        """
        Step 3 - Q1: Retrieve each person's full name and their embedded company's name.
        - Uses a simple projection from the `persons` collection.
        """
        results = self.persons.find({}, {"_id":0, "fullName": 1, "company_name": "$company.name"})
        # for doc in results:
        #     print(doc)

    @timed_query
    def query2(self):
        """
        Step 3 - Q2: Count the number of employees per company.
        - Groups persons by the embedded company name and counts them.
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$company.name",
                    "numEmployees": {"$sum": 1}
                }
            },
            {"$project": {"companyName": "$_id", "numEmployees": 1, "_id": 0}}
        ]
        for doc in self.persons.aggregate(pipeline):
            print(doc)

    @timed_query
    def query3(self):
        """
        Step 3 - Q3: Set age = 30 for all persons born before 1988-01-01.
        - Applies a conditional update on the `dateOfBirth` field.
        """
        self.persons.update_many(
            {"dateOfBirth": {"$lt": "1988-01-01"}},
            {"$set": {"age": 30}}
        )

    @timed_query
    def query4(self):
        """
        Step 3 - Q4: Append the word 'Company' to the name of each embedded company.
        - Uses aggregation-style update with $concat.
        """
        self.persons.update_many(
            {},
            [{"$set": {"company.name": {"$concat": ["$company.name", " Company"]}}}]
        )
