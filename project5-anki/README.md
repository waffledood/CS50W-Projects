# Project 5 (Anki)

## Starting The Project

### Frontend

Run `npm run dev` in `frontend/` to run webpack, any changes made to `index.js` will be automatically saved to `backend/anki/static/anki/build`.

### Backend

Run `python3 manage.py runserver` to start the Django backend server.

## System Design, Architecture

### Pages

The following are pages/views in the Anki application:

1. Main page

   - Shows all the Collection(s) the current User has.

2. Collection page

   - Shows all the details of a selected Collection:
     - the Collection's name,
     - the Collection's description
     - all of the Card(s) in this Collection
   - A User will be able to modify the Collection's name & description.
   - A User will be able to delete this Collection.
   - A User will be able to delete any of the Card(s) in this Collection.

3. Card page

   - Shows the question & answer of this Card, & the Collection this Card is associated with.
   - A User will be able to modify, or delete this Card.

4. Create Collection page

   - A User will be able to create a Collection.
   - Details to be provided:
     - Name of collection - A text-based (text, numbers & special characters) name

5. Create Card page

   - A User will be able to create a Card.
   - Details to be provided:
     - Question - A text-based (text, numbers & special characters) question
     - Answer - A text-based (text, numbers & special characters) answer

6. Account page

   - Shows the details of the current User.

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
