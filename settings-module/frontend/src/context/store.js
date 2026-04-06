import { create } from 'zustand';

export const useAuthStore = create((set, get) => ({
  user: null,
  accessToken: localStorage.getItem('accessToken'),
  isLoading: false,
  error: null,

  setUser: (user) => set({ user }),
  setAccessToken: (token) => {
    set({ accessToken: token });
    if (token) {
      localStorage.setItem('accessToken', token);
    } else {
      localStorage.removeItem('accessToken');
    }
  },
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  logout: () => {
    set({ user: null, accessToken: null });
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
  },
}));

export const useSettingsStore = create((set) => ({
  settings: null,
  isLoading: false,
  isDirty: false,
  error: null,

  setSettings: (settings) => set({ settings }),
  setLoading: (isLoading) => set({ isLoading }),
  setDirty: (isDirty) => set({ isDirty }),
  setError: (error) => set({ error }),
  updateSetting: (key, value) => {
    set((state) => ({
      settings: {
        ...state.settings,
        [key]: value,
      },
      isDirty: true,
    }));
  },
  reset: () => set({ settings: null, isDirty: false, error: null }),
}));

export const useNotificationStore = create((set) => ({
  notifications: [],
  addNotification: (notification) => {
    const id = Date.now();
    set((state) => ({
      notifications: [
        ...state.notifications,
        { ...notification, id },
      ],
    }));
    setTimeout(() => {
      set((state) => ({
        notifications: state.notifications.filter((n) => n.id !== id),
      }));
    }, 5000);
  },
  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },
}));
