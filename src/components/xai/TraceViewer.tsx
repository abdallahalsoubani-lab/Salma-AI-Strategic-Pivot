/**
 * عارض التتبع
 * Trace Viewer Component - Shows detailed AI request trace
 */

import React from 'react';
import {
  Clock,
  DollarSign,
  Cpu,
  Database,
  CheckCircle,
  XCircle,
  ChevronDown,
  ChevronUp,
  Info
} from 'lucide-react';

interface TraceViewerProps {
  trace: {
    request_id: string;
    input: {
      messages: Array<{ role: string; content: string }>;
      tokens: number;
    };
    output: {
      content: string;
      tokens: number;
    };
    routing: {
      requested_provider: string | null;
      selected_provider: string;
      selected_model: string;
      reason: string;
    };
    performance: {
      total_latency_ms: number;
      provider_latency_ms: number;
    };
    cost: {
      total_usd: number;
    };
    status: string;
  };
}

const TraceViewer: React.FC<TraceViewerProps> = ({ trace }) => {
  const [expanded, setExpanded] = React.useState({
    input: true,
    output: true,
    routing: false,
    performance: false
  });

  const toggleSection = (section: keyof typeof expanded) => {
    setExpanded(prev => ({ ...prev, [section]: !prev[section] }));
  };

  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      {/* Header */}
      <div className="p-4 bg-gray-50 border-b border-gray-200">
        <div className="flex items-center justify-between">
          <div className="flex items-center gap-3">
            {trace.status === 'success' ? (
              <CheckCircle className="w-6 h-6 text-green-500" />
            ) : (
              <XCircle className="w-6 h-6 text-red-500" />
            )}
            <div>
              <h3 className="font-medium">{trace.request_id}</h3>
              <p className="text-sm text-gray-500">
                {trace.routing.selected_provider} / {trace.routing.selected_model}
              </p>
            </div>
          </div>

          <div className="flex items-center gap-4 text-sm">
            <div className="flex items-center gap-1">
              <Clock className="w-4 h-4 text-gray-400" />
              <span>{trace.performance.total_latency_ms}ms</span>
            </div>
            <div className="flex items-center gap-1">
              <DollarSign className="w-4 h-4 text-gray-400" />
              <span>${trace.cost.total_usd.toFixed(4)}</span>
            </div>
            <div className="flex items-center gap-1">
              <Cpu className="w-4 h-4 text-gray-400" />
              <span>{trace.input.tokens + trace.output.tokens} tokens</span>
            </div>
          </div>
        </div>
      </div>

      {/* Input Section */}
      <div className="border-b border-gray-100">
        <button
          onClick={() => toggleSection('input')}
          className="w-full p-4 flex items-center justify-between hover:bg-gray-50"
        >
          <span className="font-medium">المدخلات ({trace.input.tokens} tokens)</span>
          {expanded.input ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>

        {expanded.input && (
          <div className="px-4 pb-4 space-y-2">
            {trace.input.messages.map((msg, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg ${
                  msg.role === 'user' ? 'bg-blue-50' : 'bg-gray-50'
                }`}
              >
                <p className="text-xs text-gray-500 mb-1">
                  {msg.role === 'user' ? 'المستخدم' : 'النظام'}
                </p>
                <p className="text-sm">{msg.content}</p>
              </div>
            ))}
          </div>
        )}
      </div>

      {/* Output Section */}
      <div className="border-b border-gray-100">
        <button
          onClick={() => toggleSection('output')}
          className="w-full p-4 flex items-center justify-between hover:bg-gray-50"
        >
          <span className="font-medium">المخرجات ({trace.output.tokens} tokens)</span>
          {expanded.output ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>

        {expanded.output && (
          <div className="px-4 pb-4">
            <div className="p-3 bg-green-50 rounded-lg">
              <p className="text-sm whitespace-pre-wrap">{trace.output.content}</p>
            </div>
          </div>
        )}
      </div>

      {/* Routing Section */}
      <div className="border-b border-gray-100">
        <button
          onClick={() => toggleSection('routing')}
          className="w-full p-4 flex items-center justify-between hover:bg-gray-50"
        >
          <span className="font-medium">قرار التوجيه</span>
          {expanded.routing ? <ChevronUp className="w-5 h-5" /> : <ChevronDown className="w-5 h-5" />}
        </button>

        {expanded.routing && (
          <div className="px-4 pb-4">
            <div className="grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-500">المزود المطلوب</p>
                <p className="font-medium">{trace.routing.requested_provider || 'تلقائي'}</p>
              </div>
              <div>
                <p className="text-gray-500">المزود المختار</p>
                <p className="font-medium">{trace.routing.selected_provider}</p>
              </div>
              <div>
                <p className="text-gray-500">النموذج</p>
                <p className="font-medium">{trace.routing.selected_model}</p>
              </div>
              <div>
                <p className="text-gray-500">السبب</p>
                <p className="font-medium">{trace.routing.reason}</p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default TraceViewer;
