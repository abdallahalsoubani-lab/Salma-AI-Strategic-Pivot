/**
 * لوحة التحكم الرئيسية
 * Main Dashboard with stats and charts
 *
 * Sections:
 * 1. Stats Cards (بطاقات الإحصائيات)
 * 2. Usage Chart (مخطط الاستخدام)
 * 3. Recent Activity (النشاط الأخير)
 * 4. Quick Actions (إجراءات سريعة)
 */

import React from 'react';
import {
  Zap,
  DollarSign,
  MessageSquare,
  Database,
  ArrowUpRight,
  ArrowDownRight
} from 'lucide-react';
import StatsCard from '../components/dashboard/StatsCard';
import UsageChart from '../components/dashboard/UsageChart';
import RecentActivity from '../components/dashboard/RecentActivity';
import QuickActions from '../components/dashboard/QuickActions';

const Dashboard: React.FC = () => {
  return (
    <div className="space-y-6">
      {/* Page Title */}
      <div>
        <h1 className="text-2xl font-bold text-gray-900">لوحة التحكم</h1>
        <p className="text-gray-500">مرحباً بك في بوابة سلمى للذكاء الاصطناعي</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="إجمالي الطلبات"
          value="12,847"
          change="+12.5%"
          changeType="increase"
          icon={MessageSquare}
          iconColor="bg-blue-500"
        />
        <StatsCard
          title="التكلفة الشهرية"
          value="$234.50"
          change="-8.2%"
          changeType="decrease"
          icon={DollarSign}
          iconColor="bg-green-500"
        />
        <StatsCard
          title="مصادر البيانات"
          value="5"
          change="+2"
          changeType="increase"
          icon={Database}
          iconColor="bg-purple-500"
        />
        <StatsCard
          title="متوسط زمن الاستجابة"
          value="1.2s"
          change="-15%"
          changeType="decrease"
          icon={Zap}
          iconColor="bg-orange-500"
        />
      </div>

      {/* Charts Row */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <UsageChart />
        </div>
        <div>
          <QuickActions />
        </div>
      </div>

      {/* Recent Activity */}
      <RecentActivity />
    </div>
  );
};

export default Dashboard;
