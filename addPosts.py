import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import random
import streamlit as st
import json

CONFIG_FILE_PATH = "/etc/secrets/config.json"

st.title("Welcome! Let's create posts")
key = st.text_input("Enter the private key ID of firebase", type="password")

if key != "":
    with open(CONFIG_FILE_PATH) as f:
        data = json.load(f)
        if key == data["private_key_id"]:
            # Initialize Firebase app
            if not firebase_admin._apps:
                cred = credentials.Certificate(CONFIG_FILE_PATH)
                firebase_admin.initialize_app(cred, {
                    'databaseURL': 'https://goose-village.firebaseio.com'
                })

            # db = firebase_admin.db
            db = firestore.client()

            st.header("Add a csv file containing postData")
            uploaded_file = st.file_uploader("Upload the postData file")
            if uploaded_file is not None:
                # read csv
                df=pd.read_csv(uploaded_file)
            else:
                st.warning("You need to upload a csv or excel file.")

            # Adding a delay in between posts
            delay = st.number_input("Enter the delay(in seconds) in posts", step=1, value=5)

            if st.button("Add posts to firebase"):
                # Convert data to dictionary
                data = df.to_dict(orient="records")
                # print(data)

                # # Upload data to Firebase Realtime Database with a delay between each record
                ref = db.collection("posts")
                for i, record in enumerate(data):
                    delay = random.randint(delay, delay+2)
                    ref.add(record)
                    st.write(f"Post {i} added.")
                    time.sleep(delay)
                st.success("All posts added successfully")
        else:
            st.error("Wrong private key, contact the firebase admin")
