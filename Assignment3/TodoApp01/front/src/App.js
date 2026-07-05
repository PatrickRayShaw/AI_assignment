import React, { useState, useEffect, useCallback } from 'react';
import { fetchTodos, addTodo, updateTodo, deleteTodo, clearTodos } from './api';
import './App.css';

function App() {
  const [todos, setTodos] = useState([]);
  const [filter, setFilter] = useState('all');
  const [title, setTitle] = useState('');

  const loadTodos = useCallback(async () => {
    const data = await fetchTodos(filter);
    setTodos(data);
  }, [filter]);

  useEffect(() => { loadTodos(); }, [loadTodos]);

  const handleAdd = async () => {
    if (!title.trim()) return;
    await addTodo(title.trim());
    setTitle('');
    loadTodos();
  };

  const handleToggle = async (id, completed) => {
    await updateTodo(id, !completed);
    loadTodos();
  };

  const handleDelete = async (id) => {
    await deleteTodo(id);
    loadTodos();
  };

  const handleClear = async (action) => {
    await clearTodos(action);
    loadTodos();
  };

  return (
    <div className="app">
      <h1>待办事项</h1>
      <div className="add-form">
        <input value={title} onChange={e => setTitle(e.target.value)} placeholder="输入新任务..." />
        <button onClick={handleAdd}>添加</button>
      </div>
      <div className="filter-bar">
        {['all', 'uncompleted', 'completed'].map(f => (
          <button key={f} className={filter === f ? 'active' : ''} onClick={() => setFilter(f)}>
            {f === 'all' ? '全部' : f === 'completed' ? '已完成' : '未完成'}
          </button>
        ))}
      </div>
      <ul className="todo-list">
        {todos.map(todo => (
          <li key={todo.id} className={todo.completed ? 'completed' : ''}>
            <span>{todo.title}</span>
            <div className="actions">
              <button onClick={() => handleToggle(todo.id, todo.completed)}>
                {todo.completed ? '撤销' : '完成'}
              </button>
              <button onClick={() => handleDelete(todo.id)}>删除</button>
            </div>
          </li>
        ))}
      </ul>
      <div className="clear-bar">
        <button onClick={() => handleClear('completed')}>清除已完成</button>
        <button onClick={() => handleClear('all')}>清除全部</button>
      </div>
    </div>
  );
}

export default App;
