import time

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate


router = APIRouter(
    prefix="/operations",
    tags=["Operation"]
)


@router.get("/long_operation")
@cache(expire=30)
def get_long_op():
    time.sleep(2)
    return "Много много данных, которые вычислялись сто лет"

@router.post("")
async def add_specific_operations(new_operation: OperationCreate, session: AsyncSession = Depends(get_async_session)):
    """
    docstring
    """
    stmt = insert(operation).values(**new_operation.dict())
    print(new_operation)
    await session.execute(stmt)
    await session.commit()
    return {"status": "success"}

@router.get("")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        records = result.fetchall()
        data = [] #пустой массив для каждого результата
        for record in records:
            cnt = 0
            temp_data = {}
            for i in operation.columns:
                temp_data[i.name] = record[cnt] #добавление в словарь названия столбца и информации
                cnt += 1
            data.append(temp_data) #добавление экземпляра в список результатов
        return {
            "status": "success",
            "data": data,
            "details": None
        }
    except Exception:
        # Передать ошибку разработчикам
        raise HTTPException(status_code=500, detail={
            "status": "error",
            "data": None,
            "details": Exception
        })


