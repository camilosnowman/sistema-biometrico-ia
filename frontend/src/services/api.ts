import axios from 'axios';
import type { EmotionAnalysis, BatchResponse, HealthResponse } from '../types';

// Backend API base URL
const API_URL = 'http://localhost:8000';

/**
 * Helper to handle axios errors and extract detail message
 */
const handleError = (error: any): string => {
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  return error.message || 'Error de conexión con el servidor';
};

/**
 * Send image file to backend for emotion analysis
 */
export const analyzeImage = async (file: File): Promise<EmotionAnalysis> => {
  const formData = new FormData();
  formData.append('file', file);

  try {
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
  } catch (error: any) {
    throw new Error(handleError(error));
  }
};

/**
 * Send multiple image files for batch analysis
 */
export const analyzeBatch = async (files: File[]): Promise<BatchResponse> => {
  const formData = new FormData();
  files.forEach(file => formData.append('files', file));

  try {
    const response = await axios.post<BatchResponse>(
      `${API_URL}/batch-analyze`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      }
    );
    return response.data;
  } catch (error: any) {
    throw new Error(handleError(error));
  }
};

/**
 * Check backend API health status
 */
export const checkHealth = async (): Promise<HealthResponse> => {
  try {
    const response = await axios.get<HealthResponse>(`${API_URL}/health`);
    return response.data;
  } catch (error: any) {
    throw new Error(handleError(error));
  }
};

