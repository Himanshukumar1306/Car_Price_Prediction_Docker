# Car Price Prediction Web App

An end-to-end Machine Learning web application that predicts the resale price of a used car based on its historical specifications and features. The application consists of a trained **Random Forest Regressor** model, a robust **Flask backend API**, and a premium **glassmorphic responsive UI**—all packaged inside a secure, isolated **Docker container** configured for seamless cloud deployment.

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

## 💻 Running the App Locally

### Method 1: Using Docker (Recommended)
Make sure you have Docker Desktop running on your machine.

1.  **Build the Docker Image**:
    ```bash
    docker build -t car-price-predictor .
    ```
2.  **Run the Container**:
    ```bash
    docker run -d -p 5000:5000 --name car-price-app car-price-predictor
    ```
3.  **Access the Application**:
    Open your browser and navigate to **[http://localhost:5000](http://localhost:5000)**.

---

### Method 2: Running with Local Python
Make sure you have Python 3.8+ installed.

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
2.  **Train the Model (Optional)**:
    If you want to re-train the model locally:
    ```bash
    python train.py
    ```
3.  **Start the Server**:
    ```bash
    python app.py
    ```
4.  **Access the Application**:
    Open your browser and navigate to **[http://127.0.0.1:5000](http://127.0.0.1:5000)**.

---

## ☁️ Deploying to Render

This repository is optimized for deployment on **Render** using a Blueprint specification:

1.  Create a new repository on GitHub and push this codebase.
2.  Log into your **[Render Dashboard](https://dashboard.render.com)**.
3.  Click the **New +** button (top right) and select **Blueprint**.
4.  Select the repository you just created.
5.  Render will parse `render.yaml` and configure the service environment (Docker) automatically on the **Free plan**.
6.  Click **Approve/Deploy**. The container will be compiled and launched live in the cloud.

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
