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

## Architecture

React is used on the frontend, with Django for the backend.

Django views are used as API endpoints.
