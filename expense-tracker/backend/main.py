from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import database
import models
from typing import List

app = FastAPI(title="Expense Tracker API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
database.init_database()

@app.get("/")
def read_root():
    return {"message": "Expense Tracker API"}

@app.get("/api/expenses", response_model=List[models.ExpenseResponse])
def get_all_expenses():
    conn = database.get_db_connection()
    expenses = conn.execute('''
        SELECT * FROM expenses ORDER BY date DESC
    ''').fetchall()
    conn.close()
    return [dict(expense) for expense in expenses]

@app.get("/api/expenses/{expense_id}", response_model=models.ExpenseResponse)
def get_expense(expense_id: int):
    conn = database.get_db_connection()
    expense = conn.execute(
        'SELECT * FROM expenses WHERE id = ?', (expense_id,)
    ).fetchone()
    conn.close()
    
    if expense is None:
        raise HTTPException(status_code=404, detail="Expense not found")
    return dict(expense)

@app.post("/api/expenses", response_model=dict)
def create_expense(expense: models.ExpenseCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        INSERT INTO expenses (description, amount, category, date)
        VALUES (?, ?, ?, ?)
    ''', (expense.description, expense.amount, expense.category, expense.date))
    
    expense_id = cursor.lastrowid
    conn.commit()
    conn.close()
    
    return {"message": "Expense created", "id": expense_id}

@app.put("/api/expenses/{expense_id}")
def update_expense(expense_id: int, expense: models.ExpenseCreate):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        UPDATE expenses 
        SET description = ?, amount = ?, category = ?, date = ?
        WHERE id = ?
    ''', (expense.description, expense.amount, expense.category, expense.date, expense_id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    
    conn.commit()
    conn.close()
    return {"message": "Expense updated"}

@app.delete("/api/expenses/{expense_id}")
def delete_expense(expense_id: int):
    conn = database.get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('DELETE FROM expenses WHERE id = ?', (expense_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Expense not found")
    
    conn.commit()
    conn.close()
    return {"message": "Expense deleted"}

@app.get("/api/analytics/category-totals")
def get_category_totals():
    conn = database.get_db_connection()
    totals = conn.execute('''
        SELECT category, SUM(amount) as total 
        FROM expenses 
        GROUP BY category 
        ORDER BY total DESC
    ''').fetchall()
    conn.close()
    return [dict(total) for total in totals]

@app.get("/api/analytics/monthly-totals")
def get_monthly_totals():
    conn = database.get_db_connection()
    totals = conn.execute('''
        SELECT strftime('%Y-%m', date) as month, SUM(amount) as total 
        FROM expenses 
        GROUP BY month 
        ORDER BY month
    ''').fetchall()
    conn.close()
    return [dict(total) for total in totals]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)