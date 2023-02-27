from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import json

app = FastAPI()

def get_json(json_type):
    return json.load(open(f"json/{json_type}.json"))

def update_json(json_type, d):
    json.dump(d, open(f"json/{json_type}.json", "w"), indent=4)

def count_id(id_type):
    id_json = get_json("id")
    return_id = id_json.get(id_type, 0) + 1
    id_json[id_type] = return_id
    update_json("id", id_json)
    return return_id

class LoginBody(BaseModel):
    email: str
    password: str

class RegistraionBody(BaseModel):
    memberID: str
    displayName: str
    discription: str

class UpdateMember(BaseModel):
    email: str
    displayName: str
    memberStatus: str
    discription: str

# ログイン認証関数
def check_auth(login_info):
    email = login_info.email
    password = login_info.password

    login_data_list = get_json("login")
    def can_login(d):
        return d.get("email") == email and d.get("password") == password
    return any([can_login(d) for d in login_data_list])

# ログインAPI
@app.post("/auth/login/")
def post_login(login_info: LoginBody):
    auth_result = check_auth(login_info)
    return {"email": login_info.email, "return_code": auth_result}

# ログイン情報登録API
@app.post("/auth/entry")
def post_entry(auth_info: LoginBody):
    login_list = get_json("login")
    email = auth_info.email
    password = auth_info.password

    if email in [d.get("email") for d in login_list]:
        return {"detail": "email has already used."}

    login_list.append({
        "email": email,
        "password": password,
        "memberID": str(count_id("member")).zfill(8)
    })
    update_json("login", login_list)
    return {"return_code": "success"}

# 会員登録API
@app.post("/member")
def post_member_regi(member_info: RegistraionBody):
    member_list = get_json("member")
    memberID = member_info.memberID
    displayName = member_info.displayName
    discription = member_info.discription

    if memberID in [d.get("memberID") for d in member_list]:
        return {"detail": "memberID has already used."}

    member_list.append({
        "memberID": memberID,
        "memberStatus": "active",
        "displayName": displayName,
        "discription": discription
    })
    update_json("member", member_list)
    return {"return_code": "success"}

#会員更新API
@app.put("/member/{memberID}/")
def update_member(memberID: str, update_info: UpdateMember):
    memberStatus = update_info.memberStatus
    displayName = update_info.displayName
    discription = update_info.discription
    member_list = get_json("member")

    for member_dict in member_list:
        if member_dict.get("memberID") == memberID:
            if memberStatus:
                member_dict["memberStatus"] = memberStatus
            if displayName:
                member_dict["displayName"] = displayName
            if discription:
                member_dict["discription"] = discription

    update_json("member", member_list)
    return {"return_code": "success"}
