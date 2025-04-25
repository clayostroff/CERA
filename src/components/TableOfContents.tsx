import React from 'react';
import { ChevronDown, ChevronUp } from 'lucide-react';
import { TableOfContentsItem } from '../types';

interface TableOfContentsProps {
  items: TableOfContentsItem[];
  isCollapsed: boolean;
  toggleCollapse: () => void;
}

const TableOfContents: React.FC<TableOfContentsProps> = ({ 
  items, 
  isCollapsed,
  toggleCollapse
}) => {
  return (
    <div className="bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-lg p-4 mb-6 transition-all duration-300">
      <div 
        className="flex justify-between items-center cursor-pointer"
        onClick={toggleCollapse}
      >
        <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-200">
          Table of Contents
        </h2>
        <button className="text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300">
          {isCollapsed ? <ChevronDown size={20} /> : <ChevronUp size={20} />}
        </button>
      </div>
      
      {!isCollapsed && (
        <nav className="mt-4 border-t border-gray-200 dark:border-gray-700 pt-4">
          <ul className="space-y-2">
            {items.map((item) => (
              <li 
                key={item.id}
                className={`${item.level === 1 ? '' : 'ml-4'} ${item.level === 3 ? 'ml-8' : ''}`}
              >
                <a
                  href={`#${item.id}`}
                  className="text-gray-700 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors duration-200"
                >
                  {item.title}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      )}
    </div>
  );
};

export default TableOfContents;