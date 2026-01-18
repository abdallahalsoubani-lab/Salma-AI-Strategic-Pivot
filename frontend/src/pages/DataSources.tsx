import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import ConnectionForm from '../components/ConnectionForm';
import ConnectionList from '../components/ConnectionList';
import SchemaViewer from '../components/SchemaViewer';
import './DataSources.css';

interface Connection {
  id: string;
  name: string;
  type: string;
  host?: string;
  database?: string;
  created_at: string;
  last_used?: string;
}

const DataSources: React.FC = () => {
  const { t } = useTranslation();
  const [connections, setConnections] = useState<Connection[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [selectedConnection, setSelectedConnection] = useState<Connection | null>(null);
  const [showSchema, setShowSchema] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadConnections();
  }, []);

  const loadConnections = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/connections');
      const data = await response.json();
      setConnections(data.connections || []);
    } catch (error) {
      console.error('Error loading connections:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleConnectionCreated = () => {
    setShowForm(false);
    loadConnections();
  };

  const handleDeleteConnection = async (id: string) => {
    if (window.confirm(t('data_sources.messages.delete_confirm'))) {
      try {
        const response = await fetch(`/api/connections/${id}`, {
          method: 'DELETE'
        });
        if (response.ok) {
          loadConnections();
        }
      } catch (error) {
        console.error('Error deleting connection:', error);
      }
    }
  };

  const handleViewSchema = (connection: Connection) => {
    setSelectedConnection(connection);
    setShowSchema(true);
  };

  return (
    <div className="data-sources-page">
      <div className="page-header">
        <h1>{t('data_sources.title')}</h1>
        <button
          className="btn-primary"
          onClick={() => setShowForm(true)}
        >
          {t('data_sources.add_new')}
        </button>
      </div>

      {showForm && (
        <div className="modal-overlay">
          <div className="modal-content">
            <button
              className="modal-close"
              onClick={() => setShowForm(false)}
            >
              ×
            </button>
            <ConnectionForm onSuccess={handleConnectionCreated} />
          </div>
        </div>
      )}

      {showSchema && selectedConnection && (
        <div className="modal-overlay">
          <div className="modal-content modal-large">
            <button
              className="modal-close"
              onClick={() => setShowSchema(false)}
            >
              ×
            </button>
            <SchemaViewer connectionId={selectedConnection.id} />
          </div>
        </div>
      )}

      {loading ? (
        <div className="loading">
          {t('common.loading')}...
        </div>
      ) : connections.length === 0 ? (
        <div className="empty-state">
          <h2>{t('data_sources.no_sources')}</h2>
          <p>{t('data_sources.no_sources_desc')}</p>
        </div>
      ) : (
        <ConnectionList
          connections={connections}
          onViewSchema={handleViewSchema}
          onDelete={handleDeleteConnection}
        />
      )}
    </div>
  );
};

export default DataSources;
