from fastapi import FastAPI
from app.routes import router

app = FastAPI()

# Incluindo os endpoints
app.include_router(router, prefix="/api/v1", tags=["Availability"])

@app.get("/")
def root():
    return {"message": "Availability Service is Running!"}
