import React, { useState } from 'react';
import { Card, Toggle } from './UI';
import { settingsAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiBell } from 'react-icons/fi';

export const NotificationSettings = () => {
  const [notifications, setNotifications] = useState({
    priceAlerts: { enabled: true, threshold: 5 },
    predictionAlerts: { enabled: true, buySellHints: true },
    newsAlerts: { enabled: false },
    channels: { email: true, push: false, sms: false },
    quietHours: { enabled: false, startTime: '22:00', endTime: '08:00' },
  });
  const [isLoading, setIsLoading] = useState(false);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const handleToggle = (category, field, value) => {
    setNotifications({
      ...notifications,
      [category]: {
        ...notifications[category],
        [field]: value,
      },
    });
  };

  const handleSave = async () => {
    try {
      setIsLoading(true);
      await settingsAPI.updateNotificationSettings(notifications);
      addNotification({
        type: 'success',
        message: 'Notification settings updated successfully',
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
      title="Notifications & Alerts"
      description="Control how and when you receive alerts"
      icon={FiBell}
    >
      <div className="space-y-4">
        <div className="border-b pb-4">
          <h4 className="font-semibold text-gray-900 mb-3">Alert Types</h4>
          <Toggle
            label="Price Alerts"
            value={notifications.priceAlerts.enabled}
            onChange={(value) => handleToggle('priceAlerts', 'enabled', value)}
            description="Get notified when stock price changes by threshold"
          />
        </div>

        <div className="border-b pb-4">
          <h4 className="font-semibold text-gray-900 mb-3">Notification Channels</h4>
          <Toggle
            label="Email Notifications"
            value={notifications.channels.email}
            onChange={(value) => handleToggle('channels', 'email', value)}
            description="Receive alerts via email"
          />
          <Toggle
            label="Push Notifications"
            value={notifications.channels.push}
            onChange={(value) => handleToggle('channels', 'push', value)}
            description="Receive browser push notifications"
          />
          <Toggle
            label="SMS Notifications"
            value={notifications.channels.sms}
            onChange={(value) => handleToggle('channels', 'sms', value)}
            description="Receive alerts via SMS"
          />
        </div>

        <div className="border-b pb-4">
          <h4 className="font-semibold text-gray-900 mb-3">Quiet Hours</h4>
          <Toggle
            label="Enable Quiet Hours"
            value={notifications.quietHours.enabled}
            onChange={(value) => handleToggle('quietHours', 'enabled', value)}
            description="Disable notifications during specific hours"
          />
          {notifications.quietHours.enabled && (
            <div className="grid grid-cols-2 gap-4 mt-3">
              <input
                type="time"
                value={notifications.quietHours.startTime}
                onChange={(e) => handleToggle('quietHours', 'startTime', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg"
              />
              <input
                type="time"
                value={notifications.quietHours.endTime}
                onChange={(e) => handleToggle('quietHours', 'endTime', e.target.value)}
                className="px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          )}
        </div>

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

export default NotificationSettings;
