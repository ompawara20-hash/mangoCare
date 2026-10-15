import React from 'react';
import { X, ShieldAlert, CheckCircle, AlertTriangle, BookOpen, ExternalLink, Activity } from 'lucide-react';
import { ConditionInformation } from '../types';

interface DiseaseDetailModalProps {
  disease: ConditionInformation | null;
  onClose: () => void;
}

export const DiseaseDetailModal: React.FC<DiseaseDetailModalProps> = ({ disease, onClose }) => {
  if (!disease) return null;

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in">
      <div 
        className="bg-white rounded-2xl max-w-2xl w-full max-h-[90vh] flex flex-col shadow-2xl border border-slate-200 overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Modal Header */}
        <div className="px-6 py-5 bg-slate-50 border-b border-slate-200 flex items-center justify-between">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="text-xs uppercase font-semibold tracking-wider px-2.5 py-0.5 rounded-full bg-forest-100 text-forest-800">
                {disease.category || 'Condition'}
              </span>
              {disease.severity_level && disease.severity_level !== 'None' && (
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-rose-100 text-rose-800">
                  {disease.severity_level} Severity
                </span>
              )}
            </div>
            <h2 className="text-xl font-bold text-slate-900">{disease.name}</h2>
            {disease.scientific_name && (
              <p className="text-xs italic text-slate-500 font-serif">{disease.scientific_name}</p>
            )}
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-slate-600 rounded-full hover:bg-slate-200 transition"
            title="Close"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Modal Body */}
        <div className="p-6 overflow-y-auto space-y-6 text-sm text-slate-700">
          {/* Description */}
          <div>
            <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2">Description & Etiology</h4>
            <p className="leading-relaxed text-slate-700">{disease.description}</p>
          </div>

          {/* Plant Parts & Favorable Conditions */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 bg-slate-50 p-4 rounded-xl border border-slate-200/70">
            <div>
              <span className="text-xs font-semibold text-slate-500 block mb-1">Affected Plant Parts</span>
              <span className="text-xs text-slate-800 font-medium">{disease.plant_parts_affected || 'Leaves and tender twigs'}</span>
            </div>
            {disease.favorable_conditions && (
              <div>
                <span className="text-xs font-semibold text-slate-500 block mb-1">Favorable Climate</span>
                <span className="text-xs text-slate-800 font-medium">{disease.favorable_conditions}</span>
              </div>
            )}
          </div>

          {/* Visible Symptoms */}
          {disease.visible_symptoms && disease.visible_symptoms.length > 0 && (
            <div>
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <Activity className="w-4 h-4 text-forest-600" />
                Visible Foliar Symptoms
              </h4>
              <ul className="space-y-1.5">
                {disease.visible_symptoms.map((symptom, i) => (
                  <li key={i} className="flex items-start gap-2 text-xs text-slate-700">
                    <span className="w-1.5 h-1.5 rounded-full bg-forest-600 mt-1.5 shrink-0" />
                    <span>{symptom}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}

          {/* Prevention & Cultural Management */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-5">
            {disease.prevention && disease.prevention.length > 0 && (
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <CheckCircle className="w-4 h-4 text-emerald-600" />
                  Preventative Measures
                </h4>
                <ul className="space-y-1.5 text-xs text-slate-700">
                  {disease.prevention.map((item, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-emerald-600 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {disease.management_recommendations && disease.management_recommendations.length > 0 && (
              <div>
                <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                  <ShieldAlert className="w-4 h-4 text-amber-600" />
                  Control & IPM Practice
                </h4>
                <ul className="space-y-1.5 text-xs text-slate-700">
                  {disease.management_recommendations.map((item, i) => (
                    <li key={i} className="flex items-start gap-2">
                      <span className="text-amber-600 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>

          {/* References */}
          {disease.references && disease.references.length > 0 && (
            <div className="pt-4 border-t border-slate-200">
              <h4 className="text-xs font-bold text-slate-400 uppercase tracking-wider mb-2 flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5" />
                Agricultural References & Sources
              </h4>
              <ul className="space-y-1 text-[11px] text-slate-500">
                {disease.references.map((ref, idx) => (
                  <li key={idx} className="flex items-center gap-1">
                    <span>• {ref}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>

        {/* Modal Footer */}
        <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex justify-end">
          <button
            onClick={onClose}
            className="px-4 py-2 text-xs font-semibold rounded-lg bg-forest-800 text-white hover:bg-forest-900 transition"
          >
            Close Overview
          </button>
        </div>
      </div>
    </div>
  );
};
