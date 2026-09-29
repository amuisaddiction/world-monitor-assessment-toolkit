import { Routes, Route, Navigate } from 'react-router-dom';
import Layout from './layouts/Layout';
import Overview from './pages/Overview';
import NewAssessment from './pages/NewAssessment';
import Findings from './pages/Findings';
import FindingDetail from './pages/FindingDetail';
import SystemHealth from './pages/SystemHealth';
import RiskAnalysis from './pages/RiskAnalysis';
import Reports from './pages/Reports';
import NotFound from './pages/NotFound';

function App() {
  return (
    <Routes>
      <Route path="/" element={<Layout />}>
        <Route index element={<Overview />} />
        <Route path="assessment" element={<NewAssessment />} />
        <Route path="findings" element={<Findings />} />
        <Route path="findings/:id" element={<FindingDetail />} />
        <Route path="risk" element={<RiskAnalysis />} />
        <Route path="reports" element={<Reports />} />
        <Route path="health" element={<SystemHealth />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}

export default App;
