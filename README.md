# Páginas da Vida — protótipo

Experiência interativa em três atos para o tema **“Protagonista ou coadjuvante?”**. A coleção contém trinta capítulos aprovados.

O mesmo QR Code revela progressivamente a experiência, a revelação e a conclusão de cada capítulo. O modo atual é compartilhado entre todos os celulares por um único registro protegido no Supabase.

## Abrir e testar

Inicie um servidor local na pasta do projeto e use `/?capitulo=NUMERO`. Capítulos disponíveis: 27, 34, 43, 56, 62, 68, 75, 82, 91, 104, 113, 121, 132, 138, 147, 154, 159, 171, 176, 188, 201, 219, 228, 238, 245, 263, 276, 289, 297 e 314. Use `/?capitulo=999` para validar o tratamento de capítulo inexistente.

## Alterar ou adicionar histórias

Edite `js/historias.js`. Cada capítulo usa seu número como chave e contém os momentos `experiencia`, `revelacao` e `conclusao`. A lógica e o visual não precisam ser alterados.

## Painel de controle

Abra `/admin.html`, faça login e confira o modo atual. Cada mudança exige confirmação. Antes de anunciar a troca no palco, use “Abrir página de teste” e confirme o novo texto.

Se a consulta online falhar, o participante continua vendo o último modo carregado no aparelho. O painel exibe um alerta e bloqueia alterações até recuperar a conexão.

O arquivo `supabase.sql` documenta a tabela e as políticas de segurança. `js/config.js` contém somente a URL e a chave publicável; chaves secretas nunca devem ser colocadas no site.

## Gerar QR Codes

Após saber o endereço publicado, execute:

```text
python scripts/gerar_qr.py https://USUARIO.github.io/paginas-vida/
```

Os arquivos serão gravados em `assets/qr/`. Gere novamente sempre que o endereço público mudar.

## Cartões de demonstração

Abra `cartoes-teste.html` e imprima em A4, escala de 100%, com gráficos de fundo ativados. A folha contém os trinta capítulos aprovados em cartões de 85 × 55 mm. Não use “ajustar à página”.

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
css/admin.css       visual do painel de controle
js/historias.js     conteúdo dos capítulos
js/controle.js      consulta e alteração do modo compartilhado
js/config.js        conexão pública protegida por políticas
js/app.js           leitura da URL e exibição do ato atual
js/admin.js         operação do painel administrativo
scripts/gerar_qr.py gerador dos QR Codes
index.html          experiência principal
admin.html          painel protegido da equipe
cartoes-teste.html  folha com cinco cartões
supabase.sql        estrutura do controle compartilhado
```
