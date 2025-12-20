import axios from 'axios';
import type { EmotionAnalysis } from '../types';

// Backend API base URL
const API_URL = 'http://localhost:8000';

/**
 * Send image file to backend for emotion analysis
 * @param file - Image file to analyze
 * @returns Promise with emotion analysis result
 */
export const analyzeImage = async (file: File): Promise<EmotionAnalysis> => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await axios.post<EmotionAnalysis>(
    `${API_URL}/analyze`,
    formData,
    {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    }
  );

  return response.data;
};

/**
 * Check backend API health status
 * @returns Promise with health status
 */
export const checkHealth = async (): Promise<{ status: string }> => {
  const response = await axios.get(`${API_URL}/health`);
  return response.data;
};
