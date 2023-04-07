from starlette.applications import Starlette
from starlette.routing import Route
from middleware import middleware
from routes import myquery, confirmation

app = Starlette(debug=True, routes=[
  Route('/', myquery),
  Route('/confirmation/{id}', confirmation),
], middleware=middleware)