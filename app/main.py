from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="DevOps Mini Inventory App", version="1.1.0")

class Item(BaseModel):
    name: str
    quantity: int

inventory = {
    1: {"name": "Szerver rack", "quantity": 4},
    2: {"name": "Patch kábel (Cat6)", "quantity": 50}
}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/items")
def get_items():
    return inventory

@app.post("/items/{item_id}", status_code=201)
def add_item(item_id: int, item: Item):
    if item_id in inventory:
        raise HTTPException(status_code=400, detail="Az elem már létezik")
    inventory[item_id] = item.model_dump()
    return {"id": item_id, "item": inventory[item_id]}