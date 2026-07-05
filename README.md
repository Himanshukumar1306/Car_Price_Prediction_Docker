# Car Price Prediction Web App

An end-to-end Machine Learning web application that predicts the resale price of a used car based on its historical specifications and features. The application consists of a trained **Random Forest Regressor** model, a robust **Flask backend API**, and a premium **glassmorphic responsive UI**—all packaged inside a secure, isolated **Docker container** configured for seamless cloud deployment.

🌐 **Live Website**: Access the live web application at **[https://car-price-prediction-docker-cjrn.onrender.com/](https://car-price-prediction-docker-cjrn.onrender.com/)**

---

## 🚀 Key Features

*   **High Accuracy Model**: Trained on the standard CarDekho dataset utilizing a `RandomForestRegressor` with a test $R^2$ score of **`0.9585`** (and train $R^2$ score of `0.9864`).
*   **Premium Glassmorphic UI**: Elegant interactive frontend styling utilizing violet-indigo gradients, micro-animations, backdrop-filters, and dynamic AJAX form submissions (no page reloading).
*   **Secure Containerization**:
    *   Runs as a non-privileged `appuser` (non-root execution) for defense-in-depth container security.
    *   Dynamic port-binding that adapts automatically to cloud environments (like Render).
    *   Secure, port-aware internal health check using Python's built-in `urllib` package (eliminating `curl`/`wget` dependencies).
*   **Infrastructure as Code**: Included `render.yaml` Blueprint configuration for automated one-click deployments.

---

## 📁 Repository Structure

```text
├── templates/
│   └── index.html         # Premium glassmorphic UI dashboard
├── app.py                 # Flask server & prediction endpoints
├── train.py               # Model training script
├── car_data.csv           # Model training dataset
├── model.pkl              # Serialized Random Forest model
├── requirements.txt       # Server dependencies
├── Dockerfile             # Secure container configuration
├── .dockerignore          # Docker context file exclusion
├── render.yaml            # Render Blueprint specification
├── .gitignore             # Git ignored files configuration
└── README.md              # Project documentation
```

---

## 📊 Model & Features Specification

The regression model is trained on the following input parameters:

*   **Present Price**: Ex-showroom price of the car (in Lakhs).
*   **Kilometers Driven**: Total mileage.
*   **Fuel Type**: Encoded integer representation:
    *   `0`: Petrol
    *   `1`: Diesel
    *   `2`: CNG
*   **Seller Type**: Encoded integer representation:
    *   `0`: Dealer
    *   `1`: Individual
*   **Transmission**: Encoded integer representation:
    *   `0`: Manual
    *   `1`: Automatic
*   **Number of Previous Owners**: Typically `0`, `1`, `2`, or `3`.
*   **Age of Car**: The calculated age of the car (in years) relative to the dataset collection baseline (`2020 - Purchase_Year`).
