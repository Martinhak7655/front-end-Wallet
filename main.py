import psycopg2
import uvicorn
from fastapi import FastAPI
from typing import Union
from pydantic import BaseModel

connection = psycopg2.connect(
    host="localhost",
    database="frontendwallet",
    user="postgres",
    password="MH2012"
)
cursor = connection.cursor()

create_table = '''
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(100) NOT NULL,
        password VARCHAR(100) NOT NULL,
        mail VARCHAR(100) NOT NULL,
        balance INT DEFAULT 0,
        img VARCHAR(100) NOT NULL,
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
'''
cursor.execute(create_table)
connection.commit()

app = FastAPI()

class SignIn(BaseModel):
    username: str
    password: str

class SignUp(BaseModel):
    username: str
    password: str
    mail: str
    img: str

class UserFound(BaseModel):
    username: str    

class Balance(BaseModel):
    password: str

class CashIn(BaseModel):
    password: str
    balance: int

class CashOut(BaseModel):
    password: str
    balance: int

class Transfer(BaseModel):
    password: str
    password2: str
    balance: int

class DeleteUser(BaseModel):
    password: str

@app.post("/api/signin")
def signin(user: SignIn):
    select = '''
        SELECT * FROM users WHERE username = (%s) AND password = (%s);
    '''
    cursor.execute(select, (user.username, user.password,))
    connection.commit()
    user = cursor.fetchone()
    if user:
        return {"succes": True, "message": "Welcome to your page"}

@app.post("/api/create-user")
def signup(user: SignUp):
    insert = '''
        INSERT INTO users (username, password, mail, img) VALUES (%s, %s, %s, %s);
    '''
    cursor.execute(insert, (user.username, user.password, user.mail, user.img,))
    connection.commit()
    return {"succes": True, "message": "Your page has benn saved"}

@app.post("/api/balance")
def balance(balance: Balance):
    select = '''
        SELECT * FROM users WHERE password = (%s);
    '''
    cursor.execute(select, (balance.password,))
    connection.commit()
    user = cursor.fetchone()
    if user:
        return {"succes": True, "balance": user[4]}

@app.post("/api/cashin")
def cashin(balance: CashIn):
    select = '''
        SELECT * FROM users WHERE password = (%s);
    '''
    cursor.execute(select, (balance.password,))
    connection.commit()
    user = cursor.fetchone()
    update = '''
        UPDATE users SET balance = (%s) WHERE password = (%s);
    '''
    cursor.execute(update, (user[4] + balance.balance, balance.password,))
    connection.commit()
    return {"succes": True, "message": "Procces completed succesfully"}
    
@app.post("/api/cashout")
def cashin(balance: CashOut):
    select = '''
        SELECT * FROM users WHERE password = (%s);
    '''
    cursor.execute(select, (balance.password,))
    connection.commit()
    user = cursor.fetchone()
    update = '''
        UPDATE users SET balance = (%s) WHERE password = (%s);
    '''
    cursor.execute(update, (user[4] - balance.balance, balance.password,))
    connection.commit()
    return {"succes": True, "message": "Procces completed succesfully"}
    
@app.post("/api/user")
def user(user: UserFound):
    select = '''
        SELECT * FROM users WHERE username = (%s);
    '''
    cursor.execute(select, (user.username,))
    connection.commit()
    user = cursor.fetchall()
    if user:
        user_list = []
        for data in user:
            user_data = {
                "id": data[0],
                "username": data[1],
                "mail": data[3]
            }
            user_list.append(user_data)
        return {"succes": True, "users": user_list}

@app.post("/api/transfer")
def transfer(balance: Transfer):
    select = '''
        SELECT * FROM users WHERE password = (%s);
    '''
    cursor.execute(select, (balance.password,))
    connection.commit()
    user = cursor.fetchone()
    select2 = '''
        SELECT * FROM users WHERE password = (%s);
    '''
    cursor.execute(select2, (balance.password2,))
    connection.commit()
    user2 = cursor.fetchone()

    update1 = '''
        UPDATE users SET balance = (%s) WHERE password = (%s);
    '''
    cursor.execute(update1, (user[4] + balance.balance, balance.password,))
    connection.commit()

    update2 = '''
        UPDATE users SET balance = (%s) WHERE password = (%s);
    '''
    cursor.execute(update2, (user2[4] - balance.balance, balance.password2,))
    connection.commit()
    return {"succes": True, "message": "Transfel succesfully"}

@app.delete("/api/delete-user")
def delete_user(user: DeleteUser):
    delete = '''
        DELETE FROM users WHERE password = (%s);
    '''
    cursor.execute(delete, (user.password,))
    connection.commit()
    return {"succes": True, "message": "This man has been deleted"}

uvicorn.run(app, host="0.0.0.0", port=7600)