const User = require('../models/User');
const { auditLog } = require('../middleware/logger');

exports.getProfile = async (req, res, next) => {
  try {
    const user = await User.findById(req.user.id).populate('settings');

    if (!user) {
      return res.status(404).json({
        success: false,
        message: 'User not found'
      });
    }

    res.json({
      success: true,
      data: {
        id: user._id,
        username: user.username,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName,
        profilePhoto: user.profilePhoto,
        emailVerified: user.emailVerified,
        createdAt: user.createdAt,
        twoFactorEnabled: user.twoFactorEnabled
      }
    });
  } catch (error) {
    next(error);
  }
};

exports.updateProfile = async (req, res, next) => {
  try {
    const { firstName, lastName, preferredCurrency } = req.body;

    const user = await User.findByIdAndUpdate(
      req.user.id,
      {
        firstName,
        lastName,
        updatedAt: Date.now()
      },
      { new: true, runValidators: true }
    );

    // Log action
    await auditLog(user._id, 'UPDATE', 'User', user._id, { firstName, lastName }, req);

    res.json({
      success: true,
      message: 'Profile updated successfully',
      data: {
        id: user._id,
        username: user.username,
        email: user.email,
        firstName: user.firstName,
        lastName: user.lastName
      }
    });
  } catch (error) {
    next(error);
  }
};

exports.changePassword = async (req, res, next) => {
  try {
    const { currentPassword, newPassword } = req.body;

    if (!currentPassword || !newPassword) {
      return res.status(400).json({
        success: false,
        message: 'Current password and new password are required'
      });
    }

    const user = await User.findById(req.user.id).select('+password');

    const isPasswordCorrect = await user.matchPassword(currentPassword);

    if (!isPasswordCorrect) {
      return res.status(401).json({
        success: false,
        message: 'Current password is incorrect'
      });
    }

    user.password = newPassword;
    await user.save();

    // Log action
    await auditLog(user._id, 'UPDATE', 'User', user._id, { action: 'password_changed' }, req);

    res.json({
      success: true,
      message: 'Password changed successfully'
    });
  } catch (error) {
    next(error);
  }
};

exports.getLoginHistory = async (req, res, next) => {
  try {
    const Audit = require('../models/Audit');

    const loginHistory = await Audit.find({
      userId: req.user.id,
      action: 'LOGIN'
    }).sort({ timestamp: -1 }).limit(20);

    res.json({
      success: true,
      data: loginHistory
    });
  } catch (error) {
    next(error);
  }
};

exports.deleteAccount = async (req, res, next) => {
  try {
    const { password } = req.body;

    if (!password) {
      return res.status(400).json({
        success: false,
        message: 'Password required for account deletion'
      });
    }

    const user = await User.findById(req.user.id).select('+password');

    const isPasswordCorrect = await user.matchPassword(password);

    if (!isPasswordCorrect) {
      return res.status(401).json({
        success: false,
        message: 'Incorrect password'
      });
    }

    // Delete user and related settings
    const Settings = require('../models/Settings');
    await Settings.deleteOne({ userId: user._id });
    await User.findByIdAndDelete(user._id);

    // Log action
    await auditLog(user._id, 'DELETE', 'User', user._id, { action: 'account_deleted' }, req);

    res.json({
      success: true,
      message: 'Account deleted successfully'
    });
  } catch (error) {
    next(error);
  }
};
