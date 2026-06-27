"use client"

import { useState } from "react";

export default function SearchBar() {
  const [ticker, setTicker] = useState("");

  function handleAnalyze() {
    if (!ticker.trim()) {
      alert("Please enter a stock ticker.");
      return;
    }

    console.log(`Analyzing ${ticker.toUpperCase()}...`);
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
