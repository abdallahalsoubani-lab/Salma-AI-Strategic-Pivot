import { useState } from 'react'
import translations from './locales/ar.json'

/**
 * Main App component for Salma AI Gateway
 * Provides RTL Arabic UI for MENA enterprise systems
 */
function App() {
  const [count, setCount] = useState(0)
  const t = translations

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-50">
      {/* Navigation Header */}
      <header className="bg-white shadow-sm">
        <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex items-center justify-between">
          <div className="flex items-center space-x-2 rtl:space-x-reverse">
            <div className="w-10 h-10 bg-indigo-600 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-lg">س</span>
            </div>
            <span className="text-xl font-bold text-gray-900">{t.app_name}</span>
          </div>
          <ul className="flex space-x-8 rtl:space-x-reverse">
            <li><a href="#" className="text-gray-600 hover:text-indigo-600 font-medium">{t.dashboard}</a></li>
            <li><a href="#" className="text-gray-600 hover:text-indigo-600 font-medium">{t.connections}</a></li>
            <li><a href="#" className="text-gray-600 hover:text-indigo-600 font-medium">{t.usage}</a></li>
            <li><a href="#" className="text-gray-600 hover:text-indigo-600 font-medium">{t.settings}</a></li>
          </ul>
          <button className="text-gray-600 hover:text-indigo-600 font-medium">{t.logout}</button>
        </nav>
      </header>

      {/* Hero Section */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <div className="text-center mb-12">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            {t.welcome}
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            بوابة ذكية تربط أنظمتك مع أقوى خدمات الذكاء الاصطناعي
          </p>
        </div>

        {/* Feature Cards */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-12">
          {/* API Keys Card */}
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
            <div className="w-12 h-12 bg-indigo-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🔑</span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">{t.api_keys}</h3>
            <p className="text-gray-600">أدارة مفاتيح API بسهولة وأمان</p>
          </div>

          {/* Connections Card */}
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
            <div className="w-12 h-12 bg-green-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">🔗</span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">{t.connections}</h3>
            <p className="text-gray-600">اتصل بمصادر البيانات المختلفة</p>
          </div>

          {/* Usage Card */}
          <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
            <div className="w-12 h-12 bg-purple-100 rounded-lg flex items-center justify-center mb-4">
              <span className="text-2xl">📊</span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 mb-2">{t.usage}</h3>
            <p className="text-gray-600">تتبع استخدام API والتكاليف</p>
          </div>
        </div>

        {/* Stats Section */}
        <div className="bg-white rounded-lg shadow-md p-8 mb-12">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8 text-center">
            <div>
              <div className="text-3xl font-bold text-indigo-600 mb-2">0</div>
              <div className="text-gray-600">طلبات اليوم</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-green-600 mb-2">0</div>
              <div className="text-gray-600">الاتصالات النشطة</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-orange-600 mb-2">$0.00</div>
              <div className="text-gray-600">التكلفة هذا الشهر</div>
            </div>
            <div>
              <div className="text-3xl font-bold text-blue-600 mb-2">99.9%</div>
              <div className="text-gray-600">نسبة التوفر</div>
            </div>
          </div>
        </div>

        {/* Counter Demo */}
        <div className="bg-white rounded-lg shadow-md p-8 text-center">
          <p className="text-lg text-gray-600 mb-4">عداد تجريبي:</p>
          <button
            onClick={() => setCount((count) => count + 1)}
            className="bg-indigo-600 hover:bg-indigo-700 text-white font-bold py-2 px-6 rounded-lg transition"
          >
            العدد: {count}
          </button>
        </div>
      </main>

      {/* Footer */}
      <footer className="bg-gray-900 text-white mt-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="text-center">
            <p>© 2026 {t.app_name} - جميع الحقوق محفوظة</p>
            <p className="text-gray-400 mt-2">بوابة ذكية لتوصيل الأنظمة المؤسسية بخدمات الذكاء الاصطناعي</p>
          </div>
        </div>
      </footer>
    </div>
  )
}

export default App
