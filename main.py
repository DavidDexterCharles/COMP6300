from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Hello from FastAPI!"}

@app.get("/test")
def read_root():
    return {"message": "Hello from test!"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    # Run with Uvicorn so you can start the app using: python main.py
    # Note: ensure the virtual environment is activated and uvicorn is installed.
    try:
        import uvicorn
    except Exception as e:
        print("uvicorn is required to run the server. Install it in your venv: pip install uvicorn[standard]")
        raise

    # When reload=True, uvicorn will spawn a reloader which imports this module by name.
    uvicorn.run("main:app", host="127.0.0.1", port=8080, reload=True)