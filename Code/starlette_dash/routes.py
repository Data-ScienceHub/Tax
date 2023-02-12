from starlette.templating import Jinja2Templates
from models import PropTax

templates = Jinja2Templates(directory='templates')

async def homepage(request):
  data = request.state.db.Fluvanna.find({'_id':{'$exists': True}}, limit=15)

  response = []

  for doc in data:
    response.append(
      PropTax(
      doc['_id'],
      doc['County'],
      doc['Year'],
      doc['District'],
      doc['Surname'],
      doc['First Name(s)'],
      doc['Prefix Title or Suffix'],
      doc['Free Negro Notation (FN)'],
      doc['Person A'],
      doc['Source'],
      doc['Event'],
      doc['Role A']
      )
    ) 

  return templates.TemplateResponse('index.html', {'request': request, 'response': response})

async def listing(request):
  return templates.TemplateResponse('listing.html', {'request': request})

async def confirmation(request):
  return templates.TemplateResponse('confirmation.html', {'request': request})