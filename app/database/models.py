from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String

from app.database.database import Base


class Product(Base):

    __tablename__ = "products"

    # ID do produto na Shopee
    item_id = Column(Integer, primary_key=True)

    # Nome do produto
    product_name = Column(
        String(300),
        nullable=False,
        index=True
    )

    # Categoria original da Shopee
    category = Column(
        String(100),
        nullable=True,
        index=True
    )

    # Categoria inteligente do site
    site_category = Column(
        String(50),
        nullable=True,
        index=True
    )

    # Palavra-chave utilizada na busca
    keyword = Column(
        String(100),
        nullable=True,
        index=True
    )

    # Imagem
    image_url = Column(
        String(500),
        nullable=True
    )

    # Preço
    price = Column(
        String(30),
        nullable=True
    )

    # Avaliação
    rating = Column(
        String(10),
        nullable=True
    )

    # Quantidade vendida
    sales = Column(
        Integer,
        default=0
    )

    # Link de afiliado
    offer_link = Column(
        String(500),
        nullable=True
    )

    # Data de criação
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    # Última atualização
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )