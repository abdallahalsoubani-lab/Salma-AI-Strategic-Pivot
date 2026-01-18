/**
 * بطاقة الشرح
 * Explanation Card - Shows AI decision explanation
 */

import React from 'react';
import { Lightbulb, AlertTriangle, Shield, Globe } from 'lucide-react';

interface ExplanationCardProps {
  explanation: {
    explanation_ar: string;
    explanation_en: string;
    routing_factors: {
      language_detected?: string;
      complexity_score?: number;
      selected_provider?: string;
    };
    response_confidence?: number;
    potential_issues?: string[];
    compliance?: {
      pii_detected: boolean;
      data_sensitivity: string;
    };
  };
}

const ExplanationCard: React.FC<ExplanationCardProps> = ({ explanation }) => {
  return (
    <div className="bg-white rounded-xl border border-gray-200 overflow-hidden">
      <div className="p-4 bg-amber-50 border-b border-amber-100">
        <div className="flex items-center gap-2">
          <Lightbulb className="w-5 h-5 text-amber-600" />
          <h3 className="font-medium text-amber-900">شرح القرار</h3>
        </div>
      </div>

      <div className="p-4 space-y-4">
        {/* Arabic Explanation */}
        <div>
          <p className="text-gray-700">{explanation.explanation_ar}</p>
        </div>

        {/* Routing Factors */}
        <div className="grid grid-cols-3 gap-4">
          <div className="p-3 bg-gray-50 rounded-lg text-center">
            <Globe className="w-5 h-5 mx-auto mb-1 text-blue-500" />
            <p className="text-xs text-gray-500">اللغة</p>
            <p className="font-medium">
              {explanation.routing_factors.language_detected === 'ar' ? 'العربية' : 'الإنجليزية'}
            </p>
          </div>

          <div className="p-3 bg-gray-50 rounded-lg text-center">
            <div className="w-5 h-5 mx-auto mb-1 text-purple-500">📊</div>
            <p className="text-xs text-gray-500">التعقيد</p>
            <p className="font-medium">
              {(explanation.routing_factors.complexity_score || 0) > 0.7 ? 'معقد' :
                (explanation.routing_factors.complexity_score || 0) > 0.3 ? 'متوسط' : 'بسيط'}
            </p>
          </div>

          <div className="p-3 bg-gray-50 rounded-lg text-center">
            <div className="w-5 h-5 mx-auto mb-1 text-green-500">✓</div>
            <p className="text-xs text-gray-500">الثقة</p>
            <p className="font-medium">
              {Math.round((explanation.response_confidence || 0) * 100)}%
            </p>
          </div>
        </div>

        {/* Potential Issues */}
        {explanation.potential_issues && explanation.potential_issues.length > 0 && (
          <div className="p-3 bg-amber-50 rounded-lg">
            <div className="flex items-center gap-2 mb-2">
              <AlertTriangle className="w-4 h-4 text-amber-600" />
              <p className="text-sm font-medium text-amber-800">تنبيهات محتملة</p>
            </div>
            <ul className="text-sm text-amber-700 space-y-1">
              {explanation.potential_issues.map((issue, idx) => (
                <li key={idx}>• {issue}</li>
              ))}
            </ul>
          </div>
        )}

        {/* Compliance */}
        <div className="p-3 bg-green-50 rounded-lg">
          <div className="flex items-center gap-2">
            <Shield className="w-4 h-4 text-green-600" />
            <p className="text-sm font-medium text-green-800">الامتثال</p>
          </div>
          <div className="mt-2 flex items-center gap-4 text-sm">
            <span className={`px-2 py-1 rounded ${
              explanation.compliance?.pii_detected
                ? 'bg-red-100 text-red-700'
                : 'bg-green-100 text-green-700'
            }`}>
              {explanation.compliance?.pii_detected ? 'تم اكتشاف PII' : 'لا يوجد PII'}
            </span>
            <span className="text-gray-600">
              حساسية البيانات: {explanation.compliance?.data_sensitivity || 'منخفضة'}
            </span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ExplanationCard;
