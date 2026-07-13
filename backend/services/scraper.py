import httpx
from core.config import settings


class ScraperService:
    """
    Automated Data Scraping Engine powered by Browserbase.
    Connects to cloud infrastructure to reliably fetch layout data from dynamic e-commerce platforms.
    """
    def __init__(self):
        self.api_key = settings.BROWSERBASE_API_KEY
        self.base_url = "https://api.browserbase.com/v1"

    async def fetch_page_text(self, target_url: str) -> str:
        """
        Fetches a page through Browserbase's Fetch API and returns
        clean, markdown-formatted text content.
        """
        headers = {
            "X-BB-API-Key": self.api_key,
            "Content-Type": "application/json"
        }

        payload = {
            "url": target_url,
            "format": "markdown",
            "proxies": True
        }

        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/fetch",
                    headers=headers,
                    json=payload
                )

                if response.status_code != 200:
                    return f"Error: Browserbase fetch failed with status {response.status_code} - {response.text}"

                data = response.json()
                page_content = data.get("content", "")

                if not page_content:
                    return "Error: No visible text content could be extracted from target resource."

                cleaned_text = "\n".join(
                    line.strip() for line in page_content.splitlines() if line.strip()
                )
                return cleaned_text[:12000]

            except Exception as error:
                return f"Scraping Engine Execution Interruption: {str(error)}"


scraper_service = ScraperService()