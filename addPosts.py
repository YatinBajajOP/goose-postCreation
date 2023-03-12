import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import random
import streamlit as st

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
if not firebase_admin._apps:

    cred = credentials.Certificate("/etc/secrets/config.json")
    firebase_admin.initialize_app(cred, {
        'databaseURL': 'https://goose-village.firebaseio.com'
    })
# db = firebase_admin.db
db = firestore.client()

st.title("Add a csv file containing postData")
uploaded_file = st.file_uploader("Upload the postData file")
if uploaded_file is not None:
    #read csv
    df=pd.read_csv(uploaded_file)

else:
    st.warning("You need to upload a csv or excel file.")

# Read data from Excel file
# df = pd.read_csv("postData.csv")
# print(df)

delay = st.number_input("Enter the delay(in seconds) in posts", step=1, value=5)

if st.button("Add posts to firebase"):
    # Convert data to dictionary
    data = df.to_dict(orient="records")
    # print(data)

    # # Upload data to Firebase Realtime Database with a 5-second delay between each record
    ref = db.collection("posts")
    for i, record in enumerate(data):
        delay = random.randint(delay, delay+2)
        ref.add(record)
        st.write(f"Post {i} added.")
        time.sleep(delay)
    st.success("All posts added successfully")
