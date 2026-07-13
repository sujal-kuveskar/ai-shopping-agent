import json

from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from schemas.search import UserSearchRequest, AgentSearchResponse, ProductItem
from services.scraper import scraper_service
from services.analyzer import analyzer_service
from services.database import db_service
from agent.graph import shopping_agent_executor

app = FastAPI(
    title="AI Shopping Agent API",
    description="The production backend engine powering the AI Shopping Agent",
    version="0.1.0"
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/health")
async def health_check():
    return {
        "status": "healthy",
        "project": "AI Shopping Agent Backend",
        "environment": settings.ENV,
        "version": "0.1.0"
    }


@app.post("/api/agent/test-validate")
async def test_validation(payload: UserSearchRequest):
    return {
        "message": "Data schema is perfectly valid!",
        "received_data": payload
    }


@app.get("/test-scraper")
async def test_scraper(url: str):
    """
    Test Browserbase Fetch API connection.
    """
    result = await scraper_service.fetch_page_text(url)
    return {"url": url, "content": result}


@app.post("/api/test-scrape")
async def test_scrape(url: str):
    """
    Test Browserbase page text extraction.
    """
    result = await scraper_service.fetch_page_text(url)

    return {
        "status": "success",
        "url": url,
        "content": result
    }


@app.get("/api/test/scrape")
async def test_scraper_metrics(
    url: str = Query(..., description="The live website link to scrape")
):
    """
    Utility testing route to evaluate Browserbase layout fetching metrics.
    """
    extracted_text = await scraper_service.fetch_page_text(url)

    return {
        "target_url": url,
        "character_count": len(extracted_text),
        "sample_data": extracted_text[:800]
    }


@app.post("/api/test/analyze")
async def test_analyzer(text: str, source_url: str):
    """
    Test OpenAI structured product extraction.
    """
    product = await analyzer_service.parse_product_data(
        raw_text=text,
        source_url=source_url
    )
    return product


@app.get("/api/test/analyze-url")
async def test_full_pipeline(url: str = Query(..., description="The product link to scrape and analyze")):
    """
    End-to-End Pipeline Tester:
    Browserbase scraping + OpenAI product analysis
    """
    raw_web_text = await scraper_service.fetch_page_text(url)

    if "Error" in raw_web_text or "Interruption" in raw_web_text:
        return {
            "status": "error",
            "details": raw_web_text
        }

    structured_product: ProductItem = await analyzer_service.parse_product_data(
        raw_web_text,
        url
    )

    return {
        "status": "success",
        "data": structured_product
    }


@app.post("/api/agent/search", response_model=AgentSearchResponse)
async def execute_agent_search(payload: UserSearchRequest):
    """
    Executes the shopping assistant search pipeline.
    Uses Supabase cache first to avoid unnecessary agent executions.
    """

    # STEP 1: Check database cache
    cached_data = db_service.get_cached_search(
        payload.category,
        payload.budget,
        payload.preferences or ""
    )

    if cached_data:
        print("--- CACHE HIT: Returning optimized database record instantly ---")
        return cached_data

    print("--- CACHE MISS: Launching live autonomous LangGraph agent workflow ---")

    try:
        # STEP 2: Run LangGraph agent if cache is empty
        initial_inputs = {
            "category": payload.category,
            "budget": payload.budget,
            "preferences": payload.preferences or "None provided",
            "target_urls": [],
            "scraped_raw_data": [],
            "extracted_products": [],
            "current_step": "Initialization Node Started",
            "error_message": ""
        }

        output_state = await shopping_agent_executor.ainvoke(initial_inputs)

        final_result: AgentSearchResponse = output_state.get(
            "final_recommendation"
        )

        if not final_result:
            raise HTTPException(
                status_code=500,
                detail="Agent failed to generate recommendation."
            )

        # STEP 3: Save result into Supabase cache
        result_dict = json.loads(
            final_result.model_dump_json()
        )

        db_service.save_to_cache(
            category=payload.category,
            budget=payload.budget,
            preferences=payload.preferences or "",
            data=result_dict
        )

        return final_result

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"Agent System Execution Failure: {str(error)}"
        )