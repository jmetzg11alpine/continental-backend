from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel


app = FastAPI()

origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    title: str

class Update(BaseModel):
    id: int

data = {
        1: {'title': 'one', 'stage': 1}, 
        2: {'title': 'two', 'stage': 2},
        3: {'title': 'three', 'stage': 3},
        4: {'title': 'four', 'stage': 4}
    }

@app.get('/data')
def get_board():
    return {'data': data}

@app.get('/1')
def get_one():
    ids = []
    titles = []
    for key in data:
        if data[key]['stage'] == 1:
            ids.append(key)
            titles.append(data[key]['title'])
    return {'ids': ids, 'titles': titles}

@app.get('/2')
def get_two():
    ids = []
    titles = []
    for key in data:
        if data[key]['stage'] == 2:
            ids.append(key)
            titles.append(data[key]['title'])
    return {'ids': ids, 'titles': titles}

@app.get('/3')
def get_two():
    ids = []
    titles = []
    for key in data:
        if data[key]['stage'] == 3:
            ids.append(key)
            titles.append(data[key]['title'])
    return {'ids': ids, 'titles': titles}

@app.get('/4')
def get_two():
    ids = []
    titles = []
    for key in data:
        if data[key]['stage'] == 4:
            ids.append(key)
            titles.append(data[key]['title'])
    return {'ids': ids, 'titles': titles}


@app.post('/post')
def post_item(task: Task):
    id = max(data.keys()) + 1
    data[id] = {'title': task.title, 'stage': 1}
    print(data)

@app.post('/update')
def update_item(update: Update):
    id = update.id 
    data[id]['stage'] += 1
    if data[id]['stage'] > 4:
        del data[id]
    print(data)