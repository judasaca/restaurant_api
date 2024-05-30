import motor.motor_asyncio
from fastapi import Request


async def get_db_client(request: Request) -> motor.motor_asyncio.AsyncIOMotorDatabase:
    return request.app.state.db_client
