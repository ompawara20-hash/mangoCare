import React, { useState, useRef, DragEvent, ChangeEvent } from 'react';
import { UploadCloud, Image as ImageIcon, X, AlertCircle } from 'lucide-react';

interface ImageDropzoneProps {
  onFileSelect: (file: File) => void;
  selectedFile: File | null;
  onClear: () => void;
  previewUrl: string | null;
  imageDimensions: { width: number; height: number } | null;
  disabled?: boolean;
}

const MAX_SIZE_MB = 10;
const ALLOWED_TYPES = ['image/jpeg', 'image/png', 'image/webp'];

export const ImageDropzone: React.FC<ImageDropzoneProps> = ({
  onFileSelect,
  selectedFile,
  onClear,
  previewUrl,
  imageDimensions,
  disabled = false
}) => {
  const [isDragOver, setIsDragOver] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const validateAndHandleFile = (file: File) => {
    setErrorMessage(null);

    if (!ALLOWED_TYPES.includes(file.type)) {
      setErrorMessage(`Unsupported file format (${file.type || 'unknown'}). Please upload a JPEG, PNG, or WebP.`);
      return;
    }

    if (file.size > MAX_SIZE_MB * 1024 * 1024) {
      setErrorMessage(`File is too large (${(file.size / (1024 * 1024)).toFixed(1)} MB). Maximum limit is ${MAX_SIZE_MB} MB.`);
      return;
    }

    onFileSelect(file);
  };

  const handleDragOver = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    if (!disabled) setIsDragOver(true);
  };

  const handleDragLeave = () => {
    setIsDragOver(false);
  };

  const handleDrop = (e: DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragOver(false);
    if (disabled) return;

    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      validateAndHandleFile(e.dataTransfer.files[0]);
    }
  };

  const handleInputChange = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      validateAndHandleFile(e.target.files[0]);
    }
  };

  const formatFileSize = (bytes: number): string => {
    if (bytes < 1024) return `${bytes} B`;
    if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
    return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  };

  return (
    <div className="w-full">
      <input
        type="file"
        ref={fileInputRef}
        onChange={handleInputChange}
        accept="image/jpeg,image/png,image/webp"
        className="hidden"
        disabled={disabled}
      />

      {!selectedFile || !previewUrl ? (
        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => !disabled && fileInputRef.current?.click()}
          className={`border-2 border-dashed rounded-2xl p-8 text-center cursor-pointer transition-all duration-200 ${
            isDragOver
              ? 'border-forest-600 bg-forest-50/70 scale-[1.01]'
              : 'border-slate-300 hover:border-forest-500 hover:bg-forest-50/30 bg-white'
          } ${disabled ? 'opacity-60 cursor-not-allowed' : ''}`}
        >
          <div className="w-14 h-14 mx-auto mb-4 rounded-full bg-forest-50 text-forest-700 flex items-center justify-center border border-forest-100 shadow-sm">
            <UploadCloud className="w-7 h-7" />
          </div>

          <h4 className="text-base font-semibold text-slate-800 mb-1">
            Drag and drop your mango leaf photo
          </h4>
          <p className="text-sm text-slate-500 mb-4">
            or <span className="text-forest-700 font-semibold underline underline-offset-2">browse files</span> from your computer
          </p>

          <div className="inline-flex items-center gap-2 px-3 py-1 bg-slate-100 rounded-full text-xs text-slate-600">
            <span>JPEG, PNG, WebP</span>
            <span>•</span>
            <span>Up to 10 MB</span>
          </div>
        </div>
      ) : (
        <div className="bg-white rounded-2xl border border-slate-200 p-5 shadow-sm">
          <div className="flex flex-col sm:flex-row items-center gap-5">
            {/* Image Preview Box */}
            <div className="relative w-44 h-44 rounded-xl overflow-hidden bg-slate-100 border border-slate-200 shrink-0 flex items-center justify-center group">
              <img
                src={previewUrl}
                alt="Mango Specimen Preview"
                className="w-full h-full object-cover"
              />
              <button
                type="button"
                onClick={onClear}
                disabled={disabled}
                className="absolute top-2 right-2 p-1.5 rounded-full bg-slate-900/70 text-white hover:bg-rose-600 transition shadow"
                title="Remove image"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            {/* Specimen Details */}
            <div className="flex-1 w-full text-left">
              <div className="flex items-center justify-between gap-2 mb-2">
                <span className="text-xs font-semibold uppercase tracking-wider text-forest-700 bg-forest-50 px-2.5 py-0.5 rounded-md border border-forest-100">
                  Ready for Analysis
                </span>
                <button
                  type="button"
                  onClick={() => fileInputRef.current?.click()}
                  disabled={disabled}
                  className="text-xs text-forest-700 font-medium hover:underline"
                >
                  Change Photo
                </button>
              </div>

              <h4 className="text-sm font-semibold text-slate-800 truncate mb-1" title={selectedFile.name}>
                {selectedFile.name}
              </h4>

              <div className="grid grid-cols-2 gap-2 text-xs text-slate-500 mt-3 pt-3 border-t border-slate-100">
                <div>
                  <span className="text-slate-400">File Size:</span>{' '}
                  <span className="font-medium text-slate-700">{formatFileSize(selectedFile.size)}</span>
                </div>
                <div>
                  <span className="text-slate-400">Dimensions:</span>{' '}
                  <span className="font-medium text-slate-700">
                    {imageDimensions ? `${imageDimensions.width} × ${imageDimensions.height} px` : 'Detecting...'}
                  </span>
                </div>
                <div>
                  <span className="text-slate-400">Type:</span>{' '}
                  <span className="font-medium text-slate-700">{selectedFile.type.replace('image/', '').toUpperCase()}</span>
                </div>
                <div>
                  <span className="text-slate-400">Target Specimen:</span>{' '}
                  <span className="font-medium text-forest-700">Mango Foliage</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {errorMessage && (
        <div className="mt-3 p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-800 text-xs flex items-center gap-2">
          <AlertCircle className="w-4 h-4 text-rose-600 shrink-0" />
          <span>{errorMessage}</span>
        </div>
      )}
    </div>
  );
};
