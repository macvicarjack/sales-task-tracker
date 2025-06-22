import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import TaskForm from './components/TaskForm';
import TaskTable from './components/TaskTable';
import { Task, TaskCreate, TaskStatus } from './types';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

function App() {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [showForm, setShowForm] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState('');
  const [accountFilter, setAccountFilter] = useState('');

  // Fetch tasks from API
  const fetchTasks = useCallback(async () => {
    try {
      setLoading(true);
      const params = new URLSearchParams();
      if (statusFilter) params.append('status', statusFilter);
      if (accountFilter) params.append('account', accountFilter);
      
      const response = await axios.get(`${API_BASE_URL}/tasks?${params.toString()}`);
      setTasks(response.data);
      setError(null);
    } catch (err) {
      setError('Failed to fetch tasks. Please check if the backend server is running.');
      console.error('Error fetching tasks:', err);
    } finally {
      setLoading(false);
    }
  }, [statusFilter, accountFilter]);

  // Create new task
  const handleCreateTask = async (taskData: TaskCreate) => {
    try {
      const response = await axios.post(`${API_BASE_URL}/tasks`, taskData);
      setTasks(prev => [response.data, ...prev]);
      setShowForm(false);
      setError(null);
    } catch (err) {
      setError('Failed to create task. Please try again.');
      console.error('Error creating task:', err);
    }
  };

  // Update task status
  const handleStatusChange = async (taskId: number, newStatus: TaskStatus) => {
    try {
      const response = await axios.put(`${API_BASE_URL}/tasks/${taskId}`, {
        status: newStatus
      });
      setTasks(prev => prev.map(task => 
        task.id === taskId ? response.data : task
      ));
      setError(null);
    } catch (err) {
      setError('Failed to update task status. Please try again.');
      console.error('Error updating task:', err);
    }
  };

  // Delete task
  const handleDeleteTask = async (taskId: number) => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }
    
    try {
      await axios.delete(`${API_BASE_URL}/tasks/${taskId}`);
      setTasks(prev => prev.filter(task => task.id !== taskId));
      setError(null);
    } catch (err) {
      setError('Failed to delete task. Please try again.');
      console.error('Error deleting task:', err);
    }
  };

  // Filter tasks
  const handleStatusFilterChange = (status: string) => {
    setStatusFilter(status);
  };

  const handleAccountFilterChange = (account: string) => {
    setAccountFilter(account);
  };

  // Load tasks on component mount and when filters change
  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-7xl mx-auto py-6 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="px-4 py-6 sm:px-0">
          <div className="flex justify-between items-center mb-6">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Sales Task Tracker</h1>
              <p className="mt-1 text-sm text-gray-600">
                Manage and prioritize your sales tasks efficiently
              </p>
            </div>
            <button
              onClick={() => setShowForm(true)}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
            >
              Add New Task
            </button>
          </div>

          {/* Error Message */}
          {error && (
            <div className="mb-4 bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded">
              {error}
            </div>
          )}

          {/* Loading State */}
          {loading && (
            <div className="text-center py-8">
              <div className="inline-block animate-spin rounded-full h-8 w-8 border-b-2 border-primary-600"></div>
              <p className="mt-2 text-gray-600">Loading tasks...</p>
            </div>
          )}

          {/* Task Table */}
          {!loading && (
            <TaskTable
              tasks={tasks}
              onStatusChange={handleStatusChange}
              onDelete={handleDeleteTask}
              statusFilter={statusFilter}
              accountFilter={accountFilter}
              onStatusFilterChange={handleStatusFilterChange}
              onAccountFilterChange={handleAccountFilterChange}
            />
          )}
        </div>
      </div>

      {/* Task Form Modal */}
      {showForm && (
        <TaskForm
          onSubmit={handleCreateTask}
          onCancel={() => setShowForm(false)}
        />
      )}
    </div>
  );
}

export default App; 