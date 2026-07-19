"use client";

import { useState } from "react";
import { searchProducts, AgentSearchResponse } from "@/lib/api";

export default function Home() {

  const [category, setCategory] = useState("");
  const [budget, setBudget] = useState("");
  const [preferences, setPreferences] = useState("");

  const [result, setResult] = useState<AgentSearchResponse | null>(null);
  const [loading, setLoading] = useState(false);

  const [workflowSteps, setWorkflowSteps] = useState<string[]>([]);
  const [error, setError] = useState("");


  // USD to INR converter
  const usdToInr = (usd: number) => {
    const exchangeRate = 85;
    return (usd * exchangeRate).toFixed(0);
  };



  async function handleSearch() {


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


      setWorkflowSteps([
        "✅ User request received"
      ]);


      await new Promise((resolve) =>
        setTimeout(resolve, 1000)
      );



      setWorkflowSteps((prev) => [
        ...prev,
        "🌐 Searching shopping websites"
      ]);


      await new Promise((resolve) =>
        setTimeout(resolve, 1200)
      );



      setWorkflowSteps((prev) => [
        ...prev,
        "📄 Scraping product pages"
      ]);


      await new Promise((resolve) =>
        setTimeout(resolve, 1200)
      );



      setWorkflowSteps((prev) => [
        ...prev,
        "🧠 AI analyzing products"
      ]);



      const data = await searchProducts({

        category,

        budget: Number(budget),

        preferences,

      });



      setResult(data);



      setWorkflowSteps((prev) => [
        ...prev,
        "💰 Filtering by budget",
        "⭐ Recommendation generated"
      ]);



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

    <main className="min-h-screen bg-gray-100 py-10 px-6">


      <div className="text-center mb-14">

    <div className="inline-flex items-center justify-center w-24 h-24 rounded-full bg-gradient-to-r from-blue-600 to-purple-600 text-5xl shadow-xl mb-6">
        🤖
    </div>

    <h1 className="text-6xl font-extrabold tracking-tight text-gray-900">
        AI Shopping Agent
    </h1>

    <p className="mt-5 text-xl text-gray-600 max-w-3xl mx-auto leading-8">
        Search products across multiple retailers, let AI compare features,
        analyze prices, and recommend the best option that fits your budget.
    </p>

    <div className="flex justify-center gap-4 mt-8 flex-wrap">

        <span className="px-5 py-2 bg-blue-100 text-blue-700 rounded-full font-semibold">
            🤖 AI Powered
        </span>

        <span className="px-5 py-2 bg-green-100 text-green-700 rounded-full font-semibold">
            🛒 Multi Store Search
        </span>

        <span className="px-5 py-2 bg-purple-100 text-purple-700 rounded-full font-semibold">
            ⚡ LangGraph Workflow
        </span>

    </div>

</div>




      <div className="max-w-2xl mx-auto bg-white rounded-3xl shadow-2xl overflow-hidden">

    <div className="bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600 p-6">

        <h2 className="text-3xl font-bold text-white">
            🔍 Find Your Perfect Product
        </h2>

        <p className="text-blue-100 mt-2">
            Enter your requirements and let AI search multiple stores.
        </p>

    </div>

    <div className="p-8 space-y-6">
      </div>


        <input
  className="w-full rounded-xl border border-gray-300 px-5 py-4 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
  placeholder="🎮 Gaming Keyboard"
  value={category}
  onChange={(e) => setCategory(e.target.value)}
/>



        <input
  type="number"
  className="w-full rounded-xl border border-gray-300 px-5 py-4 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
  placeholder="💰 Budget"
  value={budget}
  onChange={(e) => setBudget(e.target.value)}
/>



        <input
  className="w-full rounded-xl border border-gray-300 px-5 py-4 text-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
  placeholder="✨ RGB, Wireless, Hot-Swappable..."
  value={preferences}
  onChange={(e) => setPreferences(e.target.value)}
/>


        <button
  className="w-full rounded-xl bg-gradient-to-r from-blue-600 to-indigo-600 py-4 text-lg font-bold text-white hover:scale-[1.02] hover:from-blue-700 hover:to-indigo-700 transition-all duration-300 disabled:opacity-50"
  onClick={handleSearch}
  disabled={loading}
>

          {
            loading
              ? "AI Thinking..."
              : "🔍 Search Product"
          }


        </button>


      </div>





      {/* AI Workflow */}

      {(loading || workflowSteps.length > 0) && (

        <div
  className="
  mt-10
  max-w-4xl
  mx-auto
  bg-white
  rounded-3xl
  shadow-2xl
  overflow-hidden
  border
  border-gray-200
"
>


          <h2 className="text-xl font-bold">

            🤖 AI Shopping Agent

          </h2>


          <ul className="space-y-2 mt-4">
            {workflowSteps.map((step, index) => (
              <li key={index}>{step}</li>
            ))}
          </ul>


        </div>

      )}






      {/* Error */}

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







      {/* Product */}

      {result && (

        <div className="
        mt-8
        max-w-xl
        border
        rounded-lg
        p-6
        shadow
        ">

{/* Product Comparison Table */}

<div className="mb-10 overflow-x-auto">

    <h2 className="text-2xl font-bold text-gray-900 mb-5">

        📊 Product Comparison

    </h2>

    <table className="w-full border border-gray-300 rounded-xl overflow-hidden">

        <thead className="bg-blue-600 text-white">

            <tr>

                <th className="p-4 text-left">Product</th>

                <th className="p-4 text-left">Store</th>

                <th className="p-4 text-left">Price</th>

                <th className="p-4 text-left">Currency</th>

            </tr>

        </thead>

        <tbody>

            <tr className="border-b">

                <td className="p-4">
                    {result.recommended_product.title}
                </td>

                <td className="p-4">
                    {result.recommended_product.source}
                </td>

                <td className="p-4">
                    {result.recommended_product.price}
                </td>

                <td className="p-4">
                    {result.recommended_product.currency}
                </td>

            </tr>

            {result.alternative_options.map((product, index) => (

                <tr
                    key={index}
                    className="border-b"
                >

                    <td className="p-4">
                        {product.title}
                    </td>

                    <td className="p-4">
                        {product.source}
                    </td>

                    <td className="p-4">
                        {product.price}
                    </td>

                    <td className="p-4">
                        {product.currency}
                    </td>

                </tr>

            ))}

        </tbody>

    </table>

</div>

          <h2
className="
text-3xl
font-extrabold
text-green-600
mb-6
"
>

⭐ AI Recommendation

</h2>



{result.recommended_product.image_url && (

    <img
        src={result.recommended_product.image_url}
        alt={result.recommended_product.title}
        className="
        w-full
        h-72
        object-cover
        rounded-2xl
        mb-6
        border
        "
    />

)}

          <h3
className="
text-2xl
font-extrabold
text-gray-900
leading-relaxed
"
>

{result.recommended_product.title}

</h3> 





          <div className="mt-6">

  <h4 className="text-lg font-bold text-gray-700 mb-3">
    💰 Price
  </h4>

  <div className="bg-gray-100 rounded-xl p-4 space-y-2">

    <div className="flex justify-between">

      <span className="font-semibold">
        💵 USD
      </span>

      <span className="text-xl font-bold text-green-600">
        ${result.recommended_product.price}
      </span>

    </div>

    <div className="flex justify-between">

      <span className="font-semibold">
        🇮🇳 INR
      </span>

      <span className="text-xl font-bold text-blue-600">
        ₹{Number(
          usdToInr(result.recommended_product.price)
        ).toLocaleString("en-IN")}
      </span>

    </div>

  </div>

</div>





          <p className="mt-2">

            🛒 Source:
            {" "}
            {result.recommended_product.source}

          </p>







          <div className="mt-6">

  <div className="bg-green-50 border border-green-200 rounded-xl p-5">

    <h4 className="text-xl font-bold text-green-700 mb-3">

      ✅ Pros

    </h4>

    <ul className="space-y-2">

      {result.recommended_product.pros.map((item, index) => (

        <li
          key={index}
          className="text-gray-700"
        >
          ✓ {item}
        </li>

      ))}

    </ul>

  </div>

</div>








          <div className="mt-6">

  <div className="bg-red-50 border border-red-200 rounded-xl p-5">

    <h4 className="text-xl font-bold text-red-700 mb-3">

      ❌ Cons

    </h4>

    <ul className="space-y-2">

      {result.recommended_product.cons.map((item, index) => (

        <li
          key={index}
          className="text-gray-700"
        >
          ✗ {item}
        </li>

      ))}

    </ul>

  </div>

</div>








          <a
  href={result.recommended_product.product_url}
  target="_blank"
  rel="noopener noreferrer"
  className="
  inline-flex
  items-center
  justify-center
  gap-2
  mt-6
  px-6
  py-3
  rounded-xl
  bg-gradient-to-r
  from-blue-600
  to-indigo-600
  text-white
  font-bold
  shadow-lg
  hover:scale-105
  hover:shadow-xl
  transition-all
  duration-300
  "
>
  🛒 View Product →
</a>







          <p className="
          mt-5
          text-sm
          text-gray-600
          ">

            {result.analysis_summary}

          </p>

          {result.alternative_options.length > 0 && (

            <div className="mt-8">

              <h2 className="text-2xl font-bold mb-4">
                🔄 Alternative Options
              </h2>


              <div className="space-y-4">


                {
                  result.alternative_options.map(
                    (product, index) => (


                      <div
key={index}
className="
bg-white
border
border-gray-200
rounded-2xl
shadow-md
p-6
hover:shadow-xl
hover:scale-[1.02]
transition-all
duration-300
"
>
{product.image_url && (

    <img
        src={product.image_url}
        alt={product.title}
        className="
        w-full
        h-56
        object-cover
        rounded-xl
        mb-4
        border
        "
    />

)}

                        <h3
className="
text-2xl
font-extrabold
text-gray-900
leading-relaxed
mb-4
"
>

🔹 {product.title}

</h3>


                        <div className="mt-5">

  <h4 className="text-lg font-bold text-gray-700 mb-3">
    💰 Price
  </h4>

  <div className="bg-gray-100 rounded-xl p-4 space-y-2">

    <div className="flex justify-between">

      <span className="font-semibold">
        💵 USD
      </span>

      <span className="text-lg font-bold text-green-600">
        ${product.price}
      </span>

    </div>

    <div className="flex justify-between">

      <span className="font-semibold">
        🇮🇳 INR
      </span>

      <span className="text-lg font-bold text-blue-600">
        ₹{Number(
          usdToInr(product.price)
        ).toLocaleString("en-IN")}
      </span>

    </div>

  </div>

</div>


                        <p>
                          🛒 Source: {product.source}
                        </p>


                        <a
                          href={product.product_url}
                          target="_blank"
                          className="
inline-block
mt-3
bg-gray-800
text-white
px-3
py-2
rounded
"
                        >
                          View Product
                        </a>


                      </div>


                    )
                  )
                }


              </div>

            </div>

          )}



        </div>

      )}



    </main>

  );


}