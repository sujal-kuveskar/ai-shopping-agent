"use client";

import { useState } from "react";
import { searchProducts, ProductItem } from "@/lib/api";

export default function Home() {
  const [category, setCategory] = useState("");
  const [budget, setBudget] = useState("");
  const [preferences, setPreferences] = useState("");
  const [result, setResult] = useState<ProductItem | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleSearch() {
    if (!category.trim() || !budget) {
      alert("Please enter both a category and a budget.");
      return;
    }

    setLoading(true);
    setResult(null);

    try {
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
    }
  }

  return (
    <main className="min-h-screen p-10">
      <h1 className="text-3xl font-bold mb-6">AI Shopping Agent</h1>

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
          {loading ? "Searching..." : "Search Product"}
        </button>
      </div>

      {result && (
        <div className="mt-8 border p-5 rounded">
          <h2 className="text-xl font-bold">Recommendation</h2>
          <pre className="mt-3 text-sm">
            {JSON.stringify(result, null, 2)}
          </pre>
        </div>
      )}
    </main>
  );
}