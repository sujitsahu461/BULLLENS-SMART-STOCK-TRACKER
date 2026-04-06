const User = require('../models/User');
const Settings = require('../models/Settings');
const jwt = require('jsonwebtoken');
const { auditLog } = require('../middleware/logger');

const generateTokens = (userId, email) => {
  const accessToken = jwt.sign(
    { id: userId, email },
    process.env.JWT_SECRET || 'your_super_secret_jwt_key_change_in_production',
    { expiresIn: process.env.JWT_EXPIRE || '7d' }
  );

  const refreshToken = jwt.sign(
    { id: userId },
    process.env.JWT_REFRESH_SECRET || 'your_super_secret_refresh_key_change_in_production',
    { expiresIn: process.env.JWT_REFRESH_EXPIRE || '30d' }
  );

  return { accessToken, refreshToken };
};

exports.register = async (req, res, next) => {
  try {
    const { username, email, password, firstName, lastName } = req.validatedData;

    // Check if user already exists
    const existingUser = await User.findOne({
      $or: [{ email }, { username }]
    });

    if (existingUser) {
      return res.status(409).json({
        success: false,
        message: 'User already exists with this email or username'
      });
    }

    // Create user
    const user = new User({
      username,
      email,
      password,
      firstName,
      lastName
    });

    await user.save();

    // Create default settings
    const settings = new Settings({
      userId: user._id
    });

    await settings.save();

    // Update user with settings reference
    user.settings = settings._id;
    await user.save();

    // Log action
    await auditLog(user._id, 'CREATE', 'User', user._id, {}, req);

    // Generate tokens
    const { accessToken, refreshToken } = generateTokens(user._id, user.email);

    res.status(201).json({
      success: true,
      message: 'User registered successfully',
      data: {
        userId: user._id,
        username: user.username,
        email: user.email,
        accessToken,
        refreshToken
      }
    });
  } catch (error) {
    next(error);
  }
};

exports.login = async (req, res, next) => {
  try {
    const { email, password } = req.validatedData;

    // Find user
    const user = await User.findOne({ email }).select('+password');

    if (!user) {
      return res.status(401).json({
        success: false,
        message: 'Invalid credentials'
      });
    }

    // Check if account is locked
    if (user.isLocked()) {
      return res.status(429).json({
        success: false,
        message: 'Account is locked due to too many login attempts. Try again later.'
      });
    }

    // Check password
    const isPasswordCorrect = await user.matchPassword(password);

    if (!isPasswordCorrect) {
      await user.incLoginAttempts();
      return res.status(401).json({
        success: false,
        message: 'Invalid credentials'
      });
    }

    // Reset login attempts
    await user.resetLoginAttempts();

    // Update last login
    user.lastLogin = Date.now();
    await user.save();

    // Log action
    await auditLog(user._id, 'LOGIN', 'User', user._id, {}, req);

    // Generate tokens
    const { accessToken, refreshToken } = generateTokens(user._id, user.email);

    res.json({
      success: true,
      message: 'Login successful',
      data: {
        userId: user._id,
        username: user.username,
        email: user.email,
        accessToken,
        refreshToken
      }
    });
  } catch (error) {
    next(error);
  }
};

exports.refreshToken = async (req, res, next) => {
  try {
    const { refreshToken } = req.body;

    if (!refreshToken) {
      return res.status(400).json({
        success: false,
        message: 'Refresh token required'
      });
    }

    const decoded = jwt.verify(
      refreshToken,
      process.env.JWT_REFRESH_SECRET || 'your_super_secret_refresh_key_change_in_production'
    );

    const user = await User.findById(decoded.id);

    if (!user || !user.isActive) {
      return res.status(401).json({
        success: false,
        message: 'User not found or inactive'
      });
    }

    const { accessToken, refreshToken: newRefreshToken } = generateTokens(user._id, user.email);

    res.json({
      success: true,
      data: {
        accessToken,
        refreshToken: newRefreshToken
      }
    });
  } catch (error) {
    next(error);
  }
};

exports.logout = async (req, res, next) => {
  try {
    // Log action
    await auditLog(req.user.id, 'LOGOUT', 'User', req.user.id, {}, req);

    res.json({
      success: true,
      message: 'Logout successful'
    });
  } catch (error) {
    next(error);
  }
};

exports.enable2FA = async (req, res, next) => {
  try {
    const { method } = req.body; // TOTP, Email, SMS

    if (!['TOTP', 'Email', 'SMS'].includes(method)) {
      return res.status(400).json({
        success: false,
        message: 'Invalid 2FA method'
      });
    }

    const user = await User.findById(req.user.id);
    user.twoFactorEnabled = true;
    user.security = { ...user.security, twoFactorAuth: { enabled: true, method } };

    await user.save();

    // Log action
    await auditLog(user._id, '2FA_ENABLED', 'User', user._id, { method }, req);

    res.json({
      success: true,
      message: `2FA enabled with ${method}`
    });
  } catch (error) {
    next(error);
  }
};

exports.disable2FA = async (req, res, next) => {
  try {
    const user = await User.findById(req.user.id);
    user.twoFactorEnabled = false;

    await user.save();

    // Log action
    await auditLog(user._id, '2FA_DISABLED', 'User', user._id, {}, req);

    res.json({
      success: true,
      message: '2FA disabled successfully'
    });
  } catch (error) {
    next(error);
  }
};
