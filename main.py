from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
  title="Task Manager API",
  description="API for managing tasks",
  version="1.0.0"
)

