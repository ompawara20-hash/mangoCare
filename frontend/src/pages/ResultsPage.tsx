import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Download,
  RotateCcw,
  AlertTriangle,
  CheckCircle2,
  HelpCircle,
  XCircle,
  FileText,
  Activity,
  Layers,
  Info,
  Calendar,
  Sparkles,
  ShieldAlert
} from 'lucide-react';
import { AnalysisResult } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { ConfidenceBar } from '../components/ConfidenceBar';
import { api } from '../api/client';
import { DiseaseDetailModal } from '../components/DiseaseDetailModal';

export const ResultsPage: React.FC = () => {
  const [result, setResult] = useState<AnalysisResult | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [modalOpen, setModalOpen] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    const storedResult = sessionStorage.getItem('latest_analysis');
    const storedPreview = sessionStorage.getItem('latest_preview');

    if (storedResult) {
      try {
        setResult(JSON.parse(storedResult));
      } catch (e) {
        console.error('Error parsing stored analysis:', e);
      }
    }
    if (storedPreview) {
      setPreviewUrl(storedPreview);
    }
  }, []);

  if (!result) {
    return (
      <div className="max-w-md mx-auto text-center py-16 bg-white rounded-3xl border border-slate-200 p-8 shadow-sm">
        <FileText className="w-12 h-12 text-slate-300 mx-auto mb-3" />
        <h3 className="text-base font-bold text-slate-800 mb-1">No Active Analysis Found</h3>
        <p className="text-xs text-slate-500 mb-6">
          Please upload a mango leaf photo to generate an automated assessment.
        </p>
        <Link
          to="/analyze"
          className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl bg-forest-800 text-white font-semibold text-xs hover:bg-forest-900 transition"
        >
          Go to Upload Page
        </Link>
      </div>
    );
  }

  // Handle Invalid Non-Mango Image State Cleanly
  if (!result.success || result.status === 'invalid_image') {
    return (
      <div className="max-w-2xl mx-auto space-y-6 animate-fade-in pb-12">
        <div className="bg-white rounded-3xl border border-slate-200 p-8 shadow-sm text-center">
          <div className="w-14 h-14 mx-auto mb-4 rounded-2xl bg-amber-50 text-amber-600 border border-amber-200 flex items-center justify-center">
            <XCircle className="w-8 h-8" />
          </div>

          <h2 className="text-2xl font-extrabold text-slate-900 mb-2">
            Unable to Analyze This Image
          </h2>
          <p className="text-sm text-slate-600 max-w-lg mx-auto mb-6">
            {result.message || 'The image validation system could not identify a plausible mango plant specimen in this upload.'}
          </p>

          {previewUrl && (
            <div className="max-w-xs mx-auto mb-6 rounded-2xl overflow-hidden border border-slate-200 shadow-sm bg-slate-50">
              <img src={previewUrl} alt="Rejected upload preview" className="w-full h-48 object-cover" />
              <div className="p-2 text-[11px] text-slate-500 bg-slate-100 border-t border-slate-200">
                Uploaded image failed mango verification criteria
              </div>
            </div>
          )}

          <div className="bg-slate-50 border border-slate-200 rounded-xl p-4 text-xs text-slate-600 text-left max-w-md mx-auto mb-6">
            <h5 className="font-bold text-slate-800 mb-1.5 flex items-center gap-1.5">
              <Info className="w-3.5 h-3.5 text-forest-700" />
              What was detected?
            </h5>
            <p className="leading-relaxed">
              {result.suggestion || 'Please provide a clear photograph of a mango leaf or fruit in natural daylight. Avoid documents, non-plant objects, or extreme digital filters.'}
            </p>
          </div>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-3">
            <Link
              to="/analyze"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-6 py-3 rounded-xl bg-forest-800 text-white font-bold text-xs hover:bg-forest-900 transition shadow"
            >
              <RotateCcw className="w-4 h-4" />
              Upload a Valid Mango Specimen
            </Link>
            <Link
              to="/library"
              className="w-full sm:w-auto inline-flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-slate-100 text-slate-700 font-semibold text-xs hover:bg-slate-200 transition"
            >
              Browse Disease Guide
            </Link>
          </div>
        </div>
      </div>
    );
  }

  // Valid Analysis Result View
  const pred = result.prediction;
  const cond = result.condition_information;
  const isHealthy = result.status === 'healthy_appearance_detected';
  const isInconclusive = result.status === 'inconclusive' || result.status === 'uncertain_result';

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in pb-16">
      {/* Top Banner Actions */}
      <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pb-4 border-b border-slate-200">
        <div>
          <div className="flex items-center gap-2.5 mb-1">
            <StatusBadge status={result.status} />
            {result.analysis_id && (
              <span className="text-xs text-slate-400 font-mono">
                ID: {result.analysis_id.slice(0, 8)}...
              </span>
            )}
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
            Foliar Health Assessment Report
          </h1>
        </div>

        <div className="flex items-center gap-3 w-full sm:w-auto">
          {result.analysis_id && (
            <a
              href={api.getReportDownloadUrl(result.analysis_id)}
              target="_blank"
              rel="noreferrer"
              className="inline-flex items-center justify-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-bold text-xs shadow-md transition"
            >
              <Download className="w-4 h-4" />
              Download PDF Report
            </a>
          )}
          <Link
            to="/analyze"
            className="inline-flex items-center justify-center gap-1.5 px-4 py-2.5 rounded-xl bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 font-semibold text-xs transition"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            Analyze Another
          </Link>
        </div>
      </div>

      {/* Primary Diagnosis Card */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Photograph Thumbnail */}
          <div className="space-y-3">
            <div className="rounded-2xl overflow-hidden bg-slate-100 border border-slate-200 shadow-inner h-60 flex items-center justify-center">
              {previewUrl ? (
                <img
                  src={previewUrl}
                  alt="Analyzed Specimen"
                  className="w-full h-full object-cover"
                />
              ) : (
                <div className="text-center p-4 text-slate-400 text-xs">
                  Specimen Image Processed
                </div>
              )}
            </div>

            {result.image_metadata && (
              <div className="bg-slate-50 p-3 rounded-xl border border-slate-100 text-[11px] text-slate-500 space-y-1">
                <div className="flex justify-between">
                  <span>Resolution:</span>
                  <span className="font-medium text-slate-700">
                    {result.image_metadata.width} × {result.image_metadata.height} px
                  </span>
                </div>
                <div className="flex justify-between">
                  <span>Format:</span>
                  <span className="font-medium text-slate-700">{result.image_metadata.format}</span>
                </div>
                <div className="flex justify-between">
                  <span>Target Tissue:</span>
                  <span className="font-medium text-forest-700">Mango Foliage</span>
                </div>
              </div>
            )}
          </div>

          {/* Diagnosis & Confidence Column */}
          <div className="md:col-span-2 space-y-5">
            <div>
              <span className="text-xs uppercase font-bold tracking-wider text-forest-700 bg-forest-50 px-2.5 py-0.5 rounded-md border border-forest-100">
                Primary Classification
              </span>
              <h2 className="text-2xl sm:text-3xl font-extrabold text-slate-900 mt-2">
                {pred ? pred.class_name : 'Condition Detected'}
              </h2>
              {cond?.scientific_name && (
                <p className="text-sm italic text-slate-500 font-serif mt-0.5">
                  {cond.scientific_name}
                </p>
              )}
            </div>

            {/* Confidence Meter */}
            {pred && (
              <div className="bg-slate-50 p-4 rounded-2xl border border-slate-200/80 space-y-2">
                <ConfidenceBar
                  confidence={pred.confidence}
                  category={pred.confidence_category}
                  showLabel={true}
                />
                <p className="text-xs text-slate-600 leading-relaxed pt-1">
                  {pred.confidence_interpretation}
                </p>
              </div>
            )}

            {/* Uncertainty Warning Box if applicable */}
            {pred?.uncertainty_flag && (
              <div className="p-3.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-900 text-xs flex items-start gap-2.5">
                <ShieldAlert className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-semibold">Elevated Model Uncertainty:</span> The model observed visual ambiguity
                  among candidate classes. Re-photographing the specimen or in-person agronomist inspection is advised.
                </div>
              </div>
            )}

            {/* Candidate Alternatives */}
            {result.alternatives && result.alternatives.length > 0 && (
              <div className="space-y-2 pt-2 border-t border-slate-100">
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                  Alternative Candidate Probabilities
                </h4>
                <div className="grid grid-cols-1 sm:grid-cols-3 gap-2">
                  {result.alternatives.map((alt, i) => (
                    <div
                      key={i}
                      className="p-2.5 rounded-xl bg-white border border-slate-200 text-xs flex flex-col justify-between"
                    >
                      <span className="font-medium text-slate-700 truncate">{alt.class_name}</span>
                      <span className="text-xs font-bold text-forest-700 mt-1">
                        {(alt.confidence * 100).toFixed(1)}%
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* Disease Knowledge & Recommended Actions */}
      {cond && (
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Visible Symptoms Card */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <Activity className="w-4 h-4 text-forest-700" />
              Documented Visible Symptoms
            </h3>
            <p className="text-xs text-slate-600 leading-relaxed">
              {cond.description}
            </p>

            {cond.visible_symptoms && cond.visible_symptoms.length > 0 && (
              <ul className="space-y-2 pt-2">
                {cond.visible_symptoms.map((symptom, idx) => (
                  <li key={idx} className="flex items-start gap-2.5 text-xs text-slate-700">
                    <span className="w-1.5 h-1.5 rounded-full bg-forest-600 mt-1.5 shrink-0" />
                    <span>{symptom}</span>
                  </li>
                ))}
              </ul>
            )}

            <button
              onClick={() => setModalOpen(true)}
              className="text-xs font-semibold text-forest-700 hover:text-forest-900 hover:underline pt-2 inline-flex items-center gap-1"
            >
              Read Full Agronomic Profile & References →
            </button>
          </div>

          {/* Precautions & Integrated Management Card */}
          <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-sm space-y-4">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-600" />
              Recommended Agronomic Actions
            </h3>

            {cond.prevention && cond.prevention.length > 0 && (
              <div>
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                  Prevention & Canopy Sanitation
                </h4>
                <ul className="space-y-2 text-xs text-slate-700">
                  {cond.prevention.slice(0, 3).map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-emerald-600 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {cond.management_recommendations && cond.management_recommendations.length > 0 && (
              <div className="pt-2 border-t border-slate-100">
                <h4 className="text-xs font-bold text-slate-500 uppercase tracking-wider mb-2">
                  Integrated Management (IPM)
                </h4>
                <ul className="space-y-2 text-xs text-slate-700">
                  {cond.management_recommendations.slice(0, 3).map((item, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-amber-600 font-bold">•</span>
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Model Provenance & Limitations Disclaimer */}
      <div className="bg-slate-50 rounded-2xl border border-slate-200 p-5 text-xs text-slate-500 space-y-2">
        <div className="flex items-center gap-2 font-semibold text-slate-700">
          <Info className="w-4 h-4 text-forest-700" />
          <span>Screening Model Specifications & Constraints</span>
        </div>
        <p className="leading-relaxed">
          Analyzed with <strong>ConvNeXt-Small</strong> (fine-tuned on the MangoLeafBD foliar benchmark).
          This automated classification serves as an educational decision-support indicator.
          Visual leaf inspection cannot diagnose internal fruit rots, postharvest bacterial decay, or root pathogens.
          Consult certified agricultural extension officers before applying fungicides or restricted agrochemicals.
        </p>
      </div>

      {/* Slide-over / Modal for complete details */}
      <DiseaseDetailModal
        disease={cond || null}
        onClose={() => setModalOpen(false)}
      />
    </div>
  );
};
