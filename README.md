# 📊 Bank Customer Retention Dashboard

Hey there! Welcome to my repository. This project focuses on analyzing customer behavioral data from a European bank to understand exactly why customers leave (churn) and what keeps them around. 

I built a backend data pipeline to clean the raw numbers and calculate custom risk metrics, and then hooked it up to a live, interactive Streamlit dashboard so anyone can filter through the portfolio and spot at-risk accounts instantly.

---

## 🛠️ How the Project is Structured

* **`data_processing.py`** – This is the engine room. It reads the raw customer dataset, fixes anomalies, and calculates advanced customer profiles (like the RSI score and financial mismatches). It saves everything into `Modified_European_Bank.csv`.
* **`app.py`** – This runs the user interface. It tracks 5 main banking KPIs (like Engagement Retention and Product Depth) and maps out the data into interactive charts.
* **`Modified_European_Bank.csv`** – The final, fully cleaned and optimized dataset that feeds the dashboard.
* **`requirements.txt`** – The simple list of Python packages needed to run this project.

---

## 🚀 How to Run the Project Locally

If you want to pull this code down and play with it on your own computer, just follow these three quick steps in your terminal:

### Step 1: Install the Dependencies
Make sure you have Python installed, then run this command to install all the necessary libraries (like Pandas, Streamlit, and Plotly) at once:
```bash
pip install -r requirements.txt
python data_processing.py
streamlit run ECB_app.py
