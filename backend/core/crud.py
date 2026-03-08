from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from .models import Client
from .schemas import ClientCreate


async def get_clients(db: AsyncSession):
    result = await db.execute(select(Client))
    return result.scalars().all()


async def create_client(db: AsyncSession, client: ClientCreate):
    new_client = Client(
        name=client.name,
        email=client.email,
        phone=client.phone
    )
    db.add(new_client)
    await db.commit()
    await db.refresh(new_client)
    return new_client