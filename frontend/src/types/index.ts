/**
 * Emotion analysis result from backend API
 */
export interface EmotionAnalysis {
  emotion: string;      // Detected emotion (e.g., "joy", "sadness", "anger")
  confidence: number;   // Confidence score (0.0 to 1.0)
  reasoning: string;    // Clinical reasoning explaining the detection
}

/**
 * Multiple analysis result from batch endpoint
 */
export interface BatchResponse {
  results: EmotionAnalysis[];
  processed_count: number;
  failed_count: number;
}

/**
 * Detailed health status from backend
 */
export interface HealthResponse {
  status: string;
  service: string;
  llama_status: string;
  version: string;
}

/**
 * Structured error response from backend API
 */
export interface AnalysisError {
  detail: string;
  type?: string;
}

