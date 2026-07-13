from typing import TypedDict, List
from schemas.search import ProductItem, AgentSearchResponse


class AgentState(TypedDict):
    """
    The central memory state for our LangGraph orchestration workflow.
    Tracks structural inputs, extracted metrics, and final product selections.
    """

    # Raw Inputs from the User
    category: str
    budget: float
    preferences: str

    # Internal Operational Data Arrays
    target_urls: List[str]
    scraped_raw_data: List[str]
    extracted_products: List[ProductItem]

    # The Final Outputs to send back to the user
    final_recommendation: AgentSearchResponse

    # Execution Tracking Logs
    current_step: str
    error_message: str