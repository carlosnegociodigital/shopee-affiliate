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

    # =====================================================
    # AUTENTICAÃ‡ÃƒO
    # =====================================================

    def generate_headers(self, payload):
        timestamp = str(int(time.time()))

        factor = (
            self.app_id
            + timestamp
            + payload
            + self.secret
        )

        signature = hashlib.sha256(
            factor.encode("utf-8")
        ).hexdigest()

        return {
            "Content-Type": "application/json",
            "Authorization": (
                f"SHA256 Credential={self.app_id}, "
                f"Timestamp={timestamp}, "
                f"Signature={signature}"
            )
        }

    # =====================================================
    # REQUISIÃ‡ÃƒO GENÃ‰RICA
    # =====================================================

    def _post(self, query):
        payload = {
            "query": query
        }

        payload_json = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":")
        )

        headers = self.generate_headers(payload_json)

        response = requests.post(
            self.url,
            headers=headers,
            data=payload_json,
            timeout=30
        )

        response.raise_for_status()

        return response.json()

    # =====================================================
    # PRODUTOS
    # =====================================================

    def get_products(
        self,
        keyword,
        page=1,
        limit=30
    ):
        from app.graphql.queries import product_query

        query = product_query(
            keyword,
            page,
            limit
        )

        return self._post(query)

    # =====================================================
    # OFERTAS SHOPEE
    # =====================================================

    def get_offers(
        self,
        keyword="",
        page=1,
        limit=30
    ):
        keyword = (
            keyword
            .replace("\\", "\\\\")
            .replace('"', '\\"')
        )

        query = f"""
        {{
            shopeeOfferV2(
                keyword: "{keyword}",
                sortType: 1,
                page: {page},
                limit: {limit}
            ) {{
                nodes {{
                    commissionRate
                    imageUrl
                    offerLink
                    originalLink
                    offerName
                    offerType
                    categoryId
                    collectionId
                    periodStartTime
                    periodEndTime
                }}
                pageInfo {{
                    page
                    limit
                    hasNextPage
                }}
            }}
        }}
        """

        return self._post(query)
