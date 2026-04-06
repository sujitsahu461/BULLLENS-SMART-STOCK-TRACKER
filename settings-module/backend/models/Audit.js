const mongoose = require('mongoose');

const auditSchema = new mongoose.Schema(
  {
    userId: {
      type: mongoose.Schema.Types.ObjectId,
      ref: 'User',
      required: true,
      index: true
    },
    action: {
      type: String,
      enum: ['CREATE', 'UPDATE', 'DELETE', 'LOGIN', 'LOGOUT', '2FA_ENABLED', '2FA_DISABLED'],
      required: true
    },
    resourceType: {
      type: String,
      enum: ['Settings', 'User', 'ApiKey', 'Device'],
      required: true
    },
    resourceId: String,
    changes: mongoose.Schema.Types.Mixed,
    ipAddress: String,
    userAgent: String,
    status: {
      type: String,
      enum: ['Success', 'Failed'],
      default: 'Success'
    },
    errorMessage: String,
    timestamp: {
      type: Date,
      default: Date.now,
      index: true
    }
  },
  { timestamps: false }
);

// TTL index to automatically delete audit logs after 90 days
auditSchema.index({ timestamp: 1 }, { expireAfterSeconds: 7776000 });

module.exports = mongoose.model('Audit', auditSchema);
