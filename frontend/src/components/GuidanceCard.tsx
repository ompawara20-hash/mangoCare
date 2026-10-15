import React from 'react';
import { Sun, Focus, ZoomIn, Check, AlertCircle } from 'lucide-react';

export const GuidanceCard: React.FC = () => {
  return (
    <div className="bg-white rounded-xl border border-slate-200/80 p-5 shadow-sm">
      <h3 className="text-sm font-semibold text-forest-900 mb-3 flex items-center gap-2">
        <Sun className="w-4 h-4 text-forest-600" />
        Photography Guidance for Accurate Screening
      </h3>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs text-slate-600">
        <div className="flex items-start gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
          <Check className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
          <div>
            <span className="font-semibold text-slate-800">Natural Daylight:</span> Shoot under clear, diffused outdoor light. Avoid harsh flash reflections.
          </div>
        </div>

        <div className="flex items-start gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
          <Focus className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
          <div>
            <span className="font-semibold text-slate-800">Sharp Focus:</span> Tap your camera screen on the leaf margin or spots to eliminate motion blur.
          </div>
        </div>

        <div className="flex items-start gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
          <ZoomIn className="w-4 h-4 text-emerald-600 mt-0.5 shrink-0" />
          <div>
            <span className="font-semibold text-slate-800">Frame Single Leaf:</span> Allow the affected leaf or specimen to occupy 70-80% of the viewfinder.
          </div>
        </div>

        <div className="flex items-start gap-2 bg-slate-50 p-2.5 rounded-lg border border-slate-100">
          <AlertCircle className="w-4 h-4 text-amber-600 mt-0.5 shrink-0" />
          <div>
            <span className="font-semibold text-slate-800">No Filters:</span> Upload unaltered photographs without beautification filters or artificial color shifts.
          </div>
        </div>
      </div>

      <div className="mt-3 pt-3 border-t border-slate-100 text-[11px] text-slate-500 flex items-center justify-between">
        <span>Supported Formats: JPG, PNG, WebP (Max 10 MB)</span>
        <span className="italic">Screening target: Mango Foliage</span>
      </div>
    </div>
  );
};
