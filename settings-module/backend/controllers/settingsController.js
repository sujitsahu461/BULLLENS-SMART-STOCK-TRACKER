const Settings = require('../models/Settings');
const { auditLog } = require('../middleware/logger');

exports.getSettings = async (req, res, next) => {
  try {
    const settings = await Settings.findOne({ userId: req.user.id });

    if (!settings) {
      // Create default settings if not found
      const newSettings = new Settings({ userId: req.user.id });
      await newSettings.save();
      return res.json({
        success: true,
        data: newSettings
      });
    }

    res.json({
      success: true,
      data: settings
    });
  } catch (error) {
    next(error);
  }
};

exports.updateSettings = async (req, res, next) => {
  try {
    const validatedData = req.validatedData;
    const changes = validatedData;

    const settings = await Settings.findOneAndUpdate(
      { userId: req.user.id },
      {
        ...validatedData,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    if (!settings) {
      // Create new settings if not found
      const newSettings = new Settings({
        userId: req.user.id,
        ...validatedData
      });
      await newSettings.save();
      return res.json({
        success: true,
        message: 'Settings created successfully',
        data: newSettings
      });
    }

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', settings._id, changes, req);

    res.json({
      success: true,
      message: 'Settings updated successfully',
      data: settings
    });
  } catch (error) {
    next(error);
  }
};

exports.updateProfileSettings = async (req, res, next) => {
  try {
    const { riskProfile, preferredCurrency, brokerageAccounts } = req.body;

    const settings = await Settings.findOneAndUpdate(
      { userId: req.user.id },
      {
        'profile.riskProfile': riskProfile,
        'profile.preferredCurrency': preferredCurrency,
        'profile.brokerageAccounts': brokerageAccounts,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', settings._id, { profile: req.body }, req);

    res.json({
      success: true,
      message: 'Profile settings updated',
      data: settings.profile
    });
  } catch (error) {
    next(error);
  }
};

exports.updatePredictionSettings = async (req, res, next) => {
  try {
    const { modelSelection, predictionHorizon, confidenceThreshold, volatilityFilterEnabled } = req.body;

    const settings = await Settings.findOneAndUpdate(
      { userId: req.user.id },
      {
        'predictions.modelSelection': modelSelection,
        'predictions.predictionHorizon': predictionHorizon,
        'predictions.confidenceThreshold': confidenceThreshold,
        'predictions.volatilityFilterEnabled': volatilityFilterEnabled,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', settings._id, { predictions: req.body }, req);

    res.json({
      success: true,
      message: 'Prediction settings updated',
      data: settings.predictions
    });
  } catch (error) {
    next(error);
  }
};

exports.updateNotificationSettings = async (req, res, next) => {
  try {
    const { priceAlerts, predictionAlerts, newsAlerts, channels, quietHours } = req.body;

    const settings = await Settings.findOneAndUpdate(
      { userId: req.user.id },
      {
        'notifications.priceAlerts': priceAlerts,
        'notifications.predictionAlerts': predictionAlerts,
        'notifications.newsAlerts': newsAlerts,
        'notifications.channels': channels,
        'notifications.quietHours': quietHours,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', settings._id, { notifications: req.body }, req);

    res.json({
      success: true,
      message: 'Notification settings updated',
      data: settings.notifications
    });
  } catch (error) {
    next(error);
  }
};

exports.updateDashboardSettings = async (req, res, next) => {
  try {
    const { defaultHomepage, chartType, defaultTimeframe, darkMode, compactView } = req.body;

    const settings = await Settings.findOneAndUpdate(
      { userId: req.user.id },
      {
        'dashboard.defaultHomepage': defaultHomepage,
        'dashboard.chartType': chartType,
        'dashboard.defaultTimeframe': defaultTimeframe,
        'dashboard.darkMode': darkMode,
        'dashboard.compactView': compactView,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', settings._id, { dashboard: req.body }, req);

    res.json({
      success: true,
      message: 'Dashboard settings updated',
      data: settings.dashboard
    });
  } catch (error) {
    next(error);
  }
};

exports.updateAIBehavior = async (req, res, next) => {
  try {
    const { explanationLevel, transparencyMode, showRiskWarnings, autoSuggestions } = req.body;

    const settings = await Settings.findOneAndUpdate(
      { userId: req.user.id },
      {
        'aiBehavior.explanationLevel': explanationLevel,
        'aiBehavior.transparencyMode': transparencyMode,
        'aiBehavior.showRiskWarnings': showRiskWarnings,
        'aiBehavior.autoSuggestions': autoSuggestions,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', settings._id, { aiBehavior: req.body }, req);

    res.json({
      success: true,
      message: 'AI behavior settings updated',
      data: settings.aiBehavior
    });
  } catch (error) {
    next(error);
  }
};

exports.updateLocalization = async (req, res, next) => {
  try {
    const { language, timezone, marketHoursSync } = req.body;

    const settings = await Settings.findOneAndUpdate(
      { userId: req.user.id },
      {
        'localization.language': language,
        'localization.timezone': timezone,
        'localization.marketHoursSync': marketHoursSync,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', settings._id, { localization: req.body }, req);

    res.json({
      success: true,
      message: 'Localization settings updated',
      data: settings.localization
    });
  } catch (error) {
    next(error);
  }
};

exports.resetToDefaults = async (req, res, next) => {
  try {
    const defaultSettings = new Settings({
      userId: req.user.id
    });

    await Settings.findOneAndUpdate(
      { userId: req.user.id },
      defaultSettings,
      { new: true }
    );

    // Log action
    await auditLog(req.user.id, 'UPDATE', 'Settings', null, { action: 'reset_to_defaults' }, req);

    res.json({
      success: true,
      message: 'Settings reset to defaults',
      data: defaultSettings
    });
  } catch (error) {
    next(error);
  }
};

exports.getAuditLog = async (req, res, next) => {
  try {
    const { limit = 50, page = 1 } = req.query;
    const Audit = require('../models/Audit');

    const skip = (page - 1) * limit;

    const auditLogs = await Audit.find({
      userId: req.user.id,
      resourceType: 'Settings'
    }).sort({ timestamp: -1 }).skip(skip).limit(parseInt(limit));

    const total = await Audit.countDocuments({
      userId: req.user.id,
      resourceType: 'Settings'
    });

    res.json({
      success: true,
      data: auditLogs,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total,
        pages: Math.ceil(total / limit)
      }
    });
  } catch (error) {
    next(error);
  }
};
