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



## Work-flow

Sign-in Page - Fairooz
Purpose: Allow new users to create an account.
Functionality:
- User can enter:
  First name
  Last name
  Email address
  Username
  Password

Basic form validation (required fields, password length).
- After successful sign-up:
    User is redirected to the Login page.
- If the user already has an account:
   A link directs them to the Login page.

Login page - Daniela
Purpose: Authenticate existing users.
Functionality:
- User enters:
- Username or email
- Password
If credentials are correct:
- User is redirected to the Homepage.
If credentials are incorrect:
- An error message is displayed.
If the user does not have an account:
- A link redirects them to the Sign-Up page.


Homepage - Fairooz home.html
Purpose: Overview and starting point for budgeting.
Functionality:
Displays a progress indicator for money saved toward a goal.
User can:
- Set an income amount (optional).
- Set a savings goal.
Provides navigation buttons to:
- Budget page
- Dashboard page
- About page
- Contact page


Budget page- Keyanna budget.html
Purpose: Core budgeting functionality.
Functionality:
- Nav bar that goes to other pages
Users can:
- Set spending limits for categories (e.g., Food, Rent, Entertainment).
- Enter purchases under selected categories.
- Displays a Category Overview Table showing:
Category
- Spending limit
- Amount spent
- Remaining balance
- Options:
- Table showing the last 5 purchases
- Table showing the highest purchase per category

Dashboard page- Jana dashboard.html
Purpose: Visual analysis of spending habits.
Functionality:
- Nav bar that goes to other pages
Pie chart showing:
- Percentage of total budget spent per category.
Bar chart showing:
- Budgeted amount vs amount spent per category.

Additional optional visualizations:
- Monthly spending trends
- Category comparison insights

Contact page- Jasmine contact.html
Purpose: User communication and feedback.
Functionality:
- Nav bar that goes to other pages
Displays:
- Website email
- Phone number
- Users can submit feedback through a form.
  Form submissions are handled via a third-party service.

About us page - Jasmine about.html
Purpose: Inform users about the application.
Functionality:
- Nav bar that goes to other pages
Explains:
- Purpose of the website
- Goals of the budgeting tool
- How it helps users manage finances
