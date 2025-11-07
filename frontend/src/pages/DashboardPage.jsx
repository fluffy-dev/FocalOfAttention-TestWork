import React, { useState, useEffect, useCallback } from 'react';
import { useAuth } from '../hooks/useAuth';
import { apiService } from '../services/api';
import AddTaskForm from '../components/tasks/AddTaskForm';
import TaskList from '../components/tasks/TaskList';

const DashboardPage = () => {
  const { user, logout } = useAuth();
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [filter, setFilter] = useState('all'); // 'all', 'pending', 'in_progress', 'done'

  const fetchTasks = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const response = await apiService.tasks.getAll(filter === 'all' ? null : filter);
      setTasks(response.data);
    } catch (err) {
      setError('Failed to fetch tasks.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, [filter]);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const handleAddTask = async (taskData) => {
    const response = await apiService.tasks.create(taskData);
    setTasks(prevTasks => [response.data, ...prevTasks]);
  };

  const handleUpdateStatus = async (taskId, status) => {
    const response = await apiService.tasks.update(taskId, { status });
    setTasks(prevTasks =>
      prevTasks.map(task => (task.id === taskId ? response.data : task))
    );
  };

  const handleDeleteTask = async (taskId) => {
    await apiService.tasks.delete(taskId);
    setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
  };

  const filterButtons = ['all', 'pending', 'in_progress', 'done'];

  return (
    <div className="min-h-screen bg-gray-100 p-4 sm:p-6 lg:p-8">
      <header className="max-w-7xl mx-auto flex justify-between items-center mb-8">
        <h1 className="text-2xl sm:text-3xl font-bold text-gray-900">
          Welcome, User #{user?.id}
        </h1>
        <button
          onClick={logout}
          className="px-4 py-2 bg-red-600 text-white font-semibold rounded-lg shadow-md hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-opacity-75"
        >
          Logout
        </button>
      </header>

      <main className="max-w-7xl mx-auto">
        <AddTaskForm onAddTask={handleAddTask} />

        <div className="flex items-center justify-between mb-4">
            <h2 className="text-xl font-semibold">Your Tasks</h2>
            <div className="flex space-x-2">
                {filterButtons.map(status => (
                    <button
                        key={status}
                        onClick={() => setFilter(status)}
                        className={`px-3 py-1 text-sm font-medium rounded-full capitalize ${
                            filter === status
                            ? 'bg-indigo-600 text-white'
                            : 'bg-white text-gray-600 hover:bg-gray-200'
                        }`}
                    >
                        {status.replace('_', ' ')}
                    </button>
                ))}
            </div>
        </div>

        {loading && <p className="text-center text-gray-500">Loading tasks...</p>}
        {error && <p className="text-center text-red-500">{error}</p>}
        {!loading && !error && (
          <TaskList
            tasks={tasks}
            onUpdateStatus={handleUpdateStatus}
            onDelete={handleDeleteTask}
          />
        )}
      </main>
    </div>
  );
};

export default DashboardPage;