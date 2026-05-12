import axios, { AxiosInstance } from 'axios';
import Cookies from 'js-cookie';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

interface ApiResponse<T> {
  data: T;
  message?: string;
  status?: number;
}

class APIClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor for auth token
    this.client.interceptors.request.use((config) => {
      const token = Cookies.get('accessToken');
      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }
      return config;
    });

    // Add response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Clear tokens and redirect to login
          Cookies.remove('accessToken');
          Cookies.remove('refreshToken');
          window.location.href = '/auth/login';
        }
        return Promise.reject(error);
      }
    );
  }

  // Auth endpoints
  async register(data: {
    name: string;
    email: string;
    password: string;
  }): Promise<ApiResponse<any>> {
    const response = await this.client.post('/api/auth/register', data);
    return response.data;
  }

  async login(email: string, password: string): Promise<ApiResponse<any>> {
    const response = await this.client.post('/api/auth/login', {
      email,
      password,
    });
    if (response.data.access_token) {
      Cookies.set('accessToken', response.data.access_token);
      if (response.data.refresh_token) {
        Cookies.set('refreshToken', response.data.refresh_token);
      }
    }
    return response.data;
  }

  async getCurrentUser(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/api/auth/me');
    return response.data;
  }

  // Resume endpoints
  async uploadResume(file: File): Promise<ApiResponse<any>> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await this.client.post('/api/resume/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
    return response.data;
  }

  async getResumeHistory(skip = 0, limit = 50): Promise<ApiResponse<any[]>> {
    const response = await this.client.get('/api/resume/history', {
      params: { skip, limit },
    });
    return response.data;
  }

  async getResume(resumeId: number): Promise<ApiResponse<any>> {
    const response = await this.client.get(`/api/resume/${resumeId}`);
    return response.data;
  }

  async deleteResume(resumeId: number): Promise<ApiResponse<any>> {
    const response = await this.client.delete(`/api/resume/${resumeId}`);
    return response.data;
  }

  // Analysis endpoints
  async analyzeResume(
    resumeId: number,
    jobDescription?: string,
    analyzeType = 'full'
  ): Promise<ApiResponse<any>> {
    const response = await this.client.post('/api/resume/analyze', {
      resume_id: resumeId,
      job_description: jobDescription,
      analyze_type: analyzeType,
    });
    return response.data;
  }

  async matchWithJob(
    resumeId: number,
    jobDescription: string
  ): Promise<ApiResponse<any>> {
    const response = await this.client.post('/api/resume/job-match', {
      resume_id: resumeId,
      job_description: jobDescription,
    });
    return response.data;
  }

  // Admin endpoints
  async getAdminStats(): Promise<ApiResponse<any>> {
    const response = await this.client.get('/api/admin/stats');
    return response.data;
  }

  async getUsersReport(skip = 0, limit = 50): Promise<ApiResponse<any[]>> {
    const response = await this.client.get('/api/admin/users', {
      params: { skip, limit },
    });
    return response.data;
  }

  async deleteUser(userId: number): Promise<ApiResponse<any>> {
    const response = await this.client.delete(`/api/admin/users/${userId}`);
    return response.data;
  }
}

export default new APIClient();
