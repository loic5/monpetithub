/**
 * @license
 * SPDX-License-Identifier: Apache-2.0
 */

import React, { useState, useEffect } from 'react';
import { 
  LayoutDashboard, 
  LogOut, 
  Search, 
  ShieldCheck,
  Lock,
  FileText,
  ClipboardCheck,
  FileEdit,
  Mic,
  Languages,
  Sparkles
} from 'lucide-react';
import { motion, AnimatePresence } from 'motion/react';

// AI App Catalog Data
const AI_APPS = [
  {
    id: 1,
    name: "Profil Scorer",
    description: "Analyse comparative et scoring automatique de CV pour identifier les meilleurs talents.",
    icon: <FileText className="w-6 h-6 text-blue-400" />,
    category: "Recrutement"
  },
  {
    id: 2,
    name: "RecruitAI Evaluator",
    description: "Évaluations structurées des compétences candidats basées sur des critères objectifs.",
    icon: <ClipboardCheck className="w-6 h-6 text-purple-400" />,
    category: "Recrutement"
  },
  {
    id: 3,
    name: "RecOps Copilot",
    description: "Transforme les transcriptions de réunions en documents de recrutement exploitables.",
    icon: <FileEdit className="w-6 h-6 text-emerald-400" />,
    category: "Opérations"
  },
  {
    id: 4,
    name: "Speech to Text",
    description: "Transcription auto intelligente et résumés automatiques via Gemini.",
    icon: <Mic className="w-6 h-6 text-yellow-400" />,
    category: "Productivité"
  },
  {
    id: 5,
    name: "Slide Translator",
    description: "Traduction intelligente de présentations Powerpoint (.pptx) via Gemini.",
    icon: <Languages className="w-6 h-6 text-pink-400" />,
    category: "Productivité"
  },
  {
    id: 6,
    name: "Le Générateur de lolo",
    description: "Générateur d'images créatif avec persistance des personnages pour vos projets.",
    icon: <Sparkles className="w-6 h-6 text-orange-400" />,
    category: "Création"
  }
];

export default function App() {
  const [isLoggedIn, setIsLoggedIn] = useState<boolean>(() => {
    return localStorage.getItem('isLoggedIn') === 'true';
  });
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  // The password from environment variables (or fallback for demo)
  const CORRECT_PASSWORD = import.meta.env.VITE_APP_PASSWORD || 'admin';

  useEffect(() => {
    localStorage.setItem('isLoggedIn', isLoggedIn.toString());
  }, [isLoggedIn]);

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault();
    if (password === CORRECT_PASSWORD) {
      setIsLoggedIn(true);
      setError('');
    } else {
      setError('Mot de passe incorrect');
    }
  };

  const handleLogout = () => {
    setIsLoggedIn(false);
    setPassword('');
  };

  if (!isLoggedIn) {
    return (
      <div className="min-h-screen bg-[#0e1117] flex items-center justify-center p-4 font-sans">
        <motion.div 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="w-full max-w-md bg-[#1e2630] p-8 rounded-2xl shadow-2xl border border-white/5"
        >
          <div className="flex flex-col items-center mb-8">
            <div className="w-16 h-16 bg-blue-500/10 rounded-full flex items-center justify-center mb-4">
              <Lock className="w-8 h-8 text-blue-500" />
            </div>
            <h1 className="text-2xl font-bold text-white">Connexion</h1>
            <p className="text-gray-400 text-sm mt-2 text-center">
              Veuillez entrer le mot de passe pour accéder au catalogue.
            </p>
          </div>

          <form onSubmit={handleLogin} className="space-y-6">
            <div>
              <label className="block text-xs font-semibold text-gray-400 uppercase tracking-wider mb-2">
                Mot de passe
              </label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                placeholder="••••••••"
                className="w-full bg-[#0e1117] border border-white/10 rounded-xl px-4 py-3 text-white focus:outline-none focus:ring-2 focus:ring-blue-500/50 transition-all"
              />
              {error && (
                <p className="text-red-400 text-xs mt-2 flex items-center gap-1">
                  <ShieldCheck className="w-3 h-3" /> {error}
                </p>
              )}
            </div>

            <button
              type="submit"
              className="w-full bg-blue-600 hover:bg-blue-500 text-white font-semibold py-3 rounded-xl transition-colors shadow-lg shadow-blue-600/20"
            >
              Se connecter
            </button>
          </form>
        </motion.div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#0e1117] text-gray-100 flex font-sans">
      {/* Sidebar */}
      <aside className="w-64 border-r border-white/5 bg-[#1e2630] hidden md:flex flex-col">
        <div className="p-6">
          <div className="flex items-center gap-3 mb-8">
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <LayoutDashboard className="w-5 h-5 text-white" />
            </div>
            <span className="font-bold text-xl tracking-tight">AI Studio</span>
          </div>

          <nav className="space-y-1">
            <a href="#" className="flex items-center gap-3 px-4 py-3 bg-blue-600/10 text-blue-400 rounded-xl font-medium">
              <LayoutDashboard className="w-5 h-5" />
              Dashboard
            </a>
            <a href="#" className="flex items-center gap-3 px-4 py-3 text-gray-400 hover:bg-white/5 hover:text-white rounded-xl transition-all">
              <Search className="w-5 h-5" />
              Explorer
            </a>
          </nav>
        </div>

        <div className="mt-auto p-6 border-t border-white/5">
          <button 
            onClick={handleLogout}
            className="flex items-center gap-3 w-full px-4 py-3 text-red-400 hover:bg-red-400/10 rounded-xl transition-all font-medium"
          >
            <LogOut className="w-5 h-5" />
            Déconnexion
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="h-16 border-bottom border-white/5 flex items-center justify-between px-8 bg-[#0e1117]/80 backdrop-blur-md sticky top-0 z-10">
          <h2 className="text-lg font-semibold">Dashboard</h2>
          <div className="flex items-center gap-4">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-blue-500 to-purple-500" />
          </div>
        </header>

        <div className="p-8 max-w-6xl mx-auto">
          <div className="mb-12">
            <h1 className="text-4xl font-bold mb-4 tracking-tight">Catalogue d'Applications IA</h1>
            <p className="text-gray-400 max-w-2xl">
              Bienvenue dans votre espace sécurisé. Explorez nos outils d'intelligence artificielle 
              conçus pour booster votre productivité.
            </p>
          </div>

          {/* Grid Layout (2 columns as requested) */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <AnimatePresence>
              {AI_APPS.map((app, index) => (
                <motion.div
                  key={app.id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  whileHover={{ y: -4 }}
                  className="bg-[#1e2630] p-6 rounded-2xl border border-white/5 hover:border-blue-500/30 transition-all group cursor-pointer"
                >
                  <div className="flex items-start justify-between mb-4">
                    <div className="p-3 bg-[#0e1117] rounded-xl group-hover:bg-blue-500/10 transition-colors">
                      {app.icon}
                    </div>
                    <span className="text-[10px] uppercase font-bold tracking-widest text-gray-500 bg-[#0e1117] px-2 py-1 rounded-md">
                      {app.category}
                    </span>
                  </div>
                  <h3 className="text-xl font-bold mb-2 text-white group-hover:text-blue-400 transition-colors">
                    {app.name}
                  </h3>
                  <p className="text-gray-400 text-sm leading-relaxed">
                    {app.description}
                  </p>
                  <div className="mt-6 flex items-center text-blue-400 text-sm font-semibold opacity-0 group-hover:opacity-100 transition-opacity">
                    Lancer l'application →
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
          </div>
        </div>
      </main>
    </div>
  );
}
