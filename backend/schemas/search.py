from pydantic import BaseModel, Field
from typing import List, Optional


class UserSearchRequest(BaseModel):
    """
    Incoming user search request.
    """

    category: str = Field(
        ...,
        description="Product category to search",
        examples=["Gaming Keyboard"]
    )

    budget: float = Field(
        ...,
        gt=0,
        description="Maximum user budget",
        examples=[180]
    )

    preferences: Optional[str] = Field(
        default=None,
        description="Additional user preferences",
        examples=["RGB, Wireless"]
    )


class ProductItem(BaseModel):
    """
    Product returned by the AI Shopping Agent.
    """

    title: str

    # Numeric price
    price: float

    # Currency returned by retailer
    currency: str = "USD"

    # Optional INR price (filled only for Indian stores)
    price_inr: Optional[float] = None

    source: str = ""

    product_url: str = ""

    image_url: str = ""

    pros: List[str] = []

    cons: List[str] = []


class AgentSearchResponse(BaseModel):
    """
    Final response returned to frontend.
    """

    query: str

    recommended_product: ProductItem

    alternative_options: List[ProductItem] = Field(default_factory=list)

    analysis_summary: str