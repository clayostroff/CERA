export interface ReportStep {
    step: string;
    status: 'pending' | 'in_progress' | 'complete';
    timestamp?: string | null;
}

export interface ReportStatus {
    status: 'running' | 'in_progress' | 'complete' | 'error';
    steps: ReportStep[];
    report?: string | null;
    error?: string | null;
}

export interface TableOfContentsItem {
    id: string;
    title: string;
    level: number;
}