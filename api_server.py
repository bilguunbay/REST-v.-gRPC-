from enum import Enum
from http.client import HTTPException

from fastapi import FastAPI
from pydantic import BaseModel

#very important, instantiating fastAPI, the web framework (almost complete web server, all plumbing no furniture)
app = FastAPI()

class Category(Enum):
    TOOLS = "tools"
    CONSUMABLES = "consumables"


class Item(BaseModel):
    name: str
    price: float
    count: int
    id: int
    category: Category 

items = {
    0: Item(name="Hammer", price=9.99, count=20, id=0, category=Category.TOOLS),
    1: Item(name="Pliers", price=5.99, count=20, id=1, category=Category.TOOLS), 
    2: Item(name="Nails", price=1.99, count=100, id=2, category=Category.CONSUMABLES)
}

#FastAPI handles JSON serialization and deserialization for us.
#We can simply use built-in python adn Pydantic types, in this case dict[int, Item]

@app.get("/d") #the slash indicates the root drive, think of it as the first thing you see when you land on the site 
def index() -> dict[str, dict[int, Item]]: #we have a method called 'index' which returns a dictionary 
    return {"items": items}

@app.get("/items/{item_id}")
def query_item_by_id(item_id: int) -> Item:
    if item_id not in items:
       return HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist")
    else:
       return items[item_id]
   
@app.post("/") 
def add_item(item: Item) -> dict[str, Item]:
    
    if item.id in items:
        HTTPException(status_code=400, detail=f"Item with {item.id=} already exists.")
    
    items[item.id] = item
    return {"added": item}

@app.delete("/items/{item_id}")
def delete_item(item_id: int) -> dict[str, Item]:

    if item_id not in items:
        raise HTTPException( 
            status_code=303, detail=f"Item with {item_id=} does not exist."
        )
    
    item = items.pop(item_id)
    return {"deleted": item}

@app.put("/items/{item_id}")
def update(
    item_id: int,
    name: str | None = None,
    price: float | None = None, 
    count: int | None = None 
) -> dict[str, Item]:
    
    if item_id not in items:
        HTTPException(status_code=404, detail=f"Item with {item_id=} does not exist.")
    if all(info is None for info in (name, price, count)):
        raise HTTPException(
            status_code = 400, detail="No parameters provided for update"
        )
    
    item = items[item_id]

    if name is not None:
        item.name = name
    if price is not None:
        item.price = price
    if count is not None:
        item.count = count

    return {"Updated": item}



# @app.get("/abc")
# def index2() -> dict[str, dict[int, Item]]: 
#     return {"items": items}

# @app.get("/def")
# def index3() -> dict[str, dict[int, Item]]: 
#     return {"items": items[1]}

#Internet tech built on http protocol, which exchanges information
#Four commands often used: GET: retrieves information for client, POST: submits information, DELETE, PUT: updates info
#browser sends request to server upon landing for the index method 
#get is a RestFul call, where we return something from a certain request 
#for example, a patient getting a query for their data will first receive the homepage, then an api call is made to get
#   their specific information 
#accept encoding = the types of compression the browser can run 