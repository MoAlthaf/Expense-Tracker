from fastapi import FastAPI
import db_helper
from typing import Iterable, Dict, Any, Optional,List
from datetime import date
from pydantic import BaseModel

class Expense(BaseModel):
    expense_date: date
    amount: float
    category: str
    notes: Optional[str] = None


app= FastAPI()

@app.get("/expenses/{expense_date}",response_model=List[Expense])
def get_expenses(expense_date: str):
    expenses = db_helper.fetch_expenses(expense_date)
    return  expenses