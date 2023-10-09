from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2

app = FastAPI()


class login(BaseModel):
    username: str
    password: str


class register(BaseModel):
    username: str
    password: str
    email: str
    phone: str


class Word(BaseModel):
    word: str
    description: str


class Get_word(BaseModel):
    word: str


conn = psycopg2.connect(
    host="localhost",  # host ip address or localhost
    database="DATABASE_NAME",  # type here database name
    user="postgres",
    password="POSTGRES PASSWORD",  # postgres password
    port="PORT (DEFAULT: 5432)"  # port. default port: 5432
)

conn.autocommit = True
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS users 
                (id SERIAL PRIMARY KEY, 
                username VARCHAR(50), 
                password VARCHAR(50), 
                email VARCHAR(50), 
                phone VARCHAR(50))""")


async def insert_user(username, password, email, phone):
    cursor.execute("""INSERT INTO users (username, password, email, phone) 
                    VALUES (%s, %s, %s, %s)""", (username, password, email, phone))


async def get_user(username, password):
    cursor.execute("""SELECT * FROM users WHERE username=%s AND password=%s""", (username, password))
    row = cursor.fetchone()
    if row:
        return {
            "username": row[1],
            "password": row[2],
            "email": row[3],
            "phone": row[4]
        }
    else:
        return None


@app.get("/")
async def root():
    return {"message": "Api created by Diyarbek Oralbaev"}


@app.post("/login")
async def login_user(user: login):
    user = await get_user(user.username, user.password)
    if user:
        return {
            "status": "success",
            'username': user['username'],
            'email': user['email'],
            'phone': user['phone']
            }
    else:
        return {"message": "User not found"}


@app.post("/register")
async def register_user(user: register):
    await insert_user(user.username, user.password, user.email, user.phone)
    return {"message": "User created"}
