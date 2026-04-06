import React, { useState } from 'react';
import { Card, Toggle, Dropdown } from './UI';
import { settingsAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiGlobe } from 'react-icons/fi';

export const LocalizationSettings = () => {
  const [localization, setLocalization] = useState({
    language: 'en',
    timezone: 'Asia/Kolkata',
    marketHoursSync: true,
  });
  const [isLoading, setIsLoading] = useState(false);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const handleChange = (field, value) => {
    setLocalization({ ...localization, [field]: value });
  };

  const handleSave = async () => {
    try {
      setIsLoading(true);
      await settingsAPI.updateLocalization(localization);
      addNotification({
        type: 'success',
        message: 'Localization settings updated successfully',
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
      title="Localization"
      description="Set your language, timezone, and regional preferences"
      icon={FiGlobe}
    >
      <div className="space-y-4">
        <Dropdown
          label="Language"
          value={localization.language}
          options={[
            { label: '🇬🇧 English', value: 'en' },
            { label: '🇮🇳 Hindi', value: 'hi' },
            { label: '🇪🇸 Spanish', value: 'es' },
            { label: '🇫🇷 French', value: 'fr' },
            { label: '🇩🇪 German', value: 'de' },
            { label: '🇨🇳 Chinese', value: 'zh' },
            { label: '🇯🇵 Japanese', value: 'ja' },
          ]}
          onChange={(value) => handleChange('language', value)}
        />

        <Dropdown
          label="Timezone"
          value={localization.timezone}
          options={[
            { label: 'Asia/Kolkata (IST)', value: 'Asia/Kolkata' },
            { label: 'America/New_York (EST)', value: 'America/New_York' },
            { label: 'Europe/London (GMT)', value: 'Europe/London' },
            { label: 'Asia/Tokyo (JST)', value: 'Asia/Tokyo' },
            { label: 'Australia/Sydney (AEDT)', value: 'Australia/Sydney' },
          ]}
          onChange={(value) => handleChange('timezone', value)}
          description="Select your local timezone for accurate time displays"
        />

        <Toggle
          label="Sync with Market Hours"
          value={localization.marketHoursSync}
          onChange={(value) => handleChange('marketHoursSync', value)}
          description="Automatically adjust view based on stock market hours"
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

export default LocalizationSettings;
