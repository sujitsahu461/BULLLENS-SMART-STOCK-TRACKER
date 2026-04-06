const express = require('express');
const userController = require('../controllers/userController');
const { authenticate } = require('../middleware/auth');

const router = express.Router();

/**
 * @route GET /api/users/profile
 * @desc Get user profile
 * @access Private
 */
router.get('/profile', authenticate, userController.getProfile);

/**
 * @route PUT /api/users/profile
 * @desc Update user profile
 * @access Private
 */
router.put('/profile', authenticate, userController.updateProfile);

/**
 * @route POST /api/users/change-password
 * @desc Change user password
 * @access Private
 */
router.post('/change-password', authenticate, userController.changePassword);

/**
 * @route GET /api/users/login-history
 * @desc Get user login history
 * @access Private
 */
router.get('/login-history', authenticate, userController.getLoginHistory);

/**
 * @route DELETE /api/users/account
 * @desc Delete user account
 * @access Private
 */
router.delete('/account', authenticate, userController.deleteAccount);

module.exports = router;
