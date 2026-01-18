/**
 * صفحة سجلات التدقيق
 * Audit Logs Page
 */

import React, { useState, useEffect } from 'react';
import {
  Search,
  Filter,
  Download,
  Eye,
  Calendar,
  ChevronLeft,
  ChevronRight
} from 'lucide-react';
import TraceViewer from '../components/xai/TraceViewer';
import ExplanationCard from '../components/xai/ExplanationCard';

const AuditLogs: React.FC = () => {
  const [traces, setTraces] = useState<any[]>([
    {
      request_id: "req_abc123",
      status: "success",
      provider: "Claude Sonnet",
      model: "claude-3-sonnet",
      tokens: 600,
      cost_usd: 0.0023,
      latency_ms: 1234,
      date: "منذ 5 دقائق"
    }
  ]);
  const [selectedTrace, setSelectedTrace] = useState<any | null>(null);
  const [filters, setFilters] = useState({
    status: 'all',
    provider: 'all',
    dateRange: '7d'
  });
  const [showDetail, setShowDetail] = useState(false);

  const fetchTraces = async () => {
    // API call would happen here
    console.log('Fetching traces with filters:', filters);
  };

  useEffect(() => {
    fetchTraces();
  }, [filters]);

  const viewTraceDetail = (requestId: string) => {
    const mockTrace = {
      request_id: requestId,
      input: {
        messages: [
          { role: 'user', content: 'ما هو الذكاء الاصطناعي؟' }
        ],
        tokens: 30,
        system_prompt: "أنت مساعد ذكي"
      },
      output: {
        content: "الذكاء الاصطناعي هو فرع من علوم الحاسوب يهتم بإنشاء برامج ذكية...",
        tokens: 570
      },
      routing: {
        requested_provider: null,
        selected_provider: "Claude",
        selected_model: "claude-3-sonnet",
        reason: "أفضل توازن بين الجودة والتكلفة"
      },
      context: {
        sources_used: ["connection_1"],
        data_summary: null
      },
      performance: {
        total_latency_ms: 1234,
        provider_latency_ms: 1100,
        context_fetch_latency_ms: 134
      },
      cost: {
        total_usd: 0.0023,
        breakdown: { input: 0.0008, output: 0.0015 }
      },
      status: 'success',
      timestamps: {
        created_at: new Date().toISOString(),
        completed_at: new Date().toISOString()
      }
    };

    setSelectedTrace(mockTrace);
    setShowDetail(true);
  };

  return (
    <div className="space-y-6 p-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">سجلات التدقيق</h1>
          <p className="text-gray-500">تتبع وشرح جميع طلبات الذكاء الاصطناعي</p>
        </div>

        <div className="flex items-center gap-3">
          <button className="flex items-center gap-2 px-4 py-2 border border-gray-300 rounded-lg hover:bg-gray-50">
            <Download className="w-4 h-4" />
            <span>تصدير</span>
          </button>
        </div>
      </div>

      {/* Filters */}
      <div className="bg-white rounded-xl p-4 border border-gray-200">
        <div className="flex items-center gap-4 flex-wrap">
          <div className="relative flex-1 min-w-[200px]">
            <Search className="absolute right-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
            <input
              type="text"
              placeholder="بحث بـ Request ID..."
              className="w-full pr-10 pl-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>

          <select
            value={filters.status}
            onChange={(e) => setFilters({ ...filters, status: e.target.value })}
            className="border border-gray-300 rounded-lg px-4 py-2"
          >
            <option value="all">كل الحالات</option>
            <option value="success">ناجح</option>
            <option value="failed">فشل</option>
          </select>

          <select
            value={filters.provider}
            onChange={(e) => setFilters({ ...filters, provider: e.target.value })}
            className="border border-gray-300 rounded-lg px-4 py-2"
          >
            <option value="all">كل المزودين</option>
            <option value="claude">Claude</option>
            <option value="openai">OpenAI</option>
            <option value="jais">Jais</option>
          </select>

          <select
            value={filters.dateRange}
            onChange={(e) => setFilters({ ...filters, dateRange: e.target.value })}
            className="border border-gray-300 rounded-lg px-4 py-2"
          >
            <option value="24h">آخر 24 ساعة</option>
            <option value="7d">آخر 7 أيام</option>
            <option value="30d">آخر 30 يوم</option>
          </select>
        </div>
      </div>

      {/* Main Content */}
      <div className="flex gap-6">
        {/* Traces List */}
        <div className={`${showDetail ? 'w-1/2' : 'w-full'} transition-all`}>
          <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="text-right px-4 py-3 text-sm font-medium text-gray-500">الحالة</th>
                    <th className="text-right px-4 py-3 text-sm font-medium text-gray-500">Request ID</th>
                    <th className="text-right px-4 py-3 text-sm font-medium text-gray-500">المزود</th>
                    <th className="text-right px-4 py-3 text-sm font-medium text-gray-500">Tokens</th>
                    <th className="text-right px-4 py-3 text-sm font-medium text-gray-500">التكلفة</th>
                    <th className="text-right px-4 py-3 text-sm font-medium text-gray-500">الزمن</th>
                    <th className="text-right px-4 py-3 text-sm font-medium text-gray-500">التاريخ</th>
                    <th className="px-4 py-3"></th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-100">
                  {traces.map((trace, idx) => (
                    <tr key={idx} className="hover:bg-gray-50">
                      <td className="px-4 py-3">
                        <span className="w-2 h-2 bg-green-500 rounded-full inline-block"></span>
                      </td>
                      <td className="px-4 py-3 text-sm font-mono">{trace.request_id}</td>
                      <td className="px-4 py-3 text-sm">{trace.provider}</td>
                      <td className="px-4 py-3 text-sm">{trace.tokens}</td>
                      <td className="px-4 py-3 text-sm">${trace.cost_usd.toFixed(4)}</td>
                      <td className="px-4 py-3 text-sm">{trace.latency_ms}ms</td>
                      <td className="px-4 py-3 text-sm text-gray-500">{trace.date}</td>
                      <td className="px-4 py-3">
                        <button
                          onClick={() => viewTraceDetail(trace.request_id)}
                          className="p-1 hover:bg-gray-100 rounded"
                        >
                          <Eye className="w-4 h-4 text-gray-500" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            <div className="px-4 py-3 border-t border-gray-200 flex items-center justify-between">
              <p className="text-sm text-gray-500">عرض 1-20 من 156</p>
              <div className="flex items-center gap-2">
                <button className="p-2 border border-gray-300 rounded hover:bg-gray-50">
                  <ChevronRight className="w-4 h-4" />
                </button>
                <button className="p-2 border border-gray-300 rounded hover:bg-gray-50">
                  <ChevronLeft className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        </div>

        {/* Detail Panel */}
        {showDetail && selectedTrace && (
          <div className="w-1/2 space-y-4 max-h-[80vh] overflow-y-auto">
            <div className="flex items-center justify-between sticky top-0 bg-white p-4 rounded-lg border border-gray-200">
              <h2 className="text-lg font-semibold">تفاصيل الطلب</h2>
              <button
                onClick={() => setShowDetail(false)}
                className="text-gray-500 hover:text-gray-700"
              >
                ✕
              </button>
            </div>

            <TraceViewer trace={selectedTrace} />
            <ExplanationCard
              explanation={{
                explanation_ar: "تم اختيار Claude لأنه يوفر أفضل توازن بين جودة الاستجابة والتكلفة",
                explanation_en: "Claude was selected for optimal balance between response quality and cost",
                routing_factors: {
                  language_detected: 'ar',
                  complexity_score: 0.5,
                  selected_provider: 'claude'
                },
                response_confidence: 0.92,
                potential_issues: [],
                compliance: {
                  pii_detected: false,
                  data_sensitivity: 'low'
                }
              }}
            />
          </div>
        )}
      </div>
    </div>
  );
};

export default AuditLogs;
