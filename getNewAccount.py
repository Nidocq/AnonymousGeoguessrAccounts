#!/usr/bin/env python3

import requests as r
import time
import re 
import os

url = "https://10minutemail.com/"
addressurl = url + "/session/address"
link_url = url + "/messages/"
signupurl = "https://www.geoguessr.com/api/v3/accounts/signup"

# Get the email addrses --------

print("creating session")
ses = r.Session()

print("getting the address") 
rq = r.get(addressurl)
address = rq.text[12:-2]

print("Getting the headers (where there should be a set-cookie)")
cookieValue = rq.headers["Set-Cookie"][11:-26]
cookies = { "JSESSIONID" : str(cookieValue) }

print("getting cookies")
#cookies = dict(ses.cookies)
print(f"Cookie is {ses.cookies}")


print("Getting the cookie {} on the url {} with adress {}".format(cookies, addressurl, address))

# -------
headers = {
    'authority': 'www.geoguessr.com',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36',
    'content-type': 'application/json',
    'accept': '*/*',
    'origin': 'https://www.geoguessr.com',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.geoguessr.com/signup',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    'cookie': '__stripe_mid=f5e8581b-690e-44dc-a963-f2fa8ea40b3985f503; devicetoken=2B0305ADBB; _ncfa=nDs%2bXHqWqq4UMH%2fOOFcrn0eJifDy4j2%2fP1B41XsqEk8%3dr2YPISq9l7ANNpPc9548%2bDfALlhpRAKWFkFSOQW9UYGieNsfT%2f16%2bn9BEleqmMAX; __stripe_sid=a49b7b15-b56f-46a8-a8b0-ceed6be8c7bbd4ffd5',
}

data = str({"email":"{}".format(address)})

response = r.post(signupurl, headers=headers, data=data)
print("Getting response 201 is good {}".format(response))

#-----

# Get the read of a cookie for every user using this script
print("Wating for email to get sent and received")
time.sleep(10)

print(f"Sending GET request {link_url}, {cookies}") 
rq_mail = r.get(link_url, cookies=cookies)

#regex that will get the e-mail address 
getlink = '(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.[a-zA-Z0-9]+\.[^\s]{2,})'

link_list = re.findall(getlink, rq_mail.text)

userAccountName = address.split("@")[0]

#Make or open a file that pastes your username down, so you can log in later if you want to
myFile = open('./userAccountName.txt', 'a') 
myFile.write(userAccountName)
myFile.close()


print("SUCCESS \n\n\n")
print("Click this link and fill in the form :\n\n {}".format(link_list[1][:-6:]))


