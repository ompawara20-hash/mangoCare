import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Loader2, Sparkles, AlertCircle, ArrowRight } from 'lucide-react';
import { ImageDropzone } from '../components/ImageDropzone';
import { GuidanceCard } from '../components/GuidanceCard';
import { api } from '../api/client';
import { AnalysisResult } from '../types';

interface AnalyzePageProps {
  onAnalysisComplete?: (result: AnalysisResult, previewUrl: string) => void;
}

export const AnalyzePage: React.FC<AnalyzePageProps> = ({ onAnalysisComplete }) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [previewUrl, setPreviewUrl] = useState<string | null>(null);
  const [dimensions, setDimensions] = useState<{ width: number; height: number } | null>(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisStep, setAnalysisStep] = useState<string>('');
  const [serverError, setServerError] = useState<string | null>(null);
  const navigate = useNavigate();

  const handleFileSelect = (file: File) => {
    setSelectedFile(file);
    setServerError(null);
    const url = URL.createObjectURL(file);
    setPreviewUrl(url);

    // Read image dimensions
    const img = new Image();
    img.onload = () => {
      setDimensions({ width: img.naturalWidth, height: img.naturalHeight });
    };
    img.src = url;
  };

  const handleClear = () => {
    setSelectedFile(null);
    if (previewUrl) {
      URL.revokeObjectURL(previewUrl);
    }
    setPreviewUrl(null);
    setDimensions(null);
    setServerError(null);
  };

  const handleSubmit = async () => {
    if (!selectedFile) return;

    setIsAnalyzing(true);
    setServerError(null);

    // Progressive status messages
    setAnalysisStep('Verifying image integrity & color spectrum...');
    const t1 = setTimeout(() => {
      setAnalysisStep('Running MobileNetV3 specimen validation...');
    }, 400);

    const t2 = setTimeout(() => {
      setAnalysisStep('Evaluating foliar pathology with ConvNeXt-Small...');
    }, 900);

    const t3 = setTimeout(() => {
      setAnalysisStep('Compiling diagnostic assessment & health report...');
    }, 1400);

    try {
      const result = await api.analyzeImage(selectedFile);
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);

      if (onAnalysisComplete && previewUrl) {
        onAnalysisComplete(result, previewUrl);
      }

      // Store in sessionStorage for results page retrieval
      sessionStorage.setItem('latest_analysis', JSON.stringify(result));
      if (previewUrl) {
        sessionStorage.setItem('latest_preview', previewUrl);
      }

      navigate('/results');
    } catch (err: any) {
      clearTimeout(t1);
      clearTimeout(t2);
      clearTimeout(t3);

      const errorDetail = err.response?.data?.detail;
      if (errorDetail && errorDetail.message) {
        setServerError(errorDetail.message);
      } else {
        setServerError('An unexpected error occurred during analysis. Please ensure the backend is running and try again.');
      }
    } finally {
      setIsAnalyzing(false);
      setAnalysisStep('');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
      {/* Title Header */}
      <div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Analyze Mango Specimen
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Upload a clear photograph of a mango leaf to detect foliar diseases and receive agronomic guidance.
        </p>
      </div>

      {/* Main Analysis Form Card */}
      <div className="space-y-6">
        <ImageDropzone
          onFileSelect={handleFileSelect}
          selectedFile={selectedFile}
          onClear={handleClear}
          previewUrl={previewUrl}
          imageDimensions={dimensions}
          disabled={isAnalyzing}
        />

        {/* Server Error Alert */}
        {serverError && (
          <div className="p-4 rounded-xl bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-start gap-3">
            <AlertCircle className="w-4 h-4 text-rose-600 mt-0.5 shrink-0" />
            <div>
              <p className="font-semibold text-rose-900">Analysis Submission Error</p>
              <p className="mt-0.5">{serverError}</p>
            </div>
          </div>
        )}

        {/* Action Button */}
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4 pt-2">
          <div className="text-xs text-slate-500">
            {isAnalyzing ? (
              <span className="flex items-center gap-2 text-forest-700 font-medium">
                <Loader2 className="w-3.5 h-3.5 animate-spin" />
                {analysisStep || 'Analyzing specimen...'}
              </span>
            ) : (
              <span>Automated inference runs locally on CPU/GPU</span>
            )}
          </div>

          <button
            type="button"
            onClick={handleSubmit}
            disabled={!selectedFile || isAnalyzing}
            className={`w-full sm:w-auto inline-flex items-center justify-center gap-2 px-8 py-3.5 rounded-xl font-bold text-sm shadow-md transition active:scale-95 ${
              !selectedFile || isAnalyzing
                ? 'bg-slate-200 text-slate-400 cursor-not-allowed shadow-none'
                : 'bg-forest-800 hover:bg-forest-900 text-white shadow-forest-950/20'
            }`}
          >
            {isAnalyzing ? (
              <>
                <Loader2 className="w-4 h-4 animate-spin text-white" />
                <span>Running Screening...</span>
              </>
            ) : (
              <>
                <Sparkles className="w-4 h-4 text-emerald-400" />
                <span>Run Diagnostic Analysis</span>
                <ArrowRight className="w-4 h-4 ml-1" />
              </>
            )}
          </button>
        </div>
      </div>

      {/* Photography Best Practices Card */}
      <GuidanceCard />
    </div>
  );
};
