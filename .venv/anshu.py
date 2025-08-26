import streamlit as st
import pickle
import numpy as np
import pandas as pd

# Load pickle files
popular_pf = pickle.load(open('popular.pkl', 'rb'))
pf = pickle.load(open('pf.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open('similarity_scores.pkl', 'rb'))   # NOTE: relative path

# Streamlit UI
st.title("📚 Book Recommendation System")

# Show Popular Books
st.header("🔥 Popular Books")
for i in range(len(popular_pf)):
    with st.container():
        col1, col2 = st.columns([1,3])
        with col1:
            st.image(popular_pf['Image-URL-M'].values[i], width=100)
        with col2:
            st.write(f"**{popular_pf['Book-Title'].values[i]}**")
            st.write(f"✍️ {popular_pf['Book-Author'].values[i]}")
            st.write(f"⭐ {popular_pf['avg_ratings'].values[i]} ({popular_pf['num_ratings'].values[i]} votes)")

# Recommendation Section
st.header("🔎 Find Similar Books")
user_input = st.text_input("Enter a book name:")

if st.button("Recommend"):
    if user_input in pf.index:
        index = np.where(pf.index == user_input)[0][0]
        scores = list(enumerate(similarity_scores[index]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

        st.subheader("📖 Recommended Books:")
        for i in sorted_scores[1:6]:
            temp_df = books[books['Book-Title'] == pf.index[i[0]]]
            book_title = temp_df.drop_duplicates('Book-Title')['Book-Title'].values[0]
            author = temp_df.drop_duplicates('Book-Title')['Book-Author'].values[0]
            image = temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values[0]

            with st.container():
                col1, col2 = st.columns([1,3])
                with col1:
                    st.image(image, width=100)
                with col2:
                    st.write(f"**{book_title}**")
                    st.write(f"✍️ {author}")
    else:
        st.error("Book not found in database. Try another one.")

