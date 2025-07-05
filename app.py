import streamlit as st
import pickle
import pandas as pd
import requests

# Load movie data and similarity matrix
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB API key
API_KEY = "b76d821cbe9b6f7658da4cdc03826145"

# Function to fetch poster
import requests

API_KEY = 'b76d821cbe9b6f7658da4cdc03826145'

def fetch_poster_by_title(title):
    try:
        url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={title}"
        response = requests.get(url, timeout=5)
        data = response.json()
        results = data.get('results')

        if results:
            poster_path = results[0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"
    except Exception as e:
        print(f"❌ Error: {e}")

    return "https://via.placeholder.com/200x300?text=No+Poster"



# Recommend function
def recommend(movie_title):
    try:
        index = movies[movies['title'].str.lower() == movie_title.lower()].index[0]
    except IndexError:
        return [], []

    distances = similarity[index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        poster_url = fetch_poster_by_title(title)

        recommended_movies.append(title)
        recommended_posters.append(poster_url)

    return recommended_movies, recommended_posters

# Streamlit UI
st.title('🎬 Movie Recommender System')
selected_movie = st.selectbox("Search for a movie to get recommendations:", movies['title'].values)

if st.button('Show Recommendations'):
    names, posters = recommend(selected_movie)

    if names:
        cols = st.columns(5)
        for i in range(len(names)):
            with cols[i]:
                st.text(names[i])
                if posters[i]:
                    st.image(posters[i])
                else:
                    st.write("🚫 Poster not found")
    else:
        st.warning("Movie not found or recommendation failed.")
