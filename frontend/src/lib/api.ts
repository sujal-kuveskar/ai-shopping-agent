const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL ||
  "https://ai-shopping-agent-i5pi.onrender.com";


export interface SearchProductsRequest {
  category: string;
  budget: number;
  preferences?: string;
}


export interface ProductItem {
  title: string;

  price: number;

  currency: string;

  price_inr?: number;

  source: string;

  product_url: string;

  image_url?: string;

  pros: string[];

  cons: string[];
}

export interface AgentSearchResponse {

  query: string;

  recommended_product: ProductItem;

  alternative_options: ProductItem[];

  analysis_summary: string;

}


export async function searchProducts(
  payload: SearchProductsRequest
): Promise<AgentSearchResponse> {

  const response = await fetch(
    `${API_BASE_URL}/api/agent/search`,
    {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    }
  );


  if (!response.ok) {

    const errorBody = await response.text();

    throw new Error(
      `Search request failed with status ${response.status}: ${errorBody}`
    );
  }


  const data: AgentSearchResponse = await response.json();

  return data;
}