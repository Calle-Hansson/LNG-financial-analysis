# LNG Exports and European Gas Prices (TTF)

This project explores whether LNG exports from the United States have
explanatory or predictive power on European natural gas prices (TTF).

The project is primarily educational and focuses on data handling,
modeling, evaluation, and visualization rather than producing a
functioning predictive model.

---

## Project Overview

The hypothesis investigated is whether increased LNG export activity
from the US port Sabine Pass is associated with changes in the European TTF gas price.

The analysis includes:
- Data preprocessing and feature engineering
- Baseline modeling
- Linear Regression
- Model evaluation using MAE and RMSE
- Visualization through a Flask web application

---

## Methods

### Data Processing
- Time series alignment between export activity and gas prices
- Lagged features of TTF prices (1, 7, 14, and 21 days)
- Comparison against a baseline model

### Models
- Linear Regression

### Evaluation Metrics
- Mean Absolute Error (MAE)
- Root Mean Squared Error (RMSE)

---

## Results

The trained models did **not** outperform the baseline model.

This indicates that, within the scope of this dataset and modeling
approach, no strong linear relationship could be identified between LNG
export volumes and short-term movements in TTF prices.

This result highlights the difficulty of modeling energy markets using
simple linear methods and limited explanatory variables.

---

## Web Application

A Flask application is included to:
- Display the relevant time series
- Present evaluation metrics directly on the webpage
- Provide a clear visual overview of the data

---

## Data Availability

Raw CSV data files are not included in this repository due to GitHub file
size limitations.

Data can be obtained from:

- AIS export datasets:
- * https://marinecadastre.gov/accessais/api/v1/search/download/?id=176632433230372488&t=47a7942e-ea4a-4de6-abae-94069d5d3764&aoi=844*
- * https://marinecadastre.gov/accessais/api/v1/search/download/?id=176632433230372488&t=47a7942e-ea4a-4de6-abae-94069d5d3764&aoi=1544


After downloading, place the files in the same folder as the Import_historic_AIS.py.

---

## Reproducibility

To reproduce the analysis:

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt.txt
3. run the files in order:
   1. Import_historic_AIS.py
   2. Predictionmodel.py
   3. app.py
4. View data analysis at http://127.0.0.1:5000
