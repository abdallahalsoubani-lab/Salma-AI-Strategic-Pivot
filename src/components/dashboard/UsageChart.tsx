/**
 * مخطط الاستخدام
 * Usage over time chart using Recharts
 */

import React from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from 'recharts';

const data = [
  { name: 'السبت', requests: 400, cost: 24 },
  { name: 'الأحد', requests: 300, cost: 18 },
  { name: 'الإثنين', requests: 520, cost: 31 },
  { name: 'الثلاثاء', requests: 480, cost: 29 },
  { name: 'الأربعاء', requests: 600, cost: 36 },
  { name: 'الخميس', requests: 550, cost: 33 },
  { name: 'الجمعة', requests: 450, cost: 27 },
];

const UsageChart: React.FC = () => {
  return (
    <div className="bg-white rounded-xl p-6 shadow-sm border border-gray-100">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-lg font-semibold text-gray-900">الاستخدام الأسبوعي</h2>
        <select className="text-sm border border-gray-300 rounded-lg px-3 py-2">
          <option>آخر 7 أيام</option>
          <option>آخر 30 يوم</option>
          <option>آخر 3 أشهر</option>
        </select>
      </div>

      <div className="h-72">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart data={data}>
            <defs>
              <linearGradient id="colorRequests" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#3B82F6" stopOpacity={0.3}/>
                <stop offset="95%" stopColor="#3B82F6" stopOpacity={0}/>
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
            <XAxis
              dataKey="name"
              tick={{ fill: '#6B7280', fontSize: 12 }}
              axisLine={{ stroke: '#E5E7EB' }}
            />
            <YAxis
              tick={{ fill: '#6B7280', fontSize: 12 }}
              axisLine={{ stroke: '#E5E7EB' }}
            />
            <Tooltip
              contentStyle={{
                backgroundColor: '#fff',
                border: '1px solid #E5E7EB',
                borderRadius: '8px'
              }}
              formatter={(value: number, name: string) => [
                value,
                name === 'requests' ? 'الطلبات' : 'التكلفة'
              ]}
            />
            <Area
              type="monotone"
              dataKey="requests"
              stroke="#3B82F6"
              fillOpacity={1}
              fill="url(#colorRequests)"
              strokeWidth={2}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="flex items-center justify-center gap-6 mt-4">
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 bg-blue-500 rounded-full"></div>
          <span className="text-sm text-gray-600">عدد الطلبات</span>
        </div>
      </div>
    </div>
  );
};

export default UsageChart;
