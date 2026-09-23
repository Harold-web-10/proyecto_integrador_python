from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class FavoriteCreate(BaseModel):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "work_id": 1,
            }
        }
    )

    work_id: int = Field(..., gt=0, description="ID de la obra a marcar como favorita.")


class FavoriteRead(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 1,
                "user_id": 1,
                "work_id": 1,
                "created_at": "2026-09-15T20:00:00Z",
            }
        },
    )

    id: int
    user_id: int
    work_id: int
    created_at: datetime
