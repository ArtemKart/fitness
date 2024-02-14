from fastapi import APIRouter, HTTPException
from sqlalchemy import insert, select

from src.app.api.deps import CurrentUser, SessionDep
from src.app.api.msg_schema import Msg
from src.app.api.receipts.schemas import ReceiptCreate, ReceiptRead
from src.app.db.models import Receipt

receipt_router = APIRouter(
    prefix="/receipt",
    tags=["Receipt"],
)


@receipt_router.post("/add", response_model=Msg)
async def add_receipt(
    data: ReceiptCreate,
    user: CurrentUser,
    session: SessionDep,
) -> Msg:
    try:
        stmt = insert(Receipt).values(**data.model_dump() | {"user_id": user.id})
        await session.execute(stmt)
        await session.commit()
        return Msg(msg="Receipt was successfuly added.")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@receipt_router.get("/get-my-receipts", response_model=list[ReceiptRead])
async def get_user_receipts(
    user: CurrentUser,
    session: SessionDep,
) -> list[ReceiptRead]:
    try:
        query = select(Receipt).where(Receipt.user_id == user.id)
        raw = await session.execute(query)
        result = raw.scalars().all()
        if not result:
            return Msg(msg="You do not create any receipts yet.")
        receipts_read = [
            ReceiptRead(
                name=receipt.name,
                coocking_time=receipt.coocking_time,
                food_items=receipt.food_items,
                description=receipt.description,
            )
            for receipt in result
        ]
        return receipts_read
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
