import React, { useState, useMemo } from 'react';
import {
  User,
  TrendingUp,
  Globe,
  Bell,
  Palette,
  Star,
  Lock,
  HelpCircle,
  LogOut,
  Search,
} from 'lucide-react';

export default function SettingsSidebar() {
  const [searchQuery, setSearchQuery] = useState('');
  const [activeItem, setActiveItem] = useState('profile');

  const settingsOptions = [
    {
      id: 'profile',
      icon: User,
      title: 'Profile',
      subtitle: 'Name, email, account info',
      color: 'from-blue-500 to-blue-600',
    },
    {
      id: 'predictions',
      icon: TrendingUp,
      title: 'Prediction Preferences',
      subtitle: 'Mode, confidence threshold, risk level',
      color: 'from-green-500 to-green-600',
    },
    {
      id: 'market',
      icon: Globe,
      title: 'Market Selection',
      subtitle: 'NSE, BSE, crypto, US stocks',
      color: 'from-purple-500 to-purple-600',
    },
    {
      id: 'notifications',
      icon: Bell,
      title: 'Notifications',
      subtitle: 'Buy/sell alerts, prediction signals',
      color: 'from-orange-500 to-orange-600',
    },
    {
      id: 'appearance',
      icon: Palette,
      title: 'Appearance',
      subtitle: 'Theme, chart style',
      color: 'from-pink-500 to-pink-600',
    },
    {
      id: 'watchlist',
      icon: Star,
      title: 'Watchlist Settings',
      subtitle: 'Favorite stocks, tracking',
      color: 'from-yellow-500 to-yellow-600',
    },
    {
      id: 'security',
      icon: Lock,
      title: 'Privacy & Security',
      subtitle: 'Password, login protection',
      color: 'from-red-500 to-red-600',
    },
    {
      id: 'help',
      icon: HelpCircle,
      title: 'Help & Feedback',
      subtitle: 'Help center, report issue',
      color: 'from-cyan-500 to-cyan-600',
    },
  ];

  const filteredSettings = useMemo(() => {
    if (!searchQuery) return settingsOptions;
    return settingsOptions.filter(
      (item) =>
        item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
        item.subtitle.toLowerCase().includes(searchQuery.toLowerCase())
    );
  }, [searchQuery]);

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900 p-6">
      <div className="max-w-md mx-auto">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center gap-4 mb-6">
            <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
              <User className="w-6 h-6 text-white" />
            </div>
            <div>
              <h1 className="text-xl font-bold text-white">John Trader</h1>
              <p className="text-sm text-gray-400">Manage your account</p>
            </div>
          </div>

          {/* Search Bar */}
          <div className="relative">
            <Search className="absolute left-3 top-3.5 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search settings..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-slate-700/50 border border-slate-600 rounded-lg text-white placeholder-gray-400 focus:outline-none focus:border-blue-500 focus:ring-2 focus:ring-blue-500/20 transition"
            />
          </div>
        </div>

        {/* Settings List */}
        <div className="space-y-3 mb-6">
          {filteredSettings.length > 0 ? (
            filteredSettings.map((setting) => {
              const IconComponent = setting.icon;
              const isActive = activeItem === setting.id;

              return (
                <button
                  key={setting.id}
                  onClick={() => setActiveItem(setting.id)}
                  className={`w-full p-4 rounded-xl transition-all duration-200 group text-left ${
                    isActive
                      ? 'bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30'
                      : 'bg-slate-700/30 border border-slate-600/30 hover:bg-slate-700/50 hover:border-slate-500/50'
                  }`}
                >
                  <div className="flex items-start gap-4">
                    {/* Icon */}
                    <div
                      className={`mt-1 p-3 rounded-lg transition-all ${
                        isActive
                          ? `bg-gradient-to-br ${setting.color}`
                          : 'bg-slate-600/50 group-hover:bg-slate-600'
                      }`}
                    >
                      <IconComponent
                        className={`w-5 h-5 ${isActive ? 'text-white' : 'text-gray-300 group-hover:text-white'}`}
                      />
                    </div>

                    {/* Content */}
                    <div className="flex-1 min-w-0">
                      <h3
                        className={`font-semibold transition-colors ${
                          isActive ? 'text-blue-300' : 'text-white group-hover:text-blue-300'
                        }`}
                      >
                        {setting.title}
                      </h3>
                      <p className="text-sm text-gray-400 mt-1 line-clamp-2">
                        {setting.subtitle}
                      </p>
                    </div>

                    {/* Arrow */}
                    <div
                      className={`mt-1 opacity-0 group-hover:opacity-100 transition-opacity ${
                        isActive ? 'opacity-100' : ''
                      }`}
                    >
                      <svg
                        className="w-5 h-5 text-gray-400"
                        fill="none"
                        stroke="currentColor"
                        viewBox="0 0 24 24"
                      >
                        <path
                          strokeLinecap="round"
                          strokeLinejoin="round"
                          strokeWidth={2}
                          d="M9 5l7 7-7 7"
                        />
                      </svg>
                    </div>
                  </div>
                </button>
              );
            })
          ) : (
            <div className="py-12 text-center">
              <Search className="w-8 h-8 text-gray-500 mx-auto mb-2" />
              <p className="text-gray-400">No settings found</p>
            </div>
          )}
        </div>

        {/* Divider */}
        <div className="h-px bg-gradient-to-r from-transparent via-slate-600 to-transparent my-6" />

        {/* Logout Button */}
        <button
          onClick={() => console.log('Logout clicked')}
          className="w-full p-4 rounded-xl bg-red-600/20 border border-red-500/30 hover:bg-red-600/30 hover:border-red-500/50 transition-all duration-200 group flex items-center gap-4 text-left"
        >
          <div className="p-3 rounded-lg bg-red-600/30 group-hover:bg-red-600/50 transition-all">
            <LogOut className="w-5 h-5 text-red-400 group-hover:text-red-300" />
          </div>
          <div>
            <h3 className="font-semibold text-red-300 group-hover:text-red-200">Log out</h3>
            <p className="text-sm text-red-400/70">Sign out of your account</p>
          </div>
        </button>

        {/* Footer */}
        <div className="mt-8 pt-6 border-t border-slate-700/50 text-center">
          <p className="text-xs text-gray-500">BullLens v1.0.0</p>
          <p className="text-xs text-gray-500 mt-1">Stock Market Predictor</p>
        </div>
      </div>
    </div>
  );
}
