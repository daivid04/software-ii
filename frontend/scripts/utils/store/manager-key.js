import { SUPABASE } from "./data-store.js";

/**
 * Autentica un usuario usando el endpoint del backend.
 * @param {string} email - Email del usuario
 * @param {string} password - Contraseña del usuario
 * @returns {Object|null} Datos de autenticación o null si falla
 */
export async function obtainToken(email, password) {
  const API_BASE_URL = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://localhost:8000/api/v1'  // Desarrollo local
  : '/api/v1';
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password })
    });

    const data = await response.json();

    // El backend siempre responde 200, verificamos el campo success
    if (!data.success) {
      return null;
    }
    // Formateamos la respuesta para que sea compatible con el código existente
    return {
      session: {
        access_token: data.access_token
      },
      user: {
        email: data.user_email
      }
    };
  } catch (error) {
    return null;
  }
}

export async function closeSesion() {
  localStorage.removeItem('supabase_token');
  window.location.replace('login.html');
}