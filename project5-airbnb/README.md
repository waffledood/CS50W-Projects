# Project 5 / Capstone Project (Airbnb clone)

## Project Description

This project is an Airbnb clone, or a booking system website, where users can either list their properties for other users to rent, or search for properties to rent.

## Distinctiveness & Complexity

### Distinctiveness

This project is distinct from other projects in CS50W 2020 as this project is at its core, a booking system application. The other projects: Project 1 -- a search engine landing page, Project 2 -- an e-commerce website, Project 3 -- web-based email service, Project 4 -- a social network website are unique.

This project thus has a different set of business logic & requires a different system design.

### Complexity

Complexity of this project:

- Uses a custom `User` model & `UserManager`, `UserAdmin`, `UserCreationForm`, `UserChangeForm` classes, as this `User` model does not enforce `username`s as the unique identifier unlike Django's default `User` model.
- `Django` is used for the backend, `React` is used for the frontend. Previous projects were built fully in `Django`.

## External Packages

An accompanying `requirements.txt` listing all external packages has been included.

For ease of reference, the full list is appended below:

- `varname`
- `django-cors-headers`
- `axios`
- `js-cookie`

## Terminology

This section details the jargons used in this application & what they mean:

- Listing
  A property that has been listed on Airbnb as available for booking.
  A listing includes the following details:

  - Picture(s) of the property
  - Address of the property
  - Nightly rate of the property

- Slot/Slots
  An available window in the property's booking schedule.

  A slot refers to 1 night. Slots refer to multiple nights.

## Architecture, System Design

React is used on the frontend, with Django for the backend.

Django views are used as API endpoints.

### Pages

The following are pages/views in the Airbnb clone application:

1. Main page

   - Shows all current listings
     All listings with available slots in the near future (up to 2 years from today's date)

2. View Listing page

   - Shows details of a listing

3. Create Listing page

   - Creation of a listing

4. Account page

   - Displays details of a user's account

## Database Design

The following is the database schema of this application:

`User`

| Column    | Key |     |     | Type |
| --------- | --- | --- | --- | ---- |
| bookingId | PK  | NN  | AI  | INT  |
| userId    | FK  |     |     |      |
| listingId | FK  |     |     |      |
| startDate |     |     |     | TIME |
| endDate   |     |     |     | TIME |

`Listing`

| Column      | Key |     |     | Type   |
| ----------- | --- | --- | --- | ------ |
| listingId   | PK  | NN  | AI  | INT    |
| ownerId     | FK  |     |     |        |
| name        |     |     |     | CHAR   |
| description |     |     |     | CHAR   |
| rating      |     |     |     | DOUBLE |
| rentNightly |     |     |     | DOUBLE |

`Booking`

| Column    | Key |     |     | Type |
| --------- | --- | --- | --- | ---- |
| bookingId | PK  | NN  | AI  | INT  |
| userId    | FK  |     |     |      |
| listingId | FK  |     |     |      |
| startDate |     |     |     | TIME |
| endDate   |     |     |     | TIME |

References:

- [SQL Data types](https://www.w3schools.com/sql/sql_datatypes.asp)
