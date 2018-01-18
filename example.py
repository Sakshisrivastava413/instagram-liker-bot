from InstaLikerBot import InstaLikerBot

insta_login_auth = {
    'username': None,
    'password': None
}

insta_login_auth['username'] = str(input("Enter your instagram username/email: "))
insta_login_auth['password'] = str(input("Password: "))

target_user_id = "https://www.instagram.com/" + str(input("Enter target username: "))



InstaLikerBot(insta_login_auth, target_insta_id=target_user_id).Run()