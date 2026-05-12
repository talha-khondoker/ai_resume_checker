import { create } from 'zustand';
import Cookies from 'js-cookie';

interface User {
  id: number;
  name: string;
  email: string;
  role: string;
  is_active: boolean;
  created_at: string;
}

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
  setUser: (user: User | null) => void;
  setIsAuthenticated: (value: boolean) => void;
  setIsLoading: (value: boolean) => void;
  setError: (error: string | null) => void;
  logout: () => void;
  checkAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  isLoading: true,
  error: null,

  setUser: (user) => set({ user }),
  setIsAuthenticated: (value) => set({ isAuthenticated: value }),
  setIsLoading: (value) => set({ isLoading: value }),
  setError: (error) => set({ error }),

  logout: () => {
    Cookies.remove('accessToken');
    Cookies.remove('refreshToken');
    set({
      user: null,
      isAuthenticated: false,
      error: null,
    });
  },

  checkAuth: () => {
    const token = Cookies.get('accessToken');
    if (token) {
      set({ isAuthenticated: true });
    } else {
      set({ isAuthenticated: false, user: null });
    }
    set({ isLoading: false });
  },
}));
