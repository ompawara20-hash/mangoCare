import axios from 'axios';
import {
  HealthStatus,
  ModelInfo,
  AnalysisResult,
  HistoryResponse,
  HistoryItem,
  DashboardStatistics,
  ConditionInformation
} from '../types';

const API_BASE = import.meta.env.VITE_API_URL || '/api';

export const apiClient = axios.create({
  baseURL: API_BASE,
  timeout: 45000,
});

export const api = {
  async getHealth(): Promise<HealthStatus> {
    const res = await apiClient.get<HealthStatus>('/health');
    return res.data;
  },

  async getModelInfo(): Promise<ModelInfo> {
    const res = await apiClient.get<ModelInfo>('/model-info');
    return res.data;
  },

  async analyzeImage(file: File): Promise<AnalysisResult> {
    const formData = new FormData();
    formData.append('file', file);
    const res = await apiClient.post<AnalysisResult>('/analyze', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return res.data;
  },

  async getHistory(
    page: number = 1,
    pageSize: number = 10,
    status?: string,
    search?: string
  ): Promise<HistoryResponse> {
    const params: Record<string, any> = { page, page_size: pageSize };
    if (status && status !== 'all') params.status = status;
    if (search && search.trim()) params.search = search.trim();

    const res = await apiClient.get<HistoryResponse>('/history', { params });
    return res.data;
  },

  async getAnalysis(analysisId: string): Promise<HistoryItem> {
    const res = await apiClient.get<HistoryItem>(`/history/${analysisId}`);
    return res.data;
  },

  async deleteAnalysis(analysisId: string): Promise<{ success: boolean }> {
    const res = await apiClient.delete<{ success: boolean }>(`/history/${analysisId}`);
    return res.data;
  },

  async getStatistics(): Promise<DashboardStatistics> {
    const res = await apiClient.get<DashboardStatistics>('/statistics');
    return res.data;
  },

  async getDiseases(search?: string): Promise<{ diseases: ConditionInformation[] }> {
    const params: Record<string, any> = {};
    if (search && search.trim()) params.search = search.trim();
    const res = await apiClient.get<{ diseases: ConditionInformation[] }>('/diseases', { params });
    return res.data;
  },

  async getDisease(diseaseId: string): Promise<{ disease: ConditionInformation }> {
    const res = await apiClient.get<{ disease: ConditionInformation }>(`/diseases/${diseaseId}`);
    return res.data;
  },

  getReportDownloadUrl(analysisId: string): string {
    return `${API_BASE}/reports/${analysisId}`;
  }
};
