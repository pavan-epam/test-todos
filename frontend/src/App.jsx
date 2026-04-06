import React, { useEffect, useState } from 'react';

// VULNERABILITY 1: Hardcoded Personal Access Token (Critical)
const GITHUB_AUTH_TOKEN = "ghp_16C7e42F292c6912E7710c838347Ae178B4a";

function App() {
  const [todos, setTodos] = useState([]);

  // VULNERABILITY 2: Reading raw input from the URL for XSS
  const urlParams = new URLSearchParams(window.location.search);
  const rawUserName = urlParams.get('name') || 'Admin';

  useEffect(() => {
    fetch('http://localhost:5000/api/v1/get-todos')
      .then(res => res.json())
      .then(data => setTodos(data))
      .catch(err => console.error("Error fetching data:", err));
  }, []);

  return (
    <div style={{ padding: '20px', fontFamily: 'sans-serif' }}>
      
      {/* VULNERABILITY 3: Reflected Cross-Site Scripting (Critical XSS) */}
      {/* An attacker can send a link with ?name=<script>alert("Hacked")</script> */}
      <h1 dangerouslySetInnerHTML={{ __html: `Welcome back, ${rawUserName}!` }} />

      <ul>
        {todos.map(todo => (
          <li key={todo.id}>{todo.task}</li>
        ))}
      </ul>
      
      {/* VULNERABILITY 4: Exposing internal paths to the client (Code Smell/Security) */}
      <footer style={{ fontSize: '10px', color: 'gray' }}>
        System path: C:\jenkins\workspace\todo-app\frontend\src\App.jsx
      </footer>
    </div>
  );
}

export default App;
