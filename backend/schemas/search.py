from pydantic import BaseModel, Field
from typing import List, Optional


class UserSearchRequest(BaseModel):
    """
    Blueprint for incoming user requests.
    """

    category: str = Field(
        ...,
        description="The product category user is shopping for",
        examples=["mechanical keyboard"]
    )

    budget: float = Field(
        ...,
        gt=0,
        description="Maximum budget constraint",
        examples=[150.00]
    )

    preferences: Optional[str] = Field(
        None,
        description="User requirements and preferences",
        examples=["RGB lighting, wireless"]
    )


class ProductItem(BaseModel):
    """
    Blueprint for product information.
    """

    title: str
    price: float
    source: str
    product_url: str
    pros: List[str]
    cons: List[str]


class AgentSearchResponse(BaseModel):
    """
    Final AI recommendation response.
    """

    query: str
    recommended_product: ProductItem
    alternative_options: List[ProductItem] = []
    analysis_summary: str