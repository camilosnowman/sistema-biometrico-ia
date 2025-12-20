import type { EmotionAnalysis } from '../types';

interface EmotionDisplayProps {
  analysis: EmotionAnalysis;
}

// Mapping of emotions to their representative emojis
const emotionEmojis: Record<string, string> = {
  joy: '😊',
  happiness: '😊',
  anger: '😠',
  surprise: '😲',
  neutral: '😐',
  sadness: '😢',
  sad: '😢',
  fear: '😨',
  disgust: '🤢',
  unknown: '❓',
  error: '⚠️',
};

// Tailwind color classes for each emotion type
const emotionColors: Record<string, string> = {
  joy: 'bg-yellow-100 border-yellow-300',
  happiness: 'bg-yellow-100 border-yellow-300',
  anger: 'bg-red-100 border-red-300',
  surprise: 'bg-purple-100 border-purple-300',
  neutral: 'bg-gray-100 border-gray-300',
  sadness: 'bg-blue-100 border-blue-300',
  sad: 'bg-blue-100 border-blue-300',
  fear: 'bg-orange-100 border-orange-300',
  disgust: 'bg-green-100 border-green-300',
  unknown: 'bg-gray-100 border-gray-300',
  error: 'bg-red-100 border-red-300',
};

/**
 * Display component for emotion analysis results
 * Shows emotion with emoji, confidence percentage, and clinical reasoning
 */
export const EmotionDisplay = ({ analysis }: EmotionDisplayProps) => {
  const emoji = emotionEmojis[analysis.emotion.toLowerCase()] || '🤔';
  const colorClass = emotionColors[analysis.emotion.toLowerCase()] || 'bg-gray-100 border-gray-300';
  
  return (
    <div className={`border-2 rounded-lg p-6 ${colorClass}`}>
      <div className="text-center mb-4">
        <span className="text-6xl">{emoji}</span>
        <h2 className="text-2xl font-bold mt-2 capitalize">{analysis.emotion}</h2>
      </div>
      
      <div className="space-y-4">
        <div>
          <div className="flex justify-between items-center mb-2">
            <span className="text-sm font-medium text-gray-700">Confianza</span>
            <span className="text-sm font-bold text-gray-900">
              {(analysis.confidence * 100).toFixed(1)}%
            </span>
          </div>
          <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
            <div
              className="bg-blue-600 h-full rounded-full transition-all duration-500"
              style={{ width: `${analysis.confidence * 100}%` }}
            />
          </div>
        </div>
        
        <div className="bg-white bg-opacity-50 rounded-lg p-4">
          <h3 className="text-sm font-semibold text-gray-700 mb-2">
            Análisis Clínico
          </h3>
          <p className="text-sm text-gray-800 leading-relaxed">
            {analysis.reasoning}
          </p>
        </div>
      </div>
    </div>
  );
};
