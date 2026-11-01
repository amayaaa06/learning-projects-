from fastapi import FastAPI

app = FastAPI()

@app.get("/hello")
async def root():
    return {"message": "hello"}

@app.get("/health")
async def health_check():
    return{"status": "200"}


