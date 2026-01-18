/**
 * النشاط الأخير
 * Recent requests/activity log
 */

import React from 'react';
import { MessageSquare, CheckCircle, XCircle, Clock } from 'lucide-react';

interface Activity {
  id: number;
  type: string;
  message: string;
  provider: string;
  status: 'success' | 'error';
  time: string;
  tokens: number;
  cost: number;
}

const activities: Activity[] = [
  {
    id: 1,
    type: 'chat',
    message: 'استعلام عن بيانات المخزون',
    provider: 'Claude Sonnet',
    status: 'success',
    time: 'منذ 2 دقيقة',
    tokens: 450,
    cost: 0.002
  },
  {
    id: 2,
    type: 'chat',
    message: 'تحليل تقرير المبيعات',
    provider: 'GPT-4o',
    status: 'success',
    time: 'منذ 5 دقائق',
    tokens: 1200,
    cost: 0.008
  },
  {
    id: 3,
    type: 'chat',
    message: 'ترجمة محتوى تسويقي',
    provider: 'Jais 30B',
    status: 'success',
    time: 'منذ 12 دقيقة',
    tokens: 800,
    cost: 0.0
  },
  {
    id: 4,
    type: 'chat',
    message: 'استعلام قاعدة البيانات',
    provider: 'Claude Haiku',
    status: 'error',
    time: 'منذ 15 دقيقة',
    tokens: 0,
    cost: 0
  },
];

const RecentActivity: React.FC = () => {
  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-100">
      <div className="p-6 border-b border-gray-100">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-semibold text-gray-900">النشاط الأخير</h2>
          <a href="/logs" className="text-blue-600 text-sm hover:underline">
            عرض الكل
          </a>
        </div>
      </div>

      <div className="divide-y divide-gray-100">
        {activities.map((activity) => (
          <div key={activity.id} className="p-4 hover:bg-gray-50 transition-colors">
            <div className="flex items-center gap-4">
              {/* Icon */}
              <div className={`w-10 h-10 rounded-lg flex items-center justify-center ${
                activity.status === 'success' ? 'bg-green-100' : 'bg-red-100'
              }`}>
                {activity.status === 'success' ? (
                  <CheckCircle className="w-5 h-5 text-green-600" />
                ) : (
                  <XCircle className="w-5 h-5 text-red-600" />
                )}
              </div>

              {/* Content */}
              <div className="flex-1 min-w-0">
                <p className="font-medium text-gray-900 truncate">
                  {activity.message}
                </p>
                <p className="text-sm text-gray-500">
                  {activity.provider}
                </p>
              </div>

              {/* Stats */}
              <div className="text-left">
                <p className="text-sm font-medium text-gray-900">
                  {activity.tokens > 0 ? `${activity.tokens} tokens` : '-'}
                </p>
                <p className="text-sm text-gray-500">
                  ${activity.cost.toFixed(4)}
                </p>
              </div>

              {/* Time */}
              <div className="flex items-center gap-1 text-sm text-gray-400">
                <Clock className="w-4 h-4" />
                <span>{activity.time}</span>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default RecentActivity;
