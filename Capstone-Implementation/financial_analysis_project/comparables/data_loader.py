import logging
from .Comparables_Algorithms.Data_Fetching import Data_Fetching

data_DTW = None
data_Clustering = None

def get_data():
    global data_DTW, data_Clustering
    if data_DTW is None or data_Clustering is None:
        logging.info("Initializing data fetching...")
        data_fetching = Data_Fetching()
        data_DTW = data_fetching.Prepare_Data_DTW()
        data_Clustering = data_fetching.Prepare_Data_Clustering()
        logging.info("Data fetching completed successfully.")


    return data_DTW, data_Clustering
