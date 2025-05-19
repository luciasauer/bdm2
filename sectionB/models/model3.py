"""
This script implements Model 3 for MongoDB document design.
In Model 3, each company document embeds an array of person documents in a 'staff' field.

Pipeline Steps Implemented in this File:
Step 1: Clear previous data from the target collection (`clear_collections`)
Step 2: Insert company and employee data following the Model 3 schema (`insert_data`)
Step 3: Run and time the required queries:
    - Q1: For each person, retrieve their full name and their company’s name
    - Q2: For each company, retrieve its name and the number of employees
    - Q3: Update the age of each person born before 1988 to 30
    - Q4: Update each company's name to include the word "Company"
"""

from utils import timed_query

class Model3:
    def __init__(self, db):
        """
        Constructor: Initializes the model using a MongoDB database reference.
        """
        self.db = db
        self.companies = db.model3_companies  # Collection to store companies with embedded staff

    def clear_collections(self):
        """
        Step 1: Drop the collection to remove any existing data.
        Ensures a clean slate before inserting new data.
        """
        self.companies.drop()

    def insert_data(self, persons, companies):
        """
        Step 2: Insert data into the database following the embedded company-person model.
        - Persons are embedded as a 'staff' array inside each company document.
        - We build a map of companies and append the appropriate staff to each.
        """
        company_map = {c['name']: c for c in companies}  # Map by company name
        for c in company_map.values():
            c['staff'] = []  # Initialize the staff list

        for p in persons:
            company_name = p['company']['name']
            person_copy = p.copy()
            del person_copy['company']  # Remove company info to avoid redundancy
            company_map[company_name]['staff'].append(person_copy)

        self.companies.insert_many(company_map.values())

    @timed_query
    def query1(self):
        """
        Step 3 - Q1: Retrieve full name of each person and their company name.
        Since persons are embedded, we iterate over companies and extract names from embedded 'staff'.
        """
        companies = self.companies.find({}, {"name": 1, "staff.fullName": 1})
        for c in companies:
            for p in c.get("staff", []):
                print({"fullName": p['fullName'], "companyName": c['name']})

    @timed_query
    def query2(self):
        """
        Step 3 - Q2: Retrieve each company's name and count of employees.
        Employee count is the length of the embedded 'staff' array.
        """
        for c in self.companies.find({}, {"name": 1, "staff": 1}):
            print({
                "companyName": c["name"],
                "numEmployees": len(c.get("staff", []))
            })

    @timed_query
    def query3(self):
        """
        Step 3 - Q3: Update the age to 30 for persons born before 1988.
        As persons are embedded, this requires reading, modifying, and updating the whole document.
        """
        all_companies = list(self.companies.find())
        for c in all_companies:
            for p in c.get("staff", []):
                if p["dateOfBirth"] < "1988-01-01":
                    p["age"] = 30
            # Update the company's embedded staff array
            self.companies.update_one({"_id": c["_id"]}, {"$set": {"staff": c["staff"]}})

    @timed_query
    def query4(self):
        """
        Step 3 - Q4: Append the word 'Company' to each company name.
        Uses an aggregation pipeline update with `$concat`.
        """
        self.companies.update_many(
            {},
            [{"$set": {"name": {"$concat": ["$name", " Company"]}}}]
        )
