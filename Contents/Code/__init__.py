from PMS import *
from PMS.Objects import *
from PMS.Shortcuts import *
import csv

PLUGIN_PREFIX   = "/photos/WebGalleryOfArt"
PLUGIN_DATA     = "catalog.csv"

def Start():
  Plugin.AddPrefixHandler(PLUGIN_PREFIX, TopMenu, "Web Gallery of Art", "icon-default.png", "art-default.jpg")
  Plugin.AddViewGroup("Details", viewMode="InfoList", mediaType="items")
  MediaContainer.title1 = "Web Gallery of Art"
  MediaContainer.content = "Items"
  MediaContainer.art = R("art-default.jpg")

def TopMenu():
  dir = MediaContainer()
  dir.Append(Function(DirectoryItem(GetImages, title="All"), key=None, choice="ALL"))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By Form"), choice="FORM"))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By Type"), choice="TYPE"))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By School"), choice="SCHOOL"))
  dir.Append(Function(DirectoryItem(SectionMenu, title="By Timeline"), choice="TIMELINE"))
  return dir

def SectionMenu(sender, choice):
  dir = MediaContainer()
  reader = csv.DictReader(open(Resource.InternalPath(PLUGIN_DATA), "rb"))
  res = []
  for row in reader:
    if row[choice] not in res: res.append(row[choice])
  res.sort()
  for value in res:
    dir.Append(Function(DirectoryItem(GetImages, title=value), key=choice, choice=value))
  return dir

def GetImages(sender, key, choice):
  dir = MediaContainer(title2=sender.itemTitle)
  reader = csv.DictReader(open(Resource.InternalPath(PLUGIN_DATA), "rb"))
  for row in reader:
    if choice == "ALL" or row[key] == choice:
      dir.Append(PhotoItem(row["URL"].replace("/html/", "/art/").replace(".html", ".jpg"), row["TITLE"].decode("latin-1"), row["ARTIST"].decode("latin-1"), (row["TITLE"]+"\n"+row["ARTIST"]+"\n"+row["DATE"]+" | "+row["TECHNIQUE"]+" | "+row["LOCATION"]).decode("latin-1")))
  return dir
