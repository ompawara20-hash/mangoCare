import React from 'react';
import { ShieldCheck, Info } from 'lucide-react';

export const Footer: React.FC = () => {
  return (
    <footer className="bg-white border-t border-slate-200 mt-auto py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2 text-slate-500 text-xs">
            <ShieldCheck className="w-4 h-4 text-forest-700" />
            <span>
              <strong>MangoCare AI</strong> — Open-source plant pathology & agricultural screening system
            </span>
          </div>

          <div className="flex items-center gap-4 text-xs text-slate-500">
            <span>Powered by ConvNeXt-Small & MobileNetV3</span>
            <span>•</span>
            <span>Local SQLite Persistence</span>
            <span>•</span>
            <span>Apache 2.0 License</span>
          </div>
        </div>

        <div className="mt-4 pt-4 border-t border-slate-100 flex items-start gap-2 text-[11px] text-slate-400 leading-relaxed">
          <Info className="w-3.5 h-3.5 text-slate-400 mt-0.5 shrink-0" />
          <p>
            <strong>Educational & Decision-Support Disclaimer:</strong> MangoCare AI is designed for preliminary agricultural
            screening and educational demonstration only. Computer vision on photographic specimens cannot guarantee laboratory-grade
            phytopathological diagnosis or detect systemic latent vascular and internal fruit rot infections. Always consult
            certified regional agricultural extension specialists before applying pesticides or chemical treatments.
          </p>
        </div>
      </div>
    </footer>
  );
};
