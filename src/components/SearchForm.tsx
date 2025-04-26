import React, { useState, useEffect } from 'react';
import { Search, AlertCircle } from 'lucide-react';
import axios from 'axios';

interface SearchFormProps {
    setSearchTopic: React.Dispatch<React.SetStateAction<string | null>>;
    setTimelineStep: React.Dispatch<React.SetStateAction<string>>;
    currentTopic: string | null;
}

const SearchForm: React.FC<SearchFormProps> = ({
    setSearchTopic,
    setTimelineStep,
    currentTopic
}) => {
    const [question, setQuestion] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [error, setError] = useState('');
    const [backendStatus, setBackendStatus] = useState<'online' | 'offline' | 'checking'>('checking');
    
    // Check if the backend is running
    useEffect(() => {
    axios.get('http://localhost:8000/docs', { timeout: 2000 })
      .then(() => setBackendStatus('online'))
      .catch(() => setBackendStatus('offline'));
    }, []);

    const handleSubmit = async (e: React.FormEvent) =>
    {
        e.preventDefault();
        
        if (!question.trim()) {
            setError("Please ask a question or submit a report topic.")
            return;
        }

        if (question.trim() === currentTopic) {
            setError("A report answering that question has already been generated.");
            return;
        }
        
        if (backendStatus === 'offline') {
            setError("The backend server is not running. Please start the server with npm run start in a new terminal window.");
            return;
        }
        
        setError('');
        setIsLoading(true);
        setTimelineStep('plan_report');
        try {
            setSearchTopic(question.trim());
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="mb-8">
            {backendStatus === 'offline' && (
                <div className="mb-4 p-4 bg-amber-50 dark:bg-amber-900/20 border-2 border-amber-200 dark:border-amber-800 rounded-lg text-amber-700 dark:text-amber-400 flex items-start">
                    <AlertCircle className="mr-2 mt-0.5 flex-shrink-0" size={18}/>
                    <div>
                        <p className="font-bold inline">The backend server is not running. </p>
                        <p className="inline mt-1">Please start the server with <code className="bg-amber-100 dark:bg-amber-900/40 px-1.5 py-0.5 rounded">npm run start</code> in a new terminal and refresh the page.</p>
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
                        placeholder="What are the latest developments in the Ukraine war?"
                        className="w-full px-4 py-4 rounded-lg border-2 border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800 text-lg text-gray-900 dark:text-gray-100 focus:outline-none focus:ring-2 focus:ring-blue-500 dark:focus:ring-blue-400 transition-colors"
                        disabled={isLoading}
                    />
                </div>
                <button
                    type="submit"
                    disabled={
                        isLoading ||
                        backendStatus === 'offline' ||
                        question.trim() === currentTopic
                    }
                    className="px-6 py-4 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg flex items-center justify-center transition-colors duration-200 disabled:opacity-70 disabled:cursor-not-allowed"
                >
                    {isLoading ? (
                        <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin mr-2"></div>
                    ) : (
                        <Search size={20} className="mr-2" />
                    )}
                    Generate
                </button>
            </form>
            
            {error && (
                <div className="mt-2 text-red-500 text-sm">{error}</div>
            )}
        </div>
    );
};

export default SearchForm;