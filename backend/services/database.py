import hashlib
from supabase import create_client, Client
from core.config import settings
from typing import Optional, Dict, Any


class DatabaseService:
    """
    Data Access Object handling cloud communication with our Supabase instance.
    Implements optimized caching lookup and insert methods.
    """
    def __init__(self):
        self.client: Client = create_client(
            settings.SUPABASE_URL,
            settings.SUPABASE_ANON_KEY
        )

    def _generate_query_key(self, category: str, budget: float, preferences: str = "") -> str:
        """
        Builds a stable, unique cache key from the search parameters.
        Same inputs always produce the same key, so repeated searches
        with identical criteria hit the cache instead of re-running the agent.
        """
        raw_key = f"{category.strip().lower()}|{budget}|{preferences.strip().lower()}"
        return hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

    def get_cached_search(
        self,
        category: str,
        budget: float,
        preferences: str = ""
    ) -> Optional[Dict[str, Any]]:
        """
        Looks up a previously cached search result matching the same
        query_key. Returns None on a cache miss.
        """
        query_key = self._generate_query_key(category, budget, preferences)

        try:
            response = (
                self.client.table("search_cache")
                .select("structured_response")
                .eq("query_key", query_key)
                .execute()
            )

            if response.data and len(response.data) > 0:
                return response.data[0].get("structured_response")

            return None

        except Exception as error:
            print(f"--- CACHE LOOKUP ERROR: {str(error)} ---")
            return None

    def save_to_cache(
        self,
        category: str,
        budget: float,
        preferences: str,
        data: Dict[str, Any]
    ) -> None:
        """
        Inserts a new search result into the cache table for future reuse.
        """
        query_key = self._generate_query_key(category, budget, preferences)

        payload = {
            "query_key": query_key,
            "category": category,
            "budget": budget,
            "preferences": preferences,
            "structured_response": data
        }

        try:
            self.client.table("search_cache") \
    .upsert(payload, on_conflict="query_key") \
    .execute()

        except Exception as error:
            print(f"--- CACHE SAVE ERROR: {str(error)} ---")


db_service = DatabaseService()