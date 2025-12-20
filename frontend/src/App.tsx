import { useState } from 'react';
import { ImageUploader } from './components/ImageUploader';
import { EmotionDisplay } from './components/EmotionDisplay';
import { LoadingSpinner } from './components/LoadingSpinner';
import { ErrorMessage } from './components/ErrorMessage';
import { analyzeImage } from './services/api';
import type { EmotionAnalysis } from './types';

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
      setResult(analysis);
    } catch (err: any) {
      // Extract error message from API response or use fallback
      const errorMsg = err.response?.data?.detail || err.message || 'Error al analizar la imagen';
      setError(errorMsg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-8 max-w-4xl">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-gray-800 mb-2">
            Sistema Biométrico IA
          </h1>
          <p className="text-gray-600">
            Análisis de emociones y microexpresiones con Llama 3.2 Vision
          </p>
        </div>

        {/* Main Card */}
        <div className="bg-white rounded-2xl shadow-xl p-8 mb-6">
          <ImageUploader 
            onImageSelect={handleImageSelect} 
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
            <div className="mt-6">
              <ErrorMessage message={error} />
            </div>
          )}

          {result && (
            <div className="mt-6">
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
