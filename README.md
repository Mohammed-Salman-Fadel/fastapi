# FastAPI Assignment

## About the Repository

Includes:

- FastAPI and SQLite demonstrations.
- Logging into a `logs.log` file.
- Comments under each function that simply describes the function's purpose.

### Repo Structure

```
├── README.md
├── main.py
├── app/
│ └── api/
│ |     └── addresses.py
│ |
| ├── logs/
| |     └── logs.log
| |
| ├── core/
| |     ├── config.py
| |     └── logging.py
| ├── db/
| |   ├── addresses.db
| |   └── database.py
| |
| └── schema/
|      └── address.py
└── requirements.txt
```

For the sake of maintaining proper standards, the database file and logs file were not uploaded into the repository, however I left some sample data for demonstration purposes that you could simply uncomment the sample_date function call from the `database.py` file and once the application is ran, the database would load with the sample data, and the logs will load on your machine.

---

### How to Run

The recommended steps to run everything smoothly are:

1. Create and enter virtual environment:

   ```
   python -m venv .venv
   .venv\Scripts\activate
   ```

2. Download `requirements.txt` dependencies:

   ```
   pip install -r requirements.txt
   ```

3. Lastly, simply run the following command to view the live demo in `http://127.0.0.1:8000/docs#/(FastAPI Swagger UI)`:

   ```
   uvicorn main:app --reload
   ```

- The application should run and the API should be capable of being tested through the Swagger UI.
