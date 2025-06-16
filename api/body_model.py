from pydantic import BaseModel

class DesignRequest(BaseModel):
    raw_image: str
    