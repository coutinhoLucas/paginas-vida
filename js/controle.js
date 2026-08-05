window.CONTROLE = (() => {
  const config = window.CONTROLE_CONFIG || {};
  const validModes = ["experiencia", "revelacao", "conclusao"];
  const fallback = { modo: localStorage.getItem("paginas-vida-modo") || "experiencia", offline: true };

  const headers = (token = null, hasBody = false) => {
    const result = { apikey: config.publishableKey };
    if (token) result.Authorization = `Bearer ${token}`;
    if (hasBody) result["Content-Type"] = "application/json";
    return result;
  };

  const ready = () => Boolean(config.supabaseUrl && config.publishableKey);

  async function getMode() {
    if (!ready()) return fallback;
    try {
      const response = await fetch(
        `${config.supabaseUrl}/storage/v1/object/public/controle/controle-inicial.json?_=${Date.now()}`,
        { cache: "no-store" }
      );
      if (!response.ok) throw new Error("Não foi possível consultar o modo.");
      const state = await response.json();
      if (!state || !validModes.includes(state.modo)) throw new Error("Modo inválido.");
      localStorage.setItem("paginas-vida-modo", state.modo);
      return { ...state, offline: false };
    } catch {
      return fallback;
    }
  }

  async function signIn(email, password) {
    if (!ready()) throw new Error("O controle compartilhado ainda não foi configurado.");
    const response = await fetch(`${config.supabaseUrl}/auth/v1/token?grant_type=password`, {
      method: "POST",
      headers: headers(null, true),
      body: JSON.stringify({ email, password })
    });
    const data = await response.json();
    if (!response.ok) throw new Error("E-mail ou senha inválidos.");
    sessionStorage.setItem("paginas-vida-token", data.access_token);
    return data.access_token;
  }

  function signOut() {
    sessionStorage.removeItem("paginas-vida-token");
  }

  async function setMode(newMode, currentMode) {
    if (!validModes.includes(newMode)) throw new Error("Modo inválido.");
    const token = sessionStorage.getItem("paginas-vida-token");
    if (!token) throw new Error("Faça login novamente.");
    const state = {
      modo: newMode,
      modo_anterior: currentMode,
      atualizado_em: new Date().toISOString()
    };
    const response = await fetch(`${config.supabaseUrl}/storage/v1/object/controle/controle-inicial.json`, {
      method: "PUT",
      headers: { ...headers(token, true), "x-upsert": "true" },
      body: JSON.stringify(state)
    });
    if (!response.ok) throw new Error("A alteração não foi autorizada.");
    return state;
  }

  return { getMode, signIn, signOut, setMode, validModes };
})();
