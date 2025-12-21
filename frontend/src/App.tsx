<<<<<<< HEAD
import { useState, useEffect } from 'react';
=======
import { useState } from 'react';
>>>>>>> develop
import { ImageUploader } from './components/ImageUploader';
import { EmotionDisplay } from './components/EmotionDisplay';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';
<<<<<<< HEAD
import { analyzeImage, checkHealth } from './services/api';
import type { EmotionAnalysis, HealthResponse } from './types';
=======
import { analyzeImage } from './services/api';
import type { EmotionAnalysis } from './types';
>>>>>>> develop

/**
 * Main application component
 * Manages the emotion analysis workflow: upload -> analyze -> display results
 */
function App() {
  // Application state management
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<EmotionAnalysis | null>(null);
<<<<<<< HEAD
  const [healthStatus, setHealthStatus] = useState<HealthResponse | null>(null);

  // Check backend health on mount
  useEffect(() => {
    const getHealth = async () => {
      try {
        const health = await checkHealth();
        setHealthStatus(health);
      } catch (err) {
        console.error('Backend unreachable:', err);
      }
    };
    getHealth();
  }, []);
=======
>>>>>>> develop

  // Reset state when new image is selected
  const handleImageSelect = (file: File) => {
    setSelectedFile(file);
    setError(null);
    setResult(null);
  };

  // Send image to backend API for emotion analysis
  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError(null);
    setResult(null);

    try {
      const analysis = await analyzeImage(selectedFile);
<<<<<<< HEAD
      if (analysis.emotion === 'error') {
        throw new Error(analysis.reasoning);
      }
      setResult(analysis);
    } catch (err: any) {
      setError(err.message || 'Error al analizar la imagen');
=======
      setResult(analysis);
    } catch (err: any) {
      // Extract error message from API response or use fallback
      const errorMsg = err.response?.data?.detail || err.message || 'Error al analizar la imagen';
      setError(errorMsg);
>>>>>>> develop
    } finally {
      setLoading(false);
    }
  };

<<<<<<< HEAD

=======
>>>>>>> develop
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
<<<<<<< HEAD
          <div className="flex justify-center items-center gap-2 mb-4">
            <span className={`h-3 w-3 rounded-full ${healthStatus?.status === 'healthy' ? 'bg-green-500' : 'bg-red-500 shadow-sm animate-pulse'}`}></span>
            <span className="text-xs font-medium text-gray-500 uppercase tracking-widest">
              {healthStatus ? `Backend ${healthStatus.status}` : 'Buscando servidor...'}
              {healthStatus?.llama_status === 'disconnected' && ' (Llama Offline)'}
            </span>
          </div>
=======
>>>>>>> develop
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Sistema Biométrico IA
          </h1>
          <p className="text-gray-600">
            Análisis de emociones y microexpresiones con Llama 3.2 Vision
          </p>
        </div>

<<<<<<< HEAD

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <ImageUploader
            onImageSelect={handleImageSelect}
=======
        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <ImageUploader 
            onImageSelect={handleImageSelect} 
>>>>>>> develop
            disabled={loading}
          />

          {selectedFile && !loading && !result && (
            <div className="mt-6 text-center">
              <button
                onClick={handleAnalyze}
                className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-3 px-8 rounded-lg transition-colors duration-200 shadow-md hover:shadow-lg"
              >
                Analizar Emoción
              </button>
            </div>
          )}

          {loading && (
            <div className="mt-6">
              <LoadingSpinner />
              <p className="text-center text-gray-600 mt-2">
                Analizando imagen...
              </p>
            </div>
          )}

          {error && (
<<<<<<< HEAD
            <div className="mt-6 animate-fade-in">
=======
            <div className="mt-6">
>>>>>>> develop
              <ErrorMessage message={error} />
            </div>
          )}

          {result && (
<<<<<<< HEAD
            <div className="mt-6 animate-fade-in">
=======
            <div className="mt-6">
>>>>>>> develop
              <EmotionDisplay analysis={result} />
              <div className="mt-4 text-center">
                <button
                  onClick={() => {
                    setResult(null);
                    setSelectedFile(null);
                  }}
                  className="text-blue-600 hover:text-blue-700 font-medium"
                >
                  Analizar otra imagen
                </button>
              </div>
            </div>
          )}
<<<<<<< HEAD

=======
>>>>>>> develop
        </div>

        {/* Footer */}
        <div className="text-center text-gray-600 text-sm">
          <p>Powered by Llama 3.2 Vision (11B) • FastAPI • React</p>
        </div>
      </div>
    </div>
  );
}

export default App;
