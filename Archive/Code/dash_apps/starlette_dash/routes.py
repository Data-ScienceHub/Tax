from starlette.templating import Jinja2Templates
from starlette.responses import JSONResponse
from models import Record1782

templates = Jinja2Templates(directory='templates')

async def myquery(request):
  data = request.state.db.Tax_Record_1782.find({'_id':{'$exists': True}}, limit=1000)

  response = []

  for doc in data:
    response.append(
      Record1782(
      doc['_id'],
      doc['SourceSteward'],
      doc['SourceLocCity'],
      doc['SourceLocState'],
      doc['SourceTitle']
      )
    ) 

  return templates.TemplateResponse('index.html', {'request': request, 'response': response})

async def confirmation(request):
  return templates.TemplateResponse('confirmation.html', {'request': request})