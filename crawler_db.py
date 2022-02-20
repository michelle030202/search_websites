import firebase_admin
from firebase_admin import credentials, firestore
import re


class CrawlerDb:
    def __init__(self):
        self.credentials = credentials.Certificate("firebase-key.json")
        firebase_admin.initialize_app(self.credentials)
        self.db = firestore.client()

    def search_titles(self, query):
        for k in self.db.collection("Links and Titles").get():
            title = k.to_dict().get('Title')
            if query in title:
                print(title)

    def add_link_and_title(self, page_url,page_title):
        print("add to db")
        print(page_url)
        print(page_title)
        clean_page_url = re.sub('[^0-9a-zA-Z]+', '*', page_url)
        ref = self.db.collection("Links and Titles").document(clean_page_url)
        ref.set({
            'Url': page_url,
            'Title': page_title
        })


