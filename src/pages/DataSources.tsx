/**
 * صفحة مصادر البيانات
 * Data Sources Management Page
 */

import React from 'react';
import { Plus, Database, Trash2 } from 'lucide-react';

interface DataSource {
  id: string;
  name: string;
  type: string;
  status: string;
  lastSync: string;
}

const DataSources: React.FC = () => {
  const dataSources: DataSource[] = [
    {
      id: 'ds_1',
      name: 'قاعدة بيانات المبيعات',
      type: 'PostgreSQL',
      status: 'متصل',
      lastSync: '2026-01-18 10:30 AM'
    },
    {
      id: 'ds_2',
      name: 'API المخزون',
      type: 'REST API',
      status: 'متصل',
      lastSync: '2026-01-18 02:45 PM'
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">مصادر البيانات</h1>
          <p className="text-gray-500">إدارة مصادر البيانات المتصلة</p>
        </div>

        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          <Plus className="w-4 h-4" />
          <span>إضافة مصدر</span>
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الاسم</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">النوع</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الحالة</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">آخر مزامنة</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الإجراءات</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {dataSources.map((ds) => (
              <tr key={ds.id} className="hover:bg-gray-50">
                <td className="px-6 py-4 text-sm font-medium text-gray-900">{ds.name}</td>
                <td className="px-6 py-4 text-sm text-gray-600">{ds.type}</td>
                <td className="px-6 py-4 text-sm">
                  <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                    {ds.status}
                  </span>
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">{ds.lastSync}</td>
                <td className="px-6 py-4 text-sm">
                  <button className="text-red-600 hover:text-red-800">
                    <Trash2 className="w-4 h-4" />
                  </button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default DataSources;
