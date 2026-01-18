import React from 'react';
import { useTranslation } from 'react-i18next';
import './ConnectionList.css';

interface Connection {
  id: string;
  name: string;
  type: string;
  host?: string;
  database?: string;
  created_at: string;
  last_used?: string;
}

interface ConnectionListProps {
  connections: Connection[];
  onViewSchema: (connection: Connection) => void;
  onDelete: (id: string) => void;
}

const getConnectionIcon = (type: string): string => {
  const icons: { [key: string]: string } = {
    postgresql: '🐘',
    mysql: '🐬',
    oracle: '⭕',
    rest_api: '🔌',
    mssql: '🔷'
  };
  return icons[type] || '💾';
};

const getConnectionTypeLabel = (type: string, t: any): string => {
  const labels: { [key: string]: string } = {
    postgresql: t('data_sources.types.postgresql'),
    mysql: t('data_sources.types.mysql'),
    oracle: t('data_sources.types.oracle'),
    rest_api: t('data_sources.types.rest_api'),
    mssql: t('data_sources.types.mssql')
  };
  return labels[type] || type;
};

const ConnectionList: React.FC<ConnectionListProps> = ({
  connections,
  onViewSchema,
  onDelete
}) => {
  const { t } = useTranslation();

  return (
    <div className="connections-list">
      <div className="connections-grid">
        {connections.map(connection => (
          <div key={connection.id} className="connection-card">
            <div className="card-header">
              <div className="connection-icon">
                {getConnectionIcon(connection.type)}
              </div>
              <div className="connection-info">
                <h3>{connection.name}</h3>
                <p className="connection-type">
                  {getConnectionTypeLabel(connection.type, t)}
                </p>
              </div>
            </div>

            <div className="card-body">
              {connection.host && (
                <div className="info-row">
                  <span className="label">{t('data_sources.form.host')}:</span>
                  <span className="value">{connection.host}</span>
                </div>
              )}
              {connection.database && (
                <div className="info-row">
                  <span className="label">{t('data_sources.form.database')}:</span>
                  <span className="value">{connection.database}</span>
                </div>
              )}
              <div className="info-row">
                <span className="label">{t('common.created')}:</span>
                <span className="value">
                  {new Date(connection.created_at).toLocaleDateString()}
                </span>
              </div>
              {connection.last_used && (
                <div className="info-row">
                  <span className="label">{t('common.last_used')}:</span>
                  <span className="value">
                    {new Date(connection.last_used).toLocaleDateString()}
                  </span>
                </div>
              )}
            </div>

            <div className="card-actions">
              <button
                className="btn-small btn-secondary"
                onClick={() => onViewSchema(connection)}
                title={t('data_sources.actions.view_schema')}
              >
                📊 {t('data_sources.actions.view_schema')}
              </button>
              <button
                className="btn-small btn-danger"
                onClick={() => onDelete(connection.id)}
                title={t('data_sources.actions.delete')}
              >
                🗑️ {t('data_sources.actions.delete')}
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default ConnectionList;
