# Personal Finance Tracker

A simple web application designed to help users track income, expenses, and savings goals in a clear and easy-to-use way.

---

## Project Overview

**Primary Users:** Students and Adults  

**Problem Statement:**  
Many people struggle to stay organized and consistent when saving money for specific financial goals. Existing tools are often overly complex or fail to clearly show progress. Users need a simple system that allows them to set goals, track income and expenses, and visualize progress over time.

**Solution:**  
The Personal Finance Tracker provides a clean dashboard, goal tracking, and helpful calculations that show users how close they are to reaching their financial goals.

---

## MVP Scope

### In Scope
- User accounts (authentication)
- Add and track income and expenses
- Dashboard with summaries and progress tracking

### Out of Scope
- Bank account integration
- Multi-user shared accounts
- Advanced or automated budgeting tools

---

## Primary Workflow

1. User creates an account and logs in
2. User creates a financial goal (amount, category, target date, optional notes)
3. Application calculates required monthly savings
4. Dashboard updates to show:
   - Total income vs expenses
   - Category breakdown
   - Monthly summary
   - Goal progress

---

## Scaffold

- **Frontend:** HTML, CSS, JavaScript
- **Backend:** Python 
- **Database:** SQLite
- **Version Control:** GitHub


## Work Plan
- Fairooz Siddiquee: Acts as the primary point of contact between development team and the professor. Responsible for delivering weekly status reports regarding the Finance Tracker's development milestones, communicating technical or resource-based roadblocks, and ensuring the project's trajectory aligns with the grading rubric and course objectives.

  
- Jasmine Anike: Responsible for the end-to-end development of the Contact and About pages, managing both Frontend and backend logic. Contact page shoup provide hyperlinks that allows the user to report a bug or ask for help while the about page explains the purpose of the tool and provides credit to the developers. 

- Jana Saleh: Responsible for the end-to-end architecture of the Main Dashboard, which serves as the central nervous system of the Finance Tracker. The dashboard should automatically calculate the breakdown for all categories

- Keyana Bernard: Responsible for the end-to-end development of the Budget Limits page. This member owns both the back and front end implementation of the category-based budgeting system, where users can set maximum spending caps for specific areas (e.g., Food, Rent, Entertainment) and add purchases that deduct for spending limits. 

- Daniela Jaggan: Responsible for the end-to-end development of the Secure Login Gateway. owning both the UI of the login screen and the Backend Authentication Logic. As the project is currently designed for a single-user environment, this member must ensure that only the correct credentials grant entry to the homepage, while all unauthorized attempts are securely blocked with clear user feedback.
