import pandas as pd
import streamlit as st
import pickle
import requests

# TMDb API configuration
api_key = "01582e4a97880be66151787601d21925"
base_url = "https://api.themoviedb.org/3"

def fetch_poster(movie_id):
    # Fetch poster using the TMDb API
    url = f"{base_url}/movie/{movie_id}"
    params = {"api_key": api_key, "language": "en-US"}
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        poster_path = data.get("poster_path")
        if poster_path:
            full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
            return full_path
    return "https://via.placeholder.com/150"  # Placeholder if no poster is found

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]  # Get top 10 movies

    recommended_movie_names = []
    recommended_movie_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movie_names.append(movies.iloc[i[0]].title)
        # Fetch the poster from the API
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movie_names, recommended_movie_posters

# Load data
movies_dict = pickle.load(open('movies_dict2.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title("Recommendation System")

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    # Display in 2 rows with 5 columns each
    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.text(recommended_movie_names[idx])
            st.image(recommended_movie_posters[idx])

    cols2 = st.columns(5)
    for idx, col in enumerate(cols2):
        with col:
            st.text(recommended_movie_names[idx + 5])
            st.image(recommended_movie_posters[idx + 5])
