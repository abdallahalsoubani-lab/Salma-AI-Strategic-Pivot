/**
 * التخطيط الرئيسي للوحة التحكم
 * Main Dashboard Layout - Arabic RTL
 *
 * Structure:
 * ┌─────────────────────────────────────────────────┐
 * │  Header (الشريط العلوي)                          │
 * ├────────────┬────────────────────────────────────┤
 * │            │                                    │
 * │  Sidebar   │         Main Content              │
 * │  (القائمة) │         (المحتوى الرئيسي)           │
 * │            │                                    │
 * │            │                                    │
 * └────────────┴────────────────────────────────────┘
 */

import React from 'react';
import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';

const DashboardLayout: React.FC = () => {
  return (
    <div className="min-h-screen bg-gray-50" dir="rtl">
      <Sidebar />
      <div className="mr-64"> {/* margin-right for RTL sidebar */}
        <Header />
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default DashboardLayout;
