import csv, string, StringIO, unicodedata

PLUGIN_PREFIX = '/photos/wga'
PLUGIN_DATA = 'catalog.csv'
PLUGIN_NAME = 'Web Gallery Of Art'
LOOKUP = {
  'AUTHOR': 0, 'BORN-DIED': 1, 'TITLE': 2, 'DATE': 3, 'TECHNIQUE': 4,
  'LOCATION': 5, 'URL': 6, 'FORM': 7, 'TYPE': 8, 'SCHOOL': 9, 'TIMELINE': 10
}

def Start():
  Plugin.AddViewGroup('InfoList', viewMode='InfoList', mediaType='items')

@handler(PLUGIN_PREFIX, PLUGIN_NAME)
def TopMenu():
  oc = ObjectContainer(view_group='InfoList')
  oc.add(DirectoryObject(key=Callback(AlphaMenu), title=Locale.LocalString('AUTHOR'), summary=Locale.LocalString('database')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='FORM'), title=Locale.LocalString('FORM'), summary=Locale.LocalString('database')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='TYPE'), title=Locale.LocalString('TYPE'), summary=Locale.LocalString('database')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='SCHOOL'), title=Locale.LocalString('SCHOOL'), summary=Locale.LocalString('database')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='TIMELINE'), title=Locale.LocalString('TIMELINE'), summary=Locale.LocalString('database')))
  oc.add(InputDirectoryObject(key=Callback(SearchMenu), title=Locale.LocalString('search'), prompt=Locale.LocalString('search_desc'), summary=Locale.LocalString('database')))
  return oc

def AlphaMenu():
  oc = ObjectContainer(view_group='InfoList', title2=Locale.LocalString('first_letter'))
  for letter in list(string.ascii_uppercase):
    oc.add(DirectoryObject(key=Callback(SectionMenu, choice=letter), title=letter, summary=Locale.LocalString('database')))
  return oc

def SectionMenu(choice):
  if len(choice) > 1:
    title = Locale.LocalString(choice)
  else:
    title = Locale.LocalString('first_letter')+' '+choice
  oc = ObjectContainer(view_group='InfoList', title2=title)
  handle = StringIO.StringIO(Resource.Load(PLUGIN_DATA, binary=True))
  data = csv.reader(handle)
  data.next()
  res = []
  deco = {}
  if len(choice) > 1:
    for row in data:
      if row[LOOKUP[choice]] not in res:
        key = row[LOOKUP[choice]]
        res.append(key)
        deco[key] = [
          row[LOOKUP['URL']].replace('/html/', '/art/').replace('.html', '.jpg'),
          row[LOOKUP['URL']].replace('/html/', '/preview/').replace('.html', '.jpg')
        ]
  else:
    for row in data:
      if row[LOOKUP['AUTHOR']][0] == choice and row[LOOKUP['AUTHOR']] not in res:
        key = row[LOOKUP['AUTHOR']]
        res.append(key)
        deco[key] = [
          row[LOOKUP['URL']].replace('/html/', '/art/').replace('.html', '.jpg'),
          row[LOOKUP['URL']].replace('/html/', '/preview/').replace('.html', '.jpg')
        ]
    choice = 'AUTHOR'
  res.sort()
  for value in res:
    oc.add(DirectoryObject(key=Callback(GetImages, key=choice, choice=value), title=value.decode('utf-8').title(), art=deco[value][0], thumb=deco[value][1], summary=Locale.LocalString('database')))
  return oc

def SearchMenu(query):
  oc = ObjectContainer(view_group='InfoList', title2=query)
  handle = StringIO.StringIO(Resource.Load(PLUGIN_DATA, binary=True))
  data = csv.reader(handle)
  data.next()
  res = []
  for row in data:
    plain_author = lower_no_accents(row[LOOKUP['AUTHOR']])
    plain_title = lower_no_accents(row[LOOKUP['TITLE']])
    if (plain_author.find(query.lower()) != -1 or plain_title.find(query.lower()) != -1) and row[LOOKUP['AUTHOR']] not in res:
      res.append(row[LOOKUP['AUTHOR']])
  res.sort()
  for value in res:
    oc.add(DirectoryObject(key=Callback(GetImages, key='AUTHOR', choice=value), title=value.decode('utf-8').title(), summary=Locale.LocalString('database')))
  return oc

def lower_no_accents(input_str):
  nfkd_form = unicodedata.normalize('NFKD', input_str.decode('utf-8'))
  return ''.join(c for c in nfkd_form if not unicodedata.combining(c)).lower()

def GetImages(key, choice):
  oc = ObjectContainer(view_group='InfoList', title2=choice)
  handle = StringIO.StringIO(Resource.Load(PLUGIN_DATA, binary=True))
  data = csv.reader(handle)
  data.next()
  for row in data:
    if row[LOOKUP[key]] == choice:
      oc.add(PhotoObject(
        key=row[LOOKUP['URL']].replace('/html/', '/art/').replace('.html', '.jpg'),
        rating_key=key,
        title=row[LOOKUP['TITLE']],
        summary=row[LOOKUP['TITLE']]+'\n'+row[LOOKUP['AUTHOR']]+'\n'+row[LOOKUP['DATE']]+' | '+row[LOOKUP['TECHNIQUE']]+' | '+row[LOOKUP['LOCATION']],
        thumb=row[LOOKUP['URL']].replace('/html/', '/preview/').replace('.html', '.jpg'),
      ))
  return oc

