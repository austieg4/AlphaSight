import Hero from "@/components/Hero";
import SearchBar from "@/components/SearchBar";

export default function Home() {
  return (
    <main className="min-h-screen bg-slate-950 text-white flex items-center justify-center">
      <div className="max-w-5xl w-full px-8">
        <Hero />
        <SearchBar />
      </div>
    </main>
  );
}