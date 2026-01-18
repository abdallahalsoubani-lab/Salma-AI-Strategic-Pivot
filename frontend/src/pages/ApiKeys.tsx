import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import { apiKeysAPI } from '../services/api';
import { Sidebar } from '../components/Sidebar';
import './ApiKeys.css';

interface APIKey {
  id: string;
  name: string;
  masked_key: string;
  is_active: boolean;
  created_at: string;
  last_used_at?: string;
}

interface NewKeyResponse {
  id: string;
  name: string;
  key: string;
  created_at: string;
  warning: string;
}

export const ApiKeys: React.FC = () => {
  const { t } = useTranslation();
  const [keys, setKeys] = useState<APIKey[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [newKeyData, setNewKeyData] = useState({ name: '', expires_at: null });
  const [newKey, setNewKey] = useState<NewKeyResponse | null>(null);
  const [isCreating, setIsCreating] = useState(false);

  useEffect(() => {
    loadKeys();
  }, []);

  const loadKeys = async () => {
    setIsLoading(true);
    try {
      const response = await apiKeysAPI.list();
      setKeys(response.data);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to load API keys');
    } finally {
      setIsLoading(false);
    }
  };

  const handleCreateKey = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsCreating(true);

    try {
      const response = await apiKeysAPI.create(newKeyData);
      setNewKey(response.data);
      setNewKeyData({ name: '', expires_at: null });
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to create API key');
    } finally {
      setIsCreating(false);
    }
  };

  const handleDeleteKey = async (keyId: string) => {
    if (!confirm('هل تريد حذف هذا المفتاح؟')) return;

    try {
      await apiKeysAPI.delete(keyId);
      setKeys(keys.filter((k) => k.id !== keyId));
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete API key');
    }
  };

  const handleCopyKey = (key: string) => {
    navigator.clipboard.writeText(key);
    alert(t('api_keys.copied'));
  };

  const handleCloseModal = () => {
    setShowModal(false);
    setNewKey(null);
  };

  const handleCreateNewKey = () => {
    setShowModal(true);
    setNewKeyData({ name: '', expires_at: null });
  };

  return (
    <div className="api-keys-page">
      <Sidebar />
      <main className="api-keys-main" dir="rtl">
        <div className="api-keys-header">
          <h1>{t('api_keys.title')}</h1>
          <button onClick={handleCreateNewKey} className="create-btn">
            {t('api_keys.create')}
          </button>
        </div>

        {error && <div className="error-message">{error}</div>}

        {isLoading ? (
          <div className="loading">{t('common.loading')}</div>
        ) : keys.length === 0 ? (
          <div className="empty-state">
            <p>لا توجد مفاتيح API بعد</p>
          </div>
        ) : (
          <table className="keys-table">
            <thead>
              <tr>
                <th>{t('api_keys.name')}</th>
                <th>{t('api_keys.key')}</th>
                <th>{t('api_keys.status')}</th>
                <th>{t('api_keys.created_at')}</th>
                <th>{t('api_keys.last_used')}</th>
                <th>{t('api_keys.actions')}</th>
              </tr>
            </thead>
            <tbody>
              {keys.map((key) => (
                <tr key={key.id}>
                  <td>{key.name}</td>
                  <td>
                    <code>{key.masked_key}</code>
                  </td>
                  <td>
                    <span className={`status ${key.is_active ? 'active' : 'inactive'}`}>
                      {key.is_active ? t('api_keys.active') : t('api_keys.inactive')}
                    </span>
                  </td>
                  <td>{new Date(key.created_at).toLocaleDateString('ar')}</td>
                  <td>
                    {key.last_used_at
                      ? new Date(key.last_used_at).toLocaleDateString('ar')
                      : t('api_keys.never_used')}
                  </td>
                  <td>
                    <button
                      onClick={() => handleDeleteKey(key.id)}
                      className="delete-btn"
                    >
                      {t('api_keys.delete')}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}

        {/* Create Key Modal */}
        {showModal && !newKey && (
          <div className="modal-overlay" onClick={handleCloseModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>{t('api_keys.create_modal.title')}</h2>
                <button onClick={handleCloseModal} className="close-btn">×</button>
              </div>

              <form onSubmit={handleCreateKey} className="modal-form">
                <div className="form-group">
                  <label>{t('api_keys.create_modal.name_label')}</label>
                  <input
                    type="text"
                    value={newKeyData.name}
                    onChange={(e) =>
                      setNewKeyData({ ...newKeyData, name: e.target.value })
                    }
                    placeholder={t('api_keys.create_modal.name_placeholder')}
                    required
                    disabled={isCreating}
                  />
                </div>

                <div className="form-group">
                  <label>{t('api_keys.create_modal.expires')}</label>
                  <input
                    type="datetime-local"
                    onChange={(e) =>
                      setNewKeyData({
                        ...newKeyData,
                        expires_at: e.target.value ? new Date(e.target.value) : null,
                      })
                    }
                    disabled={isCreating}
                  />
                </div>

                <div className="modal-footer">
                  <button
                    type="button"
                    onClick={handleCloseModal}
                    className="cancel-btn"
                    disabled={isCreating}
                  >
                    {t('api_keys.create_modal.cancel')}
                  </button>
                  <button
                    type="submit"
                    className="submit-btn"
                    disabled={isCreating}
                  >
                    {isCreating ? t('common.loading') : t('api_keys.create_modal.submit')}
                  </button>
                </div>
              </form>
            </div>
          </div>
        )}

        {/* New Key Display Modal */}
        {newKey && (
          <div className="modal-overlay" onClick={handleCloseModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h2>مفتاح API جديد</h2>
                <button onClick={handleCloseModal} className="close-btn">×</button>
              </div>

              <div className="new-key-display">
                <div className="warning-box">
                  <strong>⚠️ تحذير:</strong>
                  <p>{newKey.warning}</p>
                </div>

                <div className="key-field">
                  <label>المفتاح:</label>
                  <div className="key-display">
                    <code>{newKey.key}</code>
                    <button
                      type="button"
                      onClick={() => handleCopyKey(newKey.key)}
                      className="copy-btn"
                    >
                      {t('api_keys.copy')}
                    </button>
                  </div>
                </div>

                <button
                  onClick={async () => {
                    handleCloseModal();
                    await loadKeys();
                  }}
                  className="close-modal-btn"
                >
                  تمام
                </button>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  );
};
