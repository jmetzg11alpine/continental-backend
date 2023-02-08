from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from deta import Deta

deta = Deta('b0oukw62_1eCwpwFVkcnaNJ7oqFwBnhshgSRpTckV')

db = deta.Base('data')

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

def get_all_data():
    res = db.fetch()
    all_tasks = res.items
    while res.last:
        res = db.fetch(last=res.last)
        all_tasks + res.items
    return all_tasks

@app.get('/data')
def get_board():
    res = db.fetch()
    all_tasks = res.items

    while res.last:
        res = db.fetch(last=res.last)
        all_tasks + res.items

    return {'data': all_tasks}

@app.get('/1')
def get_one():
    ids, titles = [], []
    data = get_all_data()
    for d in data:
        if d['stage'] == 1:
            ids.append(d['id'])
            titles.append(d['title'])
    return {'ids': ids, 'titles': titles}

@app.get('/2')
def get_two():
    ids, titles = [], []
    data = get_all_data()
    for d in data:
        if d['stage'] == 2:
            ids.append(d['id'])
            titles.append(d['title'])
    return {'ids': ids, 'titles': titles}

@app.get('/3')
def get_two():
    ids, titles = [], []
    data = get_all_data()
    for d in data:
        if d['stage'] == 3:
            ids.append(d['id'])
            titles.append(d['title'])
    return {'ids': ids, 'titles': titles}

@app.get('/4')
def get_two():
    ids, titles = [], []
    data = get_all_data()
    for d in data:
        if d['stage'] == 4:
            ids.append(d['id'])
            titles.append(d['title'])
    return {'ids': ids, 'titles': titles}


@app.post('/post')
def post_item(task: Task):
    data = get_all_data()
    id = max([d['id'] for d in data]) + 1
    new_task = db.put({"id": id, "title": task.title, "stage": 1})
    return {'message': 201, 'task': new_task}

@app.post('/update')
def update_item(update: Update):
    data = get_all_data()
    id = update.id 
    key = ''
    for d in data:
        if d['id'] == id:
            key = d['key']
            stage = d['stage'] + 1
            if stage > 4:
                db.delete(key)
                return {"message": '200, item deleted'}
            else:
                db.put({'id': d['id'], 'title': d['title'], "stage": stage}, key)
                return {"message": '200'}
    return {"message": "item not found"}
            


 