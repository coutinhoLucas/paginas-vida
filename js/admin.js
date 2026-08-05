(() => {
  const loginPanel = document.querySelector("#login-panel");
  const controlPanel = document.querySelector("#control-panel");
  const loginFeedback = document.querySelector("#login-feedback");
  const controlFeedback = document.querySelector("#control-feedback");
  const dialog = document.querySelector("#confirmation");
  const labels = { experiencia: "EXPERIÊNCIA", revelacao: "REVELAÇÃO", conclusao: "CONCLUSÃO" };
  let state = { modo: "experiencia", modo_anterior: null, offline: true };
  let pendingMode = null;

  function render() {
    document.querySelector("#current-mode").textContent = labels[state.modo];
    document.querySelector("#updated-at").textContent = state.atualizado_em
      ? new Intl.DateTimeFormat("pt-BR", { dateStyle: "short", timeStyle: "short" }).format(new Date(state.atualizado_em)) : "—";
    document.querySelector("#offline-warning").hidden = !state.offline;
    document.querySelector("#rollback").disabled = !state.modo_anterior || state.offline;
    document.querySelectorAll("[data-mode]").forEach((button) => {
      button.classList.toggle("active", button.dataset.mode === state.modo);
      button.disabled = state.offline || button.dataset.mode === state.modo;
    });
  }

  async function refresh() { state = await window.CONTROLE.getMode(); render(); }

  document.querySelector("#login-form").addEventListener("submit", async (event) => {
    event.preventDefault(); loginFeedback.textContent = "Verificando acesso...";
    try {
      await window.CONTROLE.signIn(document.querySelector("#email").value, document.querySelector("#password").value);
      loginPanel.hidden = true; controlPanel.hidden = false; await refresh(); loginFeedback.textContent = "";
    } catch (error) { loginFeedback.textContent = error.message; }
  });

  function confirmMode(mode, prefix = "ATIVAR MODO") {
    pendingMode = mode; document.querySelector("#confirmation-title").textContent = `${prefix} ${labels[mode]}?`; dialog.showModal();
  }
  document.querySelectorAll("[data-mode]").forEach((button) => button.addEventListener("click", () => confirmMode(button.dataset.mode)));
  document.querySelector("#rollback").addEventListener("click", () => confirmMode(state.modo_anterior, "VOLTAR PARA"));

  dialog.addEventListener("close", async () => {
    if (dialog.returnValue !== "confirm" || !pendingMode) return;
    controlFeedback.textContent = "Alterando o modo...";
    try {
      state = { ...(await window.CONTROLE.setMode(pendingMode, state.modo)), offline: false }; render();
      controlFeedback.textContent = `Modo ${labels[state.modo]} ativado com sucesso.`;
    } catch (error) { controlFeedback.textContent = error.message; }
    pendingMode = null;
  });

  document.querySelector("#logout").addEventListener("click", () => { window.CONTROLE.signOut(); location.reload(); });
})();
