import React from 'react';
import { useAuth } from '../contexts/AuthContext';
import { Sidebar } from '../components/Sidebar';
import './Dashboard.css';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <div className="dashboard-page">
      <Sidebar />
      <main className="dashboard-main" dir="rtl">
        <div className="dashboard-header">
          <h1>مرحباً، {user?.full_name}! 👋</h1>
          <p>لوحة التحكم الرئيسية</p>
        </div>

        <div className="dashboard-grid">
          <div className="dashboard-card">
            <h3>📊 الإحصائيات</h3>
            <p>سيتم إضافة إحصائيات الاستخدام هنا</p>
          </div>

          <div className="dashboard-card">
            <h3>🔑 مفاتيح API</h3>
            <p>إدارة وإنشاء مفاتيح API الخاصة بك</p>
          </div>

          <div className="dashboard-card">
            <h3>💬 مصادر البيانات</h3>
            <p>ربط وإدارة مصادر البيانات الخاصة بك</p>
          </div>

          <div className="dashboard-card">
            <h3>⚙️ الإعدادات</h3>
            <p>تخصيص إعدادات حسابك</p>
          </div>
        </div>
      </main>
    </div>
  );
};
