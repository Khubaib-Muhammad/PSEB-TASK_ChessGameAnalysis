# ♟️ Chess Game Exploratory Data Analysis & Streamlit Dashboard

This repository contains a comprehensive data analysis pipeline and an interactive **Streamlit Dashboard** built to explore and extract patterns from a dataset of over 20,000 chess games played on Lichess.

---

## 📋 Project Overview

The objective of this project is to clean, analyze, and visualize structural relationships in online chess matchups, focusing on:
- Player rating distributions and correlations.
- The relationship between game length (turns) and match outcomes.
- Opening performance metrics (win rates, draw ratios, and game longevity).
- Interactive visualizations built into a user-friendly Streamlit web app.

---

## 🔍 Key Data Insights

### 1. Data Cleaning & Duplicates
* The raw dataset contained **20,058 games**.
* Exactly **429 duplicate entries** were identified and removed, resulting in a clean dataset of **19,629 unique games**.

### 2. Victory Conditions & Game Length
* **Resignation** is the most common game outcome, followed by checkmates.
* Draws tend to have the highest average duration (**84.2 turns**), while games ending in resignations are generally the shortest (**53.9 turns**).

### 3. Ratings & Turn Correlation
* The Pearson correlation coefficients revealed a very weak positive relationship between game length and player ratings:
  * **Turns vs. White's Rating:** `0.1291`
  * **Turns vs. Black's Rating:** `0.1598`
* While higher-rated players tend to play slightly longer games on average, player rating alone does not heavily dictate game length.

### 4. Opening Performance (Top 15 Openings)
* **Longest Games:** *Philidor Defense #2* leads with an average of **69.8 turns**, confirming its defensive and maneuvering nature.
* **Shortest Games:** *Scandinavian Defense* leads to the shortest games on average (**46.7 turns**), highlighting its open, highly tactical character.
* **Highest Win Rates:** 
  * **White:** *Philidor Defense #3* (**63.8%** win rate) and *Scandinavian Defense: Mieses-Kotroc Variation* (**62.8%** win rate).
  * **Black:** *Van't Kruijs Opening* (**53.7%** win rate) and *Indian Game* (**52.2%** win rate).

---

## 🖥️ The Streamlit App (`app.py`)

The accompanying Streamlit dashboard provides a professional, highly interactive interface to continue exploring the dataset dynamically.

### Key Features:
* **Custom Filters:** Filter games dynamically by rated vs. unrated status, victory outcome, and specific player rating ranges via an interactive sidebar.
* **Plot Generator:** Create custom visualizations on the fly including Scatter Plots, Box Plots, Histograms, Bar Charts, and Correlation Heatmaps with customizable parameters (axes, bins, and color palettes).
* **Export Utility:** Download any customized graph immediately as a high-resolution PNG image.
* **Openings Analytics:** Dive deeper into the average game lengths and win ratios for the most popular chess openings.

---

## 🚀 How to Run the App Locally

Follow these quick steps to host the Streamlit application on your local machine:

### 1. Prerequisites
Ensure you have Python installed, then install the required dependencies:
```bash
pip install streamlit pandas numpy matplotlib seaborn
```

### 2. Setup Files
* Place your `games.csv` dataset and the generated `streamlit_app.py` script inside the same folder.

### 3. Start the Server
Run the following command in your terminal/command prompt from within that directory:
```bash
streamlit run app.py
```
Your default browser will automatically launch and open the app at `http://localhost:8501`.### 4. Test the App on Streamlit Cloud

Visit the link below to use the app live online:

**[Launch Chess Game Analysis App](https://pseb-taskchessgameanalysis-exjsdh9r38xdwxmhuaaf4c.streamlit.app/)**
