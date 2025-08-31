import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import geopandas as gpd
from sklearn.cluster import KMeans
from shapely.geometry import Point
# --- 1. Synthetic Data Generation ---
# Generate synthetic data for store locations and demographics
np.random.seed(42)  # for reproducibility
num_stores = 100
data = {
    'StoreID': range(1, num_stores + 1),
    'Latitude': np.random.uniform(37, 38, num_stores),
    'Longitude': np.random.uniform(-122, -121, num_stores),
    'Sales': np.random.randint(10000, 100000, num_stores),
    'PopulationDensity': np.random.randint(1000, 10000, num_stores)
}
df = pd.DataFrame(data)
# Create geospatial data
geometry = [Point(xy) for xy in zip(df['Longitude'], df['Latitude'])]
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")
# --- 2. Geospatial Clustering ---
# Apply KMeans clustering to identify clusters of stores
kmeans = KMeans(n_clusters=5, random_state=0) # Adjust number of clusters as needed
gdf['Cluster'] = kmeans.fit_predict(gdf[['Latitude', 'Longitude']])
# --- 3. Market Saturation Analysis ---
# Calculate average sales and population density per cluster
cluster_stats = gdf.groupby('Cluster').agg({'Sales': 'mean', 'PopulationDensity': 'mean'})
# --- 4. Visualization ---
# Plot store locations and clusters
plt.figure(figsize=(10, 8))
gdf.plot(column='Cluster', cmap='viridis', legend=True, markersize=30, alpha=0.7, ax=plt.gca())
plt.title('Store Locations and Clusters')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.savefig('store_clusters.png')
print("Plot saved to store_clusters.png")
#Plot Market Saturation (Sales vs Population Density)
plt.figure(figsize=(10,6))
plt.scatter(cluster_stats['PopulationDensity'], cluster_stats['Sales'], c=cluster_stats.index, cmap='viridis')
plt.title('Market Saturation Analysis')
plt.xlabel('Average Population Density')
plt.ylabel('Average Sales')
plt.colorbar(label='Cluster')
plt.savefig('market_saturation.png')
print("Plot saved to market_saturation.png")
# --- 5. Identifying Optimal Locations ---
#  (Illustrative -  requires more sophisticated analysis for real-world application)
#  Identify clusters with low saturation (low sales relative to population density) as potential locations.
#  This section would typically involve more advanced spatial analysis and consideration of external factors.
# Example:  Simple identification of a cluster with low sales relative to population
low_saturation_cluster = cluster_stats.loc[(cluster_stats['Sales'] / cluster_stats['PopulationDensity']).idxmin()].name
print(f"Cluster {low_saturation_cluster} shows potential for new store placement (based on simplified analysis).")