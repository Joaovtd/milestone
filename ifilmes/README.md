# Catálogo de Filmes (Flask + OMDb)

Aplicação simples em **Python + Flask** que lista filmes, mostra detalhes, permite **buscar** por título e **filtrar por gênero** (opcional).  
Os dados são carregados automaticamente da **API pública OMDb**.

> Obs.: A navegação principal acontece no navegador (páginas Flask).  
> Se você quiser, depois posso complementar com um menu numérico no terminal chamando essas rotas.

---

## 1. Pré‑requisitos

- Python 3.10+ instalado
- Pip funcionando no terminal
- Uma chave de API gratuita da OMDb:
  - Crie uma conta em: <http://www.omdbapi.com/apikey.aspx>
  - Você receberá uma chave do tipo `abc123`.

---

## 2. Instalar dependências

No diretório do projeto, execute:

```bash
php install -r requirements.txt
```

---

## 3. Configurar a chave da API (OMDB_API_KEY)

Você pode configurar de duas formas:

### 3.1. Via variável de ambiente (recomendado)

No Windows PowerShell:

```powershell
$env:OMDB_API_KEY="SUA_CHAVE_AQUI"
python app.py
```

Em CMD:

```cmd
set OMDB_API_KEY=SUA_CHAVE_AQUI
python app.py
```

### 3.2. Via arquivo `.env`

Crie um arquivo chamado `.env` na raiz do projeto com o conteúdo:

```text
OMDB_API_KEY=SUA_CHAVE_AQUI
```

A biblioteca `python-dotenv` irá carregar isso automaticamente.

---

## 4. Executar o projeto

No terminal, dentro da pasta do projeto:

```bash
python app.py
```

O Flask iniciará em `http://127.0.0.1:5000/`  
Abra esse endereço no navegador.

---

## 5. Funcionalidades

- **Página inicial (`/`)**
  - Lista de filmes populares com:
    - Título
    - Poster
    - Ano
    - Nota IMDb (quando disponível)
  - Layout organizado em cards, responsivo (CSS puro).

- **Sistema de busca**
  - Campo de pesquisa na barra superior.
  - Busca por título usando a OMDb (`?q=...`).

- **Filtro opcional por gênero**
  - Combo de seleção “Filtrar por gênero”.
  - Lista de gêneros calculada dinamicamente a partir dos filmes exibidos.

- **Página de detalhes (`/movie/<imdb_id>`)**
  - Poster em destaque.
  - Título, ano, duração, gêneros.
  - **Sinopse (Plot)**.
  - **Nota de avaliação (imdbRating)**.
  - Diretor, elenco, idioma, país.
  - **Botão “Voltar para a lista”**.

---

## 6. Estrutura de arquivos

- `app.py` — aplicação Flask e integração com a OMDb.
- `requirements.txt` — dependências do projeto.
- `templates/base.html` — layout base (header, footer, busca).
- `templates/index.html` — listagem de filmes + filtro por gênero.
- `templates/detail.html` — página de detalhes do filme.
- `static/style.css` — estilos e layout responsivo.

---

## 7. Próximos passos (opcional)

Se você quiser seguir exatamente o requisito de **“navegação por números no terminal”**, posso adicionar:

- Um script `menu_terminal.py` com um menu assim:
  - `1` – Listar filmes
  - `2` – Buscar filme
  - `3` – Ver detalhes (informando o índice)
  - `0` – Sair
- Esse script chamaria as mesmas funções de busca/detalhes usadas pelo Flask, mas mostrando tudo no terminal.


