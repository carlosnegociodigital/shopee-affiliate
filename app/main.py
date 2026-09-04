from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.core.categories import CATEGORIES
from app.database.database import Base, SessionLocal, engine
from app.database.models import Product
from app.services.product_service import ProductService


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="app/static"),
    name="static"
)

templates = Jinja2Templates(
    directory="app/templates"
)


# =====================================================
# ÍCONES DAS CATEGORIAS
# =====================================================

ICONS = {
    "Celulares": "📱",
    "Informática": "💻",
    "Gamer": "🎮",
    "Eletrônicos": "📺",
    "Casa": "🏠",
    "Cozinha": "🍳",
    "Beleza": "💄",
    "Moda": "👗",
    "Pets": "🐶",
    "Infantil": "👶",
    "Esportes": "🏋️",
}


def get_categories():
    categorias = [
        ("", "🏠 Todos")
    ]

    for nome in CATEGORIES.keys():
        categorias.append(
            (
                nome,
                f"{ICONS.get(nome, '📦')} {nome}"
            )
        )

    return categorias


# =====================================================
# PAGINAÇÃO
# =====================================================

def get_pages(page, total_pages):

    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    if page <= 3:
        start_page = 1
        end_page = min(5, total_pages)

    if page >= total_pages - 2:
        start_page = max(1, total_pages - 4)
        end_page = total_pages

    return list(
        range(
            start_page,
            end_page + 1
        )
    )


# =====================================================
# HOME
# =====================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def home(
    request: Request,
    busca: str = Query(default=""),
    categoria: str = Query(default=""),
    page: int = Query(default=1),
):

    db = SessionLocal()
    service = ProductService()

    per_page = 24

    if page < 1:
        page = 1

    offset = (page - 1) * per_page

    try:

        query = db.query(Product)

        # ---------------------------------------------
        # PESQUISA
        # ---------------------------------------------

        if busca.strip():

            service.search_products(
                busca.strip()
            )

            query = query.filter(
                Product.product_name.ilike(
                    f"%{busca.strip()}%"
                )
            )

        # ---------------------------------------------
        # CATEGORIA
        # ---------------------------------------------

        if categoria.strip():

            query = query.filter(
                Product.site_category == categoria
            )

        # ---------------------------------------------
        # TOTAL
        # ---------------------------------------------

        total = query.count()

        # ---------------------------------------------
        # PRODUTOS
        # ---------------------------------------------

        produtos = (
            query
            .order_by(
                Product.updated_at.desc()
            )
            .offset(offset)
            .limit(per_page)
            .all()
        )

    finally:

        db.close()

    total_pages = max(
        1,
        (total + per_page - 1) // per_page
    )

    pages = get_pages(
        page,
        total_pages
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "produtos": produtos,
            "busca": busca,
            "categoria": categoria,
            "categorias": get_categories(),
            "page": page,
            "pages": pages,
            "total_pages": total_pages,
            "titulo": "Produtos em destaque",
            "modo_ofertas": False,
        },
    )


# =====================================================
# OFERTAS
# =====================================================

@app.get(
    "/ofertas",
    response_class=HTMLResponse
)
def ofertas(
    request: Request,
    busca: str = Query(default=""),
    categoria: str = Query(default=""),
    page: int = Query(default=1),
):

    db = SessionLocal()

    per_page = 24

    if page < 1:
        page = 1

    offset = (page - 1) * per_page

    try:

        query = db.query(Product)

        # ---------------------------------------------
        # PESQUISA DENTRO DAS OFERTAS
        # ---------------------------------------------

        if busca.strip():

            query = query.filter(
                Product.product_name.ilike(
                    f"%{busca.strip()}%"
                )
            )

        # ---------------------------------------------
        # CATEGORIA
        # ---------------------------------------------

        if categoria.strip():

            query = query.filter(
                Product.site_category == categoria
            )

        # ---------------------------------------------
        # OFERTAS
        #
        # Produtos com maior número de vendas ficam
        # primeiro, seguidos pelos mais recentemente
        # atualizados.
        # ---------------------------------------------

        total = query.count()

        produtos = (
            query
            .order_by(
                Product.sales.desc(),
                Product.updated_at.desc()
            )
            .offset(offset)
            .limit(per_page)
            .all()
        )

    finally:

        db.close()

    total_pages = max(
        1,
        (total + per_page - 1) // per_page
    )

    pages = get_pages(
        page,
        total_pages
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "produtos": produtos,
            "busca": busca,
            "categoria": categoria,
            "categorias": get_categories(),
            "page": page,
            "pages": pages,
            "total_pages": total_pages,
            "titulo": "🔥 Ofertas em destaque",
            "modo_ofertas": True,
        },
    )


# =====================================================
# ATUALIZAR BANCO
# =====================================================

@app.get("/atualizar")
def atualizar():

    service = ProductService()

    service.update_products()

    return {
        "status": "ok",
        "mensagem": "Banco atualizado com sucesso.",
    }