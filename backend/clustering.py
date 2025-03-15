import pandas as pd
import time
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from sklearn.decomposition import PCA
from scipy.cluster.hierarchy import dendrogram, linkage
from sklearn.cluster import KMeans
from sklearn.mixture import GaussianMixture

def load_data(filepath):
    """Load the preprocessed dataset."""
    try:
        data = pd.read_csv(filepath)
        print(f"✅ Loaded {data.shape[0]} rows & {data.shape[1]} columns.")
        return data
    except Exception as e:
        raise RuntimeError(f"❌ Error loading processed data: {e}")

def reduce_dimensions(data):
    """Reduce dimensions using PCA to make clustering faster."""
    print("📌 Applying PCA for Dimensionality Reduction...")
    pca = PCA(n_components=min(5, data.shape[1]))  # Reduce to max 5 features
    reduced_data = pca.fit_transform(data)
    print(f"✅ Reduced to {reduced_data.shape[1]} dimensions.")
    return reduced_data

def plot_dendrogram(data):
    """Plot a dendrogram for hierarchical clustering with optimized linkage."""
    print("📌 Step 1: Dendrogram (Using Sampled Data)")
    sample_size = min(50, len(data))  # Sample max 50 rows for speed
    print(f"⚡ Sampling {sample_size} rows for dendrogram...")

    sampled_data = data[:sample_size]  # Take first 50 rows (faster than .sample())

    try:
        start_time = time.time()
        linked = linkage(sampled_data, method="centroid")  # 'centroid' is faster than 'ward'

        if time.time() - start_time > 5:  # Stop if it takes too long
            print("⏳ Dendrogram is too slow! Skipping...")
            return

        plt.figure(figsize=(8, 4))
        dendrogram(linked)
        plt.title("Dendrogram (Hierarchical Clustering)")
        plt.xlabel("Samples")
        plt.ylabel("Distance")
        plt.show()
        print("✅ Dendrogram Done!")

    except MemoryError:
        print("❌ Not enough memory for dendrogram!")

def apply_clustering(data, n_clusters):
    """Apply KMeans and GMM clustering on reduced data."""
    print("📌 Step 2: Applying Clustering...")

    print("⚡ Running KMeans...")
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    data["KMeans_Cluster"] = kmeans.fit_predict(data)

    print("⚡ Running Gaussian Mixture Model (GMM)...")
    gmm = GaussianMixture(n_components=n_clusters, random_state=42, max_iter=50, n_init=5)
    data["GMM_Cluster"] = gmm.fit_predict(data)

    return data

def visualize_clusters(data):
    """Visualize the clusters."""
    print("📌 Step 3: Visualizing Clusters...")
    
    sns.pairplot(data, hue="KMeans_Cluster", palette="Set1")
    plt.show()

    sns.pairplot(data, hue="GMM_Cluster", palette="Set2")
    plt.show()

if __name__ == "__main__":
    try:
        print("🔍 Loading processed data for clustering...")
        input_file = "../data/processed_data.csv"
        data = load_data(input_file)

        reduced_data = reduce_dimensions(data)

        plot_dendrogram(reduced_data)

        n_clusters = 5  # Adjust based on dendrogram
        clustered_data = apply_clustering(pd.DataFrame(reduced_data), n_clusters)

        output_file = "../data/clustered_data.csv"
        clustered_data.to_csv(output_file, index=False)
        print(f"✅ Clustering complete! Results saved to {output_file}")

        visualize_clusters(clustered_data)
        print("✅ All Steps Done!")

    except Exception as e:
        print(f"❌ Error: {e}")
