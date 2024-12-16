import matplotlib.dates as mdates
import pandas as pd
import os
import warnings
import numpy as np
from dtaidistance import dtw
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
from datetime import datetime
from .Data_Fetching import Data_Fetching
import logging


warnings.filterwarnings("ignore")
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger()

class DTW:
    
        def __init__(self, data_DTW):
            self.results = None
            
            self.data_DTW = data_DTW.copy()

        def compute_dtw(self, target_sequence, comparison_sequence):

            return dtw.distance(target_sequence, comparison_sequence)
        
        
        def find_most_similar(self, target_company, variables, top_n=5):
            results = {}
            
            if target_company not in self.data_DTW['Symbol'].values:
                raise ValueError(f"Company {target_company} not found in the dataset.")
            
            # Get the sector of the target company
            target_sector = self.data_DTW[self.data_DTW['Symbol'] == target_company]['Sector'].iloc[0]
            sector_data = self.data_DTW[self.data_DTW['Sector'] == target_sector]

            target_data = sector_data[sector_data['Symbol'] == target_company]

            for variable in variables:
                print(f"Processing variable: {variable}")
                target_sequence = target_data[variable].values
                distances = []

                with ThreadPoolExecutor() as executor:
                    future_to_symbol = {}

                    for symbol in sector_data['Symbol'].unique():
                        if symbol == target_company:
                            continue

                        comparison_data = sector_data[sector_data['Symbol'] == symbol]
                        comparison_sequence = comparison_data[variable].values

                        if len(target_sequence) == 0 or len(comparison_sequence) == 0:
                            continue

                        future = executor.submit(self.compute_dtw, target_sequence, comparison_sequence)
                        future_to_symbol[future] = symbol

                    for future in as_completed(future_to_symbol):
                        symbol = future_to_symbol[future]
                        try:
                            distance = future.result()
                            distances.append((symbol, distance))
                        except Exception as e:
                            print(f"Error processing {symbol}: {e}")

                distances.sort(key=lambda x: x[1])
                results[variable] = distances[:top_n]

            self.results = results


            return self.results

             

