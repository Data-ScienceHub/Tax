from starlette.middleware import Middleware
from starlette.middleware.base import BaseHTTPMiddleware
import pymongo
import ssl

class DatabaseMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
      client = pymongo.MongoClient("mongodb+srv://DS6013_Students_Rachel:DS6013_Students_RG@countyrecords.4cdfgz2.mongodb.net/test")
      db = client["TaxRecords"]
      request.state.db = db
      response = await call_next(request)
      return response

middleware = [
  Middleware(DatabaseMiddleware)
]