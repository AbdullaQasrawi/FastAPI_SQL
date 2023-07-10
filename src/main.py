import pyodbc
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

app = FastAPI(debug=True)

# Database connection configuration
server = 'localhost'  # Replace with your SQL Server hostname or IP address
database = 'D1'  # Replace with your database name
driver = '{SQL Server}'  # Driver for SQL Server

# Establish the database connection
conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;autocommit=True;'
conn = pyodbc.connect(conn_str)

# API endpoint to retrieve users from the database
@app.get("/users")
def get_users():
    # Execute a query to retrieve users from the 'users' table
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()
    users = [list(user) for user in users]
    cursor.close()

    return {"users": users}

# API endpoint to add a new user to the database
@app.post("/users")
def add_user(user: dict):
    # Check if all required fields are provided
    if not all(key in user for key in ['name', 'email']):
        raise HTTPException(status_code=400, detail="Username and email are required.")

    # Execute an insert query to add the new user to the 'users' table
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email) VALUES (?, ?)",
                   (user['name'], user['email']))
    conn.commit()
    cursor.close()

    return JSONResponse(content={"message": "User added successfully."})

# Close the database connection when the application stops
@app.on_event("shutdown")
def shutdown_event():
    conn.close()
