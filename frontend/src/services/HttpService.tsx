import axios from 'axios';
import API_URL from '../config/Config.tsx';
import { UserProfile } from '../types/User';
import { ExistingPayout, NewPayout } from '../types/Payout';
import { PaginationParams, PaginatedResponse, ApiResponse, ApiError } from '../types/General';

const httpService = {
  // --- AUTH ---
  login: async (
      provider: 'google' | 'github',
      code: string,
      state: string
  ): Promise<UserProfile> => {
    try {
      const response = await axios.post<ApiResponse<UserProfile>>(
          `${API_URL}/auth/oauth/${provider}`,
          { code, state }
      );
      return response.data.data;
    } catch (err: any) {
      console.error('Error logging in via OAuth:', err.response?.data || err.message);
      throw err as ApiError;
    }
  },

  getUserProfile: async (): Promise<UserProfile> => {
    try {
      const response = await axios.get<ApiResponse<UserProfile>>(`${API_URL}/auth/me`);
      return response.data.data;
    } catch (err: any) {
      console.error('Error fetching user profile:', err.response?.data || err.message);
      throw err as ApiError;
    }
  },

  // --- PAYOUTS ---
  createPayout: async (payoutData: NewPayout): Promise<ExistingPayout> => {
    try {
      const response = await axios.post<ApiResponse<ExistingPayout>>(
          `${API_URL}/payouts`,
          payoutData
      );
      return response.data.data;
    } catch (err: any) {
      console.error('Error creating payout:', err.response?.data || err.message);
      throw err as ApiError;
    }
  },

  getPayouts: async (
      params: PaginationParams = {}
  ): Promise<PaginatedResponse<ExistingPayout>> => {
    try {
      const response = await axios.get<PaginatedResponse<ExistingPayout>>(`${API_URL}/payouts`, {
        params,
      });
      return response.data;
    } catch (err: any) {
      console.error('Error fetching payouts:', err.response?.data || err.message);
      throw err as ApiError;
    }
  },

  getPayout: async (id: string): Promise<ExistingPayout> => {
    try {
      const response = await axios.get<ApiResponse<ExistingPayout>>(`${API_URL}/payouts/${id}`);
      return response.data.data;
    } catch (err: any) {
      console.error('Error fetching payout:', err.response?.data || err.message);
      throw err as ApiError;
    }
  },

  // --- WEBHOOKS (will be used for testing) ---
  sendWebhook: async (payload: any, signature: string): Promise<void> => {
    try {
      await axios.post(`${API_URL}/webhooks/payments`, payload, {
        headers: { 'X-Signature': signature },
      });
    } catch (err: any) {
      console.error('Error sending webhook:', err.response?.data || err.message);
      throw err as ApiError;
    }
  },
};

export default httpService;
