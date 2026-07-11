def product_query(keyword: str, page: int = 1, limit: int = 30):

    return f"""
    {{
      productOfferV2(
        keyword: "{keyword}",
        listType: 1,
        sortType: 5,
        page: {page},
        limit: {limit}
      ) {{

        nodes {{

          itemId
          productName
          imageUrl
          priceMin
          ratingStar
          sales
          offerLink

        }}

      }}
    }}
    """