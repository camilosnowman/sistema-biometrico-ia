/**
 * Emotion analysis result from backend API
 */
export interface EmotionAnalysis {
  emotion: string;      // Detected emotion (e.g., "joy", "sadness", "anger")
  confidence: number;   // Confidence score (0.0 to 1.0)
  reasoning: string;    // Clinical reasoning explaining the detection
}

/**
 * Error response from backend API
 */
export interface AnalysisError {
  detail: string;
}
