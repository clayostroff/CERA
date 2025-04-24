import React, { useState, useEffect } from 'react';
import { Search, AlertCircle } from 'lucide-react';
import axios from 'axios';

interface SearchFormProps {
    setSearchTopic: React.Dispatch<React.SetStateAction<string | null>>;
    setReportStatus: React.Dispatch<React.SetStateAction<any | null>>;
    setTimelineStep: React.Dispatch<React.SetStateAction<string>>;
}

const SearchForm: React.FC<SearchFormProps> = ({ 
    setSearchTopic, 
    setReportStatus,
    setTimelineStep 
}) => {
    const [question, setQuestion] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');
    
    // Check if backend is running
    useEffect(() => {
        const checkBackendStatus = async () => {
            try {
                await axios.get('http://localhost:8000/docs', { timeout: 2000 });
                setBackendStatus('online');
            } catch (err) {
                setBackendStatus('offline');
            }
        };
        
        checkBackendStatus();
    }, []);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        
        if (!question.trim()) {
            setError('Please enter a question');
            return;
        }
        
        if (backendStatus === 'offline') {
            setError('Backend server is not running. Please start the backend with "npm run start-api"');
            return;
        }
        
        setError('');
        setIsLoading(true);
        setTimelineStep('plan_report');
        
        try {
            // Set the search topic to start the process
            setSearchTopic(question.trim());
        } catch (err) {
            console.error('Error setting search topic:', err);
            setError('Failed to start report generation. Please try again.');
            setTimelineStep('idle');
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="mb-8">
            {backendStatus === 'offline' && (
                <div className="mb-4 p-4 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-lg text-amber-700 dark:text-amber-400 flex items-start">
                    <AlertCircle className="mr-2 mt-0.5 flex-shrink-0" size={18} />
                    <div>
                        <p className="font-medium">Backend server is not running</p>
                        <p className="text-sm mt-1">Please start the backend server with <code className="bg-amber-100 dark:bg-amber-900/40 px-1.5 py-0.5 rounded">npm run start-api</code> in a new terminal window.</p>
                    </div>
                </div>
            )}
            
            <form 
                onSubmit={handleSubmit}
                className="flex flex-col sm:flex-row space-y-3 sm:space-y-0 sm:space-x-2"
            >
                <div className="flex-grow relative">
                    <input
                        type="text"
                        value={question}
                        onChange={(e) => setQuestion(e.target.value)}
                        placeholder="What are the latest developments in renewable energy?"
                        className="w-full px-4 py-3 rounded-lg border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-800 text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-colors"
                        disabled={isLoading}
                    />
                </div>
                <button
                    type="submit"
                    disabled={isLoading || backendStatus === 'offline'}
                    className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg flex items-center justify-center transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
                >
                    {isLoading ? (
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    ) : (
                        <Search size={20} className="mr-2" />
                    )}
                    Search
                </button>
            </form>
            
            {error && (
                <div className="mt-2 text-red-500 text-sm">{error}</div>
            )}
        </div>
    );
};

export default SearchForm;