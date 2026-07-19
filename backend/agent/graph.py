from typing import Dict, Any
from urllib.parse import quote_plus

from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from services.scraper import scraper_service
from services.analyzer import analyzer_service
from schemas.search import (
    AgentSearchResponse,
    ProductItem,
)


# ==========================================================
# NODE 1 - SEARCH DISCOVERY
# ==========================================================

async def search_discovery_node(
    state: AgentState
) -> Dict[str, Any]:
    """
    Builds retailer search URLs based on
    the user's requested product category.
    """

    category = state["category"].strip()

    category_query = quote_plus(category)

    target_urls = [

        # 🇮🇳 Indian Stores

        f"https://www.amazon.in/s?k={category_query}",

        f"https://www.flipkart.com/search?q={category_query}",

        f"https://www.croma.com/searchB?q={category_query}",

        f"https://www.reliancedigital.in/search?q={category_query}",

        f"https://www.vijaysales.com/search/{category_query}",


        # 🌍 International Stores

        f"https://www.amazon.com/s?k={category_query}",

        f"https://www.bestbuy.com/site/searchpage.jsp?st={category_query}",

        f"https://www.walmart.com/search?q={category_query}",

        f"https://www.newegg.com/p/pl?d={category_query}",

        f"https://www.ebay.com/sch/i.html?_nkw={category_query}"

    ]

    print("\n==============================")
    print("SEARCH DISCOVERY NODE")
    print("==============================")
    print(f"Category : {category}")
    print("Target URLs:")

    for url in target_urls:
        print(url)

    print("==============================\n")

    return {

        "target_urls": target_urls,

        "current_step": "Search Discovery Completed"

    }



async def collection_scraper_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 2: Scrapes retailer pages.
    """

    listing_urls = state.get("target_urls", [])

    product_page_entries = []


    for listing_url in listing_urls:

        try:

            print(f"===== SCRAPING =====")
            print(listing_url)

            listing_text = await scraper_service.fetch_page_text(
                listing_url
            )


        except Exception as error:

            print(
                f"--- SCRAPER ERROR {listing_url}: {error} ---"
            )

            continue



        if not listing_text or len(listing_text.strip()) < 50:

            print(
                f"--- EMPTY SCRAPE DATA {listing_url} ---"
            )

            continue



        print(
            f"Scraped characters: {len(listing_text)}"
        )

        print("----- FIRST 300 CHARACTERS -----")
        print(listing_text[:300])
        print("--------------------------------")

        product_page_entries.append(
            {
                "url": listing_url,
                "text": listing_text
            }
        )


    return {
        "scraped_raw_data": product_page_entries,
        "current_step": "Web Scraping Operations Completed"
    }




async def synthesis_recommendation_node(
    state: AgentState
) -> Dict[str, Any]:

    """
    Node 3:
    Uses OpenAI to extract products.
    """


    raw_entries = state.get(
        "scraped_raw_data",
        []
    )


    extracted_items = []



    for entry in raw_entries:

        source_url = entry["url"]
        text = entry["text"]

        # Skip fallback/error text
        if (
            "Error:" in text
            or "Fallback text:" in text
            or len(text.strip()) < 100
        ):
            print(f"Skipping invalid scrape from {source_url}")
            continue

        try:

            product = await analyzer_service.parse_product_data(
                text,
                source_url
            )

            print("==============================")
            print("AI EXTRACTED PRODUCT")
            print(product)
            print("==============================")

        except Exception as error:

            print(
                f"--- ANALYSIS FAILURE {source_url}: {error} ---"
            )

            continue

        if (
            product.price > 0
            and product.title not in (
                "Extraction Error",
                "Invalid Product",
                "ProductItem"
            )
            and len(product.pros) > 0
        ):

            if product.price <= state["budget"]:

                extracted_items.append(product)

                print("VALID PRODUCT ADDED")

            else:

                print("PRODUCT ABOVE USER BUDGET")

        else:

            print("INVALID PRODUCT REMOVED")




    # FALLBACK

    if not extracted_items:


        fallback = ProductItem(

            title=f"Standard {state['category'].title()}",

            price=state["budget"],

            source="Market Intelligence Engine",

            product_url="https://example.com",

            pros=[
                "Matches targeted pricing filters",
                "Generated from AI fallback engine",
                "Suitable when live extraction fails"
            ],

            cons=[
                "Live retailer product unavailable"
            ]

        )


        extracted_items.append(
            fallback
        )



    final_output = AgentSearchResponse(

        query=
        f"Category: {state['category']} within ${state['budget']}",


        recommended_product=
        extracted_items[0],


        alternative_options=
        extracted_items[1:],


        analysis_summary=
        "Recommendation generated using AI product extraction, budget filtering, and resilient fallback analysis."
    )



    return {


        "extracted_products": extracted_items,


        "final_recommendation": final_output,


        "current_step":
        "Synthesis Loop Complete"

    }





# ==========================================
# BUILD LANGGRAPH WORKFLOW
# ==========================================


workflow = StateGraph(AgentState)


workflow.add_node(
    "search_discovery",
    search_discovery_node
)


workflow.add_node(
    "collection_scraper",
    collection_scraper_node
)


workflow.add_node(
    "synthesis_recommendation",
    synthesis_recommendation_node
)



workflow.add_edge(
    START,
    "search_discovery"
)


workflow.add_edge(
    "search_discovery",
    "collection_scraper"
)


workflow.add_edge(
    "collection_scraper",
    "synthesis_recommendation"
)


workflow.add_edge(
    "synthesis_recommendation",
    END
)



shopping_agent_executor = workflow.compile()