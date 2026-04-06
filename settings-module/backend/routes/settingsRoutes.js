const express = require('express');
const settingsController = require('../controllers/settingsController');
const { authenticate } = require('../middleware/auth');
const { validateSettingsUpdate } = require('../middleware/validation');

const router = express.Router();

/**
 * @route GET /api/settings
 * @desc Get all user settings
 * @access Private
 */
router.get('/', authenticate, settingsController.getSettings);

/**
 * @route PATCH /api/settings
 * @desc Update multiple settings sections
 * @access Private
 */
router.patch('/', authenticate, validateSettingsUpdate, settingsController.updateSettings);

/**
 * @route PUT /api/settings/profile
 * @desc Update profile settings
 * @access Private
 */
router.put('/profile', authenticate, settingsController.updateProfileSettings);

/**
 * @route PUT /api/settings/predictions
 * @desc Update prediction settings
 * @access Private
 */
router.put('/predictions', authenticate, settingsController.updatePredictionSettings);

/**
 * @route PUT /api/settings/notifications
 * @desc Update notification settings
 * @access Private
 */
router.put('/notifications', authenticate, settingsController.updateNotificationSettings);

/**
 * @route PUT /api/settings/dashboard
 * @desc Update dashboard settings
 * @access Private
 */
router.put('/dashboard', authenticate, settingsController.updateDashboardSettings);

/**
 * @route PUT /api/settings/ai-behavior
 * @desc Update AI behavior settings
 * @access Private
 */
router.put('/ai-behavior', authenticate, settingsController.updateAIBehavior);

/**
 * @route PUT /api/settings/localization
 * @desc Update localization settings
 * @access Private
 */
router.put('/localization', authenticate, settingsController.updateLocalization);

/**
 * @route POST /api/settings/reset
 * @desc Reset settings to defaults
 * @access Private
 */
router.post('/reset', authenticate, settingsController.resetToDefaults);

/**
 * @route GET /api/settings/audit-log
 * @desc Get settings audit log
 * @access Private
 */
router.get('/audit-log', authenticate, settingsController.getAuditLog);

module.exports = router;
