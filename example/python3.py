#!/usr/bin/env python3
import requests

'''
Quora-Formkey: This is obtained by logging in to Quora.com, viewing the page source, and finding the "formkey" dictionary key (Normally line 14). Use its value in the Quora-Formkey field.
Cookie: 'm-b=xxxx' - This is the value of the cookie with the key m-b, which is present in the list of cookies used on Quora.com (not poe.com), you can simply inspect cookies in Chrome (F12-Application-cookie) to get it.
'''
cookie = "m-b="
formkey = ""
bot = "capybara"
url = "http://localhost:8000/chat/" + bot

msg = "Hi"

data = {
  "bot":bot,
  "cookie":cookie,
  "formkey":formkey,
  "message":msg
}

response = requests.post(url, json=data)
print(response.json()["message"])