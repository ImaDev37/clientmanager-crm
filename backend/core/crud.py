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


async def get_client_by_id(db: AsyncSession, client_id: int):
    result = await db.execute(select(Client).where(Client.id == client_id))
    return result.scalar_one_or_none()


async def update_client(db: AsyncSession, client_id: int, client: ClientCreate):
    db_client = await get_client_by_id(db, client_id)
    if db_client:
        db_client.name = client.name
        db_client.email = client.email
        db_client.phone = client.phone
        await db.commit()
        await db.refresh(db_client)
    return db_client


async def delete_client(db: AsyncSession, client_id: int):
    db_client = await get_client_by_id(db, client_id)
    if db_client:
        await db.delete(db_client)
        await db.commit()
    return db_client


async def count_clients(db: AsyncSession):
    result = await db.execute(select(Client))
    return len(result.scalars().all())