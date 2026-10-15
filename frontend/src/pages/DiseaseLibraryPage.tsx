import React, { useState, useEffect } from 'react';
import { Search, BookOpen, Layers, ShieldCheck, Activity, ArrowRight } from 'lucide-react';
import { api } from '../api/client';
import { ConditionInformation } from '../types';
import { DiseaseDetailModal } from '../components/DiseaseDetailModal';

export const DiseaseLibraryPage: React.FC = () => {
  const [diseases, setDiseases] = useState<ConditionInformation[]>([]);
  const [selectedDisease, setSelectedDisease] = useState<ConditionInformation | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState<string>('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    api.getDiseases(searchQuery)
      .then((res) => setDiseases(res.diseases))
      .catch((err) => console.error('Error fetching diseases:', err))
      .finally(() => setLoading(false));
  }, [searchQuery]);

  const categories = [
    { id: 'all', label: 'All Conditions' },
    { id: 'fungal', label: 'Fungal Pathologies' },
    { id: 'bacterial', label: 'Bacterial Cankers' },
    { id: 'pest', label: 'Insect Pests' },
    { id: 'healthy', label: 'Healthy Tissue' },
  ];

  const filteredDiseases = diseases.filter((d) => {
    if (activeCategory === 'all') return true;
    return d.category?.toLowerCase() === activeCategory;
  });

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in pb-16">
      {/* Page Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-50 border border-forest-200/60 text-xs font-semibold text-forest-800 mb-2">
          <BookOpen className="w-3.5 h-3.5" />
          <span>Educational Reference Database</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Supported Mango Conditions & Pathologies
        </h1>
        <p className="text-sm text-slate-500 mt-1 max-w-3xl">
          Comprehensive scientific and agronomic profiles for all 8 foliar conditions classified by the MangoCare AI vision model.
        </p>
      </div>

      {/* Search and Category Filter Toolbar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4 bg-white p-4 rounded-2xl border border-slate-200 shadow-sm">
        {/* Search Bar */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by disease name, pathogen, or symptom..."
            className="w-full pl-10 pr-4 py-2 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-forest-600 focus:bg-white transition"
          />
        </div>

        {/* Category Pills */}
        <div className="flex items-center gap-1.5 overflow-x-auto pb-1 sm:pb-0">
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setActiveCategory(cat.id)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold whitespace-nowrap transition ${
                activeCategory === cat.id
                  ? 'bg-forest-800 text-white shadow-sm'
                  : 'bg-slate-100 text-slate-600 hover:bg-slate-200'
              }`}
            >
              {cat.label}
            </button>
          ))}
        </div>
      </div>

      {/* Diseases Grid */}
      {loading ? (
        <div className="text-center py-20 text-xs text-slate-400">Loading disease encyclopedia...</div>
      ) : filteredDiseases.length === 0 ? (
        <div className="text-center py-16 bg-white rounded-2xl border border-slate-200 p-8">
          <Layers className="w-10 h-10 text-slate-300 mx-auto mb-2" />
          <p className="text-sm font-semibold text-slate-700">No matching diseases found</p>
          <p className="text-xs text-slate-400 mt-1">Try adjusting your search terms or filter.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredDiseases.map((disease) => {
            const isHealthy = disease.category === 'healthy';
            return (
              <div
                key={disease.id || disease.name}
                onClick={() => setSelectedDisease(disease)}
                className="bg-white rounded-2xl border border-slate-200/90 p-6 shadow-sm hover:shadow-md hover:border-forest-400 transition cursor-pointer flex flex-col justify-between group"
              >
                <div>
                  <div className="flex items-center justify-between gap-2 mb-2">
                    <span
                      className={`text-[11px] font-semibold uppercase tracking-wider px-2 py-0.5 rounded-md ${
                        isHealthy
                          ? 'bg-emerald-50 text-emerald-800 border border-emerald-200'
                          : 'bg-forest-50 text-forest-800 border border-forest-100'
                      }`}
                    >
                      {disease.category}
                    </span>
                    {disease.severity_level && disease.severity_level !== 'None' && (
                      <span className="text-[10px] font-bold text-rose-700 bg-rose-50 px-2 py-0.5 rounded border border-rose-100">
                        {disease.severity_level} Severity
                      </span>
                    )}
                  </div>

                  <h3 className="text-base font-bold text-slate-900 group-hover:text-forest-800 transition">
                    {disease.name}
                  </h3>
                  {disease.scientific_name && (
                    <p className="text-xs italic text-slate-500 font-serif mb-3">
                      {disease.scientific_name}
                    </p>
                  )}

                  <p className="text-xs text-slate-600 line-clamp-3 leading-relaxed mb-4">
                    {disease.description}
                  </p>

                  {/* Symptoms quick list */}
                  {disease.visible_symptoms && disease.visible_symptoms.length > 0 && (
                    <div className="space-y-1 mb-4 pt-3 border-t border-slate-100">
                      <span className="text-[11px] font-bold text-slate-500 uppercase tracking-wider block mb-1">
                        Typical Symptoms:
                      </span>
                      {disease.visible_symptoms.slice(0, 2).map((sym, i) => (
                        <div key={i} className="text-xs text-slate-600 flex items-start gap-1.5">
                          <span className="w-1 h-1 rounded-full bg-forest-600 mt-1.5 shrink-0" />
                          <span className="truncate">{sym}</span>
                        </div>
                      ))}
                    </div>
                  )}
                </div>

                <div className="pt-3 border-t border-slate-100 flex items-center justify-between text-xs font-semibold text-forest-700 group-hover:text-forest-900">
                  <span>View Agronomic Profile</span>
                  <ArrowRight className="w-4 h-4 group-hover:translate-x-1 transition" />
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Disease Detail Modal */}
      <DiseaseDetailModal
        disease={selectedDisease}
        onClose={() => setSelectedDisease(null)}
      />
    </div>
  );
};
