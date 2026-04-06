import React, { useState } from 'react';
import { Card, Dropdown, Slider } from './UI';
import { settingsAPI } from '../utils/api';
import { useNotificationStore } from '../context/store';
import { FiTrendingUp } from 'react-icons/fi';

export const PredictionSettings = () => {
  const [predictions, setPredictions] = useState({
    modelSelection: 'Hybrid',
    predictionHorizon: 'Short-term',
    confidenceThreshold: 60,
    volatilityFilterEnabled: true,
  });
  const [isLoading, setIsLoading] = useState(false);
  const addNotification = useNotificationStore((state) => state.addNotification);

  const handleChange = (field, value) => {
    setPredictions({ ...predictions, [field]: value });
  };

  const handleSave = async () => {
    try {
      setIsLoading(true);
      await settingsAPI.updatePredictionSettings(predictions);
      addNotification({
        type: 'success',
        message: 'Prediction settings updated successfully',
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
      title="Prediction Preferences"
      description="Configure how predictions are generated and displayed"
      icon={FiTrendingUp}
    >
      <div className="space-y-4">
        <Dropdown
          label="Prediction Model"
          value={predictions.modelSelection}
          options={[
            { label: 'LSTM - Deep Learning', value: 'LSTM' },
            { label: 'ML - Machine Learning', value: 'ML' },
            { label: 'Hybrid - Combined approach', value: 'Hybrid' },
          ]}
          onChange={(value) => handleChange('modelSelection', value)}
          description="Choose the algorithm for price predictions"
        />

        <Dropdown
          label="Prediction Horizon"
          value={predictions.predictionHorizon}
          options={[
            { label: 'Intraday - Minutes to hours', value: 'Intraday' },
            { label: 'Short-term - Days to weeks', value: 'Short-term' },
            { label: 'Long-term - Months to years', value: 'Long-term' },
          ]}
          onChange={(value) => handleChange('predictionHorizon', value)}
          description="Select your trading timeframe"
        />

        <Slider
          label="Confidence Threshold"
          min={0}
          max={100}
          value={predictions.confidenceThreshold}
          onChange={(value) => handleChange('confidenceThreshold', value)}
          unit="%"
        />

        <div className="p-4 bg-light rounded-lg">
          <label className="flex items-center">
            <input
              type="checkbox"
              checked={predictions.volatilityFilterEnabled}
              onChange={(e) => handleChange('volatilityFilterEnabled', e.target.checked)}
              className="w-5 h-5 text-accent rounded cursor-pointer"
            />
            <span className="ml-3 font-semibold text-gray-900">
              Enable Volatility Filter
            </span>
          </label>
          <p className="text-sm text-gray-600 mt-2 ml-8">
            Exclude highly volatile stocks from predictions
          </p>
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

export default PredictionSettings;
