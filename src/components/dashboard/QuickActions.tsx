/**
 * إجراءات سريعة
 * Quick action buttons
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { Plus, MessageSquare, Database, Key, FileText } from 'lucide-react';

interface ActionItem {
  icon: React.ComponentType<any>;
  label: string;
  description: string;
  path: string;
  color: string;
}

const actions: ActionItem[] = [
  {
    icon: MessageSquare,
    label: 'محادثة جديدة',
    description: 'ابدأ محادثة مع الذكاء الاصطناعي',
    path: '/playground',
    color: 'bg-blue-500'
  },
  {
    icon: Database,
    label: 'إضافة مصدر بيانات',
    description: 'اربط قاعدة بيانات جديدة',
    path: '/data-sources',
    color: 'bg-purple-500'
  },
  {
    icon: Key,
    label: 'إنشاء مفتاح API',
    description: 'أنشئ مفتاح للتكامل',
    path: '/api-keys',
    color: 'bg-green-500'
  },
  {
    icon: FileText,
    label: 'عرض التقارير',
    description: 'تقارير الاستخدام والتكلفة',
    path: '/analytics',
    color: 'bg-orange-500'
  },
];

const QuickActions: React.FC = () => {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100 h-full">
      <h2 className="text-lg font-semibold text-gray-900 mb-4">إجراءات سريعة</h2>

      <div className="space-y-3">
        {actions.map((action, index) => (
          <Link
            key={index}
            to={action.path}
            className="flex items-center gap-4 p-3 rounded-lg hover:bg-gray-50 transition-colors group"
          >
            <div className={`w-10 h-10 ${action.color} rounded-lg flex items-center justify-center`}>
              <action.icon className="w-5 h-5 text-white" />
            </div>
            <div className="flex-1">
              <p className="font-medium text-gray-900 group-hover:text-blue-600">
                {action.label}
              </p>
              <p className="text-sm text-gray-500">{action.description}</p>
            </div>
          </Link>
        ))}
      </div>
    </div>
  );
};

export default QuickActions;
