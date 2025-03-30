import pandas as pd
import streamlit as st
import pickle
import requests

movies_dict = pickle.load(open('data/movie_dict.pkl', 'rb'))
similarity = pickle.load(open('data/similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)


# recommends 5 movies
def reccomend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    reccomended_movies = []
    reccomended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].id #id to fetch poster from TMDB API

        reccomended_movies.append(movies.iloc[i[0]].title)
        reccomended_movies_posters.append(fetch_poster(movie_id))
    return reccomended_movies, reccomended_movies_posters


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=247b5642bede29632cafa6acc4a56e1e&language=en-US'.format(movie_id))
    data = response.json()
    # st.text(data)
    full_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
    return full_path


st.title('Movie Reccomendation System')

selected_movie = st.selectbox(
    'Enter Movie Name',
    movies['title'].values
)

if st.button('Reccomend'):
    names, posters = reccomend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])
    with col2:
        st.text(names[1])
        st.image(posters[1])
    with col3:
        st.text(names[2])
        st.image(posters[2])
    with col4:
        st.text(names[3])
        st.image(posters[3])
    with col5:
        st.text(names[4])
        st.image(posters[4])