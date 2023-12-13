import requests


def get_movie_poster(movie_id):
    movie_id_tmdb = movie_id
    url = f"https://api.themoviedb.org/3/movie/{movie_id_tmdb}"
    print(movie_id_tmdb)
    headers = {
        "accept": "application/json",
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiIyOGUyMjcyM2M0MTQ2NTYzNGNlNTIwNjg1Y2RmNTNiZCIsInN1YiI6IjY1N2EyNzk1NGQyM2RkMDBlM2RlZTExYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.O_Q3Xti8OOvcbaAFR0mSvTRJaHXKaaDj7WicCmDrCUU"
    }

    response = requests.get(url, headers=headers)
    poster_path = response.json().get("poster_path")
    image_url = f'https://image.tmdb.org/t/p/w500{poster_path}'
    return image_url
