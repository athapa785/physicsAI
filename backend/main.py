from fastapi import FastAPI
from backend.api.endpoints import router as api_router

app = FastAPI(title="Physics Tutor Backend")

# Include API routes
app.include_router(api_router)

# Root endpoint
@app.get("/")
def read_root():
    return {"message": "Physics Tutor Backend is running"}
