/**
 * تطبيق Salma AI Gateway
 * Salma AI Gateway - Main Application
 */

import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import AuditLogs from './pages/AuditLogs';

function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gray-100">
        <Routes>
          {/* Main Routes */}
          <Route path="/" element={<div className="p-6">Home Page</div>} />
          <Route path="/audit" element={<AuditLogs />} />

          {/* Other routes would be added here from previous prompts */}
          <Route path="*" element={<div className="p-6">404 - Page Not Found</div>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;
