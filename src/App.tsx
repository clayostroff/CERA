import React, { useState } from 'react';
import SearchForm from './components/SearchForm';
import ReportViewer from './components/ReportViewer';
import ThemeToggle from './components/ThemeToggle';
import StatusTimeline from './components/StatusTimeline';

function App() {
    const [darkMode, setDarkMode] = useState(() => {
        const savedTheme = localStorage.getItem('theme');
        return savedTheme === 'dark' || 
            (!savedTheme && window.matchMedia('(prefers-color-scheme: dark)').matches);
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
            <header className="bg-grey-50 dark:bg-gray-900">
                <div className="container mx-auto px-4 py-8 relative">
                    <h1 className="absolute left-1/2 top-1/2 transform -translate-x-1/2 -translate-y-2 text-5xl sm:text-5xl font-bold text-yellow-400 dark:text-white">
                        CERA
                    </h1>
                    <div className="flex justify-end translate-y-4">
                        <ThemeToggle darkMode={darkMode} toggleDarkMode={toggleDarkMode} />
                    </div>
                </div>
            </header>

            <main className="container mx-auto px-4 py-8">
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