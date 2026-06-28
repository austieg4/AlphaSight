from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Welcome to the AlphaSight API!"}


@app.get("/health")
def health():
    return {"status": "healthy"}