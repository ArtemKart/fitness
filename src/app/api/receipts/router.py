from fastapi import APIRouter, HTTPException
from sqlalchemy import insert
from app.api.auth import schemas

from app.db.models import Receipt
from app.api.deps import CurrentUser, SessionDep
from app.api.msg_schema import Msg


receipt_router = APIRouter(
    prefix="/receipt",
    tags=["Receipt"],
)


@receipt_router.post("/add")
def add_receipt(
    data: schemas.ReceiptCreate,
    user: CurrentUser,
    session: SessionDep,
):
    try:
        stmt = insert(Receipt).values(**data.model_dump() | {"user_id": user.id})
        session.execute(stmt)
        session.commit()
        return Msg(msg="Receipt was successfuly added.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
