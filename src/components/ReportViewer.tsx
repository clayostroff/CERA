import React, { useEffect, useRef, useState } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { AlertCircle, Download } from 'lucide-react';
import jsPDF from 'jspdf';
import * as htmlToImage from 'html-to-image';
import { ReportStatus, TableOfContentsItem } from '../types';
import TableOfContents from './TableOfContents';

interface ReportViewerProps {
    searchTopic: string;
    setTimelineStep: React.Dispatch<React.SetStateAction<string>>;
}

const ReportViewer: React.FC<ReportViewerProps> = ({ searchTopic, setTimelineStep }) =>
{    
    const [report, setReport] = useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);
    const [tocItems, setTocItems] = useState<TableOfContentsItem[]>([]);
    const [tocCollapsed, setTocCollapsed] = useState(false);
    const reportRef = useRef<HTMLDivElement>(null);

    useEffect(() =>
    {
        if (!searchTopic) return;

        setIsLoading(true);
        setError(null);
        setReport(null);

        const STEPS = ['plan_report', 'search_web', 'write_section', 'compile_report'];

    
        const es = new EventSource(
            'http://localhost:8000/report?topic=' + encodeURIComponent(searchTopic)
        );
    
        es.addEventListener('step', (evt) => 
        {
            const { node, diff } = JSON.parse(evt.data);
            
            // LangGraph nodes in sub-graphs (i.e. sub-nodes) return compound node names
            // build_section.search_web
            // build_section.write_section
            const temp = node.split('.').pop()!;
            
            const subnode = temp === 'plan_report' ? 'search_web'
                : temp === 'search_web' ? 'write_section'
                : temp === 'write_section' ? 'compile_report'
                : temp === 'compile_report' ? 'complete'
                : null;


            if (subnode) {
                setTimelineStep(prev =>
                    STEPS.indexOf(subnode) > STEPS.indexOf(prev) ? subnode : prev
                );
            }
            
            if (node === 'compile_report' && diff.finished_report) {
                setReport(diff.finished_report as string);
                setIsLoading(false);
                setTimelineStep('compile_report');
                setTimeout(() => setTimelineStep('complete'), 0);
            
                es.close();
            }
        });
    
        es.addEventListener('error', (err) => {
            console.error('SSE error', err);
            if (!report) {
                setError('Connection lost. Please try again.');
                setIsLoading(false);
            }
            es.close();
        });
    
        return () => {
            es.close();
        };
    }, [searchTopic]);
    
    useEffect(() => {
        if (report) {
            const headerRegex = /^(#{1,3})\s+(.+)$/gm;
            const items: TableOfContentsItem[] = [];
            let match;
            
            while ((match = headerRegex.exec(report)) !== null) {
                const level = match[1].length;
                const title = match[2].trim();
                const id = title.toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, '-');
                
                items.push({ id, title, level });
            }
            
            setTocItems(items);
        }
    }, [report]);
    
    // Function to export report as PDF
    const exportToPDF = async () => {
        if (!reportRef.current || !report) return;
        
        try {
            const canvas = await htmlToImage.toCanvas(reportRef.current);
            const imgData = canvas.toDataURL('image/png');
            
            const pdf = new jsPDF({
                orientation: 'portrait',
                unit: 'px',
                format: [canvas.width, canvas.height]
            });
            
            pdf.addImage(imgData, 'PNG', 0, 0, canvas.width, canvas.height);
            pdf.save(`report-${searchTopic.replace(/\s+/g, '-')}.pdf`);
        } catch (err) {
            console.error('Error generating PDF:', err);
        }
    };

    // Custom renderer for headers to add IDs for anchor links
    const customRenderers = {
        h1: ({ children }: any) => {
            const id = children[0].toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, '-');
            return <h1 id={id} className="text-3xl font-bold mt-8 mb-4">{children}</h1>;
        },
        h2: ({ children }: any) => {
            const id = children[0].toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, '-');
            return <h2 id={id} className="text-2xl font-bold mt-6 mb-3">{children}</h2>;
        },
        h3: ({ children }: any) => {
            const id = children[0].toLowerCase().replace(/[^\w\s]/g, '').replace(/\s+/g, '-');
            return <h3 id={id} className="text-xl font-bold mt-5 mb-2">{children}</h3>;
        }
    };

    if (isLoading) {
        return (
            <div className="flex flex-col items-center justify-center py-12">
                <div className="loader mb-4"></div>
                <p className="text-lg text-gray-600 dark:text-gray-400">
                    Generating your report...
                </p>
                <p className="text-sm text-gray-500 dark:text-gray-500 mt-2">
                    This may take up to a minute.
                </p>
            </div>
        );
    }

    if (error) {
        return (
            <div className="bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800 rounded-lg p-4 text-red-700 dark:text-red-400">
                <div className="flex items-start">
                    <AlertCircle className="mr-2 mt-0.5 flex-shrink-0" size={20} />
                    <div>
                        <h2 className="text-lg font-semibold">Error</h2>
                        <p>{error}</p>
                    </div>
                </div>
            </div>
        );
    }

    return (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="md:col-span-1">
                {tocItems.length > 0 && (
                    <div className="sticky top-6">
                        <TableOfContents 
                            items={tocItems} 
                            isCollapsed={tocCollapsed}
                            toggleCollapse={() => setTocCollapsed(!tocCollapsed)}
                        />
                        
                        <button
                            onClick={exportToPDF}
                            className="w-full mt-4 px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg flex items-center justify-center transition-colors"
                        >
                            <Download size={18} className="mr-2" />
                            Export to PDF
                        </button>
                    </div>
                )}
            </div>
            
            <div className="md:col-span-3" ref={reportRef}>
                <div className="bg-white dark:bg-gray-800 border-2 border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-8 transition-colors">
                    {report ? (
                        <ReactMarkdown 
                            className="markdown-content"
                            remarkPlugins={[remarkGfm]}
                            components={customRenderers}
                        >
                            {report}
                        </ReactMarkdown>
                    ) : (
                        <p>No report content available</p>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ReportViewer;