from fastapi.middleware.cors import CORSMiddleware

def setup_cors(app):
    origins = ["*"]  # Adjust for production
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
