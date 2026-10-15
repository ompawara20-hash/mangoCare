export type HealthStatus = {
  status: 'healthy' | 'degraded' | 'unhealthy';
  version: string;
  database_ready: boolean;
  disease_model_ready: boolean;
  validator_model_ready: boolean;
  device: string;
  operating_mode: string;
};

export type ModelInfo = {
  name: string;
  architecture: string;
  input_dimensions: number[];
  num_classes: number;
  supported_classes: string[];
  target_tissue: string;
  preprocessing_summary: Record<string, any>;
  evaluation_metrics: {
    dataset: string;
    benchmark_accuracy: string;
    license: string;
    source: string;
  };
  limitations: string[];
};

export type ValidationDetail = {
  is_mango: boolean;
  status: string;
  error_code?: string;
  message?: string;
  suggestion?: string;
  confidence?: number;
  details?: Record<string, any>;
};

export type PredictionDetail = {
  class_id: string;
  class_name: string;
  confidence: number;
  confidence_category: 'high' | 'moderate' | 'low';
  confidence_interpretation: string;
  uncertainty_flag: boolean;
};

export type AlternativePrediction = {
  class_id: string;
  class_name: string;
  confidence: number;
};

export type ConditionInformation = {
  id?: string;
  name: string;
  scientific_name?: string;
  category?: 'fungal' | 'bacterial' | 'pest' | 'healthy' | string;
  supported_model_class?: string;
  plant_parts_affected?: string;
  severity_level?: 'High' | 'Moderate' | 'Low' | 'None' | string;
  description: string;
  visible_symptoms: string[];
  favorable_conditions?: string;
  prevention: string[];
  management_recommendations: string[];
  recommended_next_steps: string[];
  expert_inspection_advised: boolean;
  references: string[];
  important_limitations?: string;
};

export type AnalysisResult = {
  success: boolean;
  analysis_id?: string;
  status: 'healthy_appearance_detected' | 'suspected_disease' | 'inconclusive' | 'uncertain_result' | 'invalid_image' | string;
  error_code?: string;
  message?: string;
  suggestion?: string;
  image_validation: ValidationDetail;
  prediction?: PredictionDetail;
  alternatives?: AlternativePrediction[];
  condition_information?: ConditionInformation;
  model?: {
    name: string;
    architecture: string;
    version: string;
  };
  limitations?: string[];
  created_at?: string;
  report_filename?: string;
  image_metadata?: {
    filename: string;
    width: number;
    height: number;
    format: string;
  };
};

export type HistoryItem = {
  id: string;
  created_at: string;
  status: string;
  is_mango: boolean;
  predicted_class_id?: string;
  predicted_class_name?: string;
  confidence: number;
  confidence_category: string;
  uncertainty_flag: boolean;
  model_name: string;
  model_version: string;
  image_filename?: string;
  report_filename?: string;
  top_alternatives_json: string;
  symptoms_summary: string;
  recommended_action: string;
};

export type PaginationInfo = {
  page: number;
  page_size: number;
  total_items: number;
  total_pages: number;
  has_next: boolean;
  has_prev: boolean;
};

export type HistoryResponse = {
  items: HistoryItem[];
  pagination: PaginationInfo;
};

export type DashboardStatistics = {
  total_analyses: number;
  healthy_count: number;
  diseased_count: number;
  inconclusive_count: number;
  disease_breakdown: { name: string; count: number }[];
};
