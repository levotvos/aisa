import json
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel
from llama_cpp import Llama

import aisa

class UIInputData(BaseModel):
    text: str
    prompt: str


model = None

def traverse_response(response):
    """
        Megtalalja es kinyeri az elso listat a dict tipusu adatbol
    """
    if isinstance(response, list):
        print(response)
        print("huha")
        for elem in response:
            yield elem
    elif isinstance(response, dict):
        yield from traverse_response(*response.values())
    else:
        print("ez nem jo", type(response))

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    # Load the LLM model
    model = aisa.model.load_model_to_cpu(
        model_path = "./models/mistral_7B_instruct_v02_Q8_0.gguf",
        context_window = 4096
    )
    
    yield

    # At shutdown: release the resources
    del model


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"model": model.tokenize(b"Hello World!")}


@app.post("/annot")
async def annot(data: UIInputData):
    # TODO Pontos return type ?
    # TODO Error handling
    
    print(aisa.__version__)
    print(data.text)
    gd_ret = model + aisa.ner.ner_instruction(data.text)
    print(gd_ret)
    entities = gd_ret["entities"]
    
    return [entities]

@app.get("/train")
async def train():
    return {"message": "NOT IMPLEMENTED"}
