/**
 * صفحة مفاتيح API
 * API Keys Management Page
 */

import React from 'react';
import { Plus, Copy, Trash2, Eye, EyeOff } from 'lucide-react';

interface ApiKey {
  id: string;
  name: string;
  key: string;
  created: string;
  lastUsed: string;
  status: string;
}

const ApiKeys: React.FC = () => {
  const [visibleKeys, setVisibleKeys] = React.useState<Set<string>>(new Set());

  const apiKeys: ApiKey[] = [
    {
      id: 'key_1',
      name: 'مفتاح التطوير',
      key: 'sk_test_51234567890abcdef',
      created: '2026-01-10',
      lastUsed: '2026-01-18 02:45 PM',
      status: 'نشط'
    },
    {
      id: 'key_2',
      name: 'مفتاح الإنتاج',
      key: 'sk_live_98765432100fedcba',
      created: '2025-12-01',
      lastUsed: '2026-01-18 03:20 PM',
      status: 'نشط'
    },
  ];

  const toggleKeyVisibility = (keyId: string) => {
    const newSet = new Set(visibleKeys);
    if (newSet.has(keyId)) {
      newSet.delete(keyId);
    } else {
      newSet.add(keyId);
    }
    setVisibleKeys(newSet);
  };

  const maskKey = (key: string, visible: boolean) => {
    if (visible) return key;
    return key.slice(0, 10) + '*'.repeat(key.length - 14) + key.slice(-4);
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">مفاتيح API</h1>
          <p className="text-gray-500">إدارة مفاتيح API الخاصة بك</p>
        </div>

        <button className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
          <Plus className="w-4 h-4" />
          <span>إنشاء مفتاح جديد</span>
        </button>
      </div>

      <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
        <table className="w-full">
          <thead className="bg-gray-50 border-b border-gray-200">
            <tr>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الاسم</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">المفتاح</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">تاريخ الإنشاء</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">آخر استخدام</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الحالة</th>
              <th className="text-right px-6 py-4 text-sm font-medium text-gray-500">الإجراءات</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {apiKeys.map((apiKey) => {
              const isVisible = visibleKeys.has(apiKey.id);
              return (
                <tr key={apiKey.id} className="hover:bg-gray-50">
                  <td className="px-6 py-4 text-sm font-medium text-gray-900">{apiKey.name}</td>
                  <td className="px-6 py-4 text-sm text-gray-600 font-mono">
                    <div className="flex items-center gap-2">
                      <span>{maskKey(apiKey.key, isVisible)}</span>
                      <button
                        onClick={() => toggleKeyVisibility(apiKey.id)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        {isVisible ? <Eye className="w-4 h-4" /> : <EyeOff className="w-4 h-4" />}
                      </button>
                      <button
                        onClick={() => navigator.clipboard.writeText(apiKey.key)}
                        className="text-gray-400 hover:text-gray-600"
                      >
                        <Copy className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                  <td className="px-6 py-4 text-sm text-gray-600">{apiKey.created}</td>
                  <td className="px-6 py-4 text-sm text-gray-600">{apiKey.lastUsed}</td>
                  <td className="px-6 py-4 text-sm">
                    <span className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-xs">
                      {apiKey.status}
                    </span>
                  </td>
                  <td className="px-6 py-4 text-sm">
                    <button className="text-red-600 hover:text-red-800">
                      <Trash2 className="w-4 h-4" />
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default ApiKeys;
