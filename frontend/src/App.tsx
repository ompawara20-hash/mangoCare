import React from 'react';
import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { Navbar } from './components/Navbar';
import { Footer } from './components/Footer';
import { DashboardPage } from './pages/DashboardPage';
import { AnalyzePage } from './pages/AnalyzePage';
import { ResultsPage } from './pages/ResultsPage';
import { DiseaseLibraryPage } from './pages/DiseaseLibraryPage';
import { HistoryPage } from './pages/HistoryPage';
import { AboutModelPage } from './pages/AboutModelPage';
import { AlertCircle } from 'lucide-react';

const NotFoundPage: React.FC = () => (
  <div className="max-w-md mx-auto text-center py-20 bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
    <AlertCircle className="w-12 h-12 text-slate-300 mx-auto mb-3" />
    <h2 className="text-xl font-bold text-slate-800 mb-1">Page Not Found</h2>
    <p className="text-xs text-slate-500 mb-6">The requested page does not exist.</p>
    <Link
      to="/"
      className="px-4 py-2 rounded-xl bg-forest-800 text-white font-semibold text-xs hover:bg-forest-900 transition"
    >
      Return to Dashboard
    </Link>
  </div>
);

export function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen flex flex-col bg-[#faf9f5]">
        <Navbar />
        <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 pt-8 pb-12">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/analyze" element={<AnalyzePage />} />
            <Route path="/results" element={<ResultsPage />} />
            <Route path="/library" element={<DiseaseLibraryPage />} />
            <Route path="/history" element={<HistoryPage />} />
            <Route path="/about" element={<AboutModelPage />} />
            <Route path="*" element={<NotFoundPage />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </BrowserRouter>
  );
}

export default App;
