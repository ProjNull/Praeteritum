import uvicorn
from . import app  # Import the app from the __init__.py file

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
