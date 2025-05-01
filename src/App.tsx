import React, { useState, useEffect } from 'react';
import { FiGithub } from 'react-icons/fi';
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
                <h1 className="flex items-center justify-between mb-8">
                    <div className="flex items-center space-x-4 px-0.5">

                        <span className="text-4xl font-bold text-gray-800 dark:text-white">
                            Current Events Research Agent
                        </span>
                        <div className="h-10 w-10 flex items-center justify-center">
                            <ThemeToggle darkMode={darkMode} toggleDarkMode={toggleDarkMode}/>
                        </div>
                    </div>
                    <div className="flex items-center space-x-2">
                        <a
                        href="https://tavily.com"
                        target="_blank"
                        rel="noopener noreferrer"
                        className={"bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors backdrop-filter backdrop-blur-lg border border-gray-200 dark:border-gray-800 shadow-xl rounded-lg flex items-center justify-center"}
                        style={{ width: 40, height: 40, padding: 8 }}
                        aria-label="Tavily site"
                        >
                        <img
                            src="/tavilylogo.svg"
                            alt="Tavily logo"
                            className="w-full h-full object-contain"
                            style={{ width: 24, height: 24, margin: 'auto', display: 'block' }}
                        />
                        </a>
                        <a
                            href="https://github.com/clayostroff/CERA"
                            target="_blank"
                            rel="noopener noreferrer"
                            className={"bg-white dark:bg-gray-800 text-gray-800 dark:text-gray-200 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors backdrop-filter backdrop-blur-lg border border-gray-200 dark:border-gray-800 shadow-xl rounded-lg flex items-center justify-center"}
                            style={{ width: 40, height: 40, padding: 8 }}
                            aria-label="GitHub repo"
                            >
                            <FiGithub
                                style={{ width: 24, height: 24, margin: 'auto', display: 'block' }}
                            />
                        </a>
                    </div>
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