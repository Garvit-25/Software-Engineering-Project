import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
import matplotlib.pyplot as plt

class RecommenderNet(keras.Model):
    def __init__(self, num_users, num_movies, embedding_size=50, **kwargs):
        super(RecommenderNet, self).__init__(**kwargs)
        self.num_users = num_users
        self.num_movies = num_movies
        self.embedding_size = embedding_size
        self.user_embedding = layers.Embedding(
            num_users,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.user_bias = layers.Embedding(num_users, 1)
        self.movie_embedding = layers.Embedding(
            num_movies,
            embedding_size,
            embeddings_initializer="he_normal",
            embeddings_regularizer=keras.regularizers.l2(1e-6),
        )
        self.movie_bias = layers.Embedding(num_movies, 1)

    def call(self, inputs):
        user_vector = self.user_embedding(inputs[:, 0])
        user_bias = self.user_bias(inputs[:, 0])
        movie_vector = self.movie_embedding(inputs[:, 1])
        movie_bias = self.movie_bias(inputs[:, 1])
        dot_user_movie = tf.tensordot(user_vector, movie_vector, 2)
        x = dot_user_movie + user_bias + movie_bias
        return tf.nn.sigmoid(x)

class Output:

    def result(self) :
        df = pd.read_csv("E://SoftwareEngineering//ReviewRating//static//ratings.csv")
        user_ids = df["userId"].unique().tolist()
        user2user_encoded = {x: i for i, x in enumerate(user_ids)}
        userencoded2user = {i: x for i, x in enumerate(user_ids)}
        movie_ids = df["movieId"].unique().tolist()
        movie2movie_encoded = {x: i for i, x in enumerate(movie_ids)}
        movie_encoded2movie = {i: x for i, x in enumerate(movie_ids)}
        df["user"] = df["userId"].map(user2user_encoded)
        df["movie"] = df["movieId"].map(movie2movie_encoded)

        num_users = len(user2user_encoded)
        num_movies = len(movie_encoded2movie)
        df["rating"] = df["rating"].values.astype(np.float32)
   
        model = RecommenderNet(num_users, num_movies, 50)
        model.compile(loss=tf.keras.losses.BinaryCrossentropy(), optimizer=keras.optimizers.Adam(lr=0.001))
        model.load_weights('E://SoftwareEngineering//ReviewRating//savedModel')

        movie_df = pd.read_csv("E://SoftwareEngineering//ReviewRating//static//movies.csv")

        user_id = df.userId.sample(1).iloc[0]
        movies_watched_by_user = df[df.userId == user_id]
        movies_not_watched = movie_df[~movie_df["movieId"].isin(movies_watched_by_user.movieId.values)]["movieId"]
        movies_not_watched = list(set(movies_not_watched).intersection(set(movie2movie_encoded.keys())))
        movies_not_watched = [[movie2movie_encoded.get(x)] for x in movies_not_watched]
        user_encoder = user2user_encoded.get(user_id)
        user_movie_array = np.hstack(([[user_encoder]] * len(movies_not_watched), movies_not_watched))
        ratings = model.predict(user_movie_array).flatten()

        top_ratings_indices = ratings.argsort()[-10:][::-1]
        recommended_movie_ids = [
            movie_encoded2movie.get(movies_not_watched[x][0]) for x in top_ratings_indices
            ]
        top_movies_user = (
            movies_watched_by_user.sort_values(by="rating", ascending=False)
            .head(5)
            .movieId.values
            )
        movie_df_rows = movie_df[movie_df["movieId"].isin(top_movies_user)]
        
        recommended_movies = movie_df[movie_df["movieId"].isin(recommended_movie_ids)]

        return recommended_movies,movie_df_rows,user_id