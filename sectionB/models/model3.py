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
        self.companies = db.companies  # Collection to store companies with embedded staff

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

    @timed_query(repeats=5)
    def query1(self):
        """
        Step 3 - Q1: Retrieve full name of each person and their company name.
        - 1) Project only the company name and the full name of the employees.
        - 2) Unnest the staff array via unwind operator.
        - 3) Project the desired columns and rename accordingly.
        """
        pipeline = [
            {
                "$project":{
                    "_id":0,
                    "name":1,
                    "staff.fullName":1
                }
            },
            {
                "$unwind": "$staff"
            },
            {
                "$project":
                {
                    "fullName":"$staff.fullName",
                    "CompanyName":"$name"
                }
            }
        ]
        results = self.companies.aggregate(pipeline)
        # for doc in results:
        #     print(doc)

    @timed_query(repeats=5)
    def query2(self):
        """
        Step 3 - Q2: Retrieve each company's name and count of employees.
        - 1) Find all companyes and get the size of the staff arrays to know the number of employees.
        """
        results = self.companies.find({}, {"_id":0, "CompanyName":"$name","numEmployees":{"$size":"$staff"}})
        # for doc in results:
        #     print(doc)

    @timed_query(repeats=5)
    def query3(self):
        """
        Step 3 - Q3: Update the age to 30 for persons born before 1988.
        As persons are embedded in staff, we use an array filter to target the correct documents.
        - 1) Filter those companies with at least one staff member born before (less than) 1988.
        - 2) Set the age to 30 of those that pass the array filter:
            - Apply an array filter to only update the values of those born before 1988.
        """
        self.companies.update_many(
            {"staff.dateOfBirth": {"$lt": "ISODate('1988-01-01')"}}, #filter by the companies that have staff with dateOfBirth < 1988
            {"$set": {"staff.$[person].age": 30}}, #update the age of the employees who meet the condition
            array_filters=[{"person.dateOfBirth": {"$lt": "ISODate('1988-01-01')"}}] #array filter to update only the staff members who meet the condition
        )

    @timed_query(repeats=5)
    def query4(self):
        """
        Step 3 - Q4: Append the word 'Company' to each company name.
        - 1) Update many values (all in this case, as the filter is empty), setting
            the name as Company + original name, with the help of the `$concat` operator.
        """
        self.companies.update_many(
            {},
            [{"$set": {"name": {"$concat": ["Company ","$name"]}}}]
        )
