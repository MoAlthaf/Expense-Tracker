# Expense Tracker

A full-stack Expense Tracker web application built with FastAPI (backend), Streamlit (frontend), and MySQL (database). This project allows users to add, update, and analyze their daily expenses with a modern, interactive UI and robust backend API.

## Features

- **Add/Update Expenses:**
	- Enter daily expenses with amount, category, and notes.
	- Add multiple expenses for a single date.
	- Edit and update expenses for any date.

- **Expense Analytics:**
	- View expense breakdown by category for a selected date range.
	- Visual analytics with tables and bar charts (powered by Plotly and Pandas).

- **Backend API:**
	- FastAPI endpoints for CRUD operations and analytics.
	- Pydantic models for data validation.
	- MySQL database integration for persistent storage.

- **Frontend:**
	- Streamlit app for a user-friendly interface.
	- Dynamic forms for adding and editing expenses.
	- Interactive analytics tab.

## Project Structure

```
backend/
	server.py         # FastAPI backend server
	db_helper.py      # Database helper functions
frontend/
	app.py            # Streamlit frontend app
```

## Getting Started

### Prerequisites
- Python 3.8+
- MySQL Server
- pip (Python package manager)

### Backend Setup
1. **Install dependencies:**
	 ```sh
	 pip install -r requirements.txt
	 ```
2. **Configure MySQL:**
	 - Connect to your database`.
	 - Create a table:
		 ```sql
	 - Update DB credentials in `db_helper.py` if needed.
3. **Run the backend server:**
	 ```sh
	 cd backend
	 uvicorn server:app --reload
	 ```

### Frontend Setup
1. **Install dependencies:**
	 ```sh
	 pip -r requirements.txt
	 ```
2. **Run the frontend app:**
	 ```sh
	 cd frontend
	 streamlit run app.py
	 ```

### Usage
- Open the Streamlit app in your browser (usually at `http://localhost:8501`).
- Use the **Add/Update** tab to manage daily expenses.
- Use the **Analytics** tab to view expense breakdowns by category and date range.

## API Endpoints
- `GET /expenses/{expense_date}`: Get all expenses for a specific date.
- `POST /expenses/{expense_date}`: Add or update expenses for a date.
- `POST /analytics`: Get expense summary for a date range.

## Customization
- Update categories in `frontend/app.py` as needed.
- Adjust database credentials and table schema in `backend/db_helper.py`.

## License
This project is for educational purposes. Feel free to modify and use it for your own needs.

---

**Developed using FastAPI, Streamlit, and MySQL.**