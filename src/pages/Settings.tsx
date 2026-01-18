/**
 * صفحة الإعدادات
 * Settings Page
 */

import React, { useState } from 'react';
import { User, Bell, Shield, Palette } from 'lucide-react';

interface TabItem {
  id: string;
  label: string;
  icon: React.ComponentType<any>;
}

const Settings: React.FC = () => {
  const [activeTab, setActiveTab] = useState('profile');

  const tabs: TabItem[] = [
    { id: 'profile', label: 'الملف الشخصي', icon: User },
    { id: 'notifications', label: 'الإشعارات', icon: Bell },
    { id: 'security', label: 'الأمان', icon: Shield },
    { id: 'appearance', label: 'المظهر', icon: Palette },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">الإعدادات</h1>
        <p className="text-gray-500">إدارة حسابك وتفضيلاتك</p>
      </div>

      <div className="bg-white rounded-xl border border-gray-200">
        {/* Tabs */}
        <div className="border-b border-gray-200">
          <nav className="flex gap-8 px-6">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 py-4 border-b-2 transition-colors ${
                  activeTab === tab.id
                    ? 'border-blue-600 text-blue-600'
                    : 'border-transparent text-gray-500 hover:text-gray-700'
                }`}
              >
                <tab.icon className="w-5 h-5" />
                <span>{tab.label}</span>
              </button>
            ))}
          </nav>
        </div>

        {/* Content */}
        <div className="p-6">
          {activeTab === 'profile' && (
            <div className="max-w-lg space-y-6">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  الاسم الكامل
                </label>
                <input
                  type="text"
                  defaultValue="أحمد محمد"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  البريد الإلكتروني
                </label>
                <input
                  type="email"
                  defaultValue="ahmed@company.com"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  المؤسسة
                </label>
                <input
                  type="text"
                  defaultValue="شركة التقنية"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                حفظ التغييرات
              </button>
            </div>
          )}

          {activeTab === 'notifications' && (
            <div className="max-w-lg space-y-4">
              <div className="flex items-center justify-between py-3">
                <div>
                  <p className="font-medium">إشعارات البريد الإلكتروني</p>
                  <p className="text-sm text-gray-500">استلم تقارير الاستخدام أسبوعياً</p>
                </div>
                <input type="checkbox" defaultChecked className="w-5 h-5" />
              </div>
              <div className="flex items-center justify-between py-3">
                <div>
                  <p className="font-medium">تنبيهات التكلفة</p>
                  <p className="text-sm text-gray-500">تنبيه عند تجاوز حد معين</p>
                </div>
                <input type="checkbox" defaultChecked className="w-5 h-5" />
              </div>
              <div className="flex items-center justify-between py-3">
                <div>
                  <p className="font-medium">تنبيهات الأخطاء</p>
                  <p className="text-sm text-gray-500">إشعار فوري عند حدوث أخطاء</p>
                </div>
                <input type="checkbox" className="w-5 h-5" />
              </div>
            </div>
          )}

          {activeTab === 'security' && (
            <div className="max-w-lg space-y-6">
              <div>
                <h3 className="font-medium text-gray-900 mb-2">تغيير كلمة المرور</h3>
                <input
                  type="password"
                  placeholder="كلمة المرور الحالية"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-3"
                />
                <input
                  type="password"
                  placeholder="كلمة المرور الجديدة"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg mb-3"
                />
                <input
                  type="password"
                  placeholder="تأكيد كلمة المرور"
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                />
              </div>
              <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                تحديث كلمة المرور
              </button>
            </div>
          )}

          {activeTab === 'appearance' && (
            <div className="max-w-lg space-y-6">
              <div>
                <h3 className="font-medium text-gray-900 mb-4">المظهر</h3>
                <div className="space-y-3">
                  <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer">
                    <input type="radio" name="theme" defaultChecked />
                    <span>الوضع الفاتح</span>
                  </label>
                  <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer">
                    <input type="radio" name="theme" />
                    <span>الوضع الداكن</span>
                  </label>
                  <label className="flex items-center gap-3 p-3 border border-gray-200 rounded-lg cursor-pointer">
                    <input type="radio" name="theme" />
                    <span>تتبع النظام</span>
                  </label>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default Settings;
