# Section B: Implementation Instructions

## 1. 🏗️ Data Generation

We use the [`Faker`](https://faker.readthedocs.io/) Python library to simulate random companies and employees. To ensure a fair comparison across the three data models, the **same dataset** is used consistently throughout all models.

## 2. 💾 Data Insertion and Query Execution

Each data model is implemented in its own dedicated module:

* `model1.py`
* `model2.py`
* `model3.py`

These modules are responsible for:

* Structuring and inserting data into MongoDB using the respective model design.
* Defining and executing the required queries (Q1 to Q4).

To maintain clean and modular code, data generation logic is separated into `data_generator.py`, while reusable utilities (e.g., timing decorators) are housed in `utils.py`.

## 3. ⏱️ Query Timing

We measure the execution time of each query using the `timed_query` decorator defined in `utils.py`. This decorator is applied to each query function and automatically logs the time taken for query execution.

Example usage:

```python
@timed_query
def query_1():
    # MongoDB query logic
```

This ensures consistent and minimal-intrusion benchmarking of all queries across all models.

## 4. 📁 Project Structure

```bash
project/
│
├── main.py               # Orchestrates data generation, insertion, and querying
├── data_generator.py     # Responsible for generating company and person data
├── models/               # Contains one file per data model
│   ├── model1.py         # Reference-based model
│   ├── model2.py         # Embedded company inside person
│   └── model3.py         # Embedded persons inside company
└── utils.py              # Shared utilities (e.g., timing decorators)
```

## 5. Summary of Model Trade-Offs

| Model       | Characteristics                      | Pros                                    | Cons                                        |
| ----------- | ------------------------------------ | --------------------------------------- | ------------------------------------------- |
| **Model 1** | Separate collections with references | Flexible updates, normalized structure  | Requires joins/aggregation for related data |
| **Model 2** | Company embedded in each person      | Faster reads for person-centric queries | Redundant company data across persons       |
| **Model 3** | Persons embedded in each company     | Efficient company-centric queries       | Difficult to update individual person info  |
