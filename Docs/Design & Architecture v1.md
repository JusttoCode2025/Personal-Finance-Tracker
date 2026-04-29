# Software Design Document (SDD)

## 1. Introduction
- **Purpose**: The purpose of this document is to describe the software design and architecture of the FinanceTracker web application. It will explain the system structure component, data flow, and technical decision made durng development.
- **Scope**: **In Scope**: login and signup UI, user sets monthly income, expense category limits, purchase tracking, tracks purchase towards goal, dashboard, and a congratulations page when goal is reached. **Out of Scope**: multi-user account management, full authentication, muliti-user account management and banking integration
- **Definitions and Acronyms**: UI – User Interface; API – Application Programming Interface; DB – Database

- **References**: https://gist.github.com/iamhenry/2dbabd0d59051eae360d8cfa6a2782bd

---

## 2. System Overview
- **System Description**: FinanceTracker is a Flask-based web application that allows users to manage budget limits and track spending by category in order to reach a major goal
- **Design Goals**: Maintainability and simplicity
- **Architecture Summary**: Flask 
- **System Context Diagram**:
  - Example placeholder:
    ```mermaid
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/25fb445c-bde7-42e5-aca8-1aa42288c59d" />

    ```
---

## 3. Architectural Design
- **System Architecture Diagram**:
  - <img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/c7ced76c-080e-4ce0-8004-332c3adf1ad7" />
- **Component Breakdown**:
  - - Html, Java, and CSS: Displays system UI, sends a request, and updates data
  - - Flask: Routing and validation
    - Database: Stores limits and purchases
- **Technology Stack**: Python, Flask, HTML, CSS, JavaScript, Postgresql, Gunicorn (deployment), and Render (hosting)
---

## 4. Detailed Design
For each module/component:

### Budget Module
- **Responsibilities**: Set limits, add purchases, and calculate remaining balances
- **Interfaces/APIs**:
  - Inputs: category, amount and limit amount.
  - Outputs: Json warning or validation and updated balances
  - Error Handling: Invalid inputs are rejected and if there is missing info it is rejected
- **Data Structures**: spending limits and purchase history

---

## 5. Database Schema
-- Stores category spending limits
CREATE TABLE spending_limits (
    id SERIAL PRIMARY KEY,
    category TEXT UNIQUE NOT NULL,
    limit_amount REAL NOT NULL,
    remaining REAL NOT NULL
);

-- Stores all purchases
CREATE TABLE purchases (
    id SERIAL PRIMARY KEY,
    category TEXT NOT NULL,
    amount REAL NOT NULL,
    date TIMESTAMP NOT NULL
);

-- Stores the travel savings goal
CREATE TABLE travel_goals (
    id SERIAL PRIMARY KEY,
    destination TEXT NOT NULL,
    target_amount REAL NOT NULL,
    saved_amount REAL DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    note TEXT DEFAULT '',
    target_date DATE DEFAULT NULL
);

-- Stores app-wide settings (monthly reset timestamp)
CREATE TABLE settings (
    id SERIAL PRIMARY KEY,
    budget_reset_at TIMESTAMP DEFAULT NULL
);

---


## 6. Testing Strategy


---

## 7.
Project Structure
Personal-Finance-Tracker/
├── app.py                  # Flask backend, all routes
├── frontend/
│   ├── templates/          # HTML pages
│   │   ├── login.html
│   │   ├── signup.html
│   │   ├── home.html
│   │   ├── budget.html
│   │   ├── dashboard.html
│   │   ├── travel_goal.html
│   │   └── about.html
│   └── static/
│       └── script.js       # All frontend JavaScript
└── README.md

