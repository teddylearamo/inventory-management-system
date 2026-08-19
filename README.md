# Inventory Management System

A Python-based inventory management system built with Flask, SQLite, OpenFoodFacts API, and a command-line interface.

## Project Description

This project provides a REST API for managing inventory items.

Employees can:

- View all inventory items
- View a single inventory item
- Add new inventory items
- Update inventory items
- Delete inventory items
- Look up product information using the OpenFoodFacts API

The application also provides a CLI for interacting with the REST API.

## Technologies Used

- Python 3
- Flask
- SQLite
- Pytest
- Requests
- OpenFoodFacts API
- Argparse
- Git/GitHub

## Project Structure

```text
inventory-management-system/
│
├── server/
│   ├── __init__.py
│   ├── app.py
│   ├── models.py
│   └── external_api.py
│
├── cli/
│   ├── __init__.py
│   └── main.py
│
├── tests/
│   ├── test_app.py
│   └── test_external_api.py
│
├── .gitignore
├── Pipfile
├── Pipfile.lock
└── README.md