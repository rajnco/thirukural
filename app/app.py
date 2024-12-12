from fastapi import Depends, FastAPI
from sqlmodel import SQLModel, Session
import uvicorn, json, os
from contextlib import asynccontextmanager

from settings import Settings, get_settings
from group.kural import kural_router, kural_router2
from group.user import user_router, user_router2
from database.database import check_kural_data, engine
from database.model import Thirukural


def load_data(session: Session):
    app_settings: Settings = get_settings()
    db_file_name = app_settings.db_filename
    #if os.path.isfile(db_file_name):
        #db_url = "sqlite:///:memory:"
        #return
    count = check_kural_data()
    if count == 1330:
        return

    #with open("app/thirukural.json", encoding='utf-8') as fp:
    with open("thirukural.json", encoding='utf-8') as fp:
        kurrals = json.load(fp)
        for kurral in kurrals['features']:
            kp = kurral['properties']
            session.add(Thirukural(**kp))
        session.commit()
    session.close()

def create_db():
    SQLModel.metadata.create_all(engine)
    load_data(session=Session(engine))
    

@asynccontextmanager
async def lifespan(app=FastAPI):
    create_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(kural_router)
app.include_router(user_router)


app2 = FastAPI(lifespan=lifespan)
app2.include_router(kural_router2)
app2.include_router(user_router2)


'''    
@app.on_event("startup")
async def startup_event():
    print('Server started :', datetime.datetime.now())
    print('Data loading starts ')
    create_db()
    print('Data loading ends ')
    print('Server started :', datetime.datetime.now())
    

@app.on_event("shutdown")
async def shutdown_event():
    print('server Shutdown :', datetime.datetime.now())

'''

'''
@app.get("/")
def hello_world():
    return {'message': 'hello world'}
'''
    
if __name__ == "__main__":
    uvicorn.run("app:app",host='0.0.0.0', port=9090, reload=True)
    uvicorn.run("app:app2",host='0.0.0.0', port=9100, reload=True)
