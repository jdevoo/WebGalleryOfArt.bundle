import csv, string, StringIO

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
  oc.add(DirectoryObject(key=Callback(AlphaMenu), title=Locale.LocalString('AUTHOR')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='FORM'), title=Locale.LocalString('FORM'), summary=Locale.LocalString('database')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='TYPE'), title=Locale.LocalString('TYPE'), summary=Locale.LocalString('database')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='SCHOOL'), title=Locale.LocalString('SCHOOL'), summary=Locale.LocalString('database')))
  oc.add(DirectoryObject(key=Callback(SectionMenu, choice='TIMELINE'), title=Locale.LocalString('TIMELINE'), summary=Locale.LocalString('database')))
  oc.add(InputDirectoryObject(key=Callback(SearchMenu), title=Locale.LocalString('search'), prompt=Locale.LocalString('search_desc')))
  return oc

def AlphaMenu():
  oc = ObjectContainer(view_group='InfoList', title2=Locale.LocalString('first_letter'))
  for letter in list(string.ascii_uppercase):
    oc.add(DirectoryObject(key=Callback(SectionMenu, choice=letter), title=letter))
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
      if row[LOOKUP[choice]].encode('latin-1') not in res:
        key = row[LOOKUP[choice]].encode('latin-1')
        res.append(key)
        deco[key] = [
          row[LOOKUP['URL']].replace('/html/', '/art/').replace('.html', '.jpg'),
          row[LOOKUP['URL']].replace('/html/', '/preview/').replace('.html', '.jpg')
        ]
  else:
    for row in data:
      if row[LOOKUP['AUTHOR']][0] == choice and row[LOOKUP['AUTHOR']].encode('latin-1') not in res:
        key = row[LOOKUP['AUTHOR']].encode('latin-1')
        res.append(key)
        deco[key] = [
          row[LOOKUP['URL']].replace('/html/', '/art/').replace('.html', '.jpg'),
          row[LOOKUP['URL']].replace('/html/', '/preview/').replace('.html', '.jpg')
        ]
    choice = 'AUTHOR'
  res.sort()
  for value in res:
    oc.add(DirectoryObject(key=Callback(GetImages, key=choice, choice=value), title=string.capwords(value.decode('latin-1')), art=deco[value][0], thumb=deco[value][1]))
  return oc

def SearchMenu(query):
  oc = ObjectContainer(view_group='InfoList', title2=query)
  handle = StringIO.StringIO(Resource.Load(PLUGIN_DATA, binary=True))
  data = csv.reader(handle)
  data.next()
  res = []
  for row in data:
    if (row[LOOKUP['AUTHOR']].lower().find(query.lower()) != -1 or row[LOOKUP['TITLE']].lower().find(query.lower()) != -1) and \
      row[LOOKUP['AUTHOR']] not in res:
      res.append(row[LOOKUP['AUTHOR']].encode('latin-1'))
  res.sort()
  for value in res:
    oc.add(DirectoryObject(key=Callback(GetImages, key='AUTHOR', choice=value), title=string.capwords(value.decode('latin-1'))))
  return oc

def GetImages(key, choice):
  oc = ObjectContainer(view_group='InfoList', title2=choice.decode('latin-1'))
  handle = StringIO.StringIO(Resource.Load(PLUGIN_DATA, binary=True))
  data = csv.reader(handle)
  data.next()
  for row in data:
    if row[LOOKUP[key]].encode('latin-1') == choice:
      oc.add(PhotoObject(
        key=row[LOOKUP['URL']].replace('/html/', '/art/').replace('.html', '.jpg'),
        rating_key=key,
        title=row[LOOKUP['TITLE']],
        summary=row[LOOKUP['TITLE']]+'\n'+row[LOOKUP['AUTHOR']]+'\n'+row[LOOKUP['DATE']]+' | '+row[LOOKUP['TECHNIQUE']]+' | '+row[LOOKUP['LOCATION']],
        thumb=row[LOOKUP['URL']].replace('/html/', '/preview/').replace('.html', '.jpg'),
      ))
  return oc

