const mongoose = require('mongoose');

const settingsSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      unique: true,
      index: true
    },

    // 1. User Profile Settings
    profile: {
      riskProfile: {
        type: String,
        enum: ['Beginner', 'Moderate', 'Aggressive'],
        default: 'Moderate'
      },
      preferredCurrency: {
        type: String,
        enum: ['INR', 'USD', 'EUR', 'GBP', 'AUD'],
        default: 'INR'
      },
      brokerageAccounts: [
        {
          accountName: String,
          brokerName: String,
          accountNumber: String,
          isLinked: Boolean,
          linkedAt: Date
        }
      ]
    },

    // 2. Prediction Preferences
    predictions: {
      modelSelection: {
        type: String,
        enum: ['LSTM', 'ML', 'Hybrid'],
        default: 'Hybrid'
      },
      predictionHorizon: {
        type: String,
        enum: ['Intraday', 'Short-term', 'Long-term'],
        default: 'Short-term'
      },
      confidenceThreshold: {
        type: Number,
        min: 0,
        max: 100,
        default: 60
      },
      volatilityFilterEnabled: {
        type: Boolean,
        default: true
      },
      volatilityThreshold: {
        type: Number,
        min: 0,
        max: 100,
        default: 30
      }
    },

    // 3. Notifications & Alerts
    notifications: {
      priceAlerts: {
        enabled: Boolean,
        threshold: Number // percentage change
      },
      predictionAlerts: {
        enabled: Boolean,
        buySellHints: Boolean,
        strongSignalsOnly: Boolean
      },
      newsAlerts: {
        enabled: Boolean,
        categories: [String] // e.g., ['earnings', 'dividends', 'splits']
      },
      channels: {
        email: Boolean,
        push: Boolean,
        sms: Boolean,
        inApp: { type: Boolean, default: true }
      },
      quietHours: {
        enabled: Boolean,
        startTime: String, // HH:MM format
        endTime: String
      }
    },

    // 4. Portfolio Settings
    portfolio: {
      syncRealPortfolio: Boolean,
      realPortfolioApiKey: String,
      demoMode: {
        type: Boolean,
        default: true
      },
      autoTrackPnL: {
        type: Boolean,
        default: true
      },
      riskExposureLimit: {
        type: Number,
        default: 20 // percentage per stock
      }
    },

    // 5. Dashboard Customization
    dashboard: {
      defaultHomepage: {
        type: String,
        enum: ['Portfolio', 'Predictions', 'Watchlist', 'Overview'],
        default: 'Overview'
      },
      chartType: {
        type: String,
        enum: ['Candlestick', 'Line', 'HeikinAshi', 'OHLC'],
        default: 'Candlestick'
      },
      defaultTimeframe: {
        type: String,
        enum: ['1m', '5m', '15m', '1h', '1D', '1W', '1M'],
        default: '1D'
      },
      darkMode: {
        type: Boolean,
        default: false
      },
      compactView: {
        type: Boolean,
        default: false
      }
    },

    // 6. AI Behavior Settings
    aiBehavior: {
      explanationLevel: {
        type: String,
        enum: ['Simple', 'Intermediate', 'Technical'],
        default: 'Intermediate'
      },
      transparencyMode: {
        type: Boolean,
        default: true
      },
      showRiskWarnings: {
        type: Boolean,
        default: true
      },
      autoSuggestions: {
        type: Boolean,
        default: true
      }
    },

    // 7. Data & Market Settings
    market: {
      selectedMarkets: {
        type: [String],
        enum: ['NSE', 'BSE', 'Crypto', 'US'],
        default: ['NSE', 'BSE']
      },
      dataRefreshFrequency: {
        type: String,
        enum: ['Realtime', '5min', '15min', '1h'],
        default: '5min'
      },
      globalIndicatorsEnabled: {
        type: Boolean,
        default: true
      }
    },

    // 8. Security Settings
    security: {
      twoFactorAuth: {
        enabled: Boolean,
        method: {
          type: String,
          enum: ['TOTP', 'Email', 'SMS']
        }
      },
      loginAlerts: {
        type: Boolean,
        default: true
      },
      deviceManagement: [
        {
          deviceId: String,
          deviceName: String,
          lastAccess: Date,
          isActive: Boolean
        }
      ],
      apiKeys: [
        {
          keyName: String,
          createdAt: Date,
          lastUsed: Date,
          isActive: Boolean
        }
      ]
    },

    // 9. Advanced / Pro Settings
    advanced: {
      customIndicators: [
        {
          name: String,
          type: { type: String }, // RSI, MACD, BollingerBands, etc.
          parameters: mongoose.Schema.Types.Mixed
        }
      ],
      backtestingConfig: {
        enabled: Boolean,
        initialCapital: Number,
        startDate: Date,
        endDate: Date
      },
      strategyBuilder: {
        enabled: Boolean,
        customStrategies: [mongoose.Schema.Types.Mixed]
      }
    },

    // 10. Localization
    localization: {
      language: {
        type: String,
        enum: ['en', 'hi', 'es', 'fr', 'de', 'zh', 'ja'],
        default: 'en'
      },
      timezone: {
        type: String,
        default: 'Asia/Kolkata'
      },
      marketHoursSync: {
        type: Boolean,
        default: true
      }
    },

    // AI Recommendations (Bonus feature)
    recommendations: {
      aiSuggestedSettings: mongoose.Schema.Types.Mixed,
      basedOnBehavior: {
        type: Boolean,
        default: false
      },
      lastUpdated: Date
    },

    // What-if Simulation (Bonus feature)
    simulation: {
      enabled: { type: Boolean, default: false },
      simulatedPortfolioValue: Number
    },

    // Audit trail
    auditLog: [
      {
        action: String,
        changedFields: mongoose.Schema.Types.Mixed,
        changedAt: { type: Date, default: Date.now },
        changedBy: String
      }
    ],

    // Timestamps
    createdAt: {
      type: Date,
      default: Date.now
    },
    updatedAt: {
      type: Date,
      default: Date.now
    }
  },
  { timestamps: true }
);

// Index for performance
settingsSchema.index({ userId: 1, updatedAt: -1 });

module.exports = mongoose.model('Settings', settingsSchema);
