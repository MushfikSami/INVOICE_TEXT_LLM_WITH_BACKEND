⚙️ Prerequisites
Docker and Docker Compose installed.

A valid Google Gemini API Key.

(Optional) Python 3.10+ installed locally if you wish to run unit tests outside of Docker.

🚀 Setup & Installation
1. Clone the repository and navigate to the project directory:

Bash
git clone <your-repo-url>
cd gemini-invoice-extractor
2. Configure Environment Variables:
Create a .env file in the root directory and add your credentials:

Code snippet
GEMINI_API_KEY=your_actual_gemini_api_key_here
API_TOKEN=super-secret-auth-token-123
3. Setup Data Version Control (DVC) for test images:
If you want to version control sample invoices without bloating your Git repo:

Bash
pip install dvc
dvc init
# Add your test images to the data/ folder
dvc add data
4. Build and Run with Docker Compose:

Bash
docker-compose up --build
🌐 Accessing the Services
Once the Docker containers are up and running, you can access the different components at the following local addresses:

Streamlit UI: http://localhost:8501

FastAPI Interactive Docs (Swagger): http://localhost:8000/docs

Prometheus Metrics Dashboard: http://localhost:9090

🧪 Running Unit Tests
To run the mocked unit tests for the backend logic (ensuring Redis caching and Gemini API calls behave correctly):

Bash
# Navigate to the backend directory
cd backend

# Install testing requirements locally
pip install -r requirements.txt

# Run pytest
pytest tests/ -v
📝 Usage Notes
Authentication: The frontend automatically passes the API_TOKEN defined in your .env file via headers to authenticate with the FastAPI backend.

Caching: When an identical image and prompt are submitted, the backend will return the result from Redis (valid for 1 hour) instead of calling the Gemini API. The UI will indicate whether the response came from gemini_api or redis_cache.