/**
 * صفحة التحليلات
 * Analytics & Reports Page
 *
 * Sections:
 * - Cost breakdown by provider (تفصيل التكلفة حسب المزود)
 * - Usage trends (اتجاهات الاستخدام)
 * - Top queries (أكثر الاستعلامات)
 * - Provider performance (أداء المزودين)
 */

import React from 'react';
import {
  PieChart, Pie, Cell,
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip,
  ResponsiveContainer
} from 'recharts';

interface CostByProvider {
  name: string;
  value: number;
  color: string;
}

interface UsageByDay {
  day: string;
  claude: number;
  openai: number;
  jais: number;
}

const costByProvider: CostByProvider[] = [
  { name: 'Claude', value: 145.5, color: '#8B5CF6' },
  { name: 'OpenAI', value: 67.3, color: '#10B981' },
  { name: 'Jais', value: 0, color: '#F59E0B' },
];

const usageByDay: UsageByDay[] = [
  { day: 'السبت', claude: 120, openai: 80, jais: 40 },
  { day: 'الأحد', claude: 150, openai: 90, jais: 60 },
  { day: 'الإثنين', claude: 200, openai: 120, jais: 80 },
  { day: 'الثلاثاء', claude: 180, openai: 100, jais: 70 },
  { day: 'الأربعاء', claude: 220, openai: 130, jais: 90 },
  { day: 'الخميس', claude: 190, openai: 110, jais: 85 },
  { day: 'الجمعة', claude: 160, openai: 95, jais: 50 },
];

const Analytics: React.FC = () => {
  const totalCost = costByProvider.reduce((sum, p) => sum + p.value, 0);

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">التحليلات</h1>
        <p className="text-gray-500">تقارير الاستخدام والتكاليف</p>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-gray-500 text-sm mb-2">إجمالي التكلفة (هذا الشهر)</h3>
          <p className="text-3xl font-bold text-gray-900">${totalCost.toFixed(2)}</p>
        </div>
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-gray-500 text-sm mb-2">إجمالي الطلبات</h3>
          <p className="text-3xl font-bold text-gray-900">12,847</p>
        </div>
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h3 className="text-gray-500 text-sm mb-2">متوسط التكلفة/طلب</h3>
          <p className="text-3xl font-bold text-gray-900">$0.017</p>
        </div>
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Cost Breakdown Pie Chart */}
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">
            تفصيل التكلفة حسب المزود
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={costByProvider}
                  cx="50%"
                  cy="50%"
                  innerRadius={60}
                  outerRadius={100}
                  paddingAngle={5}
                  dataKey="value"
                >
                  {costByProvider.map((entry, index) => (
                    <Cell key={index} fill={entry.color} />
                  ))}
                </Pie>
                <Tooltip
                  formatter={(value: number) => [`$${value.toFixed(2)}`, 'التكلفة']}
                />
              </PieChart>
            </ResponsiveContainer>
          </div>
          {/* Legend */}
          <div className="flex justify-center gap-6 mt-4">
            {costByProvider.map((p) => (
              <div key={p.name} className="flex items-center gap-2">
                <div
                  className="w-3 h-3 rounded-full"
                  style={{ backgroundColor: p.color }}
                ></div>
                <span className="text-sm text-gray-600">{p.name}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Usage Bar Chart */}
        <div className="bg-white rounded-xl p-6 border border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900 mb-6">
            الاستخدام الأسبوعي حسب المزود
          </h2>
          <div className="h-64">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={usageByDay}>
                <CartesianGrid strokeDasharray="3 3" stroke="#E5E7EB" />
                <XAxis dataKey="day" tick={{ fill: '#6B7280', fontSize: 12 }} />
                <YAxis tick={{ fill: '#6B7280', fontSize: 12 }} />
                <Tooltip />
                <Bar dataKey="claude" fill="#8B5CF6" name="Claude" />
                <Bar dataKey="openai" fill="#10B981" name="OpenAI" />
                <Bar dataKey="jais" fill="#F59E0B" name="Jais" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Analytics;
