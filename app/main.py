from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.database.database import Base, SessionLocal, engine
from app.database.models import Product
from app.services.product_service import ProductService


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.get("/", response_class=HTMLResponse)
def home(
    request: Request,
    busca: str = Query(default=""),
    page: int = Query(default=1),
):

    db = SessionLocal()
    service = ProductService()

    per_page = 24
    offset = (page - 1) * per_page

    try:

        # -----------------------------------
        # Pesquisa híbrida
        # -----------------------------------

        if busca.strip():

            service.search_products(busca.strip())

            query = db.query(Product).filter(
                Product.product_name.ilike(f"%{busca.strip()}%")
            )

        else:

            query = db.query(Product)

        # -----------------------------------
        # Paginação
        # -----------------------------------

        total = query.count()

        produtos = (
            query
            .order_by(Product.updated_at.desc())
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

    start_page = max(1, page - 2)
    end_page = min(total_pages, page + 2)

    if page <= 3:
        start_page = 1
        end_page = min(5, total_pages)

    if page >= total_pages - 2:
        start_page = max(1, total_pages - 4)
        end_page = total_pages

    pages = list(range(start_page, end_page + 1))

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
            "produtos": produtos,
            "busca": busca,
            "page": page,
            "pages": pages,
            "total_pages": total_pages,
        },
    )


@app.get("/atualizar")
def atualizar():

    service = ProductService()

    service.update_products()

    return {
        "status": "ok",
        "mensagem": "Banco atualizado com sucesso.",
    }