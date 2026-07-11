import os
import json
import time
import hashlib

import requests
from dotenv import load_dotenv

load_dotenv()


class ShopeeClient:

    def __init__(self):
        self.app_id = os.getenv("APP_ID")
        self.secret = os.getenv("SECRET_KEY")
        self.url = os.getenv("API_URL")

    def generate_headers(self, payload):

        timestamp = str(int(time.time()))

        factor = (
            self.app_id +
            timestamp +
            payload +
            self.secret
        )

        signature = hashlib.sha256(
            factor.encode("utf-8")
        ).hexdigest()

        headers = {
            "Content-Type": "application/json",
            "Authorization": (
                f"SHA256 Credential={self.app_id}, "
                f"Timestamp={timestamp}, "
                f"Signature={signature}"
            )
        }

        return headers

    def get_products(self, keyword, page=1, limit=30):

        from app.graphql.queries import product_query

        payload = {
            "query": product_query(keyword, page, limit)
        }

        payload_json = json.dumps(payload)

        headers = self.generate_headers(payload_json)

        response = requests.post(
            self.url,
            headers=headers,
            data=payload_json
        )

        return response.json()