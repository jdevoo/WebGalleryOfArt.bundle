from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
import csv, string

PLUGIN_PREFIX = "/photos/webgalleryofart_r2"
PLUGIN_DATA   = "catalog.csv"

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, TopMenu, "Web Gallery Of Art", "icon-default.png", "art-default.png")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = "Web Gallery Of Art"
  MediaContainer.content = "Items"
  MediaContainer.art = R("art-default.png")

def TopMenu():
  dir = MediaContainer()
  dir.Append(Function(DirectoryItem(AlphaMenu, title="By Artist")))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By Form"), choice="FORM"))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By Type"), choice="TYPE"))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By School"), choice="SCHOOL"))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By Timeline"), choice="TIMELINE"))
  dir.Append(Function(SearchDirectoryItem(SearchMenu, title="Search...", prompt="Search Artist and Title")))
  return dir

def AlphaMenu(sender):
  dir = MediaContainer()
  for letter in map(chr, range(65, 91)):
    dir.Append(Function(DirectoryItem(SectionMenu, title=letter), choice=letter))
  return dir

def SectionMenu(sender, choice):
  dir = MediaContainer(title2=sender.itemTitle)
  reader = csv.DictReader(open("%s/%s" % (Resource.__resourcePath, PLUGIN_DATA), "rb"))
  res = []
  if len(choice) > 1:
    for row in reader:
      if row[choice] not in res: res.append(row[choice])
  else:
    for row in reader:
      if row["ARTIST"][0] == choice and row["ARTIST"] not in res: res.append(row["ARTIST"])
    choice = "ARTIST"
  res.sort()
  for value in res:
    dir.Append(Function(DirectoryItem(GetImages, title=string.capwords(value).decode("latin-1")), key=choice, choice=value))
  return dir

def SearchMenu(sender, query):
  dir = MediaContainer(title2=query)
  reader = csv.DictReader(open("%s/%s" % (Resource.__resourcePath, PLUGIN_DATA), "rb"))
  res = []
  for row in reader:
    if (row["ARTIST"].lower().find(query.lower()) != -1 or row["TITLE"].lower().find(query.lower()) != -1) and row["ARTIST"] not in res: res.append(row["ARTIST"])
  res.sort()
  for value in res:
    dir.Append(Function(DirectoryItem(GetImages, title=string.capwords(value).decode("latin-1")), key="ARTIST", choice=value))
  return dir

def GetImages(sender, key, choice):
  dir = MediaContainer(title2=sender.itemTitle)
  reader = csv.DictReader(open("%s/%s" % (Resource.__resourcePath, PLUGIN_DATA), "rb"))
  for row in reader:
    if row[key] == choice:
      dir.Append(PhotoItem(row["URL"].replace("/html/", "/art/").replace(".html", ".jpg"), row["TITLE"].decode("latin-1"), row["ARTIST"].decode("latin-1"), (row["TITLE"]+"\n"+row["ARTIST"]+"\n"+row["DATE"]+" | "+row["TECHNIQUE"]+" | "+row["LOCATION"]).decode("latin-1")))
  return dir
