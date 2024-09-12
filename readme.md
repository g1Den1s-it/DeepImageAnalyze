# DeepImageAnalyze

**DeepImageAnalyze** is an asynchronous API for online image analysis using machine learning models. The platform allows users to upload images for automatic processing and obtain results such as object recognition

## Key Features

- **Authorization**: Users can register and log in using JWT tokens.
- **Image Uploading**: Users can upload images via the API for further analysis.
- **File Management**: Users can manage files using CRUD methods.
- **Result Retrieval**: Provides easy access to processed results through the API.

## Technologies

- **FastAPI** - Framework for building asynchronous APIs.
- **PostgresSQL** - The database used for saving results.
## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/g1Den1s-it/DeepImageAnalyze
   cd DeepImageAnalyze
   ```
2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
3. Run the database using Docker Compose. 
   ```bash
   docker compose up --build
   ```
4. Apply migration to the database.
   ```bash
   alembic upgrade head
   ```
5. Run FastApi server
   ```bash
   python -m src.main
   ```