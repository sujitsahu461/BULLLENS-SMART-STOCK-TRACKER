import React from 'react';
import { motion } from 'framer-motion';

export const Toggle = ({ label, value, onChange, description, disabled = false }) => {
  return (
    <div className="flex items-center justify-between p-4 bg-light rounded-lg hover:bg-gray-100 transition">
      <div>
        <label className="font-semibold text-gray-900">{label}</label>
        {description && <p className="text-sm text-gray-600 mt-1">{description}</p>}
      </div>
      <button
        onClick={() => !disabled && onChange(!value)}
        disabled={disabled}
        className={`relative inline-flex h-6 w-11 items-center rounded-full transition ${
          value ? 'bg-accent' : 'bg-gray-300'
        } ${disabled ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
      >
        <motion.span
          layout
          className="inline-block h-4 w-4 transform rounded-full bg-white"
          animate={{ x: value ? '1.25rem' : '0.25rem' }}
        />
      </button>
    </div>
  );
};

export const Slider = ({ label, min = 0, max = 100, value, onChange, unit = '' }) => {
  return (
    <div className="p-4 bg-light rounded-lg">
      <div className="flex justify-between items-center mb-3">
        <label className="font-semibold text-gray-900">{label}</label>
        <span className="text-accent font-bold">
          {value}
          {unit}
        </span>
      </div>
      <input
        type="range"
        min={min}
        max={max}
        value={value}
        onChange={(e) => onChange(parseInt(e.target.value))}
        className="w-full h-2 bg-gray-300 rounded-lg appearance-none cursor-pointer accent-accent"
      />
    </div>
  );
};

export const Dropdown = ({ label, value, options, onChange, description }) => {
  return (
    <div className="p-4 bg-light rounded-lg">
      <label className="block font-semibold text-gray-900 mb-2">{label}</label>
      {description && <p className="text-sm text-gray-600 mb-3">{description}</p>}
      <select
        value={value}
        onChange={(e) => onChange(e.target.value)}
        className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-accent"
      >
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
    </div>
  );
};

export const Card = ({ title, description, children, icon: Icon }) => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-white rounded-lg shadow p-6 border border-gray-200"
    >
      <div className="flex items-center mb-4">
        {Icon && <Icon className="text-accent mr-3 text-2xl" />}
        <div>
          <h3 className="font-bold text-lg text-gray-900">{title}</h3>
          {description && <p className="text-sm text-gray-600">{description}</p>}
        </div>
      </div>
      <div>{children}</div>
    </motion.div>
  );
};

export const Button = ({ 
  label, 
  onClick, 
  variant = 'primary', 
  disabled = false, 
  loading = false,
  size = 'md'
}) => {
  const baseStyle = 'font-semibold rounded-lg transition disabled:opacity-50 disabled:cursor-not-allowed';
  
  const sizeStyle = {
    sm: 'px-3 py-1 text-sm',
    md: 'px-6 py-2 text-base',
    lg: 'px-8 py-3 text-lg',
  }[size];

  const variantStyle = {
    primary: 'bg-accent text-white hover:bg-green-600',
    secondary: 'bg-primary text-white hover:bg-blue-600',
    outline: 'border border-primary text-primary hover:bg-primary hover:text-white',
    danger: 'bg-danger text-white hover:bg-red-600',
  }[variant];

  return (
    <button
      onClick={onClick}
      disabled={disabled || loading}
      className={`${baseStyle} ${sizeStyle} ${variantStyle}`}
    >
      {loading ? '⏳ Loading...' : label}
    </button>
  );
};

export const Tooltip = ({ text, children }) => {
  const [isVisible, setIsVisible] = React.useState(false);

  return (
    <div className="relative inline-block">
      <div
        onMouseEnter={() => setIsVisible(true)}
        onMouseLeave={() => setIsVisible(false)}
      >
        {children}
      </div>
      {isVisible && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="absolute z-10 px-3 py-2 bg-gray-900 text-white text-sm rounded-lg whitespace-nowrap bottom-full left-1/2 transform -translate-x-1/2 mb-2"
        >
          {text}
          <div className="absolute w-2 h-2 bg-gray-900 transform rotate-45 -bottom-1 left-1/2 -translate-x-1/2" />
        </motion.div>
      )}
    </div>
  );
};

export const Badge = ({ label, variant = 'primary' }) => {
  const variantStyle = {
    primary: 'bg-blue-100 text-blue-800',
    success: 'bg-green-100 text-green-800',
    warning: 'bg-yellow-100 text-yellow-800',
    danger: 'bg-red-100 text-red-800',
  }[variant];

  return (
    <span className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${variantStyle}`}>
      {label}
    </span>
  );
};
