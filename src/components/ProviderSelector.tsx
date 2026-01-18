/**
 * Provider Selector Component
 * Arabic UI component for selecting AI provider
 */

interface Provider {
  id: string;
  name: string;
  nameAr: string;
  status: 'active' | 'not_configured';
  badge?: string;  // e.g., "الأفضل للعربية" for Jais
}

interface ProviderSelectorProps {
  selectedProvider: string;
  onProviderChange: (providerId: string) => void;
  providers: Provider[];
  isArabic?: boolean;
}

export const ProviderSelector: React.FC<ProviderSelectorProps> = ({
  selectedProvider,
  onProviderChange,
  providers,
  isArabic = true
}) => {
  const autoOption = {
    id: 'auto',
    name: 'Auto (Recommended)',
    nameAr: 'تلقائي (موصى به)',
    status: 'active' as const,
    badge: undefined
  };

  const allOptions = [autoOption, ...providers];
  const displayLabel = (option: Provider) => isArabic ? option.nameAr : option.name;
  const isDisabled = (option: Provider) => option.status === 'not_configured' && option.id !== 'auto';

  return (
    <div className="provider-selector" dir={isArabic ? 'rtl' : 'ltr'}>
      <label className="provider-selector-label">
        {isArabic ? 'مزود الذكاء الاصطناعي' : 'AI Provider'}
      </label>

      <div className="provider-options">
        {allOptions.map((option) => (
          <div key={option.id} className="provider-option">
            <input
              type="radio"
              id={`provider-${option.id}`}
              name="provider"
              value={option.id}
              checked={selectedProvider === option.id}
              onChange={(e) => onProviderChange(e.target.value)}
              disabled={isDisabled(option)}
              className="provider-radio"
            />

            <label htmlFor={`provider-${option.id}`} className="provider-label">
              <div className="provider-info">
                <span className="provider-name">
                  {displayLabel(option)}
                </span>

                {option.badge && (
                  <span className="provider-badge">{option.badge}</span>
                )}

                {isDisabled(option) && (
                  <span className="provider-status-badge">
                    {isArabic ? 'غير مُعد' : 'Not Configured'}
                  </span>
                )}
              </div>
            </label>
          </div>
        ))}
      </div>

      {selectedProvider === 'auto' && (
        <p className="provider-description">
          {isArabic
            ? 'اختيار تلقائي بناءً على اللغة والتعقيد والتكلفة'
            : 'Automatic selection based on language, complexity, and cost'
          }
        </p>
      )}
    </div>
  );
};
