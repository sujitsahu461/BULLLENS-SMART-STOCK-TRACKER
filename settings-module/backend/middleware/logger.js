const Audit = require('../models/Audit');

exports.logRequest = (req, res, next) => {
  const start = Date.now();

  res.on('finish', async () => {
    const duration = Date.now() - start;
    const logEntry = {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration,
      timestamp: new Date().toISOString(),
      ip: req.ip,
      userAgent: req.get('user-agent')
    };

    if (process.env.NODE_ENV !== 'test') {
      console.log(`[${logEntry.timestamp}] ${req.method} ${req.path} - ${res.statusCode} (${duration}ms)`);
    }
  });

  next();
};

exports.auditLog = async (userId, action, resourceType, resourceId, changes, req) => {
  try {
    const audit = new Audit({
      userId,
      action,
      resourceType,
      resourceId,
      changes,
      ipAddress: req.ip,
      userAgent: req.get('user-agent')
    });

    await audit.save();
  } catch (error) {
    console.error('Audit log error:', error);
    // Don't throw error - logging should not break main flow
  }
};

exports.logAction = (req, res, next) => {
  res.on('finish', async () => {
    // Log only on success
    if (res.statusCode >= 200 && res.statusCode < 300 && req.user) {
      const { auditLog } = res.locals || {};
      if (auditLog) {
        await exports.auditLog(
          req.user.id,
          auditLog.action,
          auditLog.resourceType,
          auditLog.resourceId,
          auditLog.changes,
          req
        );
      }
    }
  });

  next();
};
