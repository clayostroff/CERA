import React from 'react';
import { CheckCircle, Circle, Clock } from 'lucide-react';
import { ReportStatus } from '../types';

interface StatusTimelineProps {
    timelineStep: string;
    reportStatus: ReportStatus | null;
}

const StatusTimeline: React.FC<StatusTimelineProps> = ({ timelineStep, reportStatus }) => {
    const steps = [
        { id: 'plan_report', label: 'Planning report' },
        { id: 'initiate_section_writing', label: 'Researching sections' },
        { id: 'format_sections_as_string', label: 'Writing sections' },
        { id: 'compile_report', label: 'Compiling report' }
    ];
    
    const order = ['plan_report', 'search_web', 'write_section', 'compile_report'];
    
    const currentIndex =
    timelineStep === 'complete' ? order.length : order.indexOf(timelineStep);

    const getStepStatus = (stepId: string) => {
        const idx = order.indexOf(stepId);
        if (idx < currentIndex) return 'complete';
        if (idx === currentIndex) return 'in_progress';
        return 'pending';
    };

    return (
        <div className="my-8">
            <div className="flex items-center justify-between">
                {steps.map((step, index) => (
                    <React.Fragment key={step.id}>
                        <div className="flex flex-col items-center">
                            <div 
                                className={`
                                    w-8 h-8 rounded-full flex items-center justify-center
                                    ${getStepStatus(step.id) === 'complete' ? 'bg-green-500 text-white' : 
                                        getStepStatus(step.id) === 'in_progress' ? 'bg-blue-500 text-white' : 
                                        'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'}
                                    transition-colors duration-300
                                `}
                            >
                                {getStepStatus(step.id) === 'complete' ? (
                                    <CheckCircle size={20} />
                                ) : getStepStatus(step.id) === 'in_progress' ? (
                                    <Clock size={20} />
                                ) : (
                                    <Circle size={20} />
                                )}
                            </div>
                            <span className="mt-2 text-xs sm:text-sm text-center">{step.label}</span>
                        </div>
                        
                        {index < steps.length - 1 && (
                            <div 
                                className={`
                                    flex-grow h-1 mx-2
                                    ${getStepStatus(step.id) === 'complete' ? 'bg-green-500' : 
                                        getStepStatus(step.id) === 'in_progress' ? 'bg-blue-500' : 
                                        'bg-gray-200 dark:bg-gray-700'}
                                `}
                            ></div>
                        )}
                    </React.Fragment>
                ))}
            </div>
        </div>
    );
};

export default StatusTimeline;