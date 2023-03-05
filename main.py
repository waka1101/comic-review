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

class Comic_RegistraionBody(BaseModel):
    comicContributorID: str
    displayName: str
    discription: str
    comicPath: str

class DeleteMember(BaseModel):
    memberID: str
    memberStatus: str

class UpdateComic(BaseModel):
    comicID: str
    comicContributorID: str
    comicStatus: str
    displayName: str
    discription: str
    comicPath: str

class Comment_RegistraionBody(BaseModel):
    commentContributorID: str
    comicID: str
    replyID: str
    commentText: str

class UpdateComment(BaseModel):
        commentID: str
        commentContributorID: str
        comicID: str
        replyID: str
        commentStatus: str
        commentText: str

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
        return {"detail": "This memberID has already used."}

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

# 会員検索API
@app.get("/member")
def search_memberID(memberID: str = "", memberStatus: str = "active"):
    member_list = get_json("member")
    print(member_list)
    queryPattern = {
        "memberID": memberID,
        "memberStatus": memberStatus
    }
    print(memberID, memberStatus)
    def isMatchQuery(member):
        return all([value == member.get(key) for key, value in queryPattern.items() if value])
    return [member for member in member_list if isMatchQuery(member)]

# 漫画投稿API
@app.post("/comic")
def post_comic_regi(comic_info: Comic_RegistraionBody):
    comic_list = get_json("comic")
    comicContributorID = comic_info.comicContributorID
    displayName = comic_info.displayName
    discription = comic_info.discription
    comicPath = comic_info.comicPath

    comic_list.append({
        "comicID": str(count_id("comic")).zfill(8),
        "comicContributorID": comicContributorID,
        "comicStatus": "active",
        "displayName": displayName,
        "discription": discription,
        "comicPath": comicPath
    })
    update_json("comic", comic_list)
    return {"return_code": "success"}

# 漫画更新API
@app.put("/comic/{comicID}/")
def update_comic(comicID: str, update_info: UpdateComic):
    comicContributorID = update_info.comicContributorID
    comicStatus = update_info.comicStatus
    displayName = update_info.displayName
    discription = update_info.discription
    comicPath = update_info.comicPath
    comic_list = get_json("comic")

    for comic_dict in comic_list:
        if comic_dict.get("comicID") == comicID:
            if comicStatus:
                comic_dict["comicStatus"] = comicStatus
            if displayName:
                comic_dict["displayName"] = displayName
            if discription:
                comic_dict["discription"] = discription
            if comicPath:
                comic_dict["comicPath"] = comicPath

    update_json("comic", comic_list)
    return {"return_code": "success"}

# 漫画検索API
@app.get("/comic")
def search_comicID(comicID: str = "", contributorID: str = "", comicStatus: str = "active"):
    comic_list = get_json("comic")
    queryPattern = {
        "comicID": comicID,
        "comicContributorID": contributorID,
        "comicStatus": comicStatus
    }
    print(queryPattern)
    def isMatchQuery(comic):
        return all([value == comic.get(key) for key, value in queryPattern.items() if value])
    return [comic for comic in comic_list if isMatchQuery(comic)]

#コメント投稿API
@app.post("/comment")
def post_comment_regi(comment_info: Comment_RegistraionBody):
    comment_list = get_json("comment")
    commentContributorID = comment_info.commentContributorID
    comicID = comment_info.comicID
    replyID = comment_info.replyID
    commentText = comment_info.commentText

    comment_list.append({
        "commentID": str(count_id("comment")).zfill(8),
        "commentContributorID": commentContributorID,
        "comicID": comicID,
        "replyID": replyID,
        "commentStatus": "active",
        "commentText": commentText,
    })
    update_json("comment", comment_list)
    return {"return_code": "success"}

#コメント更新API
@app.put("/comment/{commentID}/")
def update_comment(comment: str, update_info: UpdateComment):
    commentID = update_info.commentID
    commentContributorID = update_info.commentContributorID
    comicID = update_info.comicID
    replyID = update_info.replyID
    commentStatus = update_info.commentStatus
    commentText = update_info.commentText
    comment_list = get_json("comment")

    for comment_dict in comment_list:
        if comment_dict.get("commentID") == commentID:
            if commentStatus:
                comment_dict["commentStatus"] = commentStatus
            if commentText:
                comment_dict["commentText"] = commentText

    update_json("comment", comment_list)
    return {"return_code": "success"}

#コメント投稿API
@app.get("/comment")
def search_commentID(commentID: str = "", commentContributorID: str = "", commentStatus: str = "active"):
    comment_list = get_json("comment")
    queryPattern = {
        "commentID": commentID,
        "commentContributorID": commentContributorID,
        "commentStatus": commentStatus
    }
    print(queryPattern)
    def isMatchQuery(comment):
        return all([value == comment.get(key) for key, value in queryPattern.items() if value])
    return [comment for comment in comment_list if isMatchQuery(comment)]
