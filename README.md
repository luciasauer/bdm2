# 🚀 BDM2 - NoSQL Database Design with MongoDB


![MongoDB](https://img.shields.io/badge/MongoDB-NoSQL-brightgreen?logo=mongodb)
![Status](https://img.shields.io/badge/Project%20Type-Academic-blue)
![Language](https://img.shields.io/badge/Python-3.10+-yellow?logo=python)

This project explores core concepts of document-oriented databases using **MongoDB**, one of the most widely adopted NoSQL systems. It demonstrates how to design and model document structures, import and manipulate data, and execute queries efficiently. The project also walks through setting up the environment and provides hands-on exercises that reinforce key principles of document store management, particularly in the context of Big Data.

> 👩🏻‍💻🧑‍💻 *Project by Lucia Sauer & Julian Romero*  
> 🎓 *Master in Data Science – Barcelona School of Economics*

---

## 🗂️ Repository Structure

```
BDM2-Assignment2/
│
├── SectionA/                     # JSON structure definitions for each data model
│   └── model_structures.md      # Describes the document designs for Model 1, 2, and 3
│
├── SectionB/
│   └── project/
│       ├── main.py              # Orchestrates data generation, insertion, and querying
│       ├── data_generator.py    # Generates company and person data
│       ├── models/              # Model implementations
│       │   ├── model1.py        # Reference-based model (normalized)
│       │   ├── model2.py        # Embedded company inside person (denormalized)
│       │   └── model3.py        # Embedded persons inside company (denormalized)
│       └── utils.py             # Shared utilities (e.g., for measuring execution time)
│
├── L2-T01_submission.pdf        # Final report (Section C): performance evaluation and conclusions
```

---

## 🧪 How to Run

1. Ensure MongoDB is installed and running locally.
2. Navigate to the `SectionB` directory.
3. Run the main script:

   ```bash
   python main.py
   ```

This will:

* Generate a dataset of companies and associated persons.
* Insert the data according to three data models.
* Run benchmark queries and display the average execution times.

---

## 📌 Key Findings

Each document model has its own strengths and limitations. The performance and maintainability of a MongoDB schema depend on the query patterns and update frequency.

| Model  | Characteristics                      | ✅ Pros                                 | ⚠️ Cons                                          |
| ------ | ------------------------------------ | -------------------------------------- | ------------------------------------------------ |
| **M1** | Separate collections with references | Flexible updates, normalized structure | Requires joins and aggregations for related data |
| **M2** | Company embedded in each person      | Fast person-centric queries            | Redundant company data across documents          |
| **M3** | Persons embedded in each company     | Efficient company-centric queries      | Updating individual person info is complex       |

📌 **TL;DR**:

* **M1** is best when updates are frequent and relationships change often.
* **M2** is optimal for read-heavy, person-focused applications.
* **M3** excels when queries are company-centric and updates are infrequent.

---

## 📄 Submission

The final report `L2-T01_submission.pdf` contains:

* A breakdown of each model’s design choices.
* Query performance benchmarks.
* A detailed analysis of trade-offs between schema types.
