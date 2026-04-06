import React, { useState, useEffect } from 'react';
import { Card, Toggle, Dropdown } from './UI';
import { settingsAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiUser } from 'react-icons/fi';

export const ProfileSettings = () => {
  const [profile, setProfile] = useState({
    riskProfile: 'Moderate',
    preferredCurrency: 'INR',
  });
  const [isLoading, setIsLoading] = useState(false);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const handleChange = (field, value) => {
    setProfile({ ...profile, [field]: value });
  };

  const handleSave = async () => {
    try {
      setIsLoading(true);
      await settingsAPI.updateProfileSettings(profile);
      addNotification({
        type: 'success',
        message: 'Profile settings updated successfully',
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
      title="User Profile"
      description="Manage your profile and account preferences"
      icon={FiUser}
    >
      <div className="space-y-4">
        <Dropdown
          label="Risk Profile"
          value={profile.riskProfile}
          options={[
            { label: 'Beginner - Conservative approach', value: 'Beginner' },
            { label: 'Moderate - Balanced approach', value: 'Moderate' },
            { label: 'Aggressive - High-risk tolerant', value: 'Aggressive' },
          ]}
          onChange={(value) => handleChange('riskProfile', value)}
          description="Choose how aggressive or conservative your trading should be"
        />

        <Dropdown
          label="Preferred Currency"
          value={profile.preferredCurrency}
          options={[
            { label: '₹ Indian Rupee (INR)', value: 'INR' },
            { label: '$ US Dollar (USD)', value: 'USD' },
            { label: '€ Euro (EUR)', value: 'EUR' },
            { label: '£ British Pound (GBP)', value: 'GBP' },
            { label: '$ Australian Dollar (AUD)', value: 'AUD' },
          ]}
          onChange={(value) => handleChange('preferredCurrency', value)}
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

export default ProfileSettings;
