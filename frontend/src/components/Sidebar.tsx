import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useTranslation } from 'react-i18next';
import './Sidebar.css';

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const { t } = useTranslation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="sidebar" dir="rtl">
      <div className="sidebar-header">
        <h2>بوابة سلمى</h2>
        {user && (
          <div className="user-info">
            <p className="user-name">{user.full_name}</p>
            {user.organization && (
              <p className="user-org">{user.organization}</p>
            )}
          </div>
        )}
      </div>

      <nav className="sidebar-nav">
        <ul>
          <li>
            <Link to="/dashboard">{t('sidebar.dashboard')}</Link>
          </li>
          <li>
            <Link to="/data-sources">{t('sidebar.data_sources')}</Link>
          </li>
          <li>
            <Link to="/api-keys">{t('sidebar.api_keys')}</Link>
          </li>
          <li>
            <Link to="/logs">{t('sidebar.logs')}</Link>
          </li>
          <li>
            <Link to="/settings">{t('sidebar.settings')}</Link>
          </li>
        </ul>
      </nav>

      <div className="sidebar-footer">
        <button onClick={handleLogout} className="logout-btn">
          {t('sidebar.logout')}
        </button>
      </div>
    </aside>
  );
};
