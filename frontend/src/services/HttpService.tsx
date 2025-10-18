import axios from 'axios';
import API_URL from '../config/Config';
import { UserProfile } from '../types/User';
import { ExistingPayout, NewPayout } from '../types/Payout';
import { PaginationParams, PaginatedResponse, ApiResponse, ApiError } from '../types/General';

export const httpService = {
  loginWithGoogle: async (): Promise<void> => {
    try {
      // Call backend /auth/login to get redirect URL
      const response = await axios.get(`${API_URL}/auth/login`, {
        maxRedirects: 0, // prevent axios from automatically following redirects
        validateStatus: (status) => status === 302, // only treat 302 as valid
      });

      // The backend responds with a 302 redirect to Google's OAuth page
      const redirectUrl = response.headers['location'];
      if (!redirectUrl) throw new Error('No redirect URL from backend');

      // Redirect the browser to Google
      window.location.href = redirectUrl;
    } catch (err: any) {
      console.error('Error initiating Google login:', err.response?.data || err.message);
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
