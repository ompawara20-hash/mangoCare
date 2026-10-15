import React, { useState, useEffect } from 'react';
import {
  Cpu,
  Layers,
  ShieldCheck,
  CheckCircle2,
  AlertTriangle,
  Info,
  ExternalLink,
  Sliders,
  Database,
  Eye
} from 'lucide-react';
import { api } from '../api/client';
import { ModelInfo, HealthStatus } from '../types';

export const AboutModelPage: React.FC = () => {
  const [modelInfo, setModelInfo] = useState<ModelInfo | null>(null);
  const [health, setHealth] = useState<HealthStatus | null>(null);

  useEffect(() => {
    api.getModelInfo().then(setModelInfo).catch(console.error);
    api.getHealth().then(setHealth).catch(console.error);
  }, []);

  return (
    <div className="max-w-5xl mx-auto space-y-8 animate-fade-in pb-16">
      {/* Page Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-50 border border-forest-200/60 text-xs font-semibold text-forest-800 mb-2">
          <Cpu className="w-3.5 h-3.5" />
          <span>Model Architecture & Provenance</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          About MangoCare AI Vision Models
        </h1>
        <p className="text-sm text-slate-500 mt-1 max-w-3xl">
          Complete transparent documentation of network architectures, training datasets, screening pipelines,
          and technical constraints.
        </p>
      </div>

      {/* Live Health Status Card */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 shadow-sm">
        <h3 className="text-sm font-bold text-slate-900 mb-4 flex items-center gap-2">
          <ShieldCheck className="w-4 h-4 text-emerald-600" />
          Current Operational Runtime Status
        </h3>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 text-xs">
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-slate-400 block mb-1">Inference Device</span>
            <span className="font-bold text-slate-800 uppercase">{health?.device || 'CPU'}</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-slate-400 block mb-1">Disease Model</span>
            <span className="font-bold text-emerald-700 flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              {health?.disease_model_ready ? 'Loaded & Active' : 'Offline'}
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-slate-400 block mb-1">Specimen Validator</span>
            <span className="font-bold text-emerald-700 flex items-center gap-1">
              <span className="w-2 h-2 rounded-full bg-emerald-500" />
              {health?.validator_model_ready ? 'MobileNetV3 Ready' : 'Spectral Only'}
            </span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-100">
            <span className="text-slate-400 block mb-1">Operating Mode</span>
            <span className="font-bold text-forest-800 capitalize">
              {health?.operating_mode?.replace('_', ' ') || 'Full Inference'}
            </span>
          </div>
        </div>
      </div>

      {/* Model Architecture Deep Dive */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Primary ConvNeXt Classifier Card */}
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-forest-700 bg-forest-50 px-2.5 py-0.5 rounded-md border border-forest-100">
              Primary Classifier
            </span>
            <span className="text-xs font-bold text-slate-500">49.5M Parameters</span>
          </div>

          <h3 className="text-lg font-bold text-slate-900">
            ConvNeXt-Small (<code className="text-xs text-forest-700">convnext_small</code>)
          </h3>

          <p className="text-xs text-slate-600 leading-relaxed">
            ConvNeXt modernizes standard convolutional architectures with inverted bottlenecks, larger $7 \times 7$ kernels,
            GELU activations, and LayerNorm. This fine-tuned checkpoint achieves competitive accuracy against Vision Transformers
            while maintaining lower latency for edge and CPU inference.
          </p>

          <div className="space-y-2 pt-2 border-t border-slate-100 text-xs">
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Repository:</span>
              <a
                href="https://huggingface.co/ixrbhii/mango-disease-convnext"
                target="_blank"
                rel="noreferrer"
                className="font-mono text-forest-700 font-semibold hover:underline flex items-center gap-1"
              >
                ixrbhii/mango-disease-convnext <ExternalLink className="w-3 h-3" />
              </a>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">License:</span>
              <span className="font-semibold text-slate-800">Apache 2.0 (Open Source)</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Benchmark Accuracy:</span>
              <span className="font-semibold text-emerald-700">96.4% on MangoLeafBD test split</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-500">Target Specimen:</span>
              <span className="font-semibold text-slate-800">Mango Leaves & Foliar Tissues</span>
            </div>
          </div>
        </div>

        {/* Validation Screener Card */}
        <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-7 shadow-sm space-y-4">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-700 bg-emerald-50 px-2.5 py-0.5 rounded-md border border-emerald-100">
              Specimen Screener
            </span>
            <span className="text-xs font-bold text-slate-500">2.5M Parameters</span>
          </div>

          <h3 className="text-lg font-bold text-slate-900">
            MobileNetV3-Small & Foliage Spectral Filter
          </h3>

          <p className="text-xs text-slate-600 leading-relaxed">
            To prevent false diagnostic predictions when users upload non-plant photos, a dual-layer validation
            pipeline inspects the upload before disease inference. It checks chlorophyll RGB spectral distributions
            and screens against 1,000 ImageNet categories to reject vehicles, people, indoor items, and documents.
          </p>

          <div className="space-y-2 pt-2 border-t border-slate-100 text-xs">
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Validation Pipeline:</span>
              <span className="font-semibold text-slate-800">Spectral Variance + MobileNetV3</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Weight Source:</span>
              <span className="font-semibold text-slate-800">PyTorch Torchvision Official</span>
            </div>
            <div className="flex justify-between py-1 border-b border-slate-50">
              <span className="text-slate-500">Rejection Response:</span>
              <span className="font-mono text-xs text-amber-700 font-semibold">MANGO_NOT_DETECTED</span>
            </div>
            <div className="flex justify-between py-1">
              <span className="text-slate-500">Model Footprint:</span>
              <span className="font-semibold text-slate-800">~9.8 MB on disk</span>
            </div>
          </div>
        </div>
      </div>

      {/* Preprocessing Specifications */}
      <div className="bg-white rounded-3xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-4">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Sliders className="w-4 h-4 text-forest-700" />
          Image Preprocessing & Tensor Pipeline
        </h3>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
            <span className="text-slate-400 font-medium">1. Spatial Transform</span>
            <p className="font-bold text-slate-800">224 × 224 pixels</p>
            <p className="text-[11px] text-slate-500">Bilinear interpolation with EXIF auto-orientation</p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
            <span className="text-slate-400 font-medium">2. Color Normalization</span>
            <p className="font-bold text-slate-800">ImageNet Mean & Std</p>
            <p className="text-[11px] text-slate-500">
              Mean: [0.485, 0.456, 0.406]<br />
              Std: [0.229, 0.224, 0.225]
            </p>
          </div>

          <div className="p-4 rounded-2xl bg-slate-50 border border-slate-100 space-y-1">
            <span className="text-slate-400 font-medium">3. Inference Mode</span>
            <p className="font-bold text-slate-800">torch.inference_mode()</p>
            <p className="text-[11px] text-slate-500">Evaluation mode with zero gradient retention for low memory</p>
          </div>
        </div>
      </div>

      {/* Limitations & Ethical Disclaimer */}
      <div className="bg-amber-50/60 rounded-3xl border border-amber-200 p-6 sm:p-7 space-y-3 text-xs text-amber-950">
        <div className="flex items-center gap-2 font-bold text-amber-900 text-sm">
          <AlertTriangle className="w-4 h-4 text-amber-600" />
          <span>Critical Scientific & Agronomic Limitations</span>
        </div>
        <ul className="space-y-1.5 list-disc list-inside leading-relaxed text-slate-700">
          <li>
            <strong>Foliar vs Fruit Distinction:</strong> The primary model is trained on <em>mango leaves</em>. Foliar diseases
            (like leaf anthracnose) correlate with tree infection pressure, but a foliar model must not be advertised as a validated
            postharvest fruit rot detector.
          </li>
          <li>
            <strong>Domain Shift:</strong> Lighting differences, shadow angles, dust residues, and camera sensor variations can
            affect model certainty.
          </li>
          <li>
            <strong>Internal Pathologies:</strong> Visual surface classification cannot diagnose vascular wilts inside the trunk,
            root infections, or latent sub-surface mycelia.
          </li>
          <li>
            <strong>Preliminary Screening:</strong> MangoCare AI is an educational tool. Always confirm with certified agricultural
            extension agents before purchasing or applying commercial fungicides.
          </li>
        </ul>
      </div>
    </div>
  );
};
