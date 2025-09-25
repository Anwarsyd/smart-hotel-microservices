from pydantic import BaseModel

class FaceCreate(BaseModel):
    name: str
    embedding: bytes  # This will come from frontend as bytes

class FaceVerify(BaseModel):
    embedding: bytes

class FaceResponse(BaseModel):
    id: int
    name: str