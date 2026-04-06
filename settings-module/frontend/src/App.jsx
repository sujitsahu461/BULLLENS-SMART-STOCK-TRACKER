import React, { useState } from 'react';
import { User, TrendingUp, Globe, Bell, Palette, Star, Lock, HelpCircle, LogOut, Search } from 'lucide-react';
import ProfileSettings from './components/ProfileSettings';
import PredictionSettings from './components/PredictionSettings';
import NotificationSettings from './components/NotificationSettings';
import DashboardSettings from './components/DashboardSettings';
import AIBehaviorSettings from './components/AIBehaviorSettings';
import LocalizationSettings from './components/LocalizationSettings';
import SecuritySettings from './components/SecuritySettings';
import './styles/index.css';

function App() {
  const [activeTab, setActiveTab] = useState('profile');
  const [searchQuery, setSearchQuery] = useState('');

  const settingsOptions = [
    { id: 'profile', icon: User, title: 'Profile', subtitle: 'Name, email, account info', component: ProfileSettings },
    { id: 'predictions', icon: TrendingUp, title: 'Prediction Preferences', subtitle: 'Mode, confidence threshold, risk level', component: PredictionSettings },
    { id: 'market', icon: Globe, title: 'Market Selection', subtitle: 'NSE, BSE, crypto, US stocks', component: DashboardSettings },
    { id: 'notifications', icon: Bell, title: 'Notifications', subtitle: 'Buy/sell alerts, prediction signals', component: NotificationSettings },
    { id: 'appearance', icon: Palette, title: 'Appearance', subtitle: 'Theme, chart style', component: AIBehaviorSettings },
    { id: 'watchlist', icon: Star, title: 'Watchlist Settings', subtitle: 'Favorite stocks, tracking', component: LocalizationSettings },
    { id: 'security', icon: Lock, title: 'Privacy & Security', subtitle: 'Password, login protection', component: SecuritySettings },
    { id: 'help', icon: HelpCircle, title: 'Help & Feedback', subtitle: 'Help center, report issue', component: DashboardSettings },
  ];

  const filteredSettings = searchQuery
    ? settingsOptions.filter(
        (item) =>
          item.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          item.subtitle.toLowerCase().includes(searchQuery.toLowerCase())
      )
    : settingsOptions;

  const activeSettings = settingsOptions.find((item) => item.id === activeTab);
  const ActiveComponent = activeSettings?.component;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-slate-800 to-slate-900">
      <div className="flex gap-6 p-6 max-w-7xl mx-auto">
        {/* Sidebar */}
        <div className="w-80 flex-shrink-0">
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 sticky top-6">
            {/* Header */}
            <div className="mb-6">
              <div className="flex items-center gap-4 mb-6">
                <div className="w-12 h-12 rounded-full bg-gradient-to-br from-blue-500 to-purple-500 flex items-center justify-center">
                  <User className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h1 className="text-xl font-bold text-white">Settings</h1>
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
            <div className="space-y-3">
              {filteredSettings.length > 0 ? (
                filteredSettings.map((setting) => {
                  const IconComponent = setting.icon;
                  const isActive = activeTab === setting.id;
                  return (
                    <button
                      key={setting.id}
                      onClick={() => setActiveTab(setting.id)}
                      className={`w-full p-4 rounded-xl transition-all duration-200 group text-left ${
                        isActive
                          ? 'bg-gradient-to-r from-blue-600/20 to-purple-600/20 border border-blue-500/30'
                          : 'bg-slate-700/30 border border-slate-600/30 hover:bg-slate-700/50 hover:border-slate-500/50'
                      }`}
                    >
                      <div className="flex items-start gap-4">
                        <div
                          className={`mt-1 p-3 rounded-lg transition-all ${
                            isActive ? 'bg-blue-600 text-white' : 'bg-slate-600/50 text-gray-300 group-hover:text-white'
                          }`}
                        >
                          <IconComponent className="w-5 h-5" />
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className={`font-semibold transition-colors ${
                            isActive ? 'text-blue-300' : 'text-white group-hover:text-blue-300'
                          }`}>
                            {setting.title}
                          </h3>
                          <p className="text-sm text-gray-400 mt-1 line-clamp-2">{setting.subtitle}</p>
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

            {/* Logout Button */}
            <div className="mt-6 pt-6 border-t border-slate-700/50">
              <button className="w-full p-4 rounded-xl bg-red-600/20 border border-red-500/30 hover:bg-red-600/30 hover:border-red-500/50 transition-all duration-200 group flex items-center gap-4 text-left">
                <div className="p-3 rounded-lg bg-red-600/30 group-hover:bg-red-600/50 transition-all">
                  <LogOut className="w-5 h-5 text-red-400 group-hover:text-red-300" />
                </div>
                <div>
                  <h3 className="font-semibold text-red-300 group-hover:text-red-200">Log out</h3>
                  <p className="text-sm text-red-400/70">Sign out of your account</p>
                </div>
              </button>
            </div>
          </div>
        </div>

        {/* Content Area */}
        <div className="flex-1">
          <div className="bg-slate-800/50 border border-slate-700/50 rounded-xl p-8">
            {ActiveComponent ? (
              <ActiveComponent />
            ) : (
              <div className="text-center text-gray-400">
                <p>Select a setting to view</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
