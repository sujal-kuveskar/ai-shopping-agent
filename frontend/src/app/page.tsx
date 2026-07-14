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
  const [error, setError] = useState("");


  async function handleSearch() {

    // Validation
    if (!category.trim() || !budget || Number(budget) <= 0) {

      setError(
        "Please enter a valid product category and budget."
      );

      setResult(null);
      return;
    }


    setLoading(true);
    setResult(null);
    setError("");


    try {

      setAgentStep(
        "🤖 AI Agent started searching..."
      );


      await new Promise((resolve) =>
        setTimeout(resolve, 1000)
      );


      setAgentStep(
        "🌐 Scraping shopping websites..."
      );


      await new Promise((resolve) =>
        setTimeout(resolve, 1200)
      );


      setAgentStep(
        "🧠 Analyzing products using AI..."
      );


      await new Promise((resolve) =>
        setTimeout(resolve, 1200)
      );


      setAgentStep(
        "⭐ Selecting best recommendation..."
      );


      const data = await searchProducts({

        category,

        budget: Number(budget),

        preferences,

      });


      setResult(data);


      setAgentStep(
        "✅ Recommendation generated successfully"
      );


    } catch (error) {

      console.error(error);


      setError(
        "Sorry, we couldn't complete your search. The AI agent may be temporarily unavailable. Please try again."
      );


    } finally {

      setLoading(false);

    }

  }



  return (

    <main className="min-h-screen p-10">


      <h1 className="text-3xl font-bold mb-6">
        AI Shopping Agent
      </h1>



      <div className="space-y-4 max-w-md">


        <input
          className="border p-2 w-full rounded"
          placeholder="Product category"
          value={category}
          onChange={(e)=>setCategory(e.target.value)}
        />



        <input
          type="number"
          className="border p-2 w-full rounded"
          placeholder="Budget"
          value={budget}
          onChange={(e)=>setBudget(e.target.value)}
        />



        <input
          className="border p-2 w-full rounded"
          placeholder="Preferences"
          value={preferences}
          onChange={(e)=>setPreferences(e.target.value)}
        />



        <button

          className="
          bg-black 
          text-white 
          px-5 
          py-2 
          rounded
          disabled:opacity-50
          "

          onClick={handleSearch}

          disabled={loading}

        >

          {
            loading
            ? "AI Thinking..."
            : "Search Product"
          }

        </button>


      </div>




      {/* AI Workflow Status */}

      {(loading || agentStep) && (

        <div className="
        mt-8 
        max-w-xl 
        border 
        rounded-lg 
        p-6 
        shadow
        ">


          <h2 className="text-xl font-bold">

            🤖 AI Shopping Agent

          </h2>


          <p className="mt-4 animate-pulse">

            {agentStep}

          </p>


        </div>

      )}






      {/* Error Message */}

      {error && (

        <div className="
        mt-8 
        max-w-xl 
        border 
        border-red-400 
        bg-red-100 
        rounded-lg 
        p-5
        ">


          <h2 className="
          text-lg 
          font-bold 
          text-red-700
          ">

            ⚠️ Search Failed

          </h2>



          <p className="
          mt-2 
          text-red-600
          ">

            {error}

          </p>


        </div>

      )}






      {/* Product Result */}

      {result && (

        <div className="
        mt-8 
        max-w-xl 
        border 
        rounded-lg 
        p-6 
        shadow
        ">


          <h2 className="
          text-2xl 
          font-bold 
          mb-4
          ">

            ⭐ Recommendation

          </h2>




          <h3 className="
          text-xl 
          font-semibold
          ">

            {result.recommended_product.title}

          </h3>




          <p className="mt-2">

            💰 Price: $
            {result.recommended_product.price}

          </p>



          <p>

            🛒 Source:
            {result.recommended_product.source}

          </p>






          <div className="mt-4">


            <h4 className="
            font-bold 
            text-green-600
            ">

              Pros

            </h4>



            <ul className="list-disc ml-5">

              {
                result.recommended_product.pros.map(
                  (item,index)=>(
                    <li key={index}>
                      ✓ {item}
                    </li>
                  )
                )
              }


            </ul>


          </div>






          <div className="mt-4">


            <h4 className="
            font-bold 
            text-red-600
            ">

              Cons

            </h4>



            <ul className="list-disc ml-5">


              {
                result.recommended_product.cons.map(
                  (item,index)=>(
                    <li key={index}>
                      ✗ {item}
                    </li>
                  )
                )
              }


            </ul>


          </div>






          <a

            href={
              result.recommended_product.product_url
            }

            target="_blank"

            className="
            inline-block 
            mt-5 
            bg-black 
            text-white 
            px-4 
            py-2 
            rounded
            "

          >

            View Product

          </a>




          <p className="
          mt-5 
          text-sm 
          text-gray-600
          ">

            {result.analysis_summary}

          </p>



        </div>

      )}



    </main>

  );

}