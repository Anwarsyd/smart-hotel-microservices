from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "hotel Service running"}

@app.get("/health")
def health_check():
    return {"status": "ok"}
