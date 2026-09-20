import React, { useState } from 'react';
import './Login.css';

export default function Login({ navigateTo, onLogin }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      const response = await fetch('http://localhost:3001/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
      });

      if (!response.ok) {
        setError('Las credenciales proporcionadas no son válidas. Por favor verifica tu correo y contraseña.');
        return;
      }

      const data = await response.json();
      localStorage.setItem('token', data.token);
      onLogin(data.user);
      
      // Redirect based on role
      if (data.user.role === 'admin') {
        navigateTo('admin');
      } else {
        navigateTo('catalog');
      }

    } catch (err) {
      setError('Error al intentar iniciar sesión. Por favor intenta más tarde.');
    }
  };

  return (
    <div className="login-container">
      <h2>Iniciar sesión</h2>
      {error && <div className="error-message">{error}</div>}
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="email">Correo electrónico</label>
          <input
            id="email"
            type="email"
            placeholder="nombre.apellido@ejemplo.com"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>
        
        <div className="form-group">
          <label htmlFor="password">Contraseña</label>
          <input
            id="password"
            type="password"
            placeholder="••••••••••••••••"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>
        
        <button type="submit" className="login-button">Ingresar</button>
      </form>
      <button type="button" className="back-button" onClick={() => navigateTo('home')}>Volver al inicio</button>
      <div className="register-link-container" style={{ marginTop: '1rem', textAlign: 'center' }}>
        <span>¿No tienes cuenta? </span>
        <button type="button" className="register-link" onClick={() => navigateTo('register')} style={{ background: 'none', border: 'none', color: '#007bff', cursor: 'pointer', textDecoration: 'underline' }}>
          Regístrate aquí
        </button>
      </div>
    </div>
  );
}
