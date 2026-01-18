import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import './ConnectionForm.css';

interface ConnectionType {
  type: string;
  name: string;
  name_ar: string;
  icon: string;
  default_port?: number;
}

interface ConnectionFormProps {
  onSuccess?: () => void;
}

const ConnectionForm: React.FC<ConnectionFormProps> = ({ onSuccess }) => {
  const { t, i18n } = useTranslation();
  const [types, setTypes] = useState<ConnectionType[]>([]);
  const [formData, setFormData] = useState({
    name: '',
    type: 'postgresql',
    host: '',
    port: 5432,
    database: '',
    username: '',
    password: '',
    additional_config: {}
  });
  const [authType, setAuthType] = useState('none');
  const [apiKey, setApiKey] = useState('');
  const [token, setToken] = useState('');
  const [testing, setTesting] = useState(false);
  const [testResult, setTestResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    loadConnectionTypes();
  }, []);

  const loadConnectionTypes = async () => {
    try {
      const response = await fetch('/api/connections/types');
      const data = await response.json();
      setTypes(data.types || []);
    } catch (err) {
      console.error('Error loading connection types:', err);
    }
  };

  const handleTypeChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const newType = e.target.value;
    setFormData({
      ...formData,
      type: newType
    });

    // Set default port based on type
    const selectedType = types.find(t => t.type === newType);
    if (selectedType?.default_port) {
      setFormData(prev => ({
        ...prev,
        port: selectedType.default_port || prev.port
      }));
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: name === 'port' ? parseInt(value) || 0 : value
    });
  };

  const handleTestConnection = async () => {
    setTesting(true);
    setTestResult(null);
    setError('');

    try {
      const testData: any = {
        type: formData.type,
        host: formData.host,
        port: formData.port,
        database: formData.database,
        username: formData.username,
        password: formData.password,
        additional_config: {}
      };

      if (formData.type === 'rest_api') {
        testData.additional_config.auth_type = authType;
        if (authType === 'bearer') {
          testData.additional_config.token = token;
        } else if (authType === 'api_key') {
          testData.additional_config.api_key = apiKey;
          testData.additional_config.api_key_header = 'X-API-Key';
        }
      }

      const response = await fetch('/api/connections/test', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(testData)
      });

      const result = await response.json();
      setTestResult(result);
    } catch (err) {
      setError(t('data_sources.messages.test_failed'));
    } finally {
      setTesting(false);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const submitData: any = {
        ...formData,
        additional_config: {}
      };

      if (formData.type === 'rest_api') {
        submitData.additional_config.auth_type = authType;
        if (authType === 'bearer') {
          submitData.additional_config.token = token;
        } else if (authType === 'api_key') {
          submitData.additional_config.api_key = apiKey;
          submitData.additional_config.api_key_header = 'X-API-Key';
        }
      }

      const response = await fetch('/api/connections', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(submitData)
      });

      if (response.ok) {
        setFormData({
          name: '',
          type: 'postgresql',
          host: '',
          port: 5432,
          database: '',
          username: '',
          password: '',
          additional_config: {}
        });
        onSuccess?.();
      } else {
        const data = await response.json();
        setError(data.detail || t('data_sources.messages.test_failed'));
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const isRESTAPI = formData.type === 'rest_api';
  const selectedType = types.find(t => t.type === formData.type);

  return (
    <form className="connection-form" onSubmit={handleSubmit}>
      <h2>{t('data_sources.add_new')}</h2>

      {error && <div className="error-message">{error}</div>}

      <div className="form-group">
        <label>{t('data_sources.form.name')}</label>
        <input
          type="text"
          name="name"
          value={formData.name}
          onChange={handleInputChange}
          placeholder={t('data_sources.form.name_placeholder')}
          required
        />
      </div>

      <div className="form-group">
        <label>{t('data_sources.form.type')}</label>
        <select value={formData.type} onChange={handleTypeChange}>
          {types.map(type => (
            <option key={type.type} value={type.type}>
              {i18n.language === 'ar' ? type.name_ar : type.name}
            </option>
          ))}
        </select>
      </div>

      {isRESTAPI ? (
        <>
          <div className="form-group">
            <label>{t('data_sources.form.base_url')}</label>
            <input
              type="url"
              name="host"
              value={formData.host}
              onChange={handleInputChange}
              placeholder={t('data_sources.form.base_url_placeholder')}
              required
            />
          </div>

          <div className="form-group">
            <label>{t('data_sources.form.auth_type')}</label>
            <select value={authType} onChange={(e) => setAuthType(e.target.value)}>
              <option value="none">{t('data_sources.form.auth_types.none')}</option>
              <option value="bearer">{t('data_sources.form.auth_types.bearer')}</option>
              <option value="api_key">{t('data_sources.form.auth_types.api_key')}</option>
              <option value="basic">{t('data_sources.form.auth_types.basic')}</option>
            </select>
          </div>

          {authType === 'bearer' && (
            <div className="form-group">
              <label>{t('data_sources.form.token')}</label>
              <input
                type="password"
                value={token}
                onChange={(e) => setToken(e.target.value)}
              />
            </div>
          )}

          {authType === 'api_key' && (
            <div className="form-group">
              <label>{t('data_sources.form.api_key')}</label>
              <input
                type="password"
                value={apiKey}
                onChange={(e) => setApiKey(e.target.value)}
              />
            </div>
          )}

          {authType === 'basic' && (
            <>
              <div className="form-group">
                <label>{t('data_sources.form.username')}</label>
                <input
                  type="text"
                  name="username"
                  value={formData.username}
                  onChange={handleInputChange}
                />
              </div>
              <div className="form-group">
                <label>{t('data_sources.form.password')}</label>
                <input
                  type="password"
                  name="password"
                  value={formData.password}
                  onChange={handleInputChange}
                />
              </div>
            </>
          )}
        </>
      ) : (
        <>
          <div className="form-group">
            <label>{t('data_sources.form.host')}</label>
            <input
              type="text"
              name="host"
              value={formData.host}
              onChange={handleInputChange}
              placeholder={t('data_sources.form.host_placeholder')}
              required
            />
          </div>

          <div className="form-group">
            <label>{t('data_sources.form.port')}</label>
            <input
              type="number"
              name="port"
              value={formData.port}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>{t('data_sources.form.database')}</label>
            <input
              type="text"
              name="database"
              value={formData.database}
              onChange={handleInputChange}
              placeholder={t('data_sources.form.database_placeholder')}
              required
            />
          </div>

          <div className="form-group">
            <label>{t('data_sources.form.username')}</label>
            <input
              type="text"
              name="username"
              value={formData.username}
              onChange={handleInputChange}
              required
            />
          </div>

          <div className="form-group">
            <label>{t('data_sources.form.password')}</label>
            <input
              type="password"
              name="password"
              value={formData.password}
              onChange={handleInputChange}
              required
            />
          </div>
        </>
      )}

      {testResult && (
        <div className={`test-result ${testResult.success ? 'success' : 'error'}`}>
          <strong>{testResult.message}</strong>
          {testResult.server_version && (
            <p>{testResult.server_version}</p>
          )}
        </div>
      )}

      <div className="form-actions">
        <button
          type="button"
          className="btn-secondary"
          onClick={handleTestConnection}
          disabled={testing || !formData.name || !formData.host}
        >
          {testing ? t('data_sources.form.testing') : t('data_sources.form.test_connection')}
        </button>
        <button
          type="submit"
          className="btn-primary"
          disabled={loading || !testResult?.success}
        >
          {loading ? t('common.saving') : t('data_sources.form.save')}
        </button>
      </div>
    </form>
  );
};

export default ConnectionForm;
