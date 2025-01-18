from fastapi import APIRouter, HTTPException, status
from app.models import Availability
from app.database import insert_availability, get_availabilities, get_availability_by_id, delete_availability, update_availability_in_db, get_availabilities_by_doctor_id
from bson import ObjectId

router = APIRouter()

@router.post("/availability", status_code=status.HTTP_201_CREATED)
async def create_availability(availability: Availability):
    availability_data = availability.dict()
    result = await insert_availability(availability_data)  # Função assíncrona de inserção
    return {"id": str(result.inserted_id), "message": "Availability created successfully"}

@router.get("/availability")
async def get_availabilities_route():
    availabilities = await get_availabilities()  # Recuperar todas as disponibilidades
    for availability in availabilities:
        availability["_id"] = str(availability["_id"])
    return availabilities

@router.get("/availability/{availability_id}")
async def get_availability(availability_id: str):
    availability = await get_availability_by_id(availability_id)  # Buscar por ID
    if not availability:
        raise HTTPException(status_code=404, detail="Availability not found")
    availability["_id"] = str(availability["_id"])
    return availability

@router.get("/availability/doctor/{doctor_id}")
async def get_availability(doctor_id: str):
    availabilities = await get_availabilities_by_doctor_id(doctor_id)  # Recuperar todas as disponibilidades
    for availability in availabilities:
        availability["_id"] = str(availability["_id"])
    return availabilities

@router.delete("/availability/{availability_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_availability_route(availability_id: str):
    result = await delete_availability(availability_id)  # Deletar a disponibilidade
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability deleted successfully"}

@router.put("/availability/{availability_id}", status_code=status.HTTP_200_OK)
async def update_availability(availability_id: str, availability: Availability):
    availability_data = availability.dict(exclude_unset=True)  # Exclui campos não enviados

    result = await update_availability_in_db(availability_id, availability_data)  # Atualizar no DB
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Availability not found")
    return {"message": "Availability updated successfully"}
