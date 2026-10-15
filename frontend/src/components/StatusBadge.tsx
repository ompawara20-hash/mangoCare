import React from 'react';
import { CheckCircle2, AlertTriangle, AlertCircle, HelpCircle, XCircle } from 'lucide-react';

interface StatusBadgeProps {
  status: string;
  className?: string;
  showIcon?: boolean;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status, className = '', showIcon = true }) => {
  switch (status) {
    case 'healthy_appearance_detected':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-50 text-emerald-800 border border-emerald-200 ${className}`}>
          {showIcon && <CheckCircle2 className="w-3.5 h-3.5 text-emerald-600" />}
          Healthy Appearance
        </span>
      );
    case 'suspected_disease':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-50 text-rose-800 border border-rose-200 ${className}`}>
          {showIcon && <AlertTriangle className="w-3.5 h-3.5 text-rose-600" />}
          Suspected Disease
        </span>
      );
    case 'uncertain_result':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-amber-50 text-amber-800 border border-amber-200 ${className}`}>
          {showIcon && <HelpCircle className="w-3.5 h-3.5 text-amber-600" />}
          Uncertain Result
        </span>
      );
    case 'inconclusive':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-slate-100 text-slate-700 border border-slate-300 ${className}`}>
          {showIcon && <AlertCircle className="w-3.5 h-3.5 text-slate-500" />}
          Inconclusive
        </span>
      );
    case 'invalid_image':
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-gray-100 text-gray-700 border border-gray-300 ${className}`}>
          {showIcon && <XCircle className="w-3.5 h-3.5 text-gray-500" />}
          Invalid Image
        </span>
      );
    default:
      return (
        <span className={`inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-medium bg-slate-50 text-slate-700 border border-slate-200 ${className}`}>
          {status}
        </span>
      );
  }
};
