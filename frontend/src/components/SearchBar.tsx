"use client"

import { useState } from "react";

export default function SearchBar() {
  const [ticker, setTicker] = useState("");

  async function handleAnalyze() {
  if (!ticker.trim()) {
    alert("Please enter a stock ticker.");
    return;
  }

  try {
    const response = await fetch(
      `http://127.0.0.1:8000/api/analyze/${ticker.toUpperCase()}`
    );

    const data = await response.json();

    console.log(data);

    alert(`Company: ${data.company}`);
  } catch (error) {
    console.error(error);
    alert("Unable to contact the AlphaSight backend.");
  }
}

  return (
    <div className="mt-12 flex justify-center gap-4">
      <input
        type="text"
        value={ticker}
        onChange={(e) => setTicker(e.target.value)}
        placeholder="Enter ticker (AAPL, NVDA, MSFT...)"
        className="w-full max-w-lg rounded-lg border border-slate-700 bg-slate-900 px-4 py-3 text-white focus:border-blue-500 focus:outline-none"
      />

      <button
        onClick={handleAnalyze}
        className="rounded-lg bg-blue-600 px-6 py-3 font-semibold hover:bg-blue-500 transition"
      >
        Analyze
      </button>
    </div>
  );
}
