(async () => {
  const params = new URLSearchParams(window.location.search);
  const chapterNumber = params.get("capitulo");
  const story = window.HISTORIAS[chapterNumber];
  const storyElement = document.querySelector("#story");
  const errorElement = document.querySelector("#error");

  if (!story) {
    errorElement.hidden = false;
    document.title = "Capítulo não encontrado — Páginas da Vida";
    return;
  }

  const state = await window.CONTROLE.getMode();
  const mode = story.momentos[state.modo] ? state.modo : "experiencia";
  const moment = story.momentos[mode];
  const pageNumbers = { experiencia: 1, revelacao: 2, conclusao: 3 };

  document.querySelector("#chapter").textContent = `CAPÍTULO ${chapterNumber}`;
  document.querySelector("#title").textContent = story.titulo;
  document.querySelector("#closing").textContent = moment.fraseFinal;
  document.querySelector("#page-number").textContent = `PÁGINA ${pageNumbers[mode]} DE ?`;

  const paragraphElements = moment.paragrafos.map((paragraph) => {
    const element = document.createElement("p");
    paragraph.split("\n").forEach((line, index) => {
      if (index) element.append(document.createElement("br"));
      element.append(line);
    });
    return element;
  });
  document.querySelector("#text").replaceChildren(...paragraphElements);

  const scripture = document.querySelector("#scripture");
  if (moment.citacao) {
    scripture.querySelector("blockquote").textContent = moment.citacao;
    scripture.querySelector("cite").textContent = moment.referencia;
    scripture.hidden = false;
  }

  if (mode === "conclusao") document.querySelector("#epilogue").hidden = false;
  document.title = `Capítulo ${chapterNumber} — ${story.titulo}`;
  storyElement.hidden = false;
})();
