import React, { useState } from 'react';
import { Moon, Sun } from 'lucide-react';
import SearchForm from './components/SearchForm';
import ReportViewer from './components/ReportViewer';
import ThemeToggle from './components/ThemeToggle';
import StatusTimeline from './components/StatusTimeline';
import { ReportStatus } from './types';

function App() {
    const [darkMode, setDarkMode] = useState(() => {
        const savedTheme = localStorage.getItem('theme');
        return savedTheme === 'dark' || 
            (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches);
    });
    
    const [searchTopic, setSearchTopic] = useState<string | null>(null);
    const [reportStatus, setReportStatus] = useState<ReportStatus | null>(null);
    const [timelineStep, setTimelineStep] = useState<string>('idle');

    const toggleDarkMode = () => {
        const newMode = !darkMode;
        setDarkMode(newMode);
        localStorage.setItem('theme', newMode ? 'dark' : 'light');
        document.body.classList.toggle('dark', newMode);
    };
    
    React.useEffect(() => {
        document.body.classList.toggle('dark', darkMode);
    }, []);

    return (
        <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
            <header className="bg-white dark:bg-gray-800 shadow-sm">
                <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                    <h1 className="text-2xl sm:text-3xl font-bold text-gray-800 dark:text-white">
                        CERA
                    </h1>
                    <ThemeToggle darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
                </div>
            </header>

            <main className="container mx-auto px-4 py-8">
                <SearchForm 
                    setSearchTopic={setSearchTopic} 
                    setReportStatus={setReportStatus}
                    setTimelineStep={setTimelineStep}
                />
                
                {searchTopic && (
                    <StatusTimeline 
                        timelineStep={timelineStep}
                        reportStatus={reportStatus}
                    />
                )}
                
                {searchTopic && (
                    <ReportViewer 
                        searchTopic={searchTopic} 
                        reportStatus={reportStatus}
                        setReportStatus={setReportStatus}
                        setTimelineStep={setTimelineStep}
                    />
                )}
            </main>
        </div>
    );
}

export default App;