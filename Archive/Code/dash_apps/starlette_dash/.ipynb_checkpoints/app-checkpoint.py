from starlette.applications import Starlette
from starlette.routing import Route
from starlette.responses import PlainTextResponse

async def homepage(request):
  return PlainTextResponse("Hello from Starlette")

app = Starlette(debug=True, routes=[
    Route('/', homepage),
])