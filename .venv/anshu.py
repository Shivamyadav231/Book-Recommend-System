from flask import Flask, render_template, request
import pickle
import numpy as np

# Load pickle files
popular_pf = pickle.load(open('popular.pkl', 'rb'))
pf = pickle.load(open('pf.pkl', 'rb'))
books = pickle.load(open('books.pkl', 'rb'))
similarity_scores = pickle.load(open(r"C:\Users\User\PycharmProjects\Book_Store\similarity_scores.pkl", "rb"))

# Initialize app
app = Flask(__name__)

@app.route('/')
def index():
    return render_template(
        'Shivam.html',
        book_name=list(popular_pf['Book-Title'].values),
        author=list(popular_pf['Book-Author'].values),
        image=list(popular_pf['Image-URL-M'].values),
        votes=list(popular_pf['num_ratings'].values),
        rating=list(popular_pf['avg_ratings'].values)
    )

@app.route('/recommend')
def recommend_ui():
    return render_template("recommend.html")

@app.route('/recommend_books', methods=['POST'])
def recommend_books():
    user_input = request.form.get('user_input')
    index = np.where(pf.index == user_input)[0][0]

    scores = list(enumerate(similarity_scores[index]))
    sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)

    data = []
    for i in sorted_scores[1:6]:
        item = []
        temp_df = books[books['Book-Title'] == pf.index[i[0]]]
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Title'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Book-Author'].values))
        item.extend(list(temp_df.drop_duplicates('Book-Title')['Image-URL-M'].values))
        data.append(item)

    return render_template("recommend.html", data=data)

if __name__ == "__main__":
    app.run(debug=True)
