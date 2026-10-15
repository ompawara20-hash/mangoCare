import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import {
  Upload,
  CheckCircle2,
  AlertTriangle,
  HelpCircle,
  FileText,
  ArrowRight,
  TrendingUp,
  Cpu,
  Shield,
  Activity,
  Layers
} from 'lucide-react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell
} from 'recharts';
import { api } from '../api/client';
import { DashboardStatistics, HistoryItem, HealthStatus } from '../types';
import { StatusBadge } from '../components/StatusBadge';

export const DashboardPage: React.FC = () => {
  const [stats, setStats] = useState<DashboardStatistics | null>(null);
  const [recentItems, setRecentItems] = useState<HistoryItem[]>([]);
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([
      api.getStatistics().catch(() => null),
      api.getHistory(1, 5).catch(() => ({ items: [] })),
      api.getHealth().catch(() => null),
    ]).then(([statsRes, historyRes, healthRes]) => {
      setStats(statsRes);
      setRecentItems(historyRes ? historyRes.items : []);
      setHealth(healthRes);
      setLoading(false);
    });
  }, []);

  const total = stats ? stats.total_analyses : 0;
  const healthy = stats ? stats.healthy_count : 0;
  const diseased = stats ? stats.diseased_count : 0;
  const inconclusive = stats ? stats.inconclusive_count : 0;

  const chartData = stats?.disease_breakdown && stats.disease_breakdown.length > 0
    ? stats.disease_breakdown
    : [
        { name: 'Healthy', count: healthy },
        { name: 'Anthracnose', count: 0 },
        { name: 'Bacterial Canker', count: 0 },
        { name: 'Powdery Mildew', count: 0 },
        { name: 'Die Back', count: 0 }
      ];

  const barColors = ['#16a34a', '#dc2626', '#e11d48', '#d97706', '#ca8a04', '#0284c7'];

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Hero Action Banner */}
      <div className="relative overflow-hidden rounded-3xl bg-gradient-to-r from-forest-900 via-forest-800 to-forest-950 text-white p-8 sm:p-10 shadow-xl border border-forest-700/50">
        <div className="relative z-10 max-w-2xl">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-forest-700/60 border border-forest-500/40 text-xs font-semibold text-emerald-300 mb-4 backdrop-blur-sm">
            <Activity className="w-3.5 h-3.5 text-emerald-400" />
            <span>AI-Driven Foliar Pathology Screening</span>
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight mb-3">
            Protect Your Mango Orchard with Intelligent Vision Screening
          </h1>

          <p className="text-sm sm:text-base text-forest-100/90 leading-relaxed mb-6 font-normal">
            Upload high-resolution photographs of mango leaves to detect early symptoms of Anthracnose,
            Bacterial Canker, Powdery Mildew, Die Back, and insect pest damage before yield is compromised.
          </p>

          <div className="flex flex-wrap items-center gap-4">
            <Link
              to="/analyze"
              className="inline-flex items-center gap-2.5 px-6 py-3.5 rounded-xl bg-emerald-500 hover:bg-emerald-400 text-forest-950 font-bold text-sm transition shadow-lg shadow-emerald-950/20 active:scale-95"
            >
              <Upload className="w-4 h-4" />
              Analyze Mango Leaf Specimen
            </Link>

            <Link
              to="/library"
              className="inline-flex items-center gap-2 px-5 py-3.5 rounded-xl bg-white/10 hover:bg-white/15 text-white font-semibold text-sm transition border border-white/10"
            >
              <Layers className="w-4 h-4" />
              Browse Disease Library
            </Link>
          </div>
        </div>

        {/* Decorative background shapes */}
        <div className="absolute right-0 top-0 bottom-0 w-1/3 bg-radial from-emerald-500/10 to-transparent pointer-events-none" />
      </div>

      {/* Model & System Status Bar */}
      <div className="bg-white rounded-2xl border border-slate-200 p-4 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-forest-50 text-forest-700 flex items-center justify-center border border-forest-100">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h4 className="text-xs font-bold text-slate-800">ConvNeXt-Small Active Backbone</h4>
            <p className="text-[11px] text-slate-500">
              {health?.disease_model_ready
                ? `Operational on ${health.device.toUpperCase()} • 8 Supported Pathologies & Conditions`
                : 'Connecting to inference engine...'}
            </p>
          </div>
        </div>

        <div className="flex items-center gap-3 text-xs">
          <span className="text-slate-400">Database:</span>
          <span className="font-semibold text-slate-700 flex items-center gap-1">
            <span className="w-2 h-2 rounded-full bg-emerald-500" />
            SQLite Connected
          </span>
          <span className="text-slate-300">|</span>
          <Link to="/about" className="text-forest-700 font-semibold hover:underline flex items-center gap-1">
            Model Specifications <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
      </div>

      {/* Real Statistics Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
        <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-slate-500">Total Analyses</span>
            <div className="p-2 rounded-lg bg-slate-100 text-slate-700">
              <FileText className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-slate-900">{total}</div>
          <span className="text-[11px] text-slate-400 mt-1 block">Persisted records</span>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-emerald-700">Healthy Foliage</span>
            <div className="p-2 rounded-lg bg-emerald-50 text-emerald-700">
              <CheckCircle2 className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-emerald-700">{healthy}</div>
          <span className="text-[11px] text-slate-400 mt-1 block">
            {total > 0 ? `${((healthy / total) * 100).toFixed(0)}% of total` : 'No samples recorded yet'}
          </span>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-rose-700">Suspected Pathologies</span>
            <div className="p-2 rounded-lg bg-rose-50 text-rose-700">
              <AlertTriangle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-rose-700">{diseased}</div>
          <span className="text-[11px] text-slate-400 mt-1 block">
            {total > 0 ? `${((diseased / total) * 100).toFixed(0)}% requiring care` : 'No diseases detected yet'}
          </span>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200/90 p-5 shadow-sm">
          <div className="flex items-center justify-between mb-2">
            <span className="text-xs font-semibold text-amber-700">Inconclusive / Uncertain</span>
            <div className="p-2 rounded-lg bg-amber-50 text-amber-700">
              <HelpCircle className="w-4 h-4" />
            </div>
          </div>
          <div className="text-2xl font-bold text-amber-700">{inconclusive}</div>
          <span className="text-[11px] text-slate-400 mt-1 block">Re-photograph advised</span>
        </div>
      </div>

      {/* Analytics Chart & Recent Activity */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Disease Distribution Chart */}
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-6">
            <div>
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-forest-700" />
                Condition Distribution
              </h3>
              <p className="text-xs text-slate-500">Distribution of historical screening classifications</p>
            </div>
            <Link to="/library" className="text-xs font-semibold text-forest-700 hover:underline">
              View All 8 Classes
            </Link>
          </div>

          <div className="h-64 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 20 }}>
                <XAxis
                  dataKey="name"
                  tick={{ fontSize: 11, fill: '#64748b' }}
                  interval={0}
                  angle={-15}
                  textAnchor="end"
                />
                <YAxis allowDecimals={false} tick={{ fontSize: 11, fill: '#64748b' }} />
                <Tooltip
                  cursor={{ fill: '#f1f5f9' }}
                  contentStyle={{ borderRadius: '8px', border: '1px solid #e2e8f0', fontSize: '12px' }}
                />
                <Bar dataKey="count" radius={[6, 6, 0, 0]}>
                  {chartData.map((_, index) => (
                    <Cell key={`cell-${index}`} fill={barColors[index % barColors.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Quick Recent Activity */}
        <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-sm flex flex-col">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-base font-bold text-slate-900">Recent Analyses</h3>
            <Link to="/history" className="text-xs font-semibold text-forest-700 hover:underline">
              View All
            </Link>
          </div>

          {recentItems.length === 0 ? (
            <div className="flex-1 flex flex-col items-center justify-center text-center p-6 bg-slate-50 rounded-xl border border-dashed border-slate-200">
              <FileText className="w-8 h-8 text-slate-300 mb-2" />
              <p className="text-xs font-medium text-slate-600">No analyses performed yet</p>
              <p className="text-[11px] text-slate-400 mt-1 mb-3">Upload your first mango leaf photo</p>
              <Link
                to="/analyze"
                className="px-3 py-1.5 rounded-lg bg-forest-800 text-white text-xs font-semibold hover:bg-forest-900 transition"
              >
                Start Analysis
              </Link>
            </div>
          ) : (
            <div className="space-y-3 flex-1 overflow-y-auto">
              {recentItems.map((item) => (
                <div
                  key={item.id}
                  className="p-3 rounded-xl bg-slate-50 border border-slate-100 flex items-center justify-between gap-3 hover:bg-forest-50/40 transition"
                >
                  <div className="min-w-0">
                    <h5 className="text-xs font-semibold text-slate-800 truncate">
                      {item.predicted_class_name || 'Specimen Analysis'}
                    </h5>
                    <div className="flex items-center gap-2 mt-1">
                      <StatusBadge status={item.status} className="scale-90 origin-left" showIcon={false} />
                      <span className="text-[10px] text-slate-400">
                        {new Date(item.created_at).toLocaleDateString()}
                      </span>
                    </div>
                  </div>

                  <div className="text-right shrink-0">
                    <span className="text-xs font-bold text-slate-700 block">
                      {(item.confidence * 100).toFixed(0)}%
                    </span>
                    {item.report_filename && (
                      <a
                        href={api.getReportDownloadUrl(item.id)}
                        target="_blank"
                        rel="noreferrer"
                        className="text-[10px] text-forest-700 hover:underline"
                      >
                        PDF
                      </a>
                    )}
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
