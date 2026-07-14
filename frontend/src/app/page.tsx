"use client";

import { useState } from "react";
import { searchProducts, AgentSearchResponse } from "@/lib/api";

export default function Home() {
  const [category, setCategory] = useState("");
  const [budget, setBudget] = useState("");
  const [preferences, setPreferences] = useState("");

  const [result, setResult] = useState<AgentSearchResponse | null>(null);
 const [loading, setLoading] = useState(false);
const [agentStep, setAgentStep] = useState("");


  async function handleSearch() {
    if (!category.trim() || !budget) {
      alert("Please enter both a category and a budget.");
      return;
    }

    setLoading(true);
setResult(null);

setAgentStep("🤖 AI Agent is searching...");


    try {
      setAgentStep("🌐 Scraping shopping websites...");

await new Promise((resolve) =>
  setTimeout(resolve, 1200)
);


setAgentStep("🧠 Analyzing products with AI...");

await new Promise((resolve) =>
  setTimeout(resolve, 1200)
);


setAgentStep("⭐ Selecting best recommendation");


const data = await searchProducts({
  category,
  budget: Number(budget),
  preferences,
});

      setResult(data);

    } catch (error) {
      console.error(error);
      alert("Failed to get recommendation. Please try again.");

    } finally {
  setLoading(false);
  setAgentStep("");
}
  }


  return (
    <main className="min-h-screen p-10">

      <h1 className="text-3xl font-bold mb-6">
        AI Shopping Agent
      </h1>


      <div className="space-y-4 max-w-md">

        <input
          className="border p-2 w-full"
          placeholder="Product category"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        />


        <input
          type="number"
          className="border p-2 w-full"
          placeholder="Budget"
          value={budget}
          onChange={(e) => setBudget(e.target.value)}
        />


        <input
          className="border p-2 w-full"
          placeholder="Preferences"
          value={preferences}
          onChange={(e) => setPreferences(e.target.value)}
        />


        <button
          className="bg-black text-white px-4 py-2 rounded disabled:opacity-50"
          onClick={handleSearch}
          disabled={loading}
        >
          {loading ? "AI Thinking..." : "Search Product"}
        </button>

      </div>


{loading && (
  <div className="mt-8 max-w-xl border rounded-lg p-6 shadow">

    <h2 className="text-xl font-bold">
      AI Shopping Agent
    </h2>

    <p className="mt-4 animate-pulse">
      {agentStep}
    </p>

  </div>
)}

      {result && (

        <div className="mt-8 max-w-xl border rounded-lg p-6 shadow">


          <h2 className="text-2xl font-bold mb-4">
            ⭐ Recommendation
          </h2>


          <h3 className="text-xl font-semibold">
            {result.recommended_product.title}
          </h3>


          <p className="mt-2">
            💰 Price: ${result.recommended_product.price}
          </p>


          <p>
            🛒 Source: {result.recommended_product.source}
          </p>



          <div className="mt-4">

            <h4 className="font-bold text-green-600">
              Pros
            </h4>


            <ul className="list-disc ml-5">

              {result.recommended_product.pros.map(
                (item, index) => (
                  <li key={index}>
                    ✓ {item}
                  </li>
                )
              )}

            </ul>

          </div>




          <div className="mt-4">

            <h4 className="font-bold text-red-600">
              Cons
            </h4>


            <ul className="list-disc ml-5">

              {result.recommended_product.cons.map(
                (item, index) => (
                  <li key={index}>
                    ✗ {item}
                  </li>
                )
              )}

            </ul>

          </div>




          <a
            href={result.recommended_product.product_url}
            target="_blank"
            className="inline-block mt-5 bg-black text-white px-4 py-2 rounded"
          >
            View Product
          </a>



          <p className="mt-5 text-sm text-gray-600">
            {result.analysis_summary}
          </p>


        </div>

      )}


    </main>
  );
}