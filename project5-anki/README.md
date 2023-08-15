# Project 5 (Anki)

## Starting The Project

### Frontend

Run `npm run dev` in `frontend/` to run webpack, any changes made to `index.js` will be automatically saved to `backend/anki/static/anki/build`.

### Backend

Run `python3 manage.py runserver` to start the Django backend server.

## System Design, Architecture

### Database Design

The following is the database schema of this application

`User`

| Column      | Key |     |     | Type     |
| ----------- | --- | --- | --- | -------- |
| id          | PK  | NN  | AI  | INT      |
| username    |     |     |     | VARCHAR  |
| email       |     |     |     | VARCHAR  |
| is_staff    |     |     |     | BOOLEAN  |
| is_active   |     |     |     | BOOLEAN  |
| date_joined |     |     |     | DATETIME |

`Collection`

| Column        | Key |     |     | Type     |
| ------------- | --- | --- | --- | -------- |
| id            | PK  | NN  | AI  | INT      |
| user_id       | FK  |     |     | INT      |
| name          |     |     |     | CHAR     |
| date_created  |     |     |     | DATETIME |
| date_modified |     |     |     | DATETIME |

`Card`

| Column        | Key |     |     | Type |
| ------------- | --- | --- | --- | ---- |
| id            | PK  | NN  | AI  | INT  |
| collection_id | FK  |     |     | INT  |
| question      |     |     |     | CHAR |
| answer        |     |     |     | CHAR |
