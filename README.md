# Django - Healthcare Backend API

A RESTful healthcare backend built using Django, Django REST Framework, and PostgreSQL. The API provides JWT-based authentication and allows authenticated users to manage patients, doctors, and patient-doctor mappings.

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Django REST Framework Simple JWT
- Docker Compose
- psycopg
- python-dotenv

## Features

- User registration and JWT authentication
- Patient CRUD operations with user-level ownership
- Shared doctor directory with CRUD operations
- Patient-doctor mapping management
- Duplicate mapping prevention
- Request validation and authentication permissions

## Project Structure

```text
Django_assessment/
├── accounts/
├── patients/
├── doctors/
├── mappings/
├── config/
├── manage.py
├── requirements.txt
├── docker-compose.yml
├── .env.example
└── README.md
```

## Setup Instructions

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd Django_assessment
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Create a `.env` file in the project root using `.env.example` as a reference.

Configure the following variables:

```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DB_NAME=carebridge_db
DB_USER=carebridge_user
DB_PASSWORD=your-database-password
DB_HOST=localhost
DB_PORT=5432
```

Never commit your actual `.env` file or production credentials.

### 5. Start PostgreSQL

Start the PostgreSQL database using Docker Compose:

```bash
docker compose up -d
```

### 6. Apply migrations

```bash
python manage.py migrate
```

### 7. Run the development server

```bash
python manage.py runserver
```

The API will be available at:

`http://127.0.0.1:8000/`

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain JWT tokens |

### Patients

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/patients/` | Create a patient |
| GET | `/api/patients/` | List own patients |
| GET | `/api/patients/<id>/` | Retrieve a patient |
| PUT | `/api/patients/<id>/` | Update a patient |
| DELETE | `/api/patients/<id>/` | Delete a patient |

### Doctors

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/doctors/` | Create a doctor |
| GET | `/api/doctors/` | List doctors |
| GET | `/api/doctors/<id>/` | Retrieve a doctor |
| PUT | `/api/doctors/<id>/` | Update a doctor |
| DELETE | `/api/doctors/<id>/` | Delete a doctor |

### Patient-Doctor Mappings

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List mappings for own patients |
| GET | `/api/mappings/patients/<patient_id>/` | List mappings for a patient |
| DELETE | `/api/mappings/<id>/` | Delete a mapping |

## Authentication

Protected endpoints require a JWT access token.

Include the following header in authenticated requests:

```http
Authorization: Bearer <access_token>
```

Obtain tokens through the login endpoint.

## Security and Data Access

- Patients are associated with the user who created them.
- Users can only access and manage their own patients.
- Doctors are maintained in a shared directory accessible to authenticated users.
- Patient-doctor mappings are restricted to the patient's owner.
- Duplicate patient-doctor mappings are prevented.
- Sensitive configuration is managed through environment variables.

## Running Tests

Run the complete automated test suite:

```bash
python manage.py test
```

The project includes automated tests for authentication, patient operations, doctor operations, and patient-doctor mappings.

## License

Created as part of a Django healthcare backend technical assessment.