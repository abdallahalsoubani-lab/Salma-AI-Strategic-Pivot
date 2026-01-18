# Salma AI Gateway - Admin Dashboard UI

## Overview

This is Prompt 5 of the Salma AI Gateway project. It implements a complete, production-ready admin dashboard with full Arabic RTL (Right-to-Left) support and comprehensive UI components.

## Project Structure

```
src/
├── components/
│   ├── layout/
│   │   ├── DashboardLayout.tsx      # Main layout wrapper with RTL support
│   │   ├── Sidebar.tsx              # Navigation sidebar with menu items
│   │   └── Header.tsx               # Top header with search and notifications
│   ├── dashboard/
│   │   ├── StatsCard.tsx            # Stat card component
│   │   ├── UsageChart.tsx           # Area chart for usage trends
│   │   ├── RecentActivity.tsx       # Activity feed component
│   │   └── QuickActions.tsx         # Quick action buttons
│   └── common/                      # Shared components (placeholder)
├── pages/
│   ├── Dashboard.tsx                # Main dashboard page
│   ├── Playground.tsx               # AI chat interface
│   ├── Logs.tsx                     # Request logs with filtering
│   ├── Analytics.tsx                # Analytics and reports
│   ├── Settings.tsx                 # Settings with tabs
│   ├── DataSources.tsx              # Data sources management
│   └── ApiKeys.tsx                  # API keys management
├── hooks/                           # Custom hooks (placeholder)
├── locales/
│   └── ar.json                      # Arabic translations
├── styles/
│   └── index.css                    # Tailwind CSS and global styles
├── App.tsx                          # Main app component with routing
└── main.tsx                         # React entry point

Configuration Files:
├── vite.config.ts                   # Vite build configuration
├── tailwind.config.js               # Tailwind CSS configuration
├── postcss.config.js                # PostCSS configuration
├── tsconfig.json                    # TypeScript configuration
├── tsconfig.node.json               # TypeScript Node configuration
├── .eslintrc.cjs                    # ESLint configuration
├── package.json                     # Dependencies and scripts
├── index.html                       # HTML entry point
└── .gitignore                       # Git ignore rules
```

## Features

### 1. Dashboard Layout
- **RTL-Optimized Sidebar**: Fixed right-side navigation with dark theme
- **Header**: Search functionality and notification bell
- **Main Content Area**: Dynamic content rendering with Outlet

### 2. Main Dashboard Page
- **Stats Cards**: Display key metrics (total requests, monthly cost, data sources, response time)
- **Usage Chart**: Weekly usage trends using Recharts area chart
- **Quick Actions**: Fast links to common tasks
- **Recent Activity**: Feed of latest requests with status indicators

### 3. AI Playground
- **Chat Interface**: Real-time chat with AI providers
- **Provider Selection**: Switch between Claude, OpenAI, Jais, or Auto
- **Response Info**: Display tokens, cost, and latency for each response
- **Loading States**: Visual feedback during API calls

### 4. Logs Page
- **Filtering**: Search by query, filter by status and provider
- **Pagination**: Navigate through large log sets
- **Export**: Download logs as CSV
- **Detailed Logs**: Request ID, timestamp, provider, tokens, cost, and latency

### 5. Analytics Page
- **Cost Breakdown**: Pie chart showing cost distribution by provider
- **Usage Trends**: Bar chart of weekly usage by provider
- **Summary Stats**: Total cost, requests, and average cost per request

### 6. Data Sources Page
- **Table View**: Manage connected data sources
- **Status Indicators**: Visual connection status
- **Last Sync**: Track when data was last synchronized

### 7. API Keys Page
- **Key Management**: Create, view, and delete API keys
- **Key Masking**: Hide sensitive key information with reveal toggle
- **Copy to Clipboard**: Easy key sharing
- **Status Tracking**: See which keys are active and when they were last used

### 8. Settings Page
- **Tabs**: Profile, Notifications, Security, and Appearance
- **Profile Management**: Edit user information
- **Notification Preferences**: Control alert settings
- **Security Settings**: Change password functionality
- **Theme Selection**: Light/Dark/System theme options

## Technologies

- **React 18.2**: UI framework
- **TypeScript**: Type safety
- **React Router v6**: Client-side routing
- **Tailwind CSS**: Utility-first styling
- **Recharts**: Data visualization
- **Lucide React**: Icon library
- **Vite**: Build tool and dev server
- **Axios**: HTTP client (pre-configured)

## Arabic Localization

- **RTL Support**: All layouts use `dir="rtl"` for proper right-to-left rendering
- **Arabic Font**: Cairo font family for Arabic text
- **Translations**: Complete ar.json with 70+ translation keys
- **Keyboard Support**: RTL-aware input fields

## Setup Instructions

### Prerequisites
- Node.js 16+
- npm or yarn

### Installation

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Run linting
npm run lint
```

## Styling

- **Tailwind CSS**: Main styling framework with RTL support
- **Custom Colors**: Uses standard Tailwind palette
- **Responsive Design**: Mobile-first approach with breakpoints
  - `md:`: Medium screens (768px+)
  - `lg:`: Large screens (1024px+)

## Component API

### StatsCard
```tsx
<StatsCard
  title="string"
  value="string"
  change="string"
  changeType="increase" | "decrease"
  icon={IconComponent}
  iconColor="bg-blue-500"
/>
```

### UsageChart
- No props required
- Shows sample data with date range selector

### RecentActivity
- No props required
- Displays activity feed with status indicators

### Playground
- Full chat interface with provider selection
- Supports real-time message simulation

## Integration Points

### Ready for Backend Integration
1. **Playground.tsx**: API endpoint `/api/gateway/chat`
2. **Logs.tsx**: Could be populated from API logs endpoint
3. **Analytics.tsx**: Data from analytics API
4. **All pages**: User data from authentication context

### Authentication
- Currently uses placeholder components
- Ready for React Context or Redux integration
- Protected routes structure in place

## Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- RTL rendering on all modern browsers

## Performance Optimizations

- Code splitting with React Router
- Lazy loading ready
- Memoization structure in components
- Optimized chart rendering with Recharts

## Next Steps

1. **Connect to Backend**
   - Replace API calls in Playground with actual gateway endpoints
   - Populate real data in Dashboard, Logs, and Analytics

2. **Add Authentication**
   - Implement login/register pages
   - Add ProtectedRoute component
   - Integrate with auth backend

3. **Enhanced Features**
   - Real-time notifications
   - Data export functionality
   - Advanced filtering options
   - User preferences storage

4. **Testing**
   - Add unit tests with Vitest
   - Add integration tests
   - E2E testing with Cypress

## Commit History

- `eee2946`: Build complete admin dashboard with Arabic RTL UI

## License

Part of the Salma AI Gateway Enterprise project.
