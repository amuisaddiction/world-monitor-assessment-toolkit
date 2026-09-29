import { Outlet, NavLink } from 'react-router-dom';
import { Shield, Activity, Search, AlertTriangle, FileText, Settings, Database, Server } from 'lucide-react';
import { useSystemHealth } from '../hooks/useSystemHealth';
import clsx from 'clsx';

export default function Layout() {
  const { health, loading, error, retry } = useSystemHealth();

  const navItems = [
    { name: 'Overview', path: '/', icon: Activity },
    { name: 'New Assessment', path: '/assessment', icon: Search },
    { name: 'Findings', path: '/findings', icon: AlertTriangle },
    { name: 'Risk Analysis', path: '/risk', icon: Database },
    { name: 'Reports', path: '/reports', icon: FileText },
    { name: 'System Health', path: '/health', icon: Server },
  ];

  return (
    <div className="flex h-screen bg-primaryBg text-textPrimary font-sans">
      {/* Sidebar */}
      <aside className="w-64 bg-secondaryBg border-r border-borderBg flex flex-col hidden md:flex">
        <div className="h-16 flex items-center px-6 border-b border-borderBg">
          <Shield className="w-6 h-6 text-primaryBlue mr-3" />
          <span className="font-bold text-lg tracking-wide text-white">WORLD MONITOR</span>
        </div>
        
        <div className="px-6 py-4">
          <p className="text-xs font-semibold text-textSecondary uppercase tracking-wider mb-4">
            Security Center
          </p>
          <nav className="space-y-1">
            {navItems.map((item) => (
              <NavLink
                key={item.name}
                to={item.path}
                className={({ isActive }) =>
                  clsx(
                    'flex items-center px-3 py-2.5 text-sm font-medium rounded-md transition-colors',
                    isActive 
                      ? 'bg-cardBg text-primaryBlue border border-borderBg' 
                      : 'text-textSecondary hover:bg-cardBg hover:text-textPrimary'
                  )
                }
              >
                <item.icon className="w-5 h-5 mr-3 flex-shrink-0" />
                {item.name}
              </NavLink>
            ))}
          </nav>
        </div>

        <div className="mt-auto p-4 border-t border-borderBg">
          <div className="bg-cardBg rounded-md p-3 border border-borderBg">
            <h4 className="text-xs font-medium text-textSecondary uppercase mb-2">API Status</h4>
            <div className="flex items-center justify-between">
              <div className="flex items-center">
                <span className={clsx("w-2.5 h-2.5 rounded-full mr-2", {
                  'bg-success': health?.status === 'healthy',
                  'bg-warning animate-pulse': loading,
                  'bg-critical': error || (!loading && !health)
                })} />
                <span className="text-sm font-medium">
                  {loading ? 'Connecting...' : health ? 'Operational' : 'Offline'}
                </span>
              </div>
              {(error || (!loading && !health)) && (
                <button onClick={retry} className="text-xs text-primaryBlue hover:underline">Retry</button>
              )}
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 flex flex-col overflow-hidden">
        {/* Topbar */}
        <header className="h-16 bg-secondaryBg border-b border-borderBg flex items-center justify-between px-6">
          <div className="flex items-center">
            <span className="bg-blue-900/30 text-primaryBlue border border-blue-800/50 px-3 py-1 rounded text-xs font-semibold tracking-wide">
              AUTHORIZED ASSESSMENT ENVIRONMENT
            </span>
          </div>
          <div className="flex items-center space-x-4">
            <span className="text-sm text-textSecondary">SOC Analyst</span>
            <div className="w-8 h-8 bg-cardBg rounded-full border border-borderBg flex items-center justify-center">
              <Shield className="w-4 h-4 text-textSecondary" />
            </div>
          </div>
        </header>
        
        {/* Page Content */}
        <div className="flex-1 overflow-auto p-6 lg:p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
