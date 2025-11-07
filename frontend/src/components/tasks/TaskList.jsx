/**
 * A component that renders a list of TaskItem components.
 */
import React from 'react';
import TaskItem from './TaskItem';

const TaskList = ({ tasks, onUpdateStatus, onDelete }) => {
  if (tasks.length === 0) {
    return (
      <div className="bg-white p-6 rounded-lg shadow-md text-center text-gray-500">
        You have no tasks. Add one to get started!
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {tasks.map((task) => (
        <TaskItem
          key={task.id}
          task={task}
          onUpdateStatus={onUpdateStatus}
          onDelete={onDelete}
        />
      ))}
    </div>
  );
};

export default TaskList;