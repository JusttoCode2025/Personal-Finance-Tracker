# Haven — Personal Finance Tracker

A clean, simple web application that helps users track monthly spending, set budget limits by category, and save toward a travel goal.

**Live Site:** https://personal-finance-tracker-1-0y9r.onrender.com  
**Test Site:** https://personal-finance-tracker-3-a9j9.onrender.com  
**GitHub:** https://github.com/JusttoCode2025/Personal-Finance-Tracker/tree/main  
**Version:** v1.0.0

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
---

## Team

| Name | Role |
|------|------|
| Fairooz Siddiquee | Project Lead, Sign-Up Page, Home Page |
| Jasmine Anike | About Page, Contact Page |
| Jana Saleh | Dashboard Page |
| Keyana Bernard | Budget Page |
| Daniela Jaggan | Login Page |
----

**Frontend:** HTML, CSS, Vanilla JavaScript, Chart.js  
**Backend:** Python Flask  
**Database:** PostgreSQL hosted on Render  
**Form Handling:** Formspree (About/Contact page)  
**Deployment:** Render (both production and test site)

---

## Pages

| Page | File | Description |
|------|------|-------------|
| Login | `login.html` | Entry point — two preset accounts |
| Sign Up | `signup.html` | Form UI only — redirects to login |
| Home | `home.html` | Overview with travel goal progress bar |
| Budget | `budget.html` | Set limits, add purchases, transfer to travel |
| Dashboard | `dashboard.html` | Charts, monthly breakdown, month selector |
| Travel Goal | `travel_goal.html` | Goal tracking, notes, target date |
| About | `about.html` | About the app + contact form via Formspree |

---

## Demo Login Credentials

Two preset accounts are available for testing:

| Name | Email | Password |
|------|-------|----------|
| Jane Doe | janedoe@gmail.com | haventracker |
| John Doe | johndoe@gmail.com | haventracker |

> The PostgreSQL database is hosted on Render. Contact the team for the connection string, or use the live site directly.

## Key Features

### Budget Tracking
- Set monthly spending limits per category (Rent, Groceries, Utilities, Transportation, Entertainment, Other)
- Add purchases that deduct from the category limit
- Remaining turns **yellow** at 80% used, **red** when over budget
- Edit existing limits — cannot set below amount already spent

### Monthly Reset
- Click **New Month** to reset the spending view without deleting history
- Past purchases remain visible in the Dashboard month selector
- After transferring budget to travel, new purchases are blocked until New Month is clicked

### Dashboard Analytics
- Pie chart — spending by category for selected month
- Bar chart — actual spending vs budget limit per category
- Line chart — daily spending over the last 30 days
- Month selector — browse spending history by month

### Travel Goal
- Set a savings goal with a target amount, destination, target date, and notes
- Daily savings target calculated automatically based on days remaining
- Transfer remaining budget directly to travel savings

---

## API Routes

| Method | Route | Description |
|--------|-------|-------------|
| GET | `/limits` | Get all category limits with dynamic spent/remaining |
| POST | `/limit` | Set or update a category limit |
| POST | `/purchase` | Add a purchase |
| GET | `/recent_purchases` | Get last 5 purchases since reset |
| GET | `/dashboard_data` | Get spending data, accepts `?month=YYYY-MM` |
| GET | `/travel_goals` | Get current travel goal |
| POST | `/travel_goal` | Create a new travel goal |
| POST | `/travel_goal/save` | Add a contribution to the goal |
| POST | `/travel_goal/note` | Save a note to the goal |
| POST | `/travel_goal/date` | Save target date to the goal |
| POST | `/travel_goal/reset` | Delete the travel goal |
| POST | `/transfer_to_travel` | Transfer remaining budget to travel goal |
| POST | `/new_month` | Reset spending view for new month |
| GET | `/settings` | Get current reset timestamp |

---

## Testing

Testing is performed manually using dummy inputs across all key flows:

**Budget Page**
- Negative purchase amounts → blocked
- Purchase exceeding category limit → confirm dialog
- Empty category selection → error message
- Limit over $1,000 → confirm dialog
- Limit over $10,000 → hard block
- Edit limit below amount already spent → hard block

**Travel Goal Page**
- Contribution larger than goal → blocked
- Goal over $10,000 → confirm dialog
- Goal over $1,000,000 → hard block
- Contribution over 50% of goal → confirm dialog
- Reset goal → confirm dialog

**Dashboard**
- Month selector filters all charts correctly
- Charts destroy and redraw on month change
- Progress bar caps at 100% display

**New Month Flow**
- Spending resets to $0 visually
- Past purchases preserved in dashboard history
- Transfer blocks purchases until new month clicked

## Known Limitations

- No real user authentication — login is handled client-side with localStorage
- All users share the same database (no per-user data isolation)
- Sign-up page is UI only and does not create real accounts
