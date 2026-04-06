import React, { useState } from 'react';
import { Card, Toggle } from './UI';
import { authAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiLock } from 'react-icons/fi';

export const SecuritySettings = () => {
  const [security, setSecurity] = useState({
    twoFactorAuth: false,
    loginAlerts: true,
  });
  const [isLoading, setIsLoading] = useState(false);
  const [show2FAModal, setShow2FAModal] = useState(false);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const handle2FAChange = async (value) => {
    if (value) {
      setShow2FAModal(true);
    } else {
      try {
        setIsLoading(true);
        await authAPI.disable2FA();
        setSecurity({ ...security, twoFactorAuth: false });
        addNotification({
          type: 'success',
          message: '2FA disabled successfully',
        });
      } catch (error) {
        addNotification({
          type: 'error',
          message: 'Failed to disable 2FA',
        });
      } finally {
        setIsLoading(false);
      }
    }
  };

  const handleEnable2FA = async (method) => {
    try {
      setIsLoading(true);
      await authAPI.enable2FA({ method });
      setSecurity({ ...security, twoFactorAuth: true });
      setShow2FAModal(false);
      addNotification({
        type: 'success',
        message: `2FA enabled via ${method}`,
      });
    } catch (error) {
      addNotification({
        type: 'error',
        message: 'Failed to enable 2FA',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card
      title="Security Settings"
      description="Manage your account security and access"
      icon={FiLock}
    >
      <div className="space-y-4">
        <Toggle
          label="Two-Factor Authentication"
          value={security.twoFactorAuth}
          onChange={handle2FAChange}
          description="Add an extra layer of security to your account"
        />

        <Toggle
          label="Login Alerts"
          value={security.loginAlerts}
          onChange={(value) => setSecurity({ ...security, loginAlerts: value })}
          description="Get notified of new login attempts"
        />

        <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
          <h4 className="font-semibold text-blue-900 mb-2">Security Tips</h4>
          <ul className="text-sm text-blue-800 space-y-2">
            <li>✓ Use a strong, unique password</li>
            <li>✓ Enable two-factor authentication</li>
            <li>✓ Review login history regularly</li>
            <li>✓ Never share your API keys</li>
          </ul>
        </div>

        {show2FAModal && (
          <div className="p-4 bg-warning bg-opacity-10 rounded-lg border border-warning">
            <h4 className="font-semibold text-gray-900 mb-3">Enable 2FA</h4>
            <div className="space-y-2">
              <button
                onClick={() => handleEnable2FA('TOTP')}
                disabled={isLoading}
                className="w-full p-3 text-left bg-light hover:bg-gray-200 rounded-lg transition"
              >
                <span className="font-semibold">Authenticator App</span>
                <p className="text-sm text-gray-600">Use Google Authenticator</p>
              </button>
              <button
                onClick={() => handleEnable2FA('Email')}
                disabled={isLoading}
                className="w-full p-3 text-left bg-light hover:bg-gray-200 rounded-lg transition"
              >
                <span className="font-semibold">Email</span>
                <p className="text-sm text-gray-600">Codes sent to your email</p>
              </button>
              <button
                onClick={() => handleEnable2FA('SMS')}
                disabled={isLoading}
                className="w-full p-3 text-left bg-light hover:bg-gray-200 rounded-lg transition"
              >
                <span className="font-semibold">SMS</span>
                <p className="text-sm text-gray-600">Codes sent via SMS</p>
              </button>
            </div>
          </div>
        )}
      </div>
    </Card>
  );
};

export default SecuritySettings;
