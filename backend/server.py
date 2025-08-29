from fastapi import FastAPI
import db_helper
from typing import Iterable, Dict, Any, Optional,List
from datetime import date
from pydantic import BaseModel


app= FastAPI()

class Expense(BaseModel):
    expense_date: date
    amount: float
    category: str
    notes: Optional[str] = None

class DateRange(BaseModel):
    start_date: date
    end_date: date

@app.get("/expenses/{expense_date}",response_model=List[Expense])
def get_expenses(expense_date: str):
    expenses = db_helper.fetch_expenses(expense_date)
    return  expenses


@app.post("/expenses/{expense_date}")
def add_expenses(expense_date:date,expenses: List[Expense]):
    print("Iam here")
    if not expenses:
        return {"message": "No expenses to add."}

    expense_date = expense_date.isoformat()
    db_helper.delete_expense_for_date(expense_date)
   
    for expense in expenses:
        db_helper.insert_expense(
            expense.expense_date.isoformat(),
            expense.amount,
            expense.category,
            expense.notes,
        )

    return {"message": f"Added {len(expenses)} expenses for date {expense_date}."}


@app.post("/analytics")
def get_expense_summary(DateRange: DateRange):
    rows = db_helper.fetch_expense_summary(DateRange.start_date.isoformat(), DateRange.end_date.isoformat())

    total_amount= sum([amount["total"] for amount in rows ])
    breakdown={}
    
    for row in rows:
        category = row['category']
        amount = float(row['total']) if row['total'] is not None else 0.0
        percentage = (amount / total_amount * 100) if total_amount > 0 else 0
        breakdown[category] = {
            "total": amount,
            "percentage": round(percentage, 2)
        }

    return breakdown