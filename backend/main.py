from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .db.database import AsyncSessionLocal
from .core import crud, schemas, models

import uvicorn

app = FastAPI()


async def get_db():
    async with AsyncSessionLocal() as session:
        yield session


@app.get("/")
async def root():
    return {"message": "CRM API"}


@app.get("/clients", response_model=list[schemas.ClientResponse])
async def list_clients(db: AsyncSession = Depends(get_db)):
    return await crud.get_clients(db)


@app.post("/clients", response_model=schemas.ClientResponse)
async def create_client(client: schemas.ClientCreate, db: AsyncSession = Depends(get_db)):
    return await crud.create_client(db, client)


@app.get("/clients/{client_id}", response_model=schemas.ClientResponse)
async def get_client(client_id: int, db: AsyncSession = Depends(get_db)):
    client = await crud.get_client_by_id(db, client_id)
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.patch("/clients/{client_id}", response_model=schemas.ClientResponse)
async def update_client_endpoint(client_id: int, client: schemas.ClientUpdate, db: AsyncSession = Depends(get_db)):
    updated_client = await crud.update_client(db, client_id, client)
    if not updated_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return updated_client


@app.delete("/clients/{client_id}")
async def delete_client_endpoint(client_id: int, db: AsyncSession = Depends(get_db)):
    deleted_client = await crud.delete_client(db, client_id)
    if not deleted_client:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"message": "Client deleted"}


@app.get("/clients/count", response_model=int)
async def client_count(db: AsyncSession = Depends(get_db)):
    return await crud.count_clients(db)



if __name__ == "__main__":
    uvicorn.run("backend.main:app", reload=True)