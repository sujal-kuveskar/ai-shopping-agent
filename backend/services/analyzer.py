from urllib.parse import quote_plus

from openai import OpenAI

from core.config import settings
from schemas.search import ProductItem


class AnalyzerService:
    """
    AI engine that converts raw scraped webpage text
    into structured product information.
    """

    def __init__(self):
        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)

    async def parse_product_data(
        self,
        raw_text: str,
        source_url: str
    ) -> ProductItem:

        try:

            response = self.client.responses.parse(
                model="gpt-4o-mini",
                input=[
                    {
                        "role": "system",
                        "content": (
                            "You are an expert e-commerce product extraction engine.\n\n"
                            "Extract ONE real product from the webpage.\n\n"
                            "Rules:\n"
                            "- Return only one product.\n"
                            "- Extract the product title.\n"
                            "- Extract the numeric price only.\n"
                            "- Detect the currency (USD, INR, EUR, GBP etc.).\n"
                            "- Return exactly 3 pros.\n"
                            "- Return exactly 3 cons.\n"
                            "- Never invent products.\n"
                            "- If no real product exists return title 'Invalid Product' and price 0."
                        )
                    },
                    {
                        "role": "user",
                        "content": raw_text
                    }
                ],
                text_format=ProductItem,
            )

            product = response.output_parsed

            product.product_url = source_url

            product.image_url = (
                f"https://picsum.photos/seed/{quote_plus(product.title)}/600/600"
            )

            url = source_url.lower()

            if "bestbuy" in url:
                product.source = "Best Buy"

            elif "walmart" in url:
                product.source = "Walmart"

            elif "newegg" in url:
                product.source = "Newegg"

            elif "amazon" in url:
                product.source = "Amazon"

            elif "flipkart" in url:
                product.source = "Flipkart"

            elif "croma" in url:
                product.source = "Croma"

            else:
                product.source = "Web Retailer"

            if not product.currency:
                product.currency = "USD"

            if product.currency.upper() == "USD":
                product.price_inr = round(product.price * 87, 2)

            return product

        except Exception as error:

            print("===== ANALYZER ERROR =====")
            print(error)
            print("==========================")

            return ProductItem(
                title="Extraction Error",
                price=0.0,
                currency="USD",
                price_inr=0.0,
                source="System Error",
                product_url=source_url,
                image_url="",
                pros=["Unable to analyze webpage"],
                cons=[str(error)]
            )


analyzer_service = AnalyzerService()