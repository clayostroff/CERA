import React from 'react';
import { CheckCircle, Circle, Clock } from 'lucide-react';

interface StatusTimelineProps {
  timelineStep: string;
}

const STEPS = [
  { id: 'plan_report', label: 'Planning' },
  { id: 'search_web', label: 'Researching' },
  { id: 'write_section', label: 'Writing' },
  { id: 'compile_report', label: 'Compiling' }
];

export default function StatusTimeline({ timelineStep }: StatusTimelineProps)
{
  const currIdx = timelineStep === 'complete' ? STEPS.length : STEPS.findIndex(s => s.id === timelineStep);

  const status = (idx: number) =>
    idx < currIdx ? 'complete' : idx === currIdx ? 'in_progress' : 'pending';

  return (
    <div className="my-8 bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-lg px-10 py-6 transition-colors duration-300">
      <div className="flex items-center">
        {STEPS.map((step, idx) => (
          <React.Fragment key={step.id}>
            <div className={
              `w-9 h-9 rounded-full flex items-center justify-center transition-colors
               ${status(idx)==='complete'    ? 'bg-lime-500 text-white' :
                 status(idx)==='in_progress' ? 'bg-blue-500 text-white'  :
                                               'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'}`
            }>
              {status(idx) === 'complete'    ? <CheckCircle size={20}/> :
               status(idx) === 'in_progress' ? <Clock size={20}/> :
                                               <Circle size={20}/>}
            </div>
            
            {idx < STEPS.length - 1 && (
              <div className={
                `flex-grow h-1 mx-3 rounded-full transition-colors
                 ${status(idx)==='complete'    ? 'bg-lime-500' :
                   status(idx)==='in_progress' ? 'bg-blue-500'  :
                                                 'bg-gray-200 dark:bg-gray-700'}`
              }/>
            )}
          </React.Fragment>
        ))}
      </div>
      
      <div className="flex mt-2">
        {STEPS.map((step, idx) => (
          <React.Fragment key={step.id}>
            <div className="relative w-9 h-4">
              <span className="absolute left-1/2 -translate-x-1/2 whitespace-nowrap
                               font-bold text-xs sm:text-sm text-center">
                {step.label}
              </span>
            </div>

            {idx < STEPS.length - 1 && <div className="flex-grow mx-2" />}
          </React.Fragment>
        ))}
      </div>
    </div>
  );
}