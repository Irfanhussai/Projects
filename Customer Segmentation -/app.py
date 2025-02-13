from flask import Flask, render_template, request, jsonify
import numpy as np
import joblib
import tensorflow as tf
import os
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.manifold import TSNE
import io
import base64

# Load the trained models
encoder = tf.keras.models.load_model("encoder_model.h5")
kmeans = joblib.load("kmeans_model.pkl")
scaler = joblib.load("scaler.pkl")

# Initialize Flask app
app = Flask(__name__)

# Function to generate cluster visualization
def generate_plot(sample_latent, latent_features, cluster):
    tsne = TSNE(n_components=2, perplexity=min(5, len(latent_features) - 1), random_state=42)
    tsne_results = tsne.fit_transform(np.vstack([latent_features, sample_latent]))

    plt.figure(figsize=(8, 6))
    hue_labels = list(range(len(latent_features)))
    hue_labels.append("New Sample")

    sns.scatterplot(x=tsne_results[:-1, 0], y=tsne_results[:-1, 1], hue=hue_labels[:-1], palette='viridis')
    plt.scatter(tsne_results[-1, 0], tsne_results[-1, 1], color='red', s=200, label=f"Predicted Cluster {cluster}")
    
    plt.legend()
    plt.title("Predicted Customer Cluster in 2D")
    
    img = io.BytesIO()
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    return plot_url

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Prediction route
@app.route('/predict', methods=['POST'])
def predict():
    age = float(request.form['age'])
    income = float(request.form['income'])
    spending = float(request.form['spending'])
    
    sample_input = np.array([[age, income, spending]])
    sample_scaled = scaler.transform(sample_input)
    sample_latent = encoder.predict(sample_scaled)
    cluster = kmeans.predict(sample_latent)[0]
    latent_features = kmeans.cluster_centers_

    plot_url = generate_plot(sample_latent, latent_features, cluster)
    
    return render_template('prediction.html', cluster=int(cluster), plot_url=plot_url)

if __name__ == '__main__':
    app.run(debug=True)
