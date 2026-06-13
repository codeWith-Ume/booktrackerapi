from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials



from auth import create_token, decode_token, hash_password, verify_password
from database import get_connection
from datetime import date

app = FastAPI()
security = HTTPBearer()

@app.get("/")
def home():
    return {"message": "Welcome to Book Tracker API!"}
    
@app.post("/register")
def register(username: str, email: str, password : str):
    conn = get_connection()
    cursor = conn.cursor()
    
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO users(username,email,password,created_date) VALUES (%s,%s,%s,%s)",
        (username,email,hashed,date.today())
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "User registered succesfully"}

@app.post("/login")
def login(email: str, password: str):
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM users WHERE email = %s",(email,))
    user = cursor.fetchone()
    
    if not user:
        return{"error":"User not found"}
    
    if not verify_password(password,user[3]):
        return{"error":"Wrong Password"}
    
    token = create_token({"user_id": user[0], "email":user[2]})
    
    return {"token": token}  

@app.post("/books")
def add_book(title: str, author: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    #token 
    token = credentials.credentials
    user = decode_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    #mysql connection
    conn = get_connection()
    cursor= conn.cursor()
    
    user_id = user["user_id"]
    #Insert into jobs 
    cursor.execute(
        "INSERT INTO books(user_id,title,author,added_date) VALUES (%s,%s,%s,%s)",
        (user_id,title,author,date.today())          
    )
    #Succes return
    conn.commit()
    cursor.close()
    conn.close()
    
    return{
        "message":"Book added succesfully"
    }
    
@app.get("/books")
def get_books(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = decode_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    
    user_id = user["user_id"]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "SELECT * FROM books WHERE user_id = %s",(user_id,)
    )
    books = cursor.fetchall()
    
    cursor.close()
    conn.close()
    
    return {"books": books}

@app.put("/books/{book_id}")
def update_book(book_id: int, status: str, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = decode_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    user_id = user["user_id"]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "UPDATE books SET status = %s WHERE book_id = %s AND user_id = %s",
        (status, book_id, user_id)
    )
    
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Book updated succesfully"}

@app.delete("/books/{book_id}")
def delete_book(book_id: int, credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    user = decode_token(token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token!")
    
    user_id = user["user_id"]
    
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute(
        "DELETE FROM books WHERE book_id = %s AND user_id = %s",
        (book_id,user_id)
    )
    conn.commit()
    cursor.close()
    conn.close()
    
    return {"message": "Book deleted succesfully"}
    
    

    