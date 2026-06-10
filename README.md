# Football Analytics & Market Valuation Dashboard

## Project Overview
Modern football has evolved into a multi-billion dollar industry driven by data. This project was created to explore the complex relationship between advanced on-field performance metrics and the financial market value of players across Europe's Top 5 Leagues. By leveraging Big Data and advanced statistics, the dashboard provides an interactive platform to compare leagues and seasons, analyze how specific statistics impact market valuations, and highlight player profiles that contribute to their teams' playstyles. 

## Dataset Sources
This project integrates two main data sources:
* **Transfermarkt Dataset:** Provides historical records of player market valuations, transfers, and general player information.
* **FBref Dataset (Europe's Top 5 Leagues 2017-2025):** Contains advanced performance metrics including expected goals (xG), expected assists (xA), progressive passes, and defensive actions.

## Main Tools
* **Python 3.11** 
* **Streamlit** (for the interactive web dashboard)
* **Pandas & NumPy** (for data manipulation and merging)
* **Matplotlib & Seaborn** (for static data visualization)
* **GeoPandas & Folium** (for geographic mapping)
* **Jupyter Notebook** (for EDA, data cleaning, and animation generation)

## Project Structure
The repository is organized as follows:

* `Datasets/`: Contains the original raw datasets as well as the processed `.parquet` files generated after data cleaning and transformations.
* `Notebooks/`: Includes the `.ipynb` Jupyter Notebooks used to clean, merge, and convert the datasets into parquet format. It also contains the notebook responsible for generating the bar race animations.
* `Resources/`: Stores the generated videos and GIFs for the animated visualizations.
* `.streamlit/`: Contains configuration files defining the custom theme and color palette for the dashboard.
* Main application script (`main.py`) to run the Streamlit dashboard.

## Dashboard Navigation
The Streamlit application features a persistent slider available at all times, allowing users to filter the entire dataset by a minimum number of minutes played. The dashboard is divided into the following pages:

1. **Inicio:** Project introduction, context, and overview.
2. **Metodología:** Detailed explanation of the data processing, cleaning, and merging workflow.
3. **Análisis Visual:** Simple metrics and basic data distributions.
4. **Rankings:** Top lists highlighting interesting and standout statistics.
5. **Stats Jugador:** Detailed statistics and information for specific players. Includes a search function by name and season selection.
6. **Stats Por Año:** Longitudinal analysis featuring charts averaged and grouped by league or position across different seasons. Users can select any numerical statistic to visualize its evolution.
7. **Stats de Desempeño:** Advanced visual insights, including boxplots grouped by league or position with labeled outliers, correlation heatmaps for different playstyles, heatmaps analyzing the financial impact of specific stats, and scatter plots comparing interesting metrics with standout players labeled.
8. **Mapa:** A geographic choropleth map colored by the number of players per country, featuring dynamic filters for specific leagues and teams.
9. **Bar Races:** Animated visualizations (videos) showing the dynamic evolution of player market valuations and transfers.
10. **Conclusiones:** Final thoughts, main findings, and the added value derived from the data analysis.

## Installation and Setup
To run this project locally, it is highly recommended to use an Anaconda virtual environment. 

1. Clone this repository to your local machine:
    ```bash
    git clone <repository_url>
    cd <repository_folder>
    ```

2. Create a new Conda environment with Python 3.11:
    ```bash
    conda create -n football_env python=3.11
    ```

4. Activate the virtual environment:
    ```bash
    conda activate football_env
    ```

6. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

7. Run the Streamlit dashboard:
    ```bash
    streamlit run main.py
    ```

## Future Work (To-Do)

* **English Version:** Implement bilingual support to view the entire dashboard in English.
* **Code Refactoring:** Optimize specific functions and modularize files to improve efficiency, readability, and maintainability.
* **UI/UX Tweaks:** Polish minor styling details (Streamlit theme/CSS) and improve the alignment of images and charts across all pages.