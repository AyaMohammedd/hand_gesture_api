# Hand Gesture Recognition API

A FastAPI-based service for recognizing hand gestures from landmark data and mapping them to directional commands. This API is designed to be lightweight, efficient, and easy to integrate with various frontend applications.

## Features

- Real-time hand gesture recognition
- RESTful API endpoints for predictions
- Health check and metrics monitoring
- Built with FastAPI for high performance
- Pre-trained SVM model for gesture classification
- Support for multiple gesture types (like, dislike, two_up, two_up_inverted)
- Direction mapping for intuitive gesture control

## Prerequisites

- Python 3.8+
- pip (Python package manager)

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd hand_gesture_api
   ```

2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Project Structure

```
hand_gesture_api/
├── app/
│   ├── __init__.py
│   ├── main.py          # Main FastAPI application
│   └── models/          # Directory for model files
│       ├── best_model_svm.pkl
│       └── label_encoder.pkl
├── tests/               # Test files
│   ├── __init__.py
│   └── test_api.py
└── README.md           # This file
```

## API Endpoints

### Health Check
- **GET** `/health`
  - Check if the API is running and the model is loaded
  - Response:
    ```json
    {
        "status": "healthy",
        "model_loaded": true,
        "timestamp": "2023-01-01T12:00:00.000000"
    }
    ```

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

### Get Metrics
- **GET** `/metrics`
  - Get prediction statistics
  - Response:
    ```json
    {
        "total_predictions": 42,
        "error_rate": 0.05,
        "average_latency_ms": 15.2,
        "uptime_seconds": 3600.5
    }
    ```

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

The API is optimized for low-latency predictions with the following characteristics:
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

## License

[Specify your license here]