# %%
import csv
from collections import defaultdict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import gensim
from gensim import corpora

# %%
# Load the hotel comments data
comments = []
hotel_ids = []
with open('hotel_comments_6.csv', 'r', newline='', encoding='utf-8-sig') as input_file:
    reader = csv.DictReader(input_file)
    for row in reader:
        comments.append(row['Body'])
        hotel_ids.append(row['Hotel ID'])

# Split the comments into words
tokenized_comments = [comment.lower().split() for comment in comments]

# Create a dictionary from the tokenized comments
dictionary = corpora.Dictionary(tokenized_comments)

# Create a corpus from the tokenized comments
corpus = [dictionary.doc2bow(comment) for comment in tokenized_comments]

# Train a TF-IDF model
tfidf = gensim.models.TfidfModel(corpus)
tfidf_corpus = tfidf[corpus]

# Calculate the cosine similarity matrix using Gensim
similarity_matrix = gensim.similarities.SparseMatrixSimilarity(tfidf_corpus, num_features=len(dictionary))

# Define a function to get the top N most similar hotel IDs
def get_top_n_similar(comment_index, n=5):
    sims = similarity_matrix[tfidf_corpus[comment_index]]
    sorted_sims = sorted(enumerate(sims), key=lambda item: -item[1])
    similar_indices = [i for i, _ in sorted_sims[1:n+1]]
    similar_scores = [score for _, score in sorted_sims[1:n+1]]
    similar_hotel_ids = [hotel_ids[i] for i in similar_indices]
    return similar_hotel_ids, similar_scores


# %%
# Example
target_comment_index = 4
top_n_similar, top_n_scores = get_top_n_similar(target_comment_index, n=5)

print(f"Target comment: {comments[target_comment_index]}")
print("Hotel ID của comment có mức similar cao nhất với target:")
for i, (comment, score) in enumerate(zip(top_n_similar, top_n_scores), start=1):
    print(f"{i}. {comment} (Similarity score: {score:.2f})")

# %%



