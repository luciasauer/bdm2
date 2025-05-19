"""
This script implements Model 1 for MongoDB data modeling.
In Model 1, `persons` and `companies` are stored in separate collections,
and relationships are maintained using foreign key references (companyId).

Pipeline Steps Implemented in this File:
Step 1: Clear previous data from collections (`clear_collections`)
Step 2: Insert person and company data with reference IDs (`insert_data`)
Step 3: Run and time the required queries:
    - Q1: For each person, retrieve their full name and their company’s name using a join
    - Q2: Count number of employees per company
    - Q3: Set age = 30 for all persons born before 1988
    - Q4: Append the word "Company" to all company names
"""

from utils import timed_query

class Model1:
    def __init__(self, db):
        """
        Constructor: Initializes the model with references to the person and company collections.
        """
        self.db = db
        self.persons = db.model1_persons
        self.companies = db.model1_companies

    def clear_collections(self):
        """
        Step 1: Drop collections to start from a clean state.
        """
        self.persons.drop()
        self.companies.drop()

    def insert_data(self, persons, companies):
        """
        Step 2: Insert data into two separate collections: `companies` and `persons`.
        - First, insert companies and capture their MongoDB-generated `_id`s.
        - Then, for each person, replace the `company` field with a `companyId` reference.
        """
        company_ids = self.companies.insert_many(companies).inserted_ids
        id_map = {c['name']: _id for c, _id in zip(companies, company_ids)}

        for p in persons:
            p['companyId'] = id_map[p['company']['name']]
            del p['company']  # Remove redundant embedded company info

        self.persons.insert_many(persons)

    @timed_query
    def query1(self):
        """
        Step 3 - Q1: Retrieve each person's full name and their company's name.
        - Uses a $lookup to join persons with companies on companyId.
        """
        pipeline = [
            {
                "$lookup": {
                    "from": "model1_companies",
                    "localField": "companyId",
                    "foreignField": "_id",
                    "as": "company"
                }
            },
            {"$unwind": "$company"},
            {"$project": {"fullName": 1, "companyName": "$company.name"}}
        ]
        for doc in self.persons.aggregate(pipeline):
            print(doc)

    @timed_query
    def query2(self):
        """
        Step 3 - Q2: Retrieve each company's name and number of employees.
        - First, groups persons by companyId and counts them.
        - Then, performs a $lookup to fetch the corresponding company name.
        """
        pipeline = [
            {
                "$group": {
                    "_id": "$companyId",
                    "numEmployees": {"$sum": 1}
                }
            },
            {
                "$lookup": {
                    "from": "model1_companies",
                    "localField": "_id",
                    "foreignField": "_id",
                    "as": "company"
                }
            },
            {"$unwind": "$company"},
            {"$project": {"companyName": "$company.name", "numEmployees": 1}}
        ]
        for doc in self.persons.aggregate(pipeline):
            print(doc)

    @timed_query
    def query3(self):
        """
        Step 3 - Q3: Set age = 30 for all persons born before 1988-01-01.
        - Simple update query with a condition on dateOfBirth.
        """
        self.persons.update_many(
            {"dateOfBirth": {"$lt": "1988-01-01"}},
            {"$set": {"age": 30}}
        )

    @timed_query
    def query4(self):
        """
        Step 3 - Q4: Append the word 'Company' to each company name.
        - Uses aggregation pipeline syntax in an update.
        """
        self.companies.update_many(
            {},
            [{"$set": {"name": {"$concat": ["$name", " Company"]}}}]
        )
