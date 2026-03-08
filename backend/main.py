from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .db.database import AsyncSessionLocal
from .core import crud, schemas, models


app = FastAPI()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/")
async def root():
    return {"message": "CRM API"}


@app.get("/clients", response_model=list[schemas.ClientResponse])
async def list_clients(db: AsyncSession = Depends(get_db)):
    clients = await crud.get_clients(db)
    return clients


@app.post("/clients", response_model=schemas.ClientResponse)
async def create_client(client: schemas.ClientCreate, db: AsyncSession = Depends(get_db)):
    new_client = await crud.create_client(db, client)
    return new_client