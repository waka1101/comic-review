from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3

app = FastAPI()

class LoginBody(BaseModel):
    email: str
    password: str

# ログイン認証関数
def check_auth(login_info):
    email = login_info.email
    password = login_info.password
    login_data_list = [
        {
            "email": "aaa@exmample.com",
            "password": "aaa"
        },
        {
            "email": "bbb@exmample.com",
            "password": "bbb"
        }
    ]
    for login_data in login_data_list:
        is_email_same = login_data.get("email") == email
        is_password_same = login_data.get("password") == password
        if is_email_same and is_password_same:
            return True
    return False

# ログインAPI
@app.post("/auth/login/")
def post_login(login_info: LoginBody):
    auth_result = check_auth(login_info)
    return {"email": login_info.email,"return_code": auth_result}

# ログイン情報登録API
@app.post("/auth/entry")
def post_entry(auth_info: LoginBody):
    return {"menberID": email}