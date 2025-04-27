import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import ReportViewer from './components/ReportViewer';
import ThemeToggle from './components/ThemeToggle';
import StatusTimeline from './components/StatusTimeline';

function App() {
    const [darkMode, setDarkMode] = useState(() => {
        const savedTheme = localStorage.getItem('theme');
        return savedTheme === 'dark' || 
            (!savedTheme && window.matchMedia('(prefers-color-scheme: light)').matches);
    });
    
    const [searchTopic, setSearchTopic] = useState<string | null>(null);
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
            <main className="container mx-auto px-4 py-8">
                <h1 className="flex items-center justify-between text-4xl font-bold text-gray-700 dark:text-white mb-8 px-0.5">
                    <span>Current Events Research Agent</span>
                    <ThemeToggle darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
                </h1>
                <SearchForm 
                    setSearchTopic={setSearchTopic}
                    setTimelineStep={setTimelineStep}
                    currentTopic={searchTopic}
                />
                
                {searchTopic && (
                    <StatusTimeline 
                        timelineStep={timelineStep}
                    />
                )}
                
                {searchTopic && (
                    <ReportViewer 
                        searchTopic={searchTopic}
                        setTimelineStep={setTimelineStep}
                    />
                )}
            </main>
        </div>
    );
}

export default App;