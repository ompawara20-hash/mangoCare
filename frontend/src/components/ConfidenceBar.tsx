import React from 'react';

interface ConfidenceBarProps {
  confidence: number;
  category?: 'high' | 'moderate' | 'low';
  showLabel?: boolean;
  className?: string;
}

export const ConfidenceBar: React.FC<ConfidenceBarProps> = ({
  confidence,
  category = 'moderate',
  showLabel = true,
  className = ''
}) => {
  const percentage = Math.min(100, Math.max(0, Math.round(confidence * 100)));

  let barColor = 'bg-emerald-600';
  let badgeColor = 'text-emerald-700 bg-emerald-50';

  if (confidence < 0.50 || category === 'low') {
    barColor = 'bg-amber-500';
    badgeColor = 'text-amber-700 bg-amber-50';
  } else if (confidence < 0.70 || category === 'moderate') {
    barColor = 'bg-emerald-500';
    badgeColor = 'text-emerald-700 bg-emerald-50';
  }

  return (
    <div className={`w-full ${className}`}>
      {showLabel && (
        <div className="flex items-center justify-between text-xs font-medium mb-1.5">
          <span className="text-slate-600">Model Confidence</span>
          <span className={`px-2 py-0.5 rounded font-semibold ${badgeColor}`}>
            {percentage}% ({category.toUpperCase()})
          </span>
        </div>
      )}
      <div className="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
        <div
          className={`h-2.5 rounded-full transition-all duration-500 ease-out ${barColor}`}
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
};
