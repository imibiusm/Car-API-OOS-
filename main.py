
import json
from pathlib import Path
from fastapi import FastAPI, HTTPException

app = FastAPI()

json_file_path = Path(__file__).parent / "car_data.json"

with open(json_file_path, "r", encoding="utf-8") as json_data:
    data = json.load(json_data)

data = data["brands"]

@app.get("/")
async def running():
    return {"message": "Car API is running!"}

@app.get("/cars/{car_make}/{car_model}")
async def get_car_info(car_make: str, car_model: str):
    # Find the make without relying on capitalization
    make = next(
        (key for key in data if key.lower() == car_make.lower()),
        None
    )

    if make is None:
        raise HTTPException(
            status_code=404,
            detail=f"Make '{car_make}' not found."
        )

    # Find the model without relying on capitalization
    model = next(
        (key for key in data[make] if key.lower() == car_model.lower()),
        None
    )

    if model is None:
        raise HTTPException(
            status_code=404,
            detail=f"Model '{car_model}' not found for make '{make}'."
        )

    return {"make": make, "model": model}

@app.get("/cars/{car_make}")
async def get_car_models(car_make: str):
    # Find the make without relying on capitalization
    make = next(
        (key for key in data if key.lower() == car_make.lower()),
        None
    )

    if make is None:
        raise HTTPException(
            status_code=404,
            detail=f"Make '{car_make}' not found."
        )

    return {"make": make, "models": data[make]}


@app.get("/stats")
async def get_stats():
    total_makes = len(data)
    total_models = sum(len(models) for models in data.values())
    return {"total_makes": total_makes, "total_models": total_models}

@app.get("/search")
async def search_cars(query: str):
    results = []
    for make, models in data.items():
        if query.lower() in make.lower():
            results.append({"make": make, "models": models})
        for model in models:
            if query.lower() in model.lower():
                results.append({"make": make, "model": model})
    return {"results": results}

@app.get("/random")
async def get_random_car():
    import random
    make = random.choice(list(data.keys()))
    model = random.choice(data[make])
    return {"make": make, "model": model}

@app.get("/models/{car_model}")
async def get_model_info(car_model: str):
    for make, models in data.items():
        if car_model in models:
            return {"make": make, "model": car_model}
    raise HTTPException(
        status_code=404,
        detail=f"Model '{car_model}' not found."
    )
    return {"models": all_models}

@app.get("/all_brands")
async def get_all_brands():
    return {"brands": list(data.keys())}

