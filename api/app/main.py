from fastapi import FastAPI, Request
import uvicorn
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from routes.user_route import user_route
from routes.pharmacy_route import pharmacy_route
from routes.product_route import product_route
from routes.inventory_route import inventory_route
from routes.advertisement_route import advertisement_route
from utils.database import session
from utils.settings import Settings

settings = Settings()

app = FastAPI(
    title="PharmaGuide API", 
    description="API for the registration of pharmacies and their products.",
    version="1.0.0",
)

app.include_router(user_route, prefix='/user', tags=['Users'])
app.include_router(pharmacy_route, prefix='/pharmacy', tags=['Pharmacies'])
app.include_router(product_route, prefix='/product', tags=['Products'])
app.include_router(inventory_route, prefix='/inventory', tags=['Inventories'])
app.include_router(advertisement_route, prefix='/advertisement', tags=['Advertisements'])
app.mount('/static', StaticFiles(directory='static'), name='static')
templates = Jinja2Templates(directory='templates')

@app.get('/')
async def home(request : Request):
    return templates.TemplateResponse('index.html', { 'request' : request })

@app.on_event("shutdown")
def shutdown_event():
    session.close()

if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        reload=settings.DEBUG,
        port=settings.PORT
  )
