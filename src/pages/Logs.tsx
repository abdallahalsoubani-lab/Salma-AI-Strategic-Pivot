/**
 * صفحة السجلات
 * Request Logs with filtering and search
 */

import React, { useState } from 'react';
import { Search, Filter, Download, CheckCircle, XCircle, Clock } from 'lucide-react';

interface Log {
  id: string;
  timestamp: string;
  status: 'success' | 'error';
  provider: string;
  input_tokens: number;
  output_tokens: number;
  cost: number;
  latency: number;
  query_preview: string;
}

const Logs: React.FC = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState('all');
  const [providerFilter, setProviderFilter] = useState('all');

  const logs: Log[] = [
    {
      id: 'req_abc123',
      timestamp: '2026-01-18 14:32:15',
      status: 'success',
      provider: 'Claude Sonnet',
      input_tokens: 150,
      output_tokens: 450,
      cost: 0.0023,
      latency: 1234,
      query_preview: 'ما هي مبيعات الربع الأخير...'
    },
    {
      id: 'req_def456',
      timestamp: '2026-01-18 14:30:22',
      status: 'success',
      provider: 'GPT-4o',
      input_tokens: 200,
      output_tokens: 600,
      cost: 0.0045,
      latency: 2100,
      query_preview: 'تحليل اتجاهات السوق...'
    },
    {
      id: 'req_ghi789',
      timestamp: '2026-01-18 14:28:10',
      status: 'error',
      provider: 'Claude Haiku',
      input_tokens: 0,
      output_tokens: 0,
      cost: 0,
      latency: 5000,
      query_preview: 'خطأ في الاتصال'
    },
  ];

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">السجلات</h1>
          <p className="text-gray-500">سجل جميع الطلبات والاستجابات</p>
        </div>

        <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
          <Download className="w-4 h-4" />
          <span>تصدير CSV</span>
        </button>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl p-4 border border-gray-200">
        <div className="flex items-center gap-4">
          {/* Search */}
          <div className="relative flex-1">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="بحث في السجلات..."
              className="w-full pr-10 pl-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>

          {/* Status Filter */}
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2"
          >
            <option value="all">كل الحالات</option>
            <option value="success">ناجح</option>
            <option value="error">فشل</option>
          </select>

          {/* Provider Filter */}
          <select
            value={providerFilter}
            onChange={(e) => setProviderFilter(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2"
          >
            <option value="all">كل المزودين</option>
            <option value="claude">Claude</option>
            <option value="openai">OpenAI</option>
            <option value="jais">Jais</option>
          </select>
        </div>
      </div>

      {/* Logs Table */}
      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الحالة</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الوقت</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">المزود</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الاستعلام</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">Tokens</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">التكلفة</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الزمن</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {logs.map((log) => (
              <tr key={log.id} className="hover:bg-gray-50">
                <td className="px-6 py-4">
                  {log.status === 'success' ? (
                    <CheckCircle className="w-5 h-5 text-green-500" />
                  ) : (
                    <XCircle className="w-5 h-5 text-red-500" />
                  )}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">{log.timestamp}</td>
                <td className="px-6 py-4 text-sm font-medium">{log.provider}</td>
                <td className="px-6 py-4 text-sm text-gray-600 max-w-xs truncate">
                  {log.query_preview}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {log.input_tokens + log.output_tokens}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  ${log.cost.toFixed(4)}
                </td>
                <td className="px-6 py-4 text-sm text-gray-600">
                  {log.latency}ms
                </td>
              </tr>
            ))}
          </tbody>
        </table>

        {/* Pagination */}
        <div className="px-6 py-4 border-t border-gray-200 flex items-center justify-between">
          <p className="text-sm text-gray-500">
            عرض 1-10 من 247 سجل
          </p>
          <div className="flex items-center gap-2">
            <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50">
              السابق
            </button>
            <button className="px-3 py-1 bg-blue-600 text-white rounded">1</button>
            <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50">2</button>
            <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50">3</button>
            <button className="px-3 py-1 border border-gray-300 rounded hover:bg-gray-50">
              التالي
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Logs;
