import firebase_admin
from firebase_admin import credentials, firestore
import re


class CrawlerDb:
    def __init__(self):
        self.credentials = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(self.credentials)
        self.db = firestore.client()

    def add_link_and_title(self, page_url, page_title):
        # for k in self.db.collection("news").get():
        #     print(k.id, k.to_dict())
        print("add to db")
        print(page_url)
        print(page_title)
        clean_page_url = re.sub('[^0-9a-zA-Z]+', '*', page_url)
        ref = self.db.collection("Links_and_Titles").document(clean_page_url)
        ref.set({
            'Url': page_url,
            'Title': page_title
        })
