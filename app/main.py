from fastapi import FastAPI

app = FastAPI(title="Segarer MVP")

@app.get("/health")
def health():
    return {"status": "ok"}
