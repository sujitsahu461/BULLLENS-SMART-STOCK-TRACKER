const express = require('express');
const authController = require('../controllers/authController');
const { validateUserRegistration, validateUserLogin } = require('../middleware/validation');

const router = express.Router();

/**
 * @route POST /api/auth/register
 * @desc Register a new user
 * @access Public
 */
router.post('/register', validateUserRegistration, authController.register);

/**
 * @route POST /api/auth/login
 * @desc Login user
 * @access Public
 */
router.post('/login', validateUserLogin, authController.login);

/**
 * @route POST /api/auth/refresh-token
 * @desc Refresh access token
 * @access Public
 */
router.post('/refresh-token', authController.refreshToken);

/**
 * @route POST /api/auth/logout
 * @desc Logout user
 * @access Private
 */
router.post('/logout', require('../middleware/auth').authenticate, authController.logout);

/**
 * @route POST /api/auth/2fa/enable
 * @desc Enable 2FA
 * @access Private
 */
router.post('/2fa/enable', require('../middleware/auth').authenticate, authController.enable2FA);

/**
 * @route POST /api/auth/2fa/disable
 * @desc Disable 2FA
 * @access Private
 */
router.post('/2fa/disable', require('../middleware/auth').authenticate, authController.disable2FA);

module.exports = router;
