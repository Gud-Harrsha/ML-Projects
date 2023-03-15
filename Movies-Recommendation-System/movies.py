# For forwarding 2 ports or running 2 apps at the same time, read tp.py file
# in Movie-recommender-system file folder.

import streamlit as st
import pandas as pd
import pickle
import requests # This module provides a builtin JSON decoder( It is used while dealing with JSON data).

def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=69630de511f5af4753d7bf26aec10e3f&language=en-US'.format(movie_id))
    # Here requests.get() gives us a server's Json response and is assigned to variable 'response'
    # Here requests.get() return a requests.Response object()
    # for better clarity: https://www.codecademy.com/article/http-requests
    # for better clarity: https://pynative.com/parse-json-response-using-python-requests-library/
    data = response.json()
    # Here Json parsing is done on json response using the .json() function and python dictionary is obtained.
    #st.text(data) #  It is just like print function in python and it prints dictionary.
    #st.text('https://api.themoviedb.org/3/movie/{}?api_key=69630de511f5af4753d7bf26aec10e3f&language=en-US'.format(movie_id))
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies_posters.append(fetch_poster(movie_id))
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
    'Search',
        movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)



    col1, col2, col3, col4, col5 = st.columns(5, gap = "large")
# Here, col1, col2, col3, col4, col5 are the container objects.

    with col1:
        st.subheader(names[0])
        st.image(posters[0])

    with col2:
        st.subheader(names[1])
        st.image(posters[1])

    with col3:
        st.subheader(names[2])
        st.image(posters[2])

    with col4:
        st.subheader(names[3])
        st.image(posters[3])

    with col5:
        st.subheader(names[4])
        st.image(posters[4])
