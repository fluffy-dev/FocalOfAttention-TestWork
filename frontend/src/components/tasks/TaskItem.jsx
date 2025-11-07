/**
 * A component representing a single task item.
 *
 * Displays the task's title, description, and status. It provides controls
 * to change the task's status or delete the task entirely.
 */
import React from 'react';

// A helper function to get the color scheme for a given status
const getStatusClasses = (status) => {
  switch (status) {
    case 'pending':
      return 'bg-yellow-100 text-yellow-800';
    case 'in_progress':
      return 'bg-blue-100 text-blue-800';
    case 'done':
      return 'bg-green-100 text-green-800';
    default:
      return 'bg-gray-100 text-gray-800';
  }
};

const TaskItem = ({ task, onUpdateStatus, onDelete }) => {
  return (
    <div className="bg-white p-4 rounded-lg shadow-md flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0 sm:space-x-4">
      <div className="flex-grow">
        <h3 className="font-bold text-lg text-gray-900">{task.title}</h3>
        {task.description && <p className="text-gray-600 mt-1">{task.description}</p>}
      </div>
      <div className="flex items-center space-x-3 flex-shrink-0 w-full sm:w-auto">
        <div className={`px-3 py-1 text-sm font-semibold rounded-full ${getStatusClasses(task.status)}`}>
          {task.status.replace('_', ' ')}
        </div>
        <select
          value={task.status}
          onChange={(e) => onUpdateStatus(task.id, e.target.value)}
          className="border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 text-sm p-1.5"
        >
          <option value="pending">Pending</option>
          <option value="in_progress">In Progress</option>
          <option value="done">Done</option>
        </select>
        <button
          onClick={() => onDelete(task.id)}
          className="px-3 py-1.5 bg-red-500 text-white text-sm font-semibold rounded-lg shadow-sm hover:bg-red-600 focus:outline-none focus:ring-2 focus:ring-red-400"
        >
          Delete
        </button>
      </div>
    </div>
  );
};

export default TaskItem;