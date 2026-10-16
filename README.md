# Students Database CRUD Application

**Internship assignment:** EWB Edu Tech Pvt. Ltd. — Python Backend Development  
**Stack:** Python, FastAPI, SQLite, SQLAlchemy, Pydantic

## 1. Project overview

This individual backend project manages student records using Create, Read, Update and Delete (CRUD) operations. FastAPI provides REST endpoints, SQLite stores records persistently on the local computer, and Pydantic validates incoming data.

The project follows the mandatory core requirements in the assignment PDF. The optional Ollama AI extension is not included because it is not required for completion.

## 2. Features

- Create a student record.
- List all students and filter by name, course, or date of birth.
- Retrieve one student by ID.
- Replace all editable details with `PUT`.
- Update selected fields with `PATCH`.
- Delete a student by ID.
- Validate dates, email addresses, field lengths, and contact information.
- Return clear errors for missing records and duplicate email addresses.
- Store data in SQLite so it remains after restarting the API.
- Interactive API documentation at `/docs`.
- Automated tests for core API behavior.

## 3. Project structure

```text
students_database_crud/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_main.py
├── .gitignore
├── README.md
└── requirements.txt
```

The SQLite database file `students.db` is created automatically when the application starts. It is intentionally excluded from Git so local/generated data is not committed.

## 4. Requirements

- Python 3.10 or newer
- pip
- A terminal such as PowerShell, Command Prompt, or the VS Code terminal

Check Python:

```bash
python --version
```

## 5. Installation on Windows / VS Code

1. Extract the project ZIP.
2. Open the extracted `students_database_crud` folder in VS Code.
3. Open **Terminal → New Terminal**.
4. Create a virtual environment:

```powershell
python -m venv .venv
```

5. Activate it in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use Command Prompt:

```bat
.venv\Scripts\activate.bat
```

Or run the environment's Python directly without activating it:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

6. Install dependencies (if the environment is activated):

```bash
python -m pip install -r requirements.txt
```

## 6. Run the application

From the project root folder:

```bash
python -m uvicorn app.main:app --reload
```

Open these addresses in your browser:

- API home: http://127.0.0.1:8000/
- Interactive Swagger documentation: http://127.0.0.1:8000/docs
- Alternative API documentation: http://127.0.0.1:8000/redoc

Keep the terminal open while testing. Press `Ctrl+C` to stop the server.

## 7. API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| `POST` | `/students` | Create a student |
| `GET` | `/students` | List/filter students |
| `GET` | `/students/{student_id}` | Retrieve one student |
| `PUT` | `/students/{student_id}` | Replace student details |
| `PATCH` | `/students/{student_id}` | Update selected fields |
| `DELETE` | `/students/{student_id}` | Delete a student |

### Student fields

- `id`: unique database-generated student ID
- `name`: required name
- `date_of_birth`: required date in `YYYY-MM-DD` format
- `email`: optional email address; must be unique if supplied
- `phone`: optional contact number
- `course`: optional course
- `address`: optional address
- `enrollment_date`: optional date in `YYYY-MM-DD` format

At least one contact method (email or phone) must be supplied when creating a student.

## 8. Test the API

The easiest method is to open http://127.0.0.1:8000/docs, expand an endpoint, click **Try it out**, enter the sample JSON, and click **Execute**.

### Create a student — POST `/students`

```json
{
  "name": "Aarav Patil",
  "date_of_birth": "2005-04-12",
  "email": "aarav.demo@example.com",
  "phone": "9876543210",
  "course": "Computer Engineering",
  "address": "Pune, Maharashtra",
  "enrollment_date": "2025-08-01"
}
```

The response should have status `201 Created` and include a generated `id`.

### List students — GET `/students`

No request body is needed.

Filter examples:

- `/students?name=Aarav`
- `/students?course=Computer%20Engineering`
- `/students?born_after=2005-01-01`

### Get one student — GET `/students/1`

Replace `1` with the ID returned by the create request.

### Replace student — PUT `/students/1`

Send all required fields, as in the create example. Replace the ID with the one returned by your API.

### Partially update — PATCH `/students/1`

```json
{
  "course": "Information Technology"
}
```

### Delete — DELETE `/students/1`

Use an existing ID. A successful delete returns `204 No Content`.

## 9. Error handling

- `404 Not Found`: student ID does not exist.
- `409 Conflict`: email address is already assigned to another student.
- `422 Unprocessable Entity`: invalid input, invalid email/date, missing required fields, or invalid contact details.
- `201 Created`: record created successfully.
- `204 No Content`: record deleted successfully.

## 10. Run automated tests

Install dependencies, then run from the project root:

```bash
python -m pytest -v
```

Tests use a temporary SQLite database and do not need real student data.

## 11. Upload to GitHub

1. Create a repository, for example `students-database-crud`.
2. Open the project root in VS Code.
3. Use the Source Control panel to initialize Git, stage files, enter a commit message, and commit.
4. Publish the branch / push to the repository, or use the commands below after creating an empty repository.

```bash
git init
git add .
git commit -m "Build students database CRUD API"
git branch -M main
git remote add origin https://github.com/YOUR-USERNAME/students-database-crud.git
git push -u origin main
```

Replace `YOUR-USERNAME` with your GitHub username. If Git says `remote origin already exists`, check it with `git remote -v` instead of adding it again. If authentication fails, sign in through Git Credential Manager or use GitHub's browser sign-in flow; GitHub does not accept account passwords for HTTPS Git operations.

Before committing, check that `.env`, passwords, API keys, real student personal information, and the local database file are not included.

## 12. Architecture

```text
Client / Swagger UI
        |
        v
FastAPI routes (app/main.py)
        |
        v
Pydantic validation (app/schemas.py)
        |
        v
SQLAlchemy models (app/models.py)
        |
        v
SQLite database (students.db)
```

## 13. Security and limitations

- Use only dummy/sample student records for demonstrations.
- Do not store or publish real student personal information.
- Do not commit secrets or database files.
- This is a learning project, not a production student-information system. Authentication, authorization, backups, migrations, and production deployment would need to be added before real-world use.
- The optional Ollama extension is intentionally omitted; the assignment states that the CRUD application alone is sufficient.

## 14. Submission checklist

- [ ] FastAPI application starts successfully.
- [ ] Create, read, update and delete endpoints work.
- [ ] SQLite records persist after restarting the API.
- [ ] Invalid input and missing records are handled.
- [ ] Automated tests pass.
- [ ] README, source code, and requirements are included.
- [ ] Only safe sample data is used.
- [ ] GitHub repository is public or otherwise accessible to the trainer.
- [ ] Repository link is submitted through the channel announced by the EWB trainer.
