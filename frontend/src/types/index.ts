export interface Task {
  id: number;
  title: string;
  description?: string;
  revenue_potential: number;
  days_open: number;
  priority_score: number;
  contact_person?: string;
  account?: string;
  next_steps?: string;
  due_date?: string;
  status: 'open' | 'in-progress' | 'closed';
  created_at: string; // ISO datetime string
  updated_at?: string; // ISO datetime string
}

export interface TaskCreate {
  title: string;
  description?: string;
  revenue_potential: number;
  contact_person?: string;
  account?: string;
  next_steps?: string;
  due_date?: string;
  status: 'open' | 'in-progress' | 'closed';
}

export interface TaskUpdate {
  title?: string;
  description?: string;
  revenue_potential?: number;
  contact_person?: string;
  account?: string;
  next_steps?: string;
  due_date?: string;
  status?: 'open' | 'in-progress' | 'closed';
}

export type TaskStatus = 'open' | 'in-progress' | 'closed'; 