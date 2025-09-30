// src/lib/auth.js

export function getToken() {
    return localStorage.getItem('token') || '';
  }
  
  export function setToken(token) {
    if (token) localStorage.setItem('token', token);
  }
  
  export function clearAuth() {
    localStorage.removeItem('token');
    localStorage.removeItem('me');
  }
  
  export function setMe(me) {
    try {
      localStorage.setItem('me', JSON.stringify(me || {}));
    } catch {}
  }
  
  export function getMe() {
    try {
      const raw = localStorage.getItem('me');
      if (!raw) return null;
      const me = JSON.parse(raw);
      // basic sanity check
      if (me && (me.id || me.email)) return me;
      return null;
    } catch {
      return null;
    }
  }
  
  // ✅ add this helper for axios requests
  export function authHeader() {
    const token = getToken();
    return token ? { Authorization: `Bearer ${token}` } : {};
  }
  
  
  