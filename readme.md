# Python FastAPI Application

A Python-based FastAPI application with support for development, testing, database migrations, and asynchronous database connections.

## Requirements

Before getting started, make sure you have:

* Python 3.x
* `pip`
* Virtual environment support
* PostgreSQL (if required by the configured database)
* Git

All Python dependencies are listed in:

```text
requirements.txt
```

---

## Project Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Create a Virtual Environment

Create a Python virtual environment using:

```bash
python3 -m venv venv
```

### 3. Activate the Virtual Environment

On Linux/macOS:

```bash
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

### 4. Install Dependencies

Install all required dependencies from `requirements.txt`:

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

The application uses different environment configurations depending on the environment.

| File        | Purpose                                  |
| ----------- | ---------------------------------------- |
| `.env.dev`  | Development and production configuration |
| `.env.test` | Test environment configuration           |

> **Important:** `APP_ENV` is mandatory. It determines which environment configuration the application loads.

## APP_ENV

The application requires the `APP_ENV` environment variable to be set before starting the application or running the test suite.

For example:

```bash
APP_ENV=dev
```

or:

```bash
APP_ENV=test
```

---

# Environment Variables

The following variables are important for running the application and tests.

## APP_ENV

Defines the environment in which the application is running.

Example:

```env
APP_ENV=dev
```

For tests:

```env
APP_ENV=test
```

`APP_ENV` is **mandatory** for both application startup and test execution.

---

## DB_URL_SYNC

`DB_URL_SYNC` is the synchronous database connection URL.

It is primarily used by **Alembic for database migrations**.

Example:

```env
DB_URL_SYNC=postgresql://username:password@localhost:5432/database
```

Use this connection when running Alembic migrations.

---

## DB_URL

`DB_URL` is the asynchronous database connection URL.

The application uses this URL for its **async database connection**.

Example:

```env
DB_URL=postgresql+asyncpg://username:password@localhost:5432/database
```

### Database URL Summary

| Variable      | Purpose                                           |
| ------------- | ------------------------------------------------- |
| `DB_URL_SYNC` | Synchronous connection used by Alembic migrations |
| `DB_URL`      | Asynchronous connection used by the application   |

---

# Database Migrations

Alembic migrations use the synchronous database connection configured through:

```env
DB_URL_SYNC
```

Make sure `DB_URL_SYNC` is correctly configured before running migrations.

Typical Alembic commands:

```bash
alembic upgrade head
```

To create a new migration:

```bash
alembic revision --autogenerate -m "migration message"
```

---

# Running the Application

First, activate the virtual environment:

```bash
source venv/bin/activate
```

Set the application environment:

```bash
export APP_ENV=dev
```

Then start the FastAPI application using Uvicorn:

```bash
uvicorn app.main:app --reload --port 5001
```

The application will run on:

```text
http://localhost:5001
```

### Windows

If you are using Windows PowerShell:

```powershell
$env:APP_ENV="dev"
uvicorn app.main:app --reload --port 5001
```

---

# Running Test Cases

The project uses `pytest` for testing.

The test suite must be executed with:

```bash
APP_ENV=test python3 -m pytest -s -v
```

### What the options mean

* `APP_ENV=test` — loads the test environment configuration
* `python3 -m pytest` — runs pytest using the active Python environment
* `-s` — displays output printed during tests
* `-v` — runs pytest in verbose mode

---

# Test Environment

Tests use the configuration from:

```text
.env.test
```

Make sure `.env.test` contains the correct test database configuration and other required environment variables.

Example:

```env
APP_ENV=test

DB_URL_SYNC=<test-database-sync-url>
DB_URL=<test-database-async-url>

IMAGE_DIR=<test-image-directory>
```

---

# Test Images

Some test cases depend on image files being available in the directory configured by:

```env
IMAGE_DIR
```

The required image files must always be present in the configured `IMAGE_DIR`.

The following files are required:

```text
girls.jpg
arch.jpeg
birds.png
fakePath999.jpg   // : Do not include fakePath999.jpg in the required test images. This file is intentionally missing to test the failure scenario when an image file is not available.
```

The tests reference these files using paths similar to:

```python
f"{secrets.IMAGE_DIR}/girls.jpg"
f"{secrets.IMAGE_DIR}/arch.jpeg"
f"{secrets.IMAGE_DIR}/birds.png"
f"{secrets.IMAGE_DIR}/fakePath999.jpg"
```

## Important

Make sure the following files exist under the configured `IMAGE_DIR`:

```text
<IMAGE_DIR>/
├── girls.jpg
├── arch.jpeg
├── birds.png
└── fakePath999.jpg
```

> **Note:** : Do not include fakePath999.jpg in the required test images. This file is intentionally missing to test the failure scenario when an image file is not available.

---

# Recommended Project Structure

A typical project structure may look like:

```text
.
├── app/
│   ├── main.py
│   └── ...
├── tests/
│   └── ...
├── alembic/
│   └── ...
├── .env.dev
├── .env.test
├── requirements.txt
├── alembic.ini
└── README.md
```

---

# Quick Start

For a quick local setup:

### 1. Create virtual environment

```bash
python3 -m venv venv
```

### 2. Activate virtual environment

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment

Make sure `.env.dev` is configured correctly.

### 5. Start the application

```bash
export APP_ENV=dev
uvicorn app.main:app --reload --port 5001
```

---

# Run Tests

To run the complete test suite:

```bash
APP_ENV=test python3 -m pytest -s -v
```

Before running tests, verify:

1. `.env.test` exists.
2. `DB_URL` points to the test database.
3. `DB_URL_SYNC` is configured for Alembic migrations.
4. `IMAGE_DIR` points to the correct test image directory.
5. All required test images are available.
6. Dependencies from `requirements.txt` are installed.

---

# Dependencies

All project dependencies are maintained in:

```text
requirements.txt
```

Install or update dependencies using:

```bash
pip install -r requirements.txt
```

---

# Environment Flow

The application environment can be summarized as:

```text
                    APP_ENV
                       |
          +------------+------------+
          |                         |
        dev                        test
          |                         |
     .env.dev                  .env.test
          |                         |
          |                    Test Suite
          |                         |
     FastAPI App               pytest
          |
      DB_URL
          |
   Async Database
```

For database migrations:

```text
DB_URL_SYNC
     |
     v
  Alembic
     |
     v
 Database Migrations
```

---

# Important Notes

* `APP_ENV` is **required** to start the application and run tests.
* `.env.dev` contains development configuration and is also used for production configuration.
* `.env.test` contains test-specific configuration.
* `DB_URL` is used for the application's **asynchronous database connection**.
* `DB_URL_SYNC` is used for **Alembic/database migrations**.
* `IMAGE_DIR` defines the location of test image files.
* Keep all required test images in the directory specified by `IMAGE_DIR`.
* Install all dependencies from `requirements.txt` before running the application or tests.
