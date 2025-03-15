import pandas as pd

# Load the clustered data
file_path = "C:/Users/RAJAT/Downloads/herhealthai/data/clustereddata.csv"
df = pd.read_csv(file_path)

# Display basic information
print("📌 Dataset Overview:")
print(df.head())

# Check unique clusters
print("\n🔍 Unique Clusters (KMeans):", df["KMeans_Cluster"].unique())
print("🔍 Unique Clusters (GMM):", df["GMM_Cluster"].unique())

# Count the number of samples per cluster
print("\n📊 Cluster Distribution (KMeans):")
print(df["KMeans_Cluster"].value_counts())

print("\n📊 Cluster Distribution (GMM):")
print(df["GMM_Cluster"].value_counts())
