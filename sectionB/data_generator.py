from faker import Faker
import random
from datetime import datetime

fake = Faker()

def generate_companies(n):
    companies = []
    for _ in range(n):
        companies.append({
            "name": fake.company(),
            "email": fake.company_email(),
            "domain": fake.domain_name(),
            "url": fake.url(),
            "varNumber": fake.ein()
        })
    return companies

def generate_persons(n, companies):
    persons = []
    for _ in range(n):
        company = random.choice(companies)
        dob = fake.date_of_birth(minimum_age=20, maximum_age=60)
        persons.append({
            "firstName": fake.first_name(),
            "fullName": fake.name(),
            "email": fake.email(),
            "companyEmail": fake.company_email(),
            "dateOfBirth": dob,
            "age": datetime.now().year - dob.year,
            "sex": random.choice(['M', 'F']),
            "company": company
        })
    return persons
