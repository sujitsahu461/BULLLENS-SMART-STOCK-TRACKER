exports.errorHandler = (err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || 'Internal Server Error';

  // Validation errors
  if (err.name === 'ValidationError') {
    const errors = Object.values(err.errors).map(e => e.message);
    return res.status(400).json({
      success: false,
      statusCode: 400,
      message: 'Validation Error',
      errors
    });
  }

  // Cast errors (Invalid MongoDB ID)
  if (err.name === 'CastError') {
    return res.status(400).json({
      success: false,
      statusCode: 400,
      message: 'Invalid ID format'
    });
  }

  // Duplicate key errors
  if (err.code === 11000) {
    const field = Object.keys(err.keyPattern)[0];
    return res.status(409).json({
      success: false,
      statusCode: 409,
      message: `${field} already exists`
    });
  }

  // JWT errors
  if (err.name === 'JsonWebTokenError') {
    return res.status(401).json({
      success: false,
      statusCode: 401,
      message: 'Invalid token'
    });
  }

  // Default error response
  res.status(status).json({
    success: false,
    statusCode: status,
    message,
    ...(process.env.NODE_ENV === 'development' && { stack: err.stack })
  });
};

module.exports = exports.errorHandler;
