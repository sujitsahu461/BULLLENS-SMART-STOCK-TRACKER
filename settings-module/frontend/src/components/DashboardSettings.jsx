import React, { useState } from 'react';
import { Card, Toggle, Dropdown } from './UI';
import { settingsAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiLayout } from 'react-icons/fi';

export const DashboardSettings = () => {
  const [dashboard, setDashboard] = useState({
    defaultHomepage: 'Overview',
    chartType: 'Candlestick',
    defaultTimeframe: '1D',
    darkMode: false,
    compactView: false,
  });
  const [isLoading, setIsLoading] = useState(false);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const handleChange = (field, value) => {
    setDashboard({ ...dashboard, [field]: value });
  };

  const handleSave = async () => {
    try {
      setIsLoading(true);
      await settingsAPI.updateDashboardSettings(dashboard);
      addNotification({
        type: 'success',
        message: 'Dashboard settings updated successfully',
      });
    } catch (error) {
      addNotification({
        type: 'error',
        message: error.response?.data?.message || 'Failed to update settings',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card
      title="Dashboard Customization"
      description="Personalize your dashboard appearance and layout"
      icon={FiLayout}
    >
      <div className="space-y-4">
        <Dropdown
          label="Default Homepage"
          value={dashboard.defaultHomepage}
          options={[
            { label: 'Overview - Dashboard view', value: 'Overview' },
            { label: 'Portfolio - Your holdings', value: 'Portfolio' },
            { label: 'Predictions - AI predictions', value: 'Predictions' },
            { label: 'Watchlist - Monitored stocks', value: 'Watchlist' },
          ]}
          onChange={(value) => handleChange('defaultHomepage', value)}
        />

        <Dropdown
          label="Chart Type"
          value={dashboard.chartType}
          options={[
            { label: 'Candlestick - OHLC bars', value: 'Candlestick' },
            { label: 'Line - Simple line chart', value: 'Line' },
            { label: 'Heikin Ashi - Modified candlestick', value: 'HeikinAshi' },
            { label: 'OHLC - Box format', value: 'OHLC' },
          ]}
          onChange={(value) => handleChange('chartType', value)}
        />

        <Dropdown
          label="Default Timeframe"
          value={dashboard.defaultTimeframe}
          options={[
            { label: '1 Minute', value: '1m' },
            { label: '5 Minutes', value: '5m' },
            { label: '15 Minutes', value: '15m' },
            { label: '1 Hour', value: '1h' },
            { label: '1 Day', value: '1D' },
            { label: '1 Week', value: '1W' },
            { label: '1 Month', value: '1M' },
          ]}
          onChange={(value) => handleChange('defaultTimeframe', value)}
        />

        <Toggle
          label="Dark Mode"
          value={dashboard.darkMode}
          onChange={(value) => handleChange('darkMode', value)}
          description="Enable dark theme for easier viewing"
        />

        <Toggle
          label="Compact View"
          value={dashboard.compactView}
          onChange={(value) => handleChange('compactView', value)}
          description="Display more information in less space"
        />

        <button
          onClick={handleSave}
          disabled={isLoading}
          className="w-full bg-accent text-white py-2 rounded-lg hover:bg-green-600 transition disabled:opacity-50"
        >
          {isLoading ? '⏳ Saving...' : '✓ Save Changes'}
        </button>
      </div>
    </Card>
  );
};

export default DashboardSettings;
