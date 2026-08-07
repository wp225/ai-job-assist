from fastapi import FastAPI
from .api.endpoints import router

def create_app() -> FastAPI:
    app = FastAPI(title="AI-Job-Assist")
    app.include_router(router)
    return app


app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)