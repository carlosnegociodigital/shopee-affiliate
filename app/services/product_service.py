from datetime import datetime, timedelta

from app.core.classifier import classify_product
from app.database.database import SessionLocal
from app.database.models import Product
from app.services.shopee_client import ShopeeClient


class ProductService:

    CACHE_HOURS = 24

    def __init__(self):
        self.client = ShopeeClient()

    # =====================================================
    # PESQUISA NORMAL
    # =====================================================

    def search_products(self, keyword):

        keyword = keyword.strip().lower()

        db = SessionLocal()

        try:

            produtos = (
                db.query(Product)
                .filter(
                    Product.product_name.ilike(
                        f"%{keyword}%"
                    )
                )
                .all()
            )

            if produtos:

                produtos_com_data = [
                    p for p in produtos
                    if p.updated_at
                ]

                if produtos_com_data:

                    mais_recente = max(
                        p.updated_at
                        for p in produtos_com_data
                    )

                    limite = (
                        datetime.utcnow()
                        - timedelta(
                            hours=self.CACHE_HOURS
                        )
                    )

                    if mais_recente >= limite:

                        print(
                            "âœ… Dados recentes encontrados no banco."
                        )

                        return produtos

                print(
                    "â™» Cache expirado. Atualizando Shopee..."
                )

        finally:
            db.close()

        self.fetch_from_api(keyword)

        db = SessionLocal()

        try:

            return (
                db.query(Product)
                .filter(
                    Product.product_name.ilike(
                        f"%{keyword}%"
                    )
                )
                .all()
            )

        finally:
            db.close()

    # =====================================================
    # ATUALIZAÃ‡ÃƒO GERAL
    # =====================================================

    def update_products(self):

        keywords = [
            "celular",
            "iphone",
            "xiaomi",
            "samsung",
            "motorola",
            "notebook",
            "monitor",
            "mouse",
            "teclado",
            "tv",
            "air fryer",
            "cafeteira",
            "liquidificador",
            "perfume",
            "maquiagem",
            "pet",
            "brinquedo",
            "cadeira gamer",
        ]

        for keyword in keywords:

            print(
                f"\nðŸ”Ž Atualizando {keyword}"
            )

            self.fetch_from_api(keyword)

    # =====================================================
    # BUSCA PRODUTOS NA API
    # =====================================================

    def fetch_from_api(self, keyword):

        total = 0

        for page in range(1, 6):

            response = self.client.get_products(
                keyword=keyword,
                page=page,
                limit=30
            )

            products = (
                response
                .get("data", {})
                .get("productOfferV2", {})
                .get("nodes", [])
            )

            if not products:
                break

            self.save_products(
                products,
                keyword
            )

            total += len(products)

        print(
            f"ðŸ“¦ {total} produtos processados."
        )

    # =====================================================
    # SALVA PRODUTOS
    # =====================================================

    def save_products(
        self,
        products,
        keyword
    ):

        db = SessionLocal()

        try:

            novos = 0
            atualizados = 0

            for item in products:

                categoria_shopee = item.get(
                    "categoryName",
                    ""
                )

                categoria_site = classify_product(
                    item.get(
                        "productName",
                        ""
                    ),
                    categoria_shopee
                )

                produto = db.get(
                    Product,
                    item["itemId"]
                )

                if produto:

                    produto.product_name = item.get(
                        "productName"
                    )

                    produto.category = item.get(
                        "categoryName"
                    )

                    produto.site_category = (
                        categoria_site
                    )

                    produto.keyword = keyword

                    produto.image_url = item.get(
                        "imageUrl"
                    )

                    produto.price = str(
                        item.get(
                            "priceMin",
                            ""
                        )
                    )

                    produto.rating = str(
                        item.get(
                            "ratingStar",
                            ""
                        )
                    )

                    produto.sales = item.get(
                        "sales",
                        0
                    )

                    produto.offer_link = item.get(
                        "offerLink"
                    )

                    produto.updated_at = (
                        datetime.utcnow()
                    )

                    atualizados += 1

                else:

                    produto = Product(
                        item_id=item["itemId"],

                        product_name=item.get(
                            "productName",
                            ""
                        ),

                        category=item.get(
                            "categoryName"
                        ),

                        site_category=categoria_site,

                        keyword=keyword,

                        image_url=item.get(
                            "imageUrl"
                        ),

                        price=str(
                            item.get(
                                "priceMin",
                                ""
                            )
                        ),

                        rating=str(
                            item.get(
                                "ratingStar",
                                ""
                            )
                        ),

                        sales=item.get(
                            "sales",
                            0
                        ),

                        offer_link=item.get(
                            "offerLink"
                        ),

                        created_at=(
                            datetime.utcnow()
                        ),

                        updated_at=(
                            datetime.utcnow()
                        ),
                    )

                    db.add(produto)

                    novos += 1

            db.commit()

            print(
                f"ðŸ’¾ {novos} novos | "
                f"{atualizados} atualizados."
            )

        finally:
            db.close()

    # =====================================================
    # BUSCA OFERTAS REAIS DA SHOPEE
    # =====================================================

    def get_shopee_offers(
        self,
        keyword="",
        page=1,
        limit=30
    ):

        print(
            f"ðŸ”¥ Buscando ofertas Shopee"
            f" | palavra='{keyword}'"
            f" | pÃ¡gina={page}"
        )

        response = self.client.get_offers(
            keyword=keyword,
            page=page,
            limit=limit
        )

        ofertas = (
            response
            .get("data", {})
            .get("shopeeOfferV2", {})
            .get("nodes", [])
        )

        erros = response.get(
            "errors"
        )

        if erros:

            print(
                "âŒ Erro retornado pela Shopee:"
            )

            print(erros)

        print(
            f"ðŸ”¥ {len(ofertas)} ofertas encontradas."
        )

        return ofertas
