import pandas as pd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
import random
import streamlit as st
import json
import hashlib
from datetime import datetime, timedelta


CONFIG_FILE_PATH = "./etc/secrets/config.json"

# Bot user ids
sloane_bots = ["uMnThhndiub8FI9u5VdSzdoaOPW2",
        "4j8witlNqXP0kHI76ZihQa3dHK53"
    ]

# Bots of Max
max_bots = ["tU4vSWoK8cQ94hqUHlj5pRQ6JFa2",
    "79DjhKxVIcNrvvAF9WjhPq5VrKp1",
    "tWXxza2jbbRXzwS7eZHkpo5H00d2",
    "RAA4HZcDiUZVJzDujPVIxZnzhjc2",
    "gBJxxjLigIfkZoYU9Wks0P92eG43",
    "eaa3rU0BMBODMArtcSRXzGa399C2"
]

# Bots of Ivy
ivy_bots = ["Oy0UXUTVjDQrPfsAycvIteIp2093",
    "zuW8BoYkKuYZbvI7XEsUDWlnjqg1",
    "LPzzmrA7b8QCFVymlcdKikUoNUE3",
    "Wb03scBoByWHqKRcABjgwDQA0M02",
    "u2SppBWHFwQJoyi7REE0EijpWsV2"
]

# Bots of herald
herald_bots = ["D5ibbBQTRMSmH2HlEj5YRt2psgs2",
    "Fsv4xKUaLeRwnew1fbZQqZoj5qk2",
    "0Zdt3X7AraVNLSabCW1ljKN8WuG3",
    "HvaicZHjFXcI9qJRyzVTQrboMLI2",
    "yDTu9ongLIasSbgpOLxMUGIJc6s2"
]

# Bots of 360
W360_bots = ["ugAuOhBVAZXTcPClQ3lu3OM8CQC2",
    "Z9wzzVpLOghFeE1YNoEI3uN4Kz93",
    "GGsQSZiA6MVuqPTp9MupB2aOntU2",
    "Fp9zFsM8svOj8SeyVeuyDMaoCoS2",
    "b0GPvqlnuJaeFvnky31E9RgYZIn1",
    "XOuq5be5tZQ5UMHnIid2Fl12MrC2"
]

# Category_data
categories = {
    'Help Moving': '4vSQQSLGYdk6UMywCsNk',
    'Womenswear': '5cbTfbS8KNn8xpRxnh9o',
    'House Keeping': 'AFJlW0yp2VlqiwS3MA84',
    'Craft Supplies': 'CmfDfGMHeAzQxUzbKLuL',
    'Accessories': 'FDA1V1Uj26eAKu9UolRZ',
    'Other Goods': 'FIkEStzpq6FrzFhppZkf',
    'Kitchen Stuff': 'Ppl3lPXTUwpcXezFuzbr',
    'Other Services': 'Vofa6AmsEaPLPU1sUyMq',
    'Rent and Sublease': 'arQoy2qdhz3TxQqIUaAv',
    'Menswear': 'cFhZzkaOz2KoS0YxvYcP',
    'Furniture': 'jKF0sF6AyhmJNLG7Hlnt',
    'Pet Care': 'kLVwVPWaWeETMGsMKtZR',
    'Electronics': 'q5IKEEh1hV5saXEyRpvJ',
    'Gym & Training': 'rSwf1iw73nqGGVFLAiJU',
    'Quick Help': 'tmjybp77QbdjqSHcFwTa',
    'Home Decor': 'vAO7OQLIPTUFwlz55UGH'
}

def get_random_element(my_list):
    if not my_list:
        return None
    else:
        return random.choice(my_list)

def generate_unique_hash(length):
    # Get the current timestamp
    timestamp = str(time.time())

    # Create a new SHA256 hash object
    sha256_hash = hashlib.sha256()

    # Update the hash object with the timestamp
    sha256_hash.update(timestamp.encode('utf-8'))

    # Get the hexadecimal representation of the hash value
    hash_value = sha256_hash.hexdigest()

    # Truncate the hash value to the desired length
    truncated_hash = hash_value[:length]

    return truncated_hash

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
                    'databaseURL': 'https://test-goose.firebaseio.com',
                    'storageBucket': 'test-goose.appspot.com'
                })

            # db = firebase_admin.db
            db = firestore.client()

            df = None

            st.header("Add a csv file containing postData")
            uploaded_file = st.file_uploader("Upload the postData file")
            if uploaded_file is not None:
                # read csv
                df=pd.read_csv(uploaded_file)
            else:
                st.warning("You need to upload a csv file.")

            if df is not None:
                # Adding a delay in between posts
                delay = st.number_input("Enter the delay(in seconds) in between posts", step=1, value=5)

                st.text("Select in which community you want to post")
                sloane = st.checkbox("Sloane", True)
                max = st.checkbox("Max", True)
                w360 = st.checkbox("360 W", True)
                herald = st.checkbox("Herald Towers", True)
                ivy = st.checkbox("Ivy", True)

                users = []

                if sloane:
                    users += sloane_bots
                
                if max:
                    users += max_bots

                if herald:
                    users += herald_bots

                if w360:
                    users += W360_bots

                if ivy:
                    users += ivy_bots

                if len(users) !=0:
                    if st.button("Add posts to firebase"):
                        # # Convert data to dictionary
                        # data = df.to_dict(orient="records")
                        # # print(data)

                        # # # Upload data to Firebase Realtime Database with a delay between each record
                        # ref = db.collection("banner_data")
                        # for i, record in enumerate(data):
                        #     delay = random.randint(delay, delay+2)
                        #     ref.add(record)
                        #     st.write(f"Post {i} added.")
                        #     time.sleep(delay)
                        # st.success("All posts added successfully")

                        records = df.to_dict(orient='records')

                        for i, record in enumerate(records):
                            user_ref = get_random_element(users)
                            record['req_id'] = generate_unique_hash(15)
                            doc_ref = db.collection('requests').document(record['req_id'])
                            snap = db.collection("user").document(user_ref).get()
                            community_list = snap.get("community_list")

                            # # If no image data comment this
                            # record["photo_mutiple"] = [record["photo_multiple"][2:-2]]
                            # record.pop("photo_multiple")

                            record['user_ref'] = db.collection("user").document(user_ref)

                            # To add posts for an earlier date
                            # delay_minutes = random.randint(0, 60)
                            # delay_hours = random.randint(0, 8)
                            # delay_days = random.randint(1, 3)

                            # record['created_at'] = datetime.now() - timedelta(days=delay_days, hours=delay_hours, minutes=delay_minutes)
                            record['created_at'] = datetime.now() - timedelta(hours=6)
                            record['community_list'] = community_list
                            record['active'] = True
                            record['post_in_marketplace'] = False
                            category = record['category']
                            record.pop('category')
                            record['category_ref'] = db.collection("categories").document(categories[category])
                            doc_ref.set(record)
                            st.write(f"Added post {i} successfully.")
                            delay = random.randint(delay, delay+2)
                            st.write(f"Waiting {delay} seconds to post next")
                            time.sleep(delay)


        else:
            st.error("Wrong private key, contact the firebase admin")
