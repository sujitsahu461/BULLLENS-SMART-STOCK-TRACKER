import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import ProfileSettings from './ProfileSettings';
import PredictionSettings from './PredictionSettings';
import NotificationSettings from './NotificationSettings';
import DashboardSettings from './DashboardSettings';
import AIBehaviorSettings from './AIBehaviorSettings';
import LocalizationSettings from './LocalizationSettings';
import SecuritySettings from './SecuritySettings';
import { settingsAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiSettings, FiDownload, FiRotateCcw } from 'react-icons/fi';

export const SettingsPage = () => {
  const [activeTab, setActiveTab] = useState('profile');
  const [isLoading, setIsLoading] = useState(false);
  const [settings, setSettings] = useState(null);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const tabs = [
    { id: 'profile', label: 'Profile', icon: '👤' },
    { id: 'predictions', label: 'Predictions', icon: '📈' },
    { id: 'notifications', label: 'Notifications', icon: '🔔' },
    { id: 'dashboard', label: 'Dashboard', icon: '📊' },
    { id: 'ai', label: 'AI Behavior', icon: '🤖' },
    { id: 'localization', label: 'Localization', icon: '🌐' },
    { id: 'security', label: 'Security', icon: '🔒' },
  ];

  useEffect(() => {
    const fetchSettings = async () => {
      try {
        setIsLoading(true);
        const response = await settingsAPI.getSettings();
        setSettings(response.data.data);
      } catch (error) {
        addNotification({
          type: 'error',
          message: 'Failed to load settings',
        });
      } finally {
        setIsLoading(false);
      }
    };

    fetchSettings();
  }, []);

  const handleResetDefaults = async () => {
    if (window.confirm('Are you sure you want to reset all settings to defaults?')) {
      try {
        setIsLoading(true);
        await settingsAPI.resetToDefaults();
        addNotification({
          type: 'success',
          message: 'Settings reset to defaults',
        });
      } catch (error) {
        addNotification({
          type: 'error',
          message: 'Failed to reset settings',
        });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleExportSettings = () => {
    const dataStr = JSON.stringify(settings, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `settings-${new Date().toISOString()}.json`;
    link.click();
  };

  return (
    <div className="min-h-screen bg-light">
      {/* Header */}
      <div className="bg-white shadow-sm border-b border-gray-200">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="flex items-center justify-between">
            <div className="flex items-center">
              <FiSettings className="text-3xl text-accent mr-3" />
              <div>
                <h1 className="text-3xl font-bold text-gray-900">Settings</h1>
                <p className="text-gray-600 mt-1">Customize your Stock Predictor experience</p>
              </div>
            </div>
            <div className="flex gap-2">
              <button
                onClick={handleExportSettings}
                className="flex items-center gap-2 px-4 py-2 bg-primary text-white rounded-lg hover:bg-blue-600 transition"
              >
                <FiDownload /> Export
              </button>
              <button
                onClick={handleResetDefaults}
                className="flex items-center gap-2 px-4 py-2 bg-warning text-gray-900 rounded-lg hover:bg-yellow-500 transition"
              >
                <FiRotateCcw /> Reset
              </button>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-8">
          {/* Sidebar Navigation */}
          <div className="lg:col-span-1">
            <nav className="space-y-2 sticky top-8">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full text-left px-4 py-3 rounded-lg font-semibold transition ${
                    activeTab === tab.id
                      ? 'bg-accent text-white shadow-md'
                      : 'bg-white text-gray-900 hover:bg-gray-50 border border-gray-200'
                  }`}
                >
                  <span className="mr-2">{tab.icon}</span>
                  {tab.label}
                </button>
              ))}
            </nav>
          </div>

          {/* Main Content */}
          <div className="lg:col-span-3">
            {isLoading ? (
              <div className="flex items-center justify-center h-64">
                <div className="text-center">
                  <div className="text-4xl mb-4">⏳</div>
                  <p className="text-gray-600">Loading settings...</p>
                </div>
              </div>
            ) : (
              <motion.div
                key={activeTab}
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.2 }}
              >
                {activeTab === 'profile' && <ProfileSettings />}
                {activeTab === 'predictions' && <PredictionSettings />}
                {activeTab === 'notifications' && <NotificationSettings />}
                {activeTab === 'dashboard' && <DashboardSettings />}
                {activeTab === 'ai' && <AIBehaviorSettings />}
                {activeTab === 'localization' && <LocalizationSettings />}
                {activeTab === 'security' && <SecuritySettings />}
              </motion.div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default SettingsPage;
