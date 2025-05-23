# **Database Design**


## M1: Two types of documents, one for each class and references fields.

```json
// Person document
{
  "_id": "person_id",
  "firstName": "Lucia",
  "fullName": "Lucia Roberts",
  "email": "lucia@example.com",
  "companyEmail": "lucia@company.com",
  "dateOfBirth": "1999-03-03",
  "age": 26,
  "sex": "F",
  "companyId": "company_id"
}

// Company document
{
  "_id": "company_id",
  "name": "Impactum",
  "email": "contact@econai.com",
  "domain": "impactum.ai",
  "url": "http://impactum.ai",
  "varNumber": "123456789"
}
```

## M2: One document for Person, with Company as embedded docuement.

```json
// Person document with embedded company
{
  "_id": "person_id",
  "firstName": "Lucia",
  "fullName": "Lucia Roberts",
  "email": "lucia@example.com",
  "companyEmail": "lucia@company.com",
  "dateOfBirth": "1999-03-03",
  "age": 26,
  "sex": "F",
  "company": {
    "name": "Impactum",
    "email": "contact@econai.com",
    "domain": "impactum.ai",
    "url": "http://impactum.ai",
    "varNumber": "123456789"
  }
}
```



## M3: One document for Company, with Person as embedded docuements.

```json
// Company document with embedded staff
{
  "_id": "company_id",
  "name": "Impactum",
  "email": "contact@econai.com",
  "domain": "impactum.ai",
  "url": "http://impactum.ai",
  "varNumber": "123456789",
  "staff": [
    {
      "_id": "person_id",
      "firstName": "Lucia",
      "fullName": "Lucia Roberts",
      "email": "lucia@example.com",
      "companyEmail": "lucia@company.com",
      "dateOfBirth": "1999-03-03",
      "age": 26,
      "sex": "F"
    },
    {
      "_id": "person_id2",
      "firstName": "Julian",
      "fullName": "Julian Smith",
      "email": "julian@example.com",
      "companyEmail": "julian@company.com",
      "dateOfBirth": "1999-04-24",
      "age": 26,
      "sex": "M"
    }
  ]
}

```