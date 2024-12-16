

## **Novel Approach for Estimation and Forecast of the Weighted Average Cost of Capital Using ARIMA, LSTM, and Hybrid Model + Company Peer Comparables Finder**

### Objective
This project is divided into two components:

1. **Novel ARIMA-LSTM Approach Notebook**: Focused on predicting the Weighted Average Cost of Capital (WACC) using a hybrid ARIMA-LSTM model. The notebook combines the strengths of ARIMA for short-term linear dependencies and LSTM for long-term nonlinear dependencies.

2. **Company Peer Comparables Finder**: Implements clustering techniques such as K-Means, GMM, and DTW to identify and visualize peer companies based on financial metrics and stock behavior.

---

## Component 1: Novel ARIMA-LSTM Approach

### Description
The ARIMA-LSTM hybrid model provides enhanced accuracy in predicting WACC, which is critical for financial decision-making and company valuation. The hybrid model overcomes the limitations of standalone ARIMA and LSTM by combining their capabilities.

### Features
- **ARIMA Model**: Captures linear dependencies in time-series data.
- **LSTM Model**: Handles nonlinear patterns and long-term dependencies.
- **Hybrid Model**: Utilizes ARIMA residuals as input to LSTM for enhanced predictions.
- **Evaluation Metrics**: Includes MAE, MSE, RMSE, and MAPE.
- **Data Augmentation**: Uses the Ornstein-Uhlenbeck process for augmenting financial data.

### Usage
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BlackBird300/Capstone.git
   ```

2. **Navigate to the Notebook Directory**:
   ```bash
   cd Capstone-Implementation/Capstone_Notebook
   ```

3. **Open the Notebook**:
   Use Jupyter Notebook or any compatible IDE to open the file `Capstone_Exp.ipynb`.

4. **Run the Notebook**:
   Follow the step-by-step instructions in the notebook. Ensure that all required libraries are installed.

5. **Dependencies**:
   - pandas
   - numpy
   - matplotlib
   - seaborn
   - scipy
   - statsmodels
   - sklearn
   - tensorflow
   
   **Install Required Libraries**
Run the following command to install dependencies before running the program:

```bash
pip install -r requirements.txt
```

---

## Component 2: Company Peer Comparables Finder

### Description
This tool helps identify and analyze comparable companies based on clustering algorithms and time-series similarity techniques. The backend is implemented in Django, while the frontend uses Streamlit.

### Features

- **Clustering**: K-Means and GMM are used for segmenting companies based on financial metrics.
- **Dynamic Time Warping (DTW)**: Compares stock price trajectories for time-series similarity.
- **REST API Integration**: Seamless communication between backend (Django) and frontend (Streamlit).
- **Interactive Interface**: A user-friendly Streamlit app for input and output visualization.

### Usage
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/BlackBird300/Capstone.git
   ```

2. **Set Up the Backend**:
   Navigate to the backend directory and start the Django server:
   ```bash
   cd Capstone-Implementation/financial_analysis_project
   python manage.py runserver
   ```

3. **Set Up the Frontend**:
   Open a new terminal, navigate to the frontend directory, and launch the Streamlit app:
   ```bash
   cd Capstone-Implementation/frontend
   streamlit run frontend.py
   ```

4. **Access the Application**:
   - Backend: `http://127.0.0.1:8000/`
   - Frontend: `http://localhost:8501/`

5. **System Architecture**:
   - **Backend**: Processes clustering and DTW calculations.
   - **Frontend**: Displays clustering results and peer company analysis.

6. **File Structure**:
   - `financial_analysis_project/`: Contains backend logic and APIs.
   - `frontend/`: Contains the Streamlit application.
   - `comparables/Comparables_Algorithms/`: Core algorithms for clustering and DTW.

---

## Installation

### Prerequisites
- Python
- Git



### Requirements
A `requirements.txt` file is included, which contains the following libraries:
```plaintext
pandas
numpy
matplotlib
seaborn
scipy
statsmodels
sklearn
tensorflow
django
```

---

## Contributions
Contributions are welcome. Please fork the repository and submit a pull request for any improvements or bug fixes.

---

## Contact
For any questions or support, please reach out to:
- **Salah Eddine Chahma**: [salah.eddine.chahma1@gmail.com](mailto:salah.eddine.chahma1@gmail.com)


