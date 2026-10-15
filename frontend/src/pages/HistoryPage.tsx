import React, { useState, useEffect } from 'react';
import {
  History,
  Search,
  Filter,
  Download,
  Trash2,
  FileText,
  ChevronLeft,
  ChevronRight,
  AlertCircle
} from 'lucide-react';
import { api } from '../api/client';
import { HistoryItem, PaginationInfo } from '../types';
import { StatusBadge } from '../components/StatusBadge';

export const HistoryPage: React.FC = () => {
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [pagination, setPagination] = useState<PaginationInfo>({
    page: 1,
    page_size: 10,
    total_items: 0,
    total_pages: 1,
    has_next: false,
    has_prev: false,
  });
  const [statusFilter, setStatusFilter] = useState<string>('all');
  const [searchQuery, setSearchQuery] = useState<string>('');
  const [loading, setLoading] = useState(true);
  const [deleteConfirmId, setDeleteConfirmId] = useState<string | null>(null);

  const fetchHistory = (page: number = 1) => {
    setLoading(true);
    api.getHistory(page, 10, statusFilter, searchQuery)
      .then((res) => {
        setItems(res.items);
        setPagination(res.pagination);
      })
      .catch((err) => console.error('Error fetching history:', err))
      .finally(() => setLoading(false));
  };

  useEffect(() => {
    fetchHistory(1);
  }, [statusFilter, searchQuery]);

  const handleDelete = async (id: string) => {
    try {
      await api.deleteAnalysis(id);
      setDeleteConfirmId(null);
      fetchHistory(pagination.page);
    } catch (e) {
      console.error('Failed to delete analysis record:', e);
    }
  };

  return (
    <div className="max-w-7xl mx-auto space-y-8 animate-fade-in pb-16">
      {/* Page Header */}
      <div>
        <div className="inline-flex items-center gap-1.5 px-3 py-1 rounded-full bg-forest-50 border border-forest-200/60 text-xs font-semibold text-forest-800 mb-2">
          <History className="w-3.5 h-3.5" />
          <span>Local SQLite Records</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-extrabold text-slate-900 tracking-tight">
          Analysis History & Reports
        </h1>
        <p className="text-sm text-slate-500 mt-1">
          Review, filter, and download PDF assessment records from previous mango diagnostic screenings.
        </p>
      </div>

      {/* Filter and Search Bar */}
      <div className="bg-white p-4 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-4">
        {/* Search Input */}
        <div className="relative flex-1">
          <Search className="w-4 h-4 text-slate-400 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            placeholder="Search by disease name or symptoms..."
            className="w-full pl-10 pr-4 py-2 text-xs rounded-xl bg-slate-50 border border-slate-200 focus:outline-none focus:ring-2 focus:ring-forest-600 focus:bg-white transition"
          />
        </div>

        {/* Status Dropdown Filter */}
        <div className="flex items-center gap-2 shrink-0">
          <Filter className="w-4 h-4 text-slate-400" />
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="text-xs font-semibold rounded-xl bg-slate-50 border border-slate-200 px-3 py-2 text-slate-700 focus:outline-none focus:ring-2 focus:ring-forest-600 cursor-pointer"
          >
            <option value="all">All Diagnostic Statuses</option>
            <option value="healthy_appearance_detected">Healthy Appearance</option>
            <option value="suspected_disease">Suspected Disease</option>
            <option value="uncertain_result">Uncertain Result</option>
            <option value="inconclusive">Inconclusive</option>
          </select>
        </div>
      </div>

      {/* Records Table Card */}
      <div className="bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden">
        {loading ? (
          <div className="py-20 text-center text-xs text-slate-400">Loading historical records...</div>
        ) : items.length === 0 ? (
          <div className="py-16 text-center">
            <FileText className="w-10 h-10 text-slate-300 mx-auto mb-2" />
            <h4 className="text-sm font-bold text-slate-700">No analysis records found</h4>
            <p className="text-xs text-slate-400 mt-1">
              {searchQuery || statusFilter !== 'all'
                ? 'Try clearing your filters or search keywords.'
                : 'Upload an image on the Analyze page to create your first record.'}
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-500 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="px-6 py-3.5">Analysis ID / Date</th>
                  <th className="px-6 py-3.5">Predicted Condition</th>
                  <th className="px-6 py-3.5">Status</th>
                  <th className="px-6 py-3.5">Confidence</th>
                  <th className="px-6 py-3.5 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100">
                {items.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/60 transition">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="font-mono text-slate-800 font-semibold text-[11px]">
                        {item.id.slice(0, 13)}...
                      </div>
                      <div className="text-[11px] text-slate-400 mt-0.5">
                        {new Date(item.created_at).toLocaleString()}
                      </div>
                    </td>

                    <td className="px-6 py-4">
                      <div className="font-semibold text-slate-900">
                        {item.predicted_class_name || 'N/A'}
                      </div>
                      <div className="text-[11px] text-slate-500 line-clamp-1 max-w-xs mt-0.5">
                        {item.symptoms_summary || item.model_name}
                      </div>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <StatusBadge status={item.status} className="scale-95 origin-left" />
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className="font-bold text-slate-800">
                        {(item.confidence * 100).toFixed(1)}%
                      </span>
                      <span className="text-[10px] text-slate-400 uppercase ml-1">
                        ({item.confidence_category})
                      </span>
                    </td>

                    <td className="px-6 py-4 whitespace-nowrap text-right space-x-2">
                      {item.report_filename && (
                        <a
                          href={api.getReportDownloadUrl(item.id)}
                          target="_blank"
                          rel="noreferrer"
                          className="inline-flex items-center gap-1 px-3 py-1.5 rounded-lg bg-emerald-50 text-emerald-800 hover:bg-emerald-100 font-semibold text-xs border border-emerald-200 transition"
                          title="Download PDF"
                        >
                          <Download className="w-3.5 h-3.5" />
                          PDF
                        </a>
                      )}

                      {deleteConfirmId === item.id ? (
                        <span className="inline-flex items-center gap-1">
                          <button
                            onClick={() => handleDelete(item.id)}
                            className="px-2 py-1 text-[11px] font-bold text-white bg-rose-600 rounded hover:bg-rose-700"
                          >
                            Confirm
                          </button>
                          <button
                            onClick={() => setDeleteConfirmId(null)}
                            className="px-2 py-1 text-[11px] text-slate-600 hover:bg-slate-200 rounded"
                          >
                            Cancel
                          </button>
                        </span>
                      ) : (
                        <button
                          onClick={() => setDeleteConfirmId(item.id)}
                          className="p-1.5 rounded-lg text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition"
                          title="Delete Record"
                        >
                          <Trash2 className="w-4 h-4" />
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination Controls */}
        {pagination.total_pages > 1 && (
          <div className="px-6 py-4 bg-slate-50 border-t border-slate-200 flex items-center justify-between text-xs text-slate-600">
            <div>
              Showing page <strong>{pagination.page}</strong> of <strong>{pagination.total_pages}</strong> ({pagination.total_items} total items)
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => fetchHistory(pagination.page - 1)}
                disabled={!pagination.has_prev}
                className={`p-1.5 rounded-lg border border-slate-200 bg-white ${
                  pagination.has_prev ? 'hover:bg-slate-100 text-slate-700' : 'opacity-40 cursor-not-allowed text-slate-300'
                }`}
              >
                <ChevronLeft className="w-4 h-4" />
              </button>
              <button
                onClick={() => fetchHistory(pagination.page + 1)}
                disabled={!pagination.has_next}
                className={`p-1.5 rounded-lg border border-slate-200 bg-white ${
                  pagination.has_next ? 'hover:bg-slate-100 text-slate-700' : 'opacity-40 cursor-not-allowed text-slate-300'
                }`}
              >
                <ChevronRight className="w-4 h-4" />
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};
