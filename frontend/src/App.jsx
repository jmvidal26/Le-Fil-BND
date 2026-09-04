import { useState, useEffect } from 'react';
import { Cpu, Terminal, ShieldAlert, Activity, CheckCircle, Zap } from 'lucide-react';
import './App.css';

export default function App() {
  const [pythonStatus, setPythonStatus] = useState('Conectando a backend Python...');
  const [activeTab, setActiveTab] = useState('overview');

  useEffect(() => {
    // Probar conexión o simular estado
    setTimeout(() => {
      setPythonStatus('Entorno Python .venv activo (.venv Python 3.12)');
    }, 1000);
  }, []);

  return (
    <div className="app-container">
      <header className="app-header">
        <div className="header-brand">
          <div className="brand-logo">
            <Zap className="icon-bolt" />
          </div>
          <div>
            <h1>Le'Fil BND System</h1>
            <p className="subtitle">Plataforma Modular Integrada (Vite + React + Python .venv)</p>
          </div>
        </div>
        <div className="status-badge">
          <span className="status-dot"></span>
          {pythonStatus}
        </div>
      </header>

      <main className="app-main">
        <nav className="nav-tabs">
          <button 
            className={`tab-btn ${activeTab === 'overview' ? 'active' : ''}`}
            onClick={() => setActiveTab('overview')}
          >
            <Activity size={18} /> Panel General
          </button>
          <button 
            className={`tab-btn ${activeTab === 'edith' ? 'active' : ''}`}
            onClick={() => setActiveTab('edith')}
          >
            <ShieldAlert size={18} /> Módulos EDITH
          </button>
          <button 
            className={`tab-btn ${activeTab === 'lf' ? 'active' : ''}`}
            onClick={() => setActiveTab('lf')}
          >
            <Cpu size={18} /> Servicios LF
          </button>
        </nav>

        <section className="dashboard-grid">
          <div className="card glass-card">
            <h3><CheckCircle size={20} className="text-emerald" /> Configuración Entorno JS</h3>
            <ul className="info-list">
              <li><strong>Frontend Framework:</strong> React 18 + Vite</li>
              <li><strong>Lenguaje:</strong> JavaScript (ES Modules)</li>
              <li><strong>Puerto Servidor Dev:</strong> http://localhost:5173</li>
            </ul>
          </div>

          <div className="card glass-card">
            <h3><Terminal size={20} className="text-cyan" /> Configuración Python (.venv)</h3>
            <ul className="info-list">
              <li><strong>Versión Recomendada:</strong> Python 3.12 (Máxima compatibilidad de librerías)</li>
              <li><strong>Entorno Virtual:</strong> <code>.venv</code> habilitado en la raíz</li>
              <li><strong>Librerías Soportadas:</strong> PyTorch, TensorFlow, OpenCV, MediaPipe, SpaCy, Whisper, etc.</li>
            </ul>
          </div>
        </section>
      </main>

      <footer className="app-footer">
        <p>Le'Fil BND &copy; {new Date().getFullYear()} - Entorno configurado con Vite, React y Python .venv</p>
      </footer>
    </div>
  );
}
