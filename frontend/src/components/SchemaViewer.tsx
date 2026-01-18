import React, { useState, useEffect } from 'react';
import { useTranslation } from 'react-i18next';
import './SchemaViewer.css';

interface Column {
  name: string;
  type: string;
  nullable?: boolean;
  default?: string;
}

interface TableData {
  columns: string[];
  rows: any[][];
}

interface SchemaViewerProps {
  connectionId: string;
}

const SchemaViewer: React.FC<SchemaViewerProps> = ({ connectionId }) => {
  const { t } = useTranslation();
  const [tables, setTables] = useState<string[]>([]);
  const [selectedTable, setSelectedTable] = useState<string | null>(null);
  const [columns, setColumns] = useState<Column[]>([]);
  const [sampleData, setSampleData] = useState<TableData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    loadTables();
  }, [connectionId]);

  const loadTables = async () => {
    try {
      setLoading(true);
      setError('');
      const response = await fetch(`/api/connections/${connectionId}/tables`);
      if (response.ok) {
        const data = await response.json();
        setTables(data.tables || []);
        if (data.tables && data.tables.length > 0) {
          setSelectedTable(data.tables[0]);
          loadTableSchema(data.tables[0]);
        }
      } else {
        setError(t('common.error'));
      }
    } catch (err) {
      setError(t('common.error'));
      console.error('Error loading tables:', err);
    } finally {
      setLoading(false);
    }
  };

  const loadTableSchema = async (tableName: string) => {
    try {
      setLoading(true);

      // Load columns
      const colResponse = await fetch(
        `/api/connections/${connectionId}/tables/${encodeURIComponent(tableName)}/columns`
      );
      if (colResponse.ok) {
        const colData = await colResponse.json();
        setColumns(colData.columns || []);
      }

      // Load sample data
      const dataResponse = await fetch(
        `/api/connections/${connectionId}/tables/${encodeURIComponent(tableName)}/sample?limit=10`
      );
      if (dataResponse.ok) {
        const tableData = await dataResponse.json();
        setSampleData(tableData);
      }
    } catch (err) {
      console.error('Error loading schema:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTableSelect = (tableName: string) => {
    setSelectedTable(tableName);
    loadTableSchema(tableName);
  };

  if (loading && tables.length === 0) {
    return <div className="schema-viewer loading">{t('common.loading')}...</div>;
  }

  return (
    <div className="schema-viewer">
      <h2>{t('data_sources.schema.title')}</h2>

      {error && <div className="error-message">{error}</div>}

      {tables.length === 0 ? (
        <div className="empty-state">
          <p>{t('data_sources.schema.no_tables')}</p>
        </div>
      ) : (
        <div className="schema-container">
          <div className="tables-panel">
            <h3>{t('data_sources.schema.tables')}</h3>
            <div className="tables-list">
              {tables.map(table => (
                <button
                  key={table}
                  className={`table-item ${selectedTable === table ? 'active' : ''}`}
                  onClick={() => handleTableSelect(table)}
                >
                  📋 {table}
                </button>
              ))}
            </div>
          </div>

          {selectedTable && (
            <div className="details-panel">
              <div className="columns-section">
                <h3>{t('data_sources.schema.columns')}</h3>
                {loading ? (
                  <div className="loading">{t('common.loading')}...</div>
                ) : columns.length === 0 ? (
                  <p>{t('data_sources.schema.no_tables')}</p>
                ) : (
                  <table className="columns-table">
                    <thead>
                      <tr>
                        <th>{t('data_sources.schema.column_name')}</th>
                        <th>{t('data_sources.schema.column_type')}</th>
                        <th>{t('data_sources.schema.nullable')}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {columns.map(col => (
                        <tr key={col.name}>
                          <td className="column-name">{col.name}</td>
                          <td className="column-type">{col.type}</td>
                          <td className="column-nullable">
                            {col.nullable ? '✓' : '✗'}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                )}
              </div>

              {sampleData && sampleData.rows && sampleData.rows.length > 0 && (
                <div className="sample-data-section">
                  <h3>{t('data_sources.schema.sample_data')}</h3>
                  <div className="sample-data-table">
                    <table>
                      <thead>
                        <tr>
                          {sampleData.columns.map(col => (
                            <th key={col}>{col}</th>
                          ))}
                        </tr>
                      </thead>
                      <tbody>
                        {sampleData.rows.map((row, idx) => (
                          <tr key={idx}>
                            {row.map((cell, cellIdx) => (
                              <td key={cellIdx}>
                                {cell === null ? (
                                  <span className="null-value">NULL</span>
                                ) : (
                                  String(cell)
                                )}
                              </td>
                            ))}
                          </tr>
                        ))}
                      </tbody>
                    </table>
                  </div>
                  {sampleData.truncated && (
                    <p className="truncated-message">
                      ({t('common.showing')} {sampleData.row_count} {t('common.of')} {sampleData.row_count}+)
                    </p>
                  )}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default SchemaViewer;
