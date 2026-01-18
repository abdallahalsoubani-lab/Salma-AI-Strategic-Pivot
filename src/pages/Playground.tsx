/**
 * صفحة المحادثات / الـ Playground
 * AI Chat Playground for testing
 *
 * Features:
 * - Chat interface (واجهة المحادثة)
 * - Provider selector (اختيار المزود)
 * - Context sources selector (مصادر السياق)
 * - Response info (معلومات الرد): tokens, cost, latency
 */

import React, { useState } from 'react';
import { Send, Settings2, Database, Sparkles, Loader2 } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant';
  content: string;
  provider?: string;
  tokens?: number;
  cost?: number;
  latency?: number;
}

interface Provider {
  id: string;
  name: string;
  nameEn: string;
  badge?: string;
}

const Playground: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedProvider, setSelectedProvider] = useState('auto');
  const [showSettings, setShowSettings] = useState(false);

  const providers: Provider[] = [
    { id: 'auto', name: 'تلقائي', nameEn: 'Auto' },
    { id: 'claude', name: 'كلود', nameEn: 'Claude' },
    { id: 'openai', name: 'أوبن إيه آي', nameEn: 'OpenAI' },
    { id: 'jais', name: 'جيس', nameEn: 'Jais', badge: 'الأفضل للعربية' },
  ];

  const handleSend = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage: Message = { role: 'user', content: input };
    setMessages([...messages, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise(resolve => setTimeout(resolve, 1000));

      const assistantMessage: Message = {
        role: 'assistant',
        content: 'هذا رد تجريبي من الخادم. سيتم ربطه بـ API البوابة لاحقاً.',
        provider: selectedProvider === 'auto' ? 'Claude Sonnet' : selectedProvider,
        tokens: 150,
        cost: 0.002,
        latency: 1234
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      console.error('Error:', error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="h-[calc(100vh-8rem)] flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">المحادثات</h1>
          <p className="text-gray-500">اختبر بوابة الذكاء الاصطناعي</p>
        </div>

        <div className="flex items-center gap-3">
          {/* Provider Selector */}
          <select
            value={selectedProvider}
            onChange={(e) => setSelectedProvider(e.target.value)}
            className="border border-gray-300 rounded-lg px-4 py-2 text-sm"
          >
            {providers.map((p) => (
              <option key={p.id} value={p.id}>
                {p.name} {p.badge && `(${p.badge})`}
              </option>
            ))}
          </select>

          <button
            onClick={() => setShowSettings(!showSettings)}
            className="p-2 border border-gray-300 rounded-lg hover:bg-gray-50"
          >
            <Settings2 className="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>

      {/* Chat Container */}
      <div className="flex-1 bg-white rounded-xl border border-gray-200 flex flex-col overflow-hidden">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-6 space-y-6">
          {messages.length === 0 ? (
            <div className="h-full flex items-center justify-center">
              <div className="text-center">
                <div className="w-16 h-16 bg-blue-100 rounded-full flex items-center justify-center mx-auto mb-4">
                  <Sparkles className="w-8 h-8 text-blue-600" />
                </div>
                <h3 className="text-lg font-medium text-gray-900 mb-2">
                  ابدأ محادثة جديدة
                </h3>
                <p className="text-gray-500 max-w-sm">
                  اكتب رسالتك بالعربية أو الإنجليزية وسيتم توجيهها تلقائياً لأفضل مزود
                </p>
              </div>
            </div>
          ) : (
            messages.map((msg, index) => (
              <div
                key={index}
                className={`flex ${msg.role === 'user' ? 'justify-start' : 'justify-end'}`}
              >
                <div
                  className={`max-w-[70%] rounded-2xl px-4 py-3 ${
                    msg.role === 'user'
                      ? 'bg-blue-600 text-white'
                      : 'bg-gray-100 text-gray-900'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{msg.content}</p>

                  {/* Response info for assistant messages */}
                  {msg.role === 'assistant' && (
                    <div className="mt-2 pt-2 border-t border-gray-200 flex items-center gap-4 text-xs text-gray-500">
                      <span>{msg.provider}</span>
                      <span>{msg.tokens} tokens</span>
                      <span>${msg.cost?.toFixed(4)}</span>
                      <span>{msg.latency}ms</span>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}

          {isLoading && (
            <div className="flex justify-end">
              <div className="bg-gray-100 rounded-2xl px-4 py-3">
                <Loader2 className="w-5 h-5 animate-spin text-gray-500" />
              </div>
            </div>
          )}
        </div>

        {/* Input */}
        <div className="border-t border-gray-200 p-4">
          <div className="flex items-center gap-3">
            <button className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg">
              <Database className="w-5 h-5" />
            </button>

            <input
              type="text"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="اكتب رسالتك هنا..."
              className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />

            <button
              onClick={handleSend}
              disabled={!input.trim() || isLoading}
              className="p-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <Send className="w-5 h-5" />
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Playground;
