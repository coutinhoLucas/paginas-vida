# Páginas da Vida — protótipo

Experiência interativa para o tema **“Protagonista ou coadjuvante?”**. O protótipo contém somente os capítulos 27, 104 e 219.

## Abrir e testar

Inicie um servidor local na pasta do projeto e abra `/?capitulo=27`, `/?capitulo=104` ou `/?capitulo=219`. Use `/?capitulo=999` para validar o tratamento de capítulo inexistente. Evite abrir o HTML diretamente; um servidor local reproduz melhor a publicação.

## Alterar ou adicionar histórias

Edite `js/historias.js`. Cada história usa o número do capítulo como chave e possui `titulo`, `paragrafos` e `fraseFinal`. A lógica e o visual não precisam ser alterados.

## Gerar QR Codes

Após saber o endereço publicado, execute:

```text
python scripts/gerar_qr.py https://USUARIO.github.io/paginas-vida/
```

Os arquivos serão gravados em `assets/qr/`. Gere novamente sempre que o endereço público mudar.

## Cartões de teste

Abra `cartoes-teste.html` e imprima em A4, escala de 100%, com gráficos de fundo ativados. A folha contém cinco cartões em tamanho 85 × 55 mm. Não use “ajustar à página”.

## Publicação no GitHub Pages

O site não exige compilação. Publique a raiz do branch `main` em **Settings → Pages → Deploy from a branch → main / root**.

## Checklist — Android e iPhone

- Escanear cada um dos três QR Codes com a câmera nativa.
- Confirmar capítulo, título, texto e frase final corretos.
- Testar um capítulo inexistente e conferir a mensagem de orientação.
- Testar com Wi-Fi da igreja e com dados móveis.
- Verificar contraste e leitura com brilho de tela baixo e alto.
- Confirmar que não há rolagem horizontal, zoom obrigatório ou texto cortado.
- Cronometrar a leitura de cada história com pelo menos três pessoas.
- Testar novamente os QR Codes impressos, não apenas na tela.
- Medir a leitura a 30, 50 e 80 cm, em luz clara e ambiente escuro.

## Antes de produzir 100 cartões

1. Imprima somente a folha com cinco cartões, em escala de 100%.
2. Recorte preservando a área branca ao redor dos QR Codes.
3. Peça a cinco pessoas para escanear, sem explicar como posicionar o celular.
4. Use pelo menos dois Androids e dois iPhones, incluindo um aparelho mais antigo.
5. Anote tempo até a página abrir, erros de leitura e tempo de leitura do texto.
6. Aprove papel, contraste, tamanho, acabamento e endereço publicado antes do lote definitivo.

## Estrutura

```text
assets/qr/          QR Codes gerados
css/styles.css      visual do site
css/cartoes.css     visual para impressão
js/historias.js     conteúdo dos capítulos
js/app.js           leitura da URL e exibição
scripts/gerar_qr.py gerador dos QR Codes
index.html          experiência principal
cartoes-teste.html  folha com cinco cartões
```
