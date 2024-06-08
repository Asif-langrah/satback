from fastapi import FastAPI
#from openai import OpenAI
from sqlmodel import Field, SQLModel,create_engine, select,Session,delete


DATABASE_KEY= 'postgresql://neondb_owner:LAYBh2ETrNs0@ep-shrill-shadow-a1dtu58s.ap-southeast-1.aws.neon.tech/satbblack?sslmode=require'
#OPENAPI_KEY='add_your_openapi_key'


#table todo
class Todo(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    task: str 

#table user
class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    username: str 
    password: str

#engine links table to database 
engine = create_engine(DATABASE_KEY, echo=True)
SQLModel.metadata.create_all(engine)

app = FastAPI()

@app.get("/todo")
def get_todo():
    with Session(engine) as session:
        todo = session.exec(select(Todo)).all()
    return todo

@app.post("/todo")
def add_todo(id:int,task:str):
    with Session(engine) as session:
        session.add(Todo(id=id,task=task))
        session.commit()
    return "task added successfully"

@app.delete("/todo")
def add_todo(id:int):
    with Session(engine) as session:
        session.exec(delete(Todo).where(id== Todo.id))
        session.commit()
    return "task deleted successfully"

@app.put("/todo")
def add_todo(id:int,new_task:str):
    with Session(engine) as session:
        todo = session.exec(select(Todo).where(id== Todo.id)).one()
        todo.task = new_task
        session.add(todo)
        session.commit()
    return "task updated successfully"


@app.get("/user")
def get_User():
    with Session(engine) as session:
        user = session.exec(select(User)).all()
    return user

@app.post("/user")
def add_user(username:str,password:str):
    with Session(engine) as session:
        session.add(User(username=username,password=password))
        session.commit()
    return "user added successfully"

@app.delete("/user")
def delete_user(id:int):
    with Session(engine) as session:
        session.exec(delete(User).where(id== User.id))
        session.commit()
    return "user deleted successfully"

@app.put("/user")
def add_todo(id:int,username:str):
    with Session(engine) as session:
        user = session.exec(select(User).where(id== User.id)).one()
    user.username = username
    session.add(user)
    session.commit()
    return "user updated successfully"


#link with openai
#client = OpenAI(api_key=OPENAPI_KEY)
#@app.post("/chatgpt")
# def talk_to_gpt(message):
#     response = client.chat.completions.create(
#         model="gpt-3.5-turbo",
#         messages=[
#     {"role": "user", "content": message},
#   ]
#     ) 
#     return response.choices[0].message.content
