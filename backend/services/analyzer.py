from openai import OpenAI
from core.config import settings
from schemas.search import ProductItem


class AnalyzerService:
    """
    AI Processing Engine that transforms messy web text into structured product data.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def parse_product_data(self, raw_text: str, source_url: str) -> ProductItem:

        try:
            response = self.client.responses.parse(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert e-commerce data extraction specialist. "
                            "Extract product information from raw webpage text. "
                            "Return title, price, exactly 3 pros and exactly 3 cons. "
                            "Do not create fake products. If the page does not contain "
                            "a valid product, return title as 'Invalid Product' with "
                            "price 0 and empty pros/cons."
                        )
                    },
                    {
                        "role": "user",
                        "content": raw_text
                    }
                ],
                text_format=ProductItem,
            )

            parsed_product = response.output_parsed

            parsed_product.product_url = source_url

            if "amazon" in source_url.lower():
                parsed_product.source = "Amazon"
            elif "bestbuy" in source_url.lower():
                parsed_product.source = "Best Buy"
            else:
                parsed_product.source = "Web Retailer"

            return parsed_product

        except Exception as error:

            return ProductItem(
                title="Extraction Error",
                price=0.0,
                source="System Error",
                product_url=source_url,
                pros=[
                    "Could not process product data"
                ],
                cons=[
                    str(error)
                ]
            )


analyzer_service = AnalyzerService()