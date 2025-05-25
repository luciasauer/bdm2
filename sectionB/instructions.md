# Section B: Implementation Instructions

1. Before running `main.py`, ensure to have MongoDB service running. 
2. Located in the root directory of the repository, create a virtual environment by running `uv sync` ([check uv installation](https://docs.astral.sh/uv/getting-started/installation/)).
3. Activate the virtual environment:
    ```bash
    source .venv/bin/activate
    ```
3. Execute the `main.py`
    ```bash
    $ python main.py

    Generating datasets...

    Running Model1...
    Number of results collected: 1000000
    Run 1/5: 9.2089 seconds
    Number of results collected: 1000000
    Run 2/5: 8.9989 seconds
    Number of results collected: 1000000
    Run 3/5: 9.1434 seconds
    Number of results collected: 1000000
    Run 4/5: 9.0844 seconds
    Number of results collected: 1000000
    Run 5/5: 8.9850 seconds
    Average execution time for query1 over 5 runs: 9.0841 seconds
    Number of results collected: 37009
    Run 1/5: 0.5590 seconds
    Number of results collected: 37009
    Run 2/5: 0.5391 seconds
    Number of results collected: 37009
    Run 3/5: 0.5393 seconds
    Number of results collected: 37009
    Run 4/5: 0.5703 seconds
    Number of results collected: 37009
    Run 5/5: 0.5438 seconds
    Average execution time for query2 over 5 runs: 0.5503 seconds
    Documents matched: 575787
    Documents modified: 575787
    Run 1/1: 1.7027 seconds
    Average execution time for query3 over 1 runs: 1.7027 seconds
    Documents matched: 50000
    Documents modified: 50000
    Run 1/5: 0.1924 seconds
    Documents matched: 50000
    Documents modified: 50000
    Run 2/5: 0.2102 seconds
    Documents matched: 50000
    Documents modified: 50000
    Run 3/5: 0.2182 seconds
    Documents matched: 50000
    Documents modified: 50000
    Run 4/5: 0.3509 seconds
    Documents matched: 50000
    Documents modified: 50000
    Run 5/5: 0.4803 seconds
    Average execution time for query4 over 5 runs: 0.2904 seconds

    Running Model2...
    ```

The code will execute the steps described in section 1, 2 and 3.

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

| Model        | Characteristics                      | Pros                                    | Cons                                        |
| -----------  | ------------------------------------ | --------------------------------------- | ------------------------------------------- |
| **M1**  | Separate collections with references | Flexible updates, normalized structure  | Requires joins/aggregation for related data |
| **M2**  | Company embedded in each person      | Faster reads for person-centric queries | Redundant company data across persons       |
| **M3**  | Persons embedded in each company     | Efficient company-centric queries       | Difficult to update individual person info  |
