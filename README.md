## Getting Started

### Prerequisites

- Python 3.8+
- Docker & Docker Compose

### Setup

1. **Clone the repository:**
    ```sh
    git clone https://github.com/yourusername/e-commerce-api.git
    cd e-commerce-api
    ```

2. **Initialize environment variables:**
    ```sh
    bash scripts/init-project.sh
    ```

3. **Start the application with Docker Compose:**
    ```sh
    docker-compose up --build
    ```

4. **Access the API:**
    - API root: [http://localhost:8000](http://localhost:8000)
    - Swagger docs: [http://localhost:8000/docs](http://localhost:8000/docs)

## Configuration

- Environment variables are loaded from `.env` (see [`scripts/init-project.sh`](scripts/init-project.sh)).
- Database URL is set in `docker-compose.yml` and `.env`.

## License

MIT License