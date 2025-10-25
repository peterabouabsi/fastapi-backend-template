# FastAPI Boilerplate
A production-ready FastAPI boilerplate for building scalable and performant APIs with built-in support for PostgreSQL, AWS Secrets Manager, and more.

## Getting Started

1. Clone the repository and navigate to the project directory.
2. Install the dependencies with `pip install -r requirements.txt`.
3. Create a `.env`, and `.env.prod`, and `.env.dev` files with the required environment variables.
    
    APP__PORT
    APP__TITLE
    APP__DESCRIPTION
    APP__VERSION
    APP__OPENAPI_URL
    APP__DOCS_URL
    APP__REDOC_URL
    AWS_SM__SECRET_NAME_PG
    AWS_RDS__DB_NAME_PG

4. Run the application with `uvicorn <main:app> --env-file <.env> --host <0.0.0.0> --port <port> --reload`.
5. Access the API at `http://localhost:<port>/docs`

## Configuration

The application uses environment variables to configure the database, AWS Secrets Manager, and other settings. The following environment variables are required:

- `AWS_SM__SECRET_NAME_PG`: The name of the AWS Secrets Manager secret containing the PostgreSQL database credentials.
- `AWS_RDS__DB_NAME_PG`: The name of the AWS RDS database.