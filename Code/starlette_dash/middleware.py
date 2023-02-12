from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import pymongo
import ssl

class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
      client = pymongo.MongoClient("mongodb+srv://racheltreene:Rgftw2000!@cluster0.uwoettr.mongodb.net/test")
      db = client["onesharedstory"]
      request.state.db = db
      response = await call_next(request)
      return response

middleware = [
  Middleware(DatabaseMiddleware)
]