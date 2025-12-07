

# 📚 Book Recommender Web App

[![Streamlit](https://img.shields.io/badge/Streamlit-App-green)](https://share.streamlit.io/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue)]()
[![AWS](https://img.shields.io/badge/AWS-Cloud-orange)]()
[![License](https://img.shields.io/badge/License-MIT-yellow)]()

A **content-based book recommender system** built using **Streamlit** and **AWS services**, allowing users to get personalized book recommendations based on **book title, author, or genre**.

---

## 🌟 Live Demo

Check out the live app on **Streamlit Community Cloud**:
🔗 [Open Book Recommender App](https://share.streamlit.io/sreeja126/book-recommender-system/main/app.py)

---

## 📷 Snapshot

![book-recommender-snapshot](image.png)

---

## 🛠 Approach

The app uses **content-based filtering** to recommend books by comparing:

* Book title
* Author
* Genre / Category

Key differences from traditional setups:

* **Book metadata** is fetched in real-time from the **Google Books API**.
* **AWS DynamoDB** stores user preferences and precomputed recommendations.
* **AWS Lambda** handles recommendation logic and API queries.
* **AWS Comprehend** processes textual features (like descriptions and categories) for similarity computation.

Users can get recommendations based on **any combination** of book, author, or genre.

---

## ⚡ Features

* Book, author, and genre-based recommendations
* Real-time data fetch from **Google Books API**
* Scalable using AWS backend services
* Displays book thumbnails in a clean grid
* Avoids duplicate recommendations when multiple filters match

---

## 💻 Installation & Local Testing

1. **Clone the repository**

```bash
git clone https://github.com/sreeja126/book-recommender-system.git
cd book-recommender-system
```

2. **Install dependencies**

```bash
pip install -r requirements.txt
```

3. **Run locally**

```bash
streamlit run app.py
```

Open your browser at [http://localhost:8501/](http://localhost:8501/)

> Note: Local testing requires valid **Google Books API key** and access to AWS credentials to query DynamoDB and invoke Lambda functions.

---

## 🚀 Deployment

Deploy the app on **Streamlit Community Cloud**:

1. Push your project to GitHub (including `app.py` and `requirements.txt`).
2. Go to [Streamlit Cloud](https://share.streamlit.io/) → New app → Connect GitHub repository → Select branch → Set main file (`app.py`) → Deploy.
3. The app fetches live data from **Google Books API** and queries AWS services, so ensure your credentials are correctly configured.
4. To update, push changes to GitHub → Streamlit automatically redeploys.

---

## 📝 Usage

1. Open the app in a browser.
2. Enter any combination of **book title, author, or genre**.
3. Click **Get Recommendations**.
4. View recommended books with thumbnails.

---

## ⚠️ Known Limitations

* Recommendations depend on **Google Books API** metadata.
* Limited diversity if books have similar features.
* AWS Lambda or API latency may slow responses; caching can improve speed.

---

## 🧰 Tools & Technologies

* **Python 3.10+**
* **Streamlit** for UI
* **AWS DynamoDB** for storing user preferences and recommendations
* **AWS Lambda** for backend recommendation logic
* **AWS Comprehend** for text feature processing
* **Google Books API** for book metadata
* **NumPy** for similarity computation

---


