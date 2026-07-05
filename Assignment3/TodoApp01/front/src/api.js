import axios from 'axios';

const API_BASE = 'http://localhost:8000';

export const fetchTodos = async (filter = 'all') => {
  const res = await axios.get(${API_BASE}/todos, { params: { filter } });
  return res.data;
};

export const addTodo = async (title) => {
  const res = await axios.post(${API_BASE}/todos, { title });
  return res.data;
};

export const updateTodo = async (id, completed) => {
  const res = await axios.put(`${API_BASE}/todos/${id}`, { completed });
  return res.data;
};

export const deleteTodo = async (id) => {
  const res = await axios.delete(`${API_BASE}/todos/${id}`);
  return res.data;
};

export const clearTodos = async (action) => {
  const res = await axios.delete(${API_BASE}/todos, { params: { action } });
  return res.data;
};
