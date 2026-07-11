from datetime import datetime, timedelta

from app.database.database import SessionLocal
from app.database.models import Product
from app.services.shopee_client import ShopeeClient


class ProductService:

    CACHE_HOURS = 24

    def __init__(self):
        self.client = ShopeeClient()

    # -------------------------------------------------
    # Pesquisa híbrida
    # Banco -> API -> Banco
    # -------------------------------------------------

    def search_products(self, keyword):

        keyword = keyword.strip().lower()

        db = SessionLocal()

        try:

            produtos = (
                db.query(Product)
                .filter(Product.product_name.ilike(f"%{keyword}%"))
                .all()
            )

            if produtos:

                mais_recente = max(
                    p.updated_at for p in produtos if p.updated_at
                )

                limite = datetime.utcnow() - timedelta(hours=self.CACHE_HOURS)

                if mais_recente >= limite:

                    print("✅ Dados recentes encontrados no banco.")

                    return produtos

                print("♻ Cache expirado. Atualizando Shopee...")

        finally:

            db.close()

        self.fetch_from_api(keyword)

        db = SessionLocal()

        try:

            return (
                db.query(Product)
                .filter(Product.product_name.ilike(f"%{keyword}%"))
                .all()
            )

        finally:

            db.close()

    # -------------------------------------------------
    # Atualização manual
    # -------------------------------------------------

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

            print(f"\n🔎 Atualizando {keyword}")

            self.fetch_from_api(keyword)

    # -------------------------------------------------
    # Consulta Shopee
    # -------------------------------------------------

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

            self.save_products(products, keyword)

            total += len(products)

        print(f"📦 {total} produtos processados.")

    # -------------------------------------------------
    # Salvar produtos
    # -------------------------------------------------

    def save_products(self, products, keyword):

        db = SessionLocal()

        try:

            novos = 0
            atualizados = 0

            for item in products:

                produto = db.get(Product, item["itemId"])

                if produto:

                    produto.product_name = item["productName"]
                    produto.category = item.get("categoryName")
                    produto.keyword = keyword
                    produto.image_url = item["imageUrl"]
                    produto.price = str(item["priceMin"])
                    produto.rating = str(item["ratingStar"])
                    produto.sales = item["sales"]
                    produto.offer_link = item["offerLink"]
                    produto.updated_at = datetime.utcnow()

                    atualizados += 1

                else:

                    produto = Product(

                        item_id=item["itemId"],
                        product_name=item["productName"],
                        category=item.get("categoryName"),
                        keyword=keyword,
                        image_url=item["imageUrl"],
                        price=str(item["priceMin"]),
                        rating=str(item["ratingStar"]),
                        sales=item["sales"],
                        offer_link=item["offerLink"],
                        created_at=datetime.utcnow(),
                        updated_at=datetime.utcnow(),

                    )

                    db.add(produto)

                    novos += 1

            db.commit()

            print(
                f"💾 {novos} novos | {atualizados} atualizados."
            )

        finally:

            db.close()