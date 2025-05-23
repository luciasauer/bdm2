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
        self.persons = db.persons
        self.companies = db.companies

    def clear_collections(self):
        """
        Step 1: Drop collections to start from a clean state.
        """
        self.persons.drop()
        self.companies.drop()

    def insert_data(self, persons_data, companies_data):
        """
        Step 2: Insert data into two separate collections: `companies` and `persons`.
        - First, insert companies and capture their MongoDB-generated `_id`s.
        - Then, for each person, replace the `company` field with a `companyId` reference.
        """
        company_ids = self.companies.insert_many(companies_data).inserted_ids
        id_map = {c['name']: _id for c, _id in zip(companies_data, company_ids)}

        for p in persons_data:
            p['companyId'] = id_map[p['company']['name']]
            del p['company']  # Remove redundant embedded company info

        self.persons.insert_many(persons_data)

    @timed_query
    def query1(self):
        """
        Step 3 - Q1: Retrieve each person's full name and their company's name.
        - Uses a $lookup to join persons with companies on companyId.
        """
        pipeline = [
            {"$project":{"_id":0,"fullName":1, "companyId":1}}, #keep only the needed columns for the lookup from persons
            {
             "$lookup": {
                "from": "companies", #collection to join with
                "localField": "companyId", #companyId in persons
                "foreignField": "_id", #_id in companies
                "as": "company" #rename the array
            }
            },
            {"$unwind": "$company"}, #unnest the fields from the company
            {"$project": {"fullName": 1, "companyName": "$company.name"}} #select only the columns to project
        ]
        results = self.persons.aggregate(pipeline)
        # for doc in results:
        #     print(doc)

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
                    "from": "companies",
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
