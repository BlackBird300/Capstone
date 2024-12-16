
import pandas as pd
from datetime import datetime
from sklearn.cluster import KMeans
import numpy as np
from sklearn.preprocessing import MinMaxScaler, StandardScaler, LabelEncoder
from sklearn.decomposition import PCA

from .Data_Fetching import Data_Fetching
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
import logging
import warnings

warnings.filterwarnings("ignore")

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class Clustering:

    def __init__(self, data_Clustering):
        
        self.data_clustering = data_Clustering.copy()


    def Clustering(self): 
        label_encoder = LabelEncoder()
        self.data_clustering['Sector_Encoded'] = label_encoder.fit_transform(self.data_clustering['Sector'])
        numerical_columns = ['Sector_Encoded', 'Market Cap', 'P/E Ratio', 'EPS', 'Dividend Yield', 'Revenue', 'Profit Margin', 'Operating Margin', 'Return on Assets', 'Return on Equity', 'Debt to Equity', 'Current Ratio', 'Quick Ratio']
        scaler = MinMaxScaler()
        scaled_data = scaler.fit_transform(self.data_clustering[numerical_columns])
        data_clustering_scaled = pd.DataFrame(scaled_data, columns=numerical_columns)

        # K-Means Clustering
        k = 15
        kmeans = KMeans(n_clusters=k, random_state=0).fit(data_clustering_scaled)
        self.data_clustering['Cluster K-Means'] = kmeans.fit_predict(data_clustering_scaled)

        # Gaussian Mixture Model
        gmm = GaussianMixture(n_components=k, random_state=0).fit(data_clustering_scaled)
        self.data_clustering['Cluster GMM'] = gmm.predict(data_clustering_scaled)

        return self.data_clustering


 



