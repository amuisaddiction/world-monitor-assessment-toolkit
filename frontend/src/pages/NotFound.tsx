import { Link } from 'react-router-dom';
import { AlertOctagon } from 'lucide-react';

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center h-full">
      <AlertOctagon className="w-16 h-16 text-warning mb-4" />
      <h1 className="text-2xl font-bold mb-2">404 - Not Found</h1>
      <p className="text-textSecondary mb-6">The page you are looking for does not exist in the Security Center.</p>
      <Link to="/" className="bg-primaryBlue hover:bg-secondaryBlue text-white px-6 py-2 rounded-md font-medium transition-colors">
        Return to Overview
      </Link>
    </div>
  );
}
