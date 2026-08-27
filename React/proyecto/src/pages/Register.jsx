import React, { useState } from 'react';
import './Login.css'; // We can reuse the login css or create a new one

export default function Register({ navigateTo }) {
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');

    if (password !== confirmPassword) {
      setError('Las contraseñas no coinciden.');
      return;
    }

    try {
      const response = await fetch('http://localhost:3001/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password, role_id: 1 }) // role_id 1 for normal user
      });

      if (!response.ok) {
        setError('Error al crear la cuenta. Por favor verifica los datos.');
        return;
      }

      setSuccess('Cuenta creada exitosamente. Ahora puedes iniciar sesión.');
      setTimeout(() => navigateTo('login'), 2000);

    } catch (err) {
      setError('Error al intentar registrar. Por favor intenta más tarde.');
    }
  };

  return (
    <div className="login-container">
      <h2>Registrarse</h2>
      {error && <div className="error-message">{error}</div>}
      {success && <div className="success-message" style={{ color: 'green', marginBottom: '1rem' }}>{success}</div>}
      <form onSubmit={handleSubmit} className="login-form">
        <div className="form-group">
          <label htmlFor="username">Nombre de usuario</label>
          <input
            id="username"
            type="text"
            placeholder="Tu usuario"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </div>

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
        
        <div className="form-group">
          <label htmlFor="confirmPassword">Confirmar contraseña</label>
          <input
            id="confirmPassword"
            type="password"
            placeholder="••••••••••••••••"
            value={confirmPassword}
            onChange={e => setConfirmPassword(e.target.value)}
            required
          />
        </div>
        
        <button type="submit" className="login-button">Crear cuenta</button>
      </form>
      <button type="button" className="back-button" onClick={() => navigateTo('login')}>Volver a Iniciar sesión</button>
    </div>
  );
}
