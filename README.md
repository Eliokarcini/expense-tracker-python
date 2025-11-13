# 💰 Python Expense Tracker

A full-stack expense tracking application built with Python, FastAPI, and Streamlit.

## 🚀 Features

- Add, edit, and delete expenses
- Categorize expenses (Food, Transportation, Entertainment, etc.)
- Real-time analytics with interactive charts
- Monthly spending trends
- Category-wise spending breakdown
- Responsive web interface

## 🛠 Tech Stack

**Frontend:** Streamlit, Plotly, Pandas  
**Backend:** FastAPI, SQLite  
**Data Visualization:** Plotly charts  
**API:** RESTful API design

## 📁 Project Structure

- **expense-tracker/**
  - **backend/**
    - `main.py` - FastAPI server
    - `database.py` - Database initialization  
    - `models.py` - Pydantic models
    - `requirements.txt` - Backend dependencies
  - **frontend/**
    - `app.py` - Streamlit application
    - `requirements.txt` - Frontend dependencies
  - `README.md` - Project documentation

## 🏃‍♂️ Quick Start

### Backend Setup
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Server runs on `http://localhost:8000`

### Frontend Setup
```bash
cd frontend
pip install -r requirements.txt
streamlit run app.py
```
App opens on `http://localhost:8501`

## 📊 Features Demo

- **Add Expenses**: Simple form with description, amount, category, and date
- **View All Expenses**: Sortable list with edit/delete functionality
- **Analytics Dashboard**: Interactive charts showing spending patterns
- **Category Breakdown**: Visualize where your money goes
- **Monthly Trends**: Track spending over time

## 🎯 Learning Outcomes

- Full-stack development with Python
- REST API design with FastAPI
- Data visualization with Plotly
- Database management with SQLite
- Frontend development with Streamlit
