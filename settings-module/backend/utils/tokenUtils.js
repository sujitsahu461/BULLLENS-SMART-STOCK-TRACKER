const jwt = require("jsonwebtoken");

const generateTokens = (userId) => {
  const accessToken = jwt.sign(
    { userId, type: "access" },
    process.env.JWT_SECRET,
    { expiresIn: process.env.JWT_EXPIRE || "7d" }
  );

  const refreshToken = jwt.sign(
    { userId, type: "refresh" },
    process.env.JWT_SECRET,
    { expiresIn: "30d" }
  );

  return { accessToken, refreshToken };
};

const verifyToken = (token) => {
  try {
    return jwt.verify(token, process.env.JWT_SECRET);
  } catch (error) {
    return null;
  }
};

module.exports = { generateTokens, verifyToken };
