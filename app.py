import streamlit as st
import numpy as np
import sqlite3
import zipfile

DATABASE = "./database.db"

# ------------------- Load similarity.npy from zip -------------------
zip_path = "./similarity.zip"
file_to_extract = "similarity.npy"
output_dir = "./"

try:
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extract(file_to_extract, output_dir)
except KeyError:
    print(f"{file_to_extract} not found in {zip_path}")
except zipfile.BadZipFile:
    print("Error: The file is not a valid zip archive.")

similarity = np.load("./similarity.npy")

# ------------------- Database connection -------------------
def get_connection():
    db = sqlite3.connect(DATABASE, check_same_thread=False)
    return db

conn = get_connection()
cursor = conn.cursor()

# ------------------- Streamlit UI -------------------
st.title("Book Recommender System :book:")

form = st.form("my_form")
fav_book = form.text_input("Enter Favourite Book (Optional)")
fav_author = form.text_input("Enter Favourite Author (Optional)")
fav_genre = form.text_input("Enter Favourite Genre (Optional)")

submit_btn = form.form_submit_button(
    'Get Recommendations',
    use_container_width=True,
)

# ------------------- Recommendation Functions -------------------

# 1️⃣ Book-based (partial & case-insensitive match)
def get_similar_books(name: str, cur: sqlite3.Cursor, similarity_data: np.ndarray):
    # Use LIKE for partial matching and case-insensitive search
    query = "SELECT id, title FROM books WHERE title LIKE ? COLLATE NOCASE"
    cur.execute(query, ('%' + name + '%',))
    rows = cur.fetchall()
    if not rows:
        st.warning(f"No book found for '{name}'. Please check the spelling.")
        return []

    # Take the first match
    book_index = rows[0][0]
    distances = similarity_data[book_index]
    books_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:9]
    book_ids = [item[0] for item in books_list]

    query = "SELECT title, thumbnail FROM books WHERE id IN ({})".format(",".join("?" for _ in book_ids))
    cur.execute(query, book_ids)
    return cur.fetchall()

# 2️⃣ Author-based
def get_author_recommendations(author_name: str, cur: sqlite3.Cursor):
    if not author_name:
        return []
    query = "SELECT title, thumbnail FROM books WHERE authors LIKE ? COLLATE NOCASE LIMIT 8"
    cur.execute(query, ('%' + author_name + '%',))
    return cur.fetchall()

# 3️⃣ Genre-based
def get_genre_recommendations(genre: str, cur: sqlite3.Cursor):
    if not genre:
        return []
    query = "SELECT title, thumbnail FROM books WHERE categories LIKE ? COLLATE NOCASE LIMIT 8"
    cur.execute(query, ('%' + genre + '%',))
    return cur.fetchall()

# ------------------- Display Function -------------------
def display_books(book_list, header, displayed_titles=set()):
    if not book_list:
        return displayed_titles

    filtered_list = [b for b in book_list if b[0] not in displayed_titles]
    if not filtered_list:
        return displayed_titles

    st.subheader(header)

    titles = [x[0] for x in filtered_list]
    image_urls = [x[1] for x in filtered_list]

    row1 = st.columns(4)
    row2 = st.columns(4)

    for col, title, image_url in zip(row1 + row2, titles, image_urls):
        tile = col.container(height=300)
        tile.text(title)
        tile.image(image_url)
        displayed_titles.add(title)

    return displayed_titles

# ------------------- Main Logic -------------------
if submit_btn:
    shown_titles = set()

    if not (fav_book or fav_author or fav_genre):
        st.warning("Please enter at least one of Book, Author, or Genre to get recommendations.")
    else:
        # Book-based
        if fav_book:
            book_recs = get_similar_books(fav_book, cursor, similarity)
            shown_titles = display_books(book_recs, "📘 Book-Based Recommendations", shown_titles)

        # Author-based
        if fav_author:
            author_recs = get_author_recommendations(fav_author, cursor)
            shown_titles = display_books(author_recs, f"✍🏼 Books by {fav_author}", shown_titles)

        # Genre-based
        if fav_genre:
            genre_recs = get_genre_recommendations(fav_genre, cursor)
            display_books(genre_recs, f"🎭 Genre: {fav_genre}", shown_titles)

# ------------------- Close DB connection -------------------
conn.close()
