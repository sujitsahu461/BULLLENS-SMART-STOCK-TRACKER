const Joi = require('joi');

exports.validateUserRegistration = (req, res, next) => {
  const schema = Joi.object({
    username: Joi.string().alphanum().min(3).max(30).required(),
    email: Joi.string().email().required(),
    password: Joi.string().min(6).required(),
    firstName: Joi.string().min(2),
    lastName: Joi.string().min(2)
  });

  const { error, value } = schema.validate(req.body);
  if (error) {
    return res.status(400).json({
      success: false,
      message: error.details[0].message
    });
  }
  req.validatedData = value;
  next();
};

exports.validateUserLogin = (req, res, next) => {
  const schema = Joi.object({
    email: Joi.string().email().required(),
    password: Joi.string().min(6).required()
  });

  const { error, value } = schema.validate(req.body);
  if (error) {
    return res.status(400).json({
      success: false,
      message: error.details[0].message
    });
  }
  req.validatedData = value;
  next();
};

exports.validateSettingsUpdate = (req, res, next) => {
  const schema = Joi.object({
    profile: Joi.object({
      riskProfile: Joi.string().valid('Beginner', 'Moderate', 'Aggressive'),
      preferredCurrency: Joi.string().valid('INR', 'USD', 'EUR', 'GBP', 'AUD')
    }),
    predictions: Joi.object({
      modelSelection: Joi.string().valid('LSTM', 'ML', 'Hybrid'),
      predictionHorizon: Joi.string().valid('Intraday', 'Short-term', 'Long-term'),
      confidenceThreshold: Joi.number().min(0).max(100),
      volatilityFilterEnabled: Joi.boolean()
    }),
    notifications: Joi.object({
      priceAlerts: Joi.object({
        enabled: Joi.boolean(),
        threshold: Joi.number()
      }),
      channels: Joi.object({
        email: Joi.boolean(),
        push: Joi.boolean(),
        sms: Joi.boolean(),
        inApp: Joi.boolean()
      })
    }),
    dashboard: Joi.object({
      defaultHomepage: Joi.string().valid('Portfolio', 'Predictions', 'Watchlist', 'Overview'),
      chartType: Joi.string().valid('Candlestick', 'Line', 'HeikinAshi', 'OHLC'),
      defaultTimeframe: Joi.string().valid('1m', '5m', '15m', '1h', '1D', '1W', '1M'),
      darkMode: Joi.boolean()
    }),
    aiBehavior: Joi.object({
      explanationLevel: Joi.string().valid('Simple', 'Intermediate', 'Technical'),
      transparencyMode: Joi.boolean(),
      showRiskWarnings: Joi.boolean(),
      autoSuggestions: Joi.boolean()
    }),
    localization: Joi.object({
      language: Joi.string().valid('en', 'hi', 'es', 'fr', 'de', 'zh', 'ja'),
      timezone: Joi.string()
    })
  });

  const { error, value } = schema.validate(req.body, { abortEarly: false });
  if (error) {
    const errors = error.details.map(d => d.message);
    return res.status(400).json({
      success: false,
      message: 'Validation error',
      errors
    });
  }
  req.validatedData = value;
  next();
};
