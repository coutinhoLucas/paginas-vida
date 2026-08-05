(() => {
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

  document.querySelector("#chapter").textContent = `CAPÍTULO ${chapterNumber}`;
  document.querySelector("#title").textContent = story.titulo;
  document.querySelector("#closing").textContent = story.fraseFinal;
  document.querySelector("#page-number").textContent = chapterNumber;
  document.querySelector("#text").replaceChildren(
    ...story.paragrafos.map((paragraph) => {
      const element = document.createElement("p");
      paragraph.split("\n").forEach((line, index) => {
        if (index) element.append(document.createElement("br"));
        element.append(line);
      });
      return element;
    })
  );

  document.title = `Capítulo ${chapterNumber} — ${story.titulo}`;
  storyElement.hidden = false;
})();
