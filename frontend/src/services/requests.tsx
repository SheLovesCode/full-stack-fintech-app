import axios, { AxiosRequestConfig, AxiosError } from 'axios';
import API_URL from '../config/Config'
import { ApiResponse } from '../types/General';

// Create Axios instance
const apiClient = axios.create({
    baseURL: API_URL,
    timeout: 10000,
    headers: { 'Content-Type': 'application/json' },
});

// Request interceptor: add auth token if exists
apiClient.interceptors.request.use((config) => {
    const token = localStorage.getItem('accessToken');
    if (token && config.headers) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// Response interceptor: centralized error handling
apiClient.interceptors.response.use(
    (response) => response,
    (error: AxiosError) => {
        console.error('API Error:', error.response?.data || error.message);
        return Promise.reject(error);
    }
);

// Generic request methods with correct <T> declaration
const request = {
    get: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
        const response = await apiClient.get<ApiResponse<T>>(url, config);
        return response.data.data;
    },

    post: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
        const response = await apiClient.post<ApiResponse<T>>(url, data, config);
        return response.data.data;
    },

    put: async <T>(url: string, data?: any, config?: AxiosRequestConfig): Promise<T> => {
        const response = await apiClient.put<ApiResponse<T>>(url, data, config);
        return response.data.data;
    },

    delete: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
        const response = await apiClient.delete<ApiResponse<T>>(url, config);
        return response.data.data;
    },
};

export default request;
