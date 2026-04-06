import React, { useState } from 'react';
import { Card, Toggle, Dropdown } from './UI';
import { settingsAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiBot } from 'react-icons/fi';

export const AIBehaviorSettings = () => {
  const [aiBehavior, setAIBehavior] = useState({
    explanationLevel: 'Intermediate',
    transparencyMode: true,
    showRiskWarnings: true,
    autoSuggestions: true,
  });
  const [isLoading, setIsLoading] = useState(false);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const handleChange = (field, value) => {
    setAIBehavior({ ...aiBehavior, [field]: value });
  };

  const handleSave = async () => {
    try {
      setIsLoading(true);
      await settingsAPI.updateAIBehavior(aiBehavior);
      addNotification({
        type: 'success',
        message: 'AI behavior settings updated successfully',
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
      title="AI Behavior Settings"
      description="Configure how AI explains and interacts with you"
      icon={FiBot}
    >
      <div className="space-y-4">
        <Dropdown
          label="Explanation Level"
          value={aiBehavior.explanationLevel}
          options={[
            { label: 'Simple - Plain language', value: 'Simple' },
            { label: 'Intermediate - Balanced detail', value: 'Intermediate' },
            { label: 'Technical - In-depth analysis', value: 'Technical' },
          ]}
          onChange={(value) => handleChange('explanationLevel', value)}
          description="How detailed should AI explanations be?"
        />

        <Toggle
          label="AI Transparency Mode"
          value={aiBehavior.transparencyMode}
          onChange={(value) => handleChange('transparencyMode', value)}
          description="Show AI reasoning and confidence scores"
        />

        <Toggle
          label="Show Risk Warnings"
          value={aiBehavior.showRiskWarnings}
          onChange={(value) => handleChange('showRiskWarnings', value)}
          description="Display warnings about potential risks"
        />

        <Toggle
          label="Auto Suggestions"
          value={aiBehavior.autoSuggestions}
          onChange={(value) => handleChange('autoSuggestions', value)}
          description="Receive automated buy/sell suggestions"
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

export default AIBehaviorSettings;
