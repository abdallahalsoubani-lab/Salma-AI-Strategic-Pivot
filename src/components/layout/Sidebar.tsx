/**
 * القائمة الجانبية
 * Sidebar Navigation - Arabic
 *
 * Menu Items:
 * - لوحة التحكم (Dashboard) - icon: LayoutDashboard
 * - المحادثات (Playground) - icon: MessageSquare
 * - مصادر البيانات (Data Sources) - icon: Database
 * - مفاتيح API (API Keys) - icon: Key
 * - السجلات (Logs) - icon: FileText
 * - التحليلات (Analytics) - icon: BarChart3
 * - الإعدادات (Settings) - icon: Settings
 *
 * Bottom:
 * - User info + تسجيل الخروج (Logout)
 */

import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  MessageSquare,
  Database,
  Key,
  FileText,
  BarChart3,
  Settings,
  LogOut,
  Sparkles
} from 'lucide-react';

interface MenuItemType {
  path: string;
  icon: React.ComponentType<any>;
  label: string;
}

const menuItems: MenuItemType[] = [
  { path: '/dashboard', icon: LayoutDashboard, label: 'لوحة التحكم' },
  { path: '/playground', icon: MessageSquare, label: 'المحادثات' },
  { path: '/data-sources', icon: Database, label: 'مصادر البيانات' },
  { path: '/api-keys', icon: Key, label: 'مفاتيح API' },
  { path: '/logs', icon: FileText, label: 'السجلات' },
  { path: '/analytics', icon: BarChart3, label: 'التحليلات' },
  { path: '/settings', icon: Settings, label: 'الإعدادات' },
];

interface SidebarProps {
  user?: {
    full_name?: string;
    organization?: string;
  };
  onLogout?: () => void;
}

const Sidebar: React.FC<SidebarProps> = ({
  user = { full_name: 'المستخدم', organization: 'المؤسسة' },
  onLogout = () => {}
}) => {
  return (
    <aside className="fixed right-0 top-0 h-screen w-64 bg-slate-900 text-white flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b border-slate-700">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
            <Sparkles className="w-6 h-6" />
          </div>
          <div>
            <h1 className="font-bold text-lg">بوابة سلمى</h1>
            <p className="text-xs text-slate-400">Enterprise AI Gateway</p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => (
            <li key={item.path}>
              <NavLink
                to={item.path}
                className={({ isActive }) =>
                  `flex items-center gap-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-600 text-white'
                      : 'text-slate-300 hover:bg-slate-800'
                  }`
                }
              >
                <item.icon className="w-5 h-5" />
                <span>{item.label}</span>
              </NavLink>
            </li>
          ))}
        </ul>
      </nav>

      {/* User Info & Logout */}
      <div className="p-4 border-t border-slate-700">
        <div className="flex items-center gap-3 mb-4">
          <div className="w-10 h-10 bg-slate-700 rounded-full flex items-center justify-center">
            <span className="text-sm font-medium">
              {user?.full_name?.charAt(0) || 'U'}
            </span>
          </div>
          <div className="flex-1 min-w-0">
            <p className="font-medium truncate">{user?.full_name}</p>
            <p className="text-xs text-slate-400 truncate">{user?.organization}</p>
          </div>
        </div>
        <button
          onClick={onLogout}
          className="w-full flex items-center gap-3 px-4 py-2 text-slate-300 hover:bg-slate-800 rounded-lg transition-colors"
        >
          <LogOut className="w-5 h-5" />
          <span>تسجيل الخروج</span>
        </button>
      </div>
    </aside>
  );
};

export default Sidebar;
