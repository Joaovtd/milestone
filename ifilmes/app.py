import os
from flask import Flask, render_template, request, abort
import requests
from dotenv import load_dotenv


load_dotenv()

app = Flask(__name__)

OMDB_API_KEY = os.getenv("OMDB_API_KEY")

# Lista base de filmes para exibir na página inicial (títulos populares)
BASE_MOVIES = [
    "The Matrix",
    "Inception",
    "Interstellar",
    "The Dark Knight",
    "Pulp Fiction",
    "Fight Club",
    "Forrest Gump",
    "The Lord of the Rings: The Fellowship of the Ring",
    "The Lord of the Rings: The Two Towers",
    "The Lord of the Rings: The Return of the King",
]


def fetch_movie_by_title(title: str):
    """Busca um filme na API OMDb pelo título."""
    if not OMDB_API_KEY:
        return None

    params = {"apikey": OMDB_API_KEY, "t": title}
    resp = requests.get("https://www.omdbapi.com/", params=params, timeout=10)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if data.get("Response") != "True":
        return None
    return data


def fetch_movie_by_imdb_id(imdb_id: str):
    """Busca um filme específico pelo imdbID."""
    if not OMDB_API_KEY:
        return None

    params = {"apikey": OMDB_API_KEY, "i": imdb_id}
    resp = requests.get("https://www.omdbapi.com/", params=params, timeout=10)
    if resp.status_code != 200:
        return None
    data = resp.json()
    if data.get("Response") != "True":
        return None
    return data


def search_movies(query: str):
    """Busca uma lista de filmes pelo termo informado."""
    if not OMDB_API_KEY:
        return []

    params = {"apikey": OMDB_API_KEY, "s": query}
    resp = requests.get("https://www.omdbapi.com/", params=params, timeout=10)
    if resp.status_code != 200:
        return []
    data = resp.json()
    if data.get("Response") != "True":
        return []
    return data.get("Search", [])


def get_home_movies():
    """
    Monta a lista de filmes da página inicial usando os títulos em BASE_MOVIES.
    Cada item terá título, ano, poster e imdbID.
    """
    movies = []
    for title in BASE_MOVIES:
        movie = fetch_movie_by_title(title)
        if not movie:
            continue
        movies.append(
            {
                "Title": movie.get("Title"),
                "Year": movie.get("Year"),
                "Poster": movie.get("Poster"),
                "imdbID": movie.get("imdbID"),
                "Genre": movie.get("Genre"),
                "imdbRating": movie.get("imdbRating"),
            }
        )
    return movies


def extract_genres(movies):
    """Extrai conjunto de gêneros a partir da lista de filmes."""
    genres = set()
    for m in movies:
        genre_str = m.get("Genre") or ""
        for g in genre_str.split(","):
            g = g.strip()
            if g:
                genres.add(g)
    return sorted(genres)


@app.route("/")
def index():
    query = request.args.get("q", "").strip()
    selected_genre = request.args.get("genre", "").strip()

    if query:
        raw_results = search_movies(query)
        movies = []
        # A busca simples da OMDb não traz os gêneros,
        # então buscamos os detalhes de cada resultado.
        for item in raw_results:
            details = fetch_movie_by_imdb_id(item.get("imdbID"))
            if not details:
                continue

            movies.append(
                {
                    "Title": details.get("Title"),
                    "Year": details.get("Year"),
                    "Poster": details.get("Poster"),
                    "imdbID": details.get("imdbID"),
                    "Genre": details.get("Genre"),
                    "imdbRating": details.get("imdbRating"),
                }
            )
    else:
        movies = get_home_movies()

    # Gêneros disponíveis para filtro (com base nos filmes carregados)
    genres = extract_genres(movies)

    # Aplicar filtro por gênero, se houver
    if selected_genre:
        filtered = []
        for m in movies:
            genre_str = m.get("Genre") or ""
            movie_genres = [g.strip() for g in genre_str.split(",") if g.strip()]
            if selected_genre in movie_genres:
                filtered.append(m)
        movies = filtered

    return render_template(
        "index.html",
        movies=movies,
        genres=genres,
        selected_genre=selected_genre,
        query=query,
        has_api_key=bool(OMDB_API_KEY),
    )


@app.route("/movie/<imdb_id>")
def movie_detail(imdb_id):
    movie = fetch_movie_by_imdb_id(imdb_id)
    if not movie:
        abort(404)
    return render_template("detail.html", movie=movie)


if __name__ == "__main__":
    # Permite rodar com `python app.py`
    app.run(debug=True)


