import React from 'react';
import { Sidebar } from '../components/Sidebar';
import './PlaceholderPage.css';

export const Logs: React.FC = () => {
  return (
    <div className="placeholder-page">
      <Sidebar />
      <main className="placeholder-main" dir="rtl">
        <h1>السجلات</h1>
        <p>سيتم تطوير هذه الصفحة قريباً</p>
      </main>
    </div>
  );
};
