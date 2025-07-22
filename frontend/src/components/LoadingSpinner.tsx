import React from 'react';
import { Loader } from 'lucide-react';

export const LoadingSpinner: React.FC = () => {
  return (
    <div className="flex items-center justify-center py-8">
      <div className="flex items-center gap-2 text-gray-500">
        <Loader className="animate-spin" size={20} />
        <span>Loading...</span>
      </div>
    </div>
  );
};