# Hand Gesture Recognition API with Monitoring

A FastAPI-based service for recognizing hand gestures from landmark data, with built-in monitoring using Prometheus and Grafana. This API is containerized with Docker for easy deployment and scaling.

![Architecture](https://img.shields.io/badge/Architecture-Microservice-brightgreen)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-blue)
![Docker](https://img.shields.io/badge/Docker-24.0.5-blue)
![Prometheus](https://img.shields.io/badge/Prometheus-2.40.0-orange)
![Grafana](https://img.shields.io/badge/Grafana-9.5.0-orange)

## Features

- 🚀 **Real-time Hand Gesture Recognition**
- 📊 **Built-in Monitoring** with Prometheus metrics
- 📈 **Visualization** with Grafana dashboards
- 🐳 **Containerized** with Docker for easy deployment
- 🏗 **RESTful API** with FastAPI
- 🤖 Pre-trained **SVM model** for gesture classification
- 🎯 Multiple gesture types support (like, dislike, two_up, two_up_inverted)
- ⏱ Performance metrics and health checks
- 🔄 Auto-restart and health monitoring

## Prerequisites

- 🐍 Python 3.11+
- 🐳 Docker 20.10.0+
- 🐳 Docker Compose 2.0.0+
- 💻 Unix-based system (Linux/macOS) or WSL2 for Windows

## 🚀 Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hand_gesture_api
   ```

2. Build and start the services:
   ```bash
   docker-compose up --build -d
   ```

3. The following services will be available:
   - API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs
   - Prometheus: http://localhost:9090
   - Grafana: http://localhost:3000 (admin/admin)

## 🛠 Development Setup

1. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## 🗂 Project Structure

```
hand_gesture_api/
├── app/                    # Application code
│   ├── __init__.py
│   ├── main.py             # FastAPI application
│   └── models/             # Model files
│       ├── best_model_svm.pkl
│       └── label_encoder.pkl
├── monitoring/            # Monitoring configuration
│   ├── grafana/
│   │   ├── provisioning/
│   │   │   ├── dashboards/
│   │   │   └── datasources/
│   │   └── dashboards/
│   └── prometheus/
├── tests/                 # Test files
│   ├── __init__.py
│   └── test_api.py
├── .gitignore
├── docker-compose.yml     # Docker Compose configuration
├── Dockerfile            # Docker configuration
├── prometheus.yml        # Prometheus configuration
└── requirements.txt      # Python dependencies
```

## 🛠 Monitoring

### Prometheus Metrics

Prometheus is configured to scrape the following metrics:
- Request count and latency
- Error rates
- System metrics
- Custom application metrics

Access Prometheus at: http://localhost:9090

### Grafana Dashboards

Pre-configured dashboards are available at: http://localhost:3000
- Default credentials: admin/admin
- Includes:
  - API Performance Overview
  - Request Rate & Latency
  - Error Rates
  - System Resources

## 📚 API Endpoints

### Health Check
- **GET** `/health`
  - Check if the API is running and the model is loaded
  - Response:
    ```json
    {
        "status": "healthy",
        "model_loaded": true,
        "version": "1.0.0",
        "timestamp": "2023-01-01T12:00:00.000000"
    }
    ```

### Metrics
- **GET** `/metrics`
  - Prometheus metrics endpoint
  - Returns detailed metrics in Prometheus format

### Predict Gesture
- **POST** `/predict`
  - Predict hand gesture from landmark data
  - Request body (JSON):
    ```json
    {
        "landmarks": [x1,y1,z1, x2,y2,z2, ..., x21,y21,z21]  // 63 values total
    }
    ```
  - Response:
    ```json
    {
        "gesture": "like",
        "direction": "up",
        "confidence": 0.95,
        "timestamp": "2023-01-01T12:00:00.000000"
    }
    ```

## 🚨 Troubleshooting

### Common Issues

1. **Port Conflicts**
   - Ensure ports 8000, 9090, and 3000 are available
   - Or update the ports in `docker-compose.yml`

2. **Prometheus Directory Permissions**
   If you see permission errors, ensure the `/tmp/prometheus_data` directory has proper permissions:
   ```bash
   chmod 777 /tmp/prometheus_data
   ```

3. **Grafana Login Issues**
   Default credentials are admin/admin
   - If locked out, reset with:
   ```bash
   docker exec -it hand_gesture_grafana grafana-cli admin reset-admin-password admin
   ```


## 👥 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Available Gestures

| Gesture         | Direction | Description                     |
|----------------|-----------|---------------------------------|
| like           | up        | Thumbs up gesture               |
| dislike        | down      | Thumbs down gesture             |
| two_up         | right     | Two fingers up                  |
| two_up_inverted| left     | Two fingers up (inverted)       |


## Running the API

1. Start the FastAPI server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. Access the interactive API documentation at:
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite with:
```bash
pytest tests/
```

## Performance

The API is optimized for predictions with the following characteristics:
- Average prediction time: < 20ms
- Memory efficient model loading
- Built-in request validation
- Error handling and logging

## Error Handling

The API returns appropriate HTTP status codes and error messages for various scenarios:
- `400 Bad Request`: Invalid input format or missing parameters
- `500 Internal Server Error`: Model loading issues or server errors

## Contributing

1. Fork the repository
2. Create a new branch for your feature
3. Commit your changes
4. Push to the branch
5. Create a new Pull Request


 ## Grafana Dashboard

 <img width="1469" alt="Screenshot 2025-06-02 at 10 29 55 AM" src="https://github.com/user-attachments/assets/2aa8b29a-47a0-47ba-96cc-8e61f961b9a0" />
 

 **Model-Related Metric: Model Prediction Response Time (POST /predict)** • What it Tracks: The average time it takes for the model to respond to inference requests on the /predict endpoint. 

• Why It’s Important: It directly reflects model performance and responsiveness. High latency here can degrade user experience or break downstream systems expecting real-time results.

**Data-Related Metric: Data Volume Returned by /metrics**
 • What it Tracks: The average size of the HTTP response payload served from the /metrics endpoint. 
 
 • Why It’s Important: /metrics is used by Prometheus to scrape system data—if its payload becomes too large: Scrapes may time out or fail. Monitoring may slow down or become incomplete. Networking or storage costs may rise, especially in high-frequency scraping environments.

**Server-Related Metric: Server Load by Route**
 • What it Tracks: The number of HTTP requests received by each handler/route (e.g., /predict, /health, /metrics). 
 
 • Why It’s Important: Shows how traffic is distributed across your API. • Helps detect: Overloaded routes (e.g., /predict under constant stress). Unexpected usage patterns (e.g., bots hammering /docs or /health). Underused routes that may be obsolete or misconfigured.

