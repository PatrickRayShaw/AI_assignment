// ===== DOM 元素 =====
const todoForm = document.getElementById('todo-form');
const todoInput = document.getElementById('todo-input');
const todoList = document.getElementById('todo-list');
const todoCount = document.getElementById('todo-count');
const clearCompletedBtn = document.getElementById('clear-completed');
const clearAllBtn = document.getElementById('clear-all');
const filterBtns = document.querySelectorAll('.filter-btn');

// ===== 状态 =====
let todos = [];           // 完整待办数组: [{id, text, completed}]
let currentFilter = 'all'; // 'all' | 'active' | 'completed'

// ===== LocalStorage 读写 =====
function saveTodos() {
    localStorage.setItem('todo-app-data', JSON.stringify(todos));
}

function loadTodos() {
    const raw = localStorage.getItem('todo-app-data');
    if (raw) {
        try {
            todos = JSON.parse(raw);
        } catch (e) {
            todos = [];
        }
    }
}

// ===== 生成唯一 ID =====
function generateId() {
    return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

// ===== 筛选后的待办 =====
function getFilteredTodos() {
    if (currentFilter === 'active') {
        return todos.filter(t => !t.completed);
    }
    if (currentFilter === 'completed') {
        return todos.filter(t => t.completed);
    }
    return todos; // 'all'
}

// ===== 渲染列表 =====
function render() {
    const filtered = getFilteredTodos();
    todoList.innerHTML = '';

    filtered.forEach(todo => {
        const li = document.createElement('li');
        li.dataset.id = todo.id;
        if (todo.completed) {
            li.classList.add('completed');
        }

        // 文字
        const textSpan = document.createElement('span');
        textSpan.className = 'todo-text';
        textSpan.textContent = todo.text;

        // 完成按钮
        const doneBtn = document.createElement('button');
        doneBtn.className = 'btn-done';
        doneBtn.textContent = todo.completed ? '撤销' : '完成';
        doneBtn.addEventListener('click', () => toggleComplete(todo.id));

        // 删除按钮
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn-delete';
        deleteBtn.textContent = '删除';
        deleteBtn.addEventListener('click', () => deleteTodo(todo.id));

        li.appendChild(textSpan);
        li.appendChild(doneBtn);
        li.appendChild(deleteBtn);
        todoList.appendChild(li);
    });

    // 更新计数
    const activeCount = todos.filter(t => !t.completed).length;
    todoCount.textContent = activeCount + ' 个待办事项';
}

// ===== 添加待办 =====
function addTodo(text) {
    const trimmed = text.trim();
    if (!trimmed) return;

    todos.push({
        id: generateId(),
        text: trimmed,
        completed: false
    });
    saveTodos();
    render();
}

// ===== 切换完成状态 =====
function toggleComplete(id) {
    const todo = todos.find(t => t.id === id);
    if (todo) {
        todo.completed = !todo.completed;
        saveTodos();
        render();
    }
}

// ===== 删除单个 =====
function deleteTodo(id) {
    todos = todos.filter(t => t.id !== id);
    saveTodos();
    render();
}

// ===== 清除已完成 =====
function clearCompleted() {
    todos = todos.filter(t => !t.completed);
    saveTodos();
    render();
}

// ===== 清除全部 =====
function clearAll() {
    if (todos.length === 0) return;
    if (!confirm('确定要删除所有待办事项吗？此操作不可恢复。')) return;
    todos = [];
    saveTodos();
    render();
}

// ===== 筛选切换 =====
function setFilter(filter) {
    currentFilter = filter;
    // 更新按钮激活状态
    filterBtns.forEach(btn => {
        btn.classList.toggle('active', btn.dataset.filter === filter);
    });
    render();
}

// ===== 事件绑定 =====
todoForm.addEventListener('submit', (e) => {
    e.preventDefault();
    addTodo(todoInput.value);
    todoInput.value = '';
    todoInput.focus();
});

filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        setFilter(btn.dataset.filter);
    });
});

clearCompletedBtn.addEventListener('click', clearCompleted);
clearAllBtn.addEventListener('click', clearAll);

// ===== 初始化 =====
loadTodos();
render();
