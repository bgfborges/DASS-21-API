# DASS-21 API

## Overview

This API, built using Python with Django and PostgreSQL, is designed to facilitate the registration of profiles and collect responses to the Depression, Anxiety, and Stress Scale (DASS-21). The primary functionalities include retrieving a list of DASS-21 questions and answer options, as well as submitting responses and building an initial profile.

## API Endpoints

### Profile Registration

#### GET /api/dass21/questions

- **Description:** Retrieve a list of DASS-21 questions along with available answer options.

- **Parameters:** None

- **Response:**
  ```json
  {
    "questions": [
      {
        "id": 1,
        "text": "I found it hard to wind down.",
        "options": ["Never", "Sometimes", "Often", "Always"]
      },
      // ... other questions
    ]
  }
  ```

#### POST /api/dass21/profile

- **Description:** Submit a list of DASS-21 question answers along with possible extra-text.

- **Request:**
  ```json
  {
    "answers": [
      {"question_id": 1, "answer": "Sometimes"},
      {"question_id": 2, "answer": "Often"},
      // ... other answers
    ],
    "extra_text": "Additional comments or context."
  }
  ```

- **Response:**
  ```json
  {
    "profile_id": 123,
    "message": "Profile successfully created."
  }
  ```

### Backend

- **Validation:** The backend validates the submitted answers and ensures that they conform to the expected format.

- **Profile Creation:** After validation, the backend creates a profile, associating it with the provided answers and saving it to the database.

## Database Schema

### Profile Model

- **Fields:**
  - `id` (AutoField)
  - `created_at` (DateTimeField)
  - `updated_at` (DateTimeField)
  - `extra_text` (TextField, optional)
  
### Answer Model

- **Fields:**
  - `id` (AutoField)
  - `question` (ForeignKey to Question Model)
  - `answer` (CharField)
  - `profile` (ForeignKey to Profile Model)

### Question Model

- **Fields:**
  - `id` (AutoField)
  - `text` (CharField)
  - `options` (ArrayField of CharField)

## Setup

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/dass21-api.git
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Apply database migrations:

   ```bash
   python manage.py migrate
   ```

4. Run the development server:

   ```bash
   python manage.py runserver
   ```

The API is now accessible at `http://localhost:8000/api/dass21/`.