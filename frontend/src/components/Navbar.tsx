import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import { Leaf, Cpu, History, BookOpen, Upload, Menu, X, CheckCircle, AlertCircle } from 'lucide-react';
import { api } from '../api/client';
import { HealthStatus } from '../types';

export const Navbar: React.FC = () => {
  const [health, setHealth] = useState<HealthStatus | null>(null);
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  useEffect(() => {
    api.getHealth()
      .then(setHealth)
      .catch(() => setHealth(null));
  }, []);

  const navLinks = [
    { to: '/', label: 'Dashboard', icon: Leaf },
    { to: '/analyze', label: 'Analyze Mango', icon: Upload },
    { to: '/library', label: 'Disease Library', icon: BookOpen },
    { to: '/history', label: 'Analysis History', icon: History },
    { to: '/about', label: 'About Model', icon: Cpu },
  ];

  return (
    <header className="sticky top-0 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo */}
          <NavLink to="/" className="flex items-center gap-2.5 group">
            <div className="w-10 h-10 rounded-xl bg-forest-800 text-emerald-400 flex items-center justify-center shadow-md group-hover:bg-forest-900 transition">
              <Leaf className="w-5 h-5 fill-emerald-400" />
            </div>
            <div>
              <span className="text-lg font-bold text-slate-900 tracking-tight flex items-center gap-1.5">
                MangoCare <span className="text-forest-600 font-extrabold">AI</span>
              </span>
              <span className="text-[10px] text-slate-500 font-medium block -mt-1 tracking-wide">
                Health & Pathology System
              </span>
            </div>
          </NavLink>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navLinks.map((link) => {
              const Icon = link.icon;
              return (
                <NavLink
                  key={link.to}
                  to={link.to}
                  className={({ isActive }) =>
                    `flex items-center gap-2 px-3.5 py-2 rounded-lg text-xs font-semibold transition ${
                      isActive
                        ? 'bg-forest-50 text-forest-800 border border-forest-200/60'
                        : 'text-slate-600 hover:text-slate-900 hover:bg-slate-100'
                    }`
                  }
                >
                  <Icon className="w-4 h-4" />
                  {link.label}
                </NavLink>
              );
            })}
          </nav>

          {/* Model Status Pill */}
          <div className="hidden sm:flex items-center gap-3">
            {health ? (
              <div
                className={`flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full border ${
                  health.disease_model_ready
                    ? 'bg-emerald-50 text-emerald-800 border-emerald-200'
                    : 'bg-amber-50 text-amber-800 border-amber-200'
                }`}
                title={`Operating Mode: ${health.operating_mode} | Device: ${health.device}`}
              >
                {health.disease_model_ready ? (
                  <CheckCircle className="w-3.5 h-3.5 text-emerald-600" />
                ) : (
                  <AlertCircle className="w-3.5 h-3.5 text-amber-600" />
                )}
                <span className="font-medium">
                  {health.disease_model_ready ? 'ConvNeXt Active' : 'Model Offline'}
                </span>
              </div>
            ) : (
              <div className="flex items-center gap-1.5 text-xs px-2.5 py-1 rounded-full bg-slate-100 text-slate-500 border border-slate-200">
                <span className="w-2 h-2 rounded-full bg-slate-400 animate-pulse" />
                <span>Checking...</span>
              </div>
            )}
          </div>

          {/* Mobile Menu Button */}
          <div className="flex md:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100"
            >
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu Dropdown */}
      {mobileMenuOpen && (
        <div className="md:hidden border-b border-slate-200 bg-white px-4 pt-2 pb-4 space-y-1">
          {navLinks.map((link) => {
            const Icon = link.icon;
            return (
              <NavLink
                key={link.to}
                to={link.to}
                onClick={() => setMobileMenuOpen(false)}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium ${
                    isActive
                      ? 'bg-forest-50 text-forest-800 font-semibold'
                      : 'text-slate-600 hover:bg-slate-100'
                  }`
                }
              >
                <Icon className="w-5 h-5" />
                {link.label}
              </NavLink>
            );
          })}
        </div>
      )}
    </header>
  );
};
