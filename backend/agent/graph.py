from typing import Dict, Any
from urllib.parse import quote_plus

from langgraph.graph import StateGraph, START, END

from agent.state import AgentState
from services.scraper import scraper_service
from services.analyzer import analyzer_service
from schemas.search import AgentSearchResponse, ProductItem


# ==========================================
# 1. DEFINE THE GRAPH PROCESSING NODES
# ==========================================

async def search_discovery_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 1: Finds possible product URLs.
    Generates shopping search URLs based on user category.
    """

    category_query = quote_plus(state["category"])

    target_urls = [
        f"https://www.amazon.com/s?k={category_query}",
        f"https://www.bestbuy.com/site/searchpage.jsp?st={category_query}"
    ]

    return {
        "target_urls": target_urls,
        "current_step": "Search Discovery Completed"
    }


async def collection_scraper_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 2: Scrapes webpage content using Browserbase.
    Hardened: isolates failures per-URL so one bad scrape
    doesn't take down the whole node.
    """

    urls_to_scrape = state.get("target_urls", [])
    raw_results = []

    for url in urls_to_scrape:
        try:
            text = await scraper_service.fetch_page_text(url)
        except Exception as error:
            print(f"--- SCRAPE FAILURE for {url}: {str(error)} ---")
            text = ""

        raw_results.append({"url": url, "text": text})

    return {
        "scraped_raw_data": raw_results,
        "current_step": "Web Scraping Operations Completed"
    }


async def synthesis_recommendation_node(state: AgentState) -> Dict[str, Any]:
    """
    Node 3: Uses OpenAI analyzer and creates final recommendation.
    Hardened: isolates failures per-entry so one bad analysis
    doesn't take down the whole node.
    """

    raw_entries = state.get("scraped_raw_data", [])
    extracted_items = []

    for entry in raw_entries:
        source_url = entry["url"]
        text = entry["text"]

        if not text or not text.strip():
            print(f"--- SKIPPED empty scraped content for {source_url} ---")
            continue

        try:
            product = await analyzer_service.parse_product_data(
                text,
                source_url
            )
        except Exception as error:
            print(f"--- ANALYSIS FAILURE for {source_url}: {str(error)} ---")
            continue

        # Only accept extractions that look genuinely valid:
        # a real price, a non-empty pros list, and not a placeholder title.
        if (
            product.price > 0
            and product.title not in ("ProductItem", "Invalid Product", "Extraction Error")
            and len(product.pros) > 0
        ):
            if product.price <= state["budget"]:
                extracted_items.append(product)

    if not extracted_items:
        fallback = ProductItem(
            title=f"Generic {state['category']}",
            price=state["budget"],
            source="System Engine",
            product_url="https://example.com",
            pros=["Fits budget requirement"],
            cons=["No matching products found"]
        )
        extracted_items.append(fallback)

    final_output = AgentSearchResponse(
        query=f"Category: {state['category']} within ${state['budget']}",
        recommended_product=extracted_items[0],
        alternative_options=extracted_items[1:],
        analysis_summary="Selected based on budget and preferences."
    )

    return {
        "extracted_products": extracted_items,
        "final_recommendation": final_output,
        "current_step": "Synthesis Loop Complete"
    }


# ==========================================
# 2. BUILD LANGGRAPH WORKFLOW
# ==========================================

workflow = StateGraph(AgentState)

workflow.add_node("search_discovery", search_discovery_node)
workflow.add_node("collection_scraper", collection_scraper_node)
workflow.add_node("synthesis_recommendation", synthesis_recommendation_node)

workflow.add_edge(START, "search_discovery")
workflow.add_edge("search_discovery", "collection_scraper")
workflow.add_edge("collection_scraper", "synthesis_recommendation")
workflow.add_edge("synthesis_recommendation", END)

shopping_agent_executor = workflow.compile()