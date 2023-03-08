import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import random
# from dotenv import load_dotenv
# import os
# # import streamlit as st
# load_dotenv()

# CONFIG = {
#   "type": os.getenv("type"),
#   "project_id": os.getenv("project_id"),
#   "private_key_id": os.getenv("private_key_id"),
#   "private_key": os.getenv("private_key"),
#   "client_email": os.getenv("client_email"),
#   "client_id": os.getenv("client_id"),
#   "auth_uri": os.getenv("auth_uri"),
#   "token_uri": os.getenv("token_uri"),
#   "auth_provider_x509_cert_url": os.getenv("auth_provider_x509_cert_url"),
#   "client_x509_cert_url": os.getenv("client_x509_cert_url")
# }

# print(CONFIG)
# Initialize Firebase app
cred = credentials.Certificate("/etc/secrets/config.json")
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://goose-village.firebaseio.com'
})
# db = firebase_admin.db
db = firestore.client()
# Read data from Excel file
df = pd.read_csv("postData.csv")
# print(df)

# Convert data to dictionary
data = df.to_dict(orient="records")
# print(data)

# # Upload data to Firebase Realtime Database with a 5-second delay between each record
ref = db.collection("posts")
for i, record in enumerate(data):
    delay = random.randint(2, 5)
    ref.add(record)
    print(f"Post {i} added.")
    time.sleep(delay)
