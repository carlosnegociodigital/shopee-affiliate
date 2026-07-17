import re

from app.core.categories import CATEGORIES
from app.core.brands import BRANDS
from app.core.rules import SPECIAL_RULES
from app.core.context_rules import CONTEXT_RULES


def normalize(text: str) -> str:
    """
    Normaliza um texto para facilitar comparações.
    """

    if not text:
        return ""

    return re.sub(r"\s+", " ", text.lower()).strip()


def classify_product(product_name: str, shopee_category: str = "") -> str:
    """
    Classifica um produto utilizando:

    1 - Contexto
    2 - Regras absolutas
    3 - Marcas
    4 - Palavras-chave
    5 - Categoria da Shopee
    """

    texto = normalize(product_name)
    categoria_shopee = normalize(shopee_category)

    # =====================================================
    # 1 - CONTEXTO (MAIOR PRIORIDADE)
    # =====================================================

    for categoria, expressoes in CONTEXT_RULES.items():

        for expressao in expressoes:

            if normalize(expressao) in texto:
                return categoria

    # =====================================================
    # 2 - REGRAS ABSOLUTAS
    # =====================================================

    for regra, categoria in SPECIAL_RULES.items():

        if normalize(regra) in texto:
            return categoria

    # =====================================================
    # 3 - INICIALIZA A PONTUAÇÃO
    # =====================================================

    scores = {
        categoria: 0
        for categoria in CATEGORIES.keys()
    }

    # =====================================================
    # 4 - PALAVRAS-CHAVE
    # =====================================================

    for categoria, palavras in CATEGORIES.items():

        for palavra, peso in palavras.items():

            if normalize(palavra) in texto:
                scores[categoria] += peso

    # =====================================================
    # 5 - MARCAS
    # =====================================================

    for marca, categoria in BRANDS.items():

        if normalize(marca) in texto:
            scores[categoria] += 30

    # =====================================================
    # 6 - CATEGORIA ORIGINAL DA SHOPEE
    # =====================================================

    if categoria_shopee:

        for categoria in scores.keys():

            if categoria.lower() in categoria_shopee:
                scores[categoria] += 15

    # =====================================================
    # RESULTADO
    # =====================================================

    melhor_categoria = max(scores, key=scores.get)

    if scores[melhor_categoria] == 0:
        return "Outros"

    return melhor_categoria