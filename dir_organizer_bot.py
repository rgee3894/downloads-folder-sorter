from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from watchdog.events import LoggingEventHandler
import shutil
import sys
import logging

import os
import json
import time
from pathlib import Path 

fileTypeDict = {
  "Audio":['.mp3','.wav','.wma','.ogg','.mdi'],
  "Images":['.ai','.jpg', '.jpeg', '.png', '.psd', '.svg', '.gif', '.tif','.tiff', '.ico', '.bmp','.webp'],
  "Videos":['.3g2', '.3gp', '.avi', '.flv', '.h264', '.m4v', '.mkv', '.mov', '.mp4', '.mpg', '.mpeg', '.rm', '.swf', '.vob', '.wmv'],
  "Zipped Files":['.7z', '.arj', '.rar', '.deb', '.pkg', '.rpm', '.tar.gz', '.z', '.zip'],
  "Disc Files":['.bin', '.dmg', '.iso', '.toast', '.vcd'],
  "Database Files":['.dat', '.db', '.dbf', '.log', '.mdb', '.sav', '.sql', '.tar', '.xml'],
  "Executables":['.apk', '.bat', '.bin', '.com', '.exe', '.gadget', '.jar', '.wsf','.msi'],
  "Fonts":['.fnt', '.fon', '.otf', '.ttf'],
  "Web Files":['.asp', '.aspx', '.cer', '.cgi', '.pl', '.css', '.xhtml', '.html', '.htm','.js', '.jsp', '.part','.php','.rss'],
  "Programming Files":['.py', '.c', '.cpp', '.class', '.java', '.cs', '.h', '.sh', '.swift', '.vb'],
  "Presentation Slides":['.ppt', '.key', '.pps', '.pptx', '.odp'],
  "Spreadsheets":['.ods', '.xlr', '.xls', '.xlsx', '.csv'],
  "Documents":['.doc', '.docx', '.odt', '.pdf', '.rtf', '.tex', '.txt', '.wks', '.wps', '.wpd'],
  "Others":[],
}

tempFileExts = {'.tmp', '.crdownload'}


def search_dir(ext):
  for k, v in fileTypeDict.items():
    if(ext in v):
      return k
  return "Others"


class FolderOrganizer(FileSystemEventHandler):
  def on_any_event(self, event):
    print('{}:{}'.format(event.src_path,event.event_type))
  def on_modified(self, event):
    #Get source path of file to be transferred.
    src_path = event.src_path

    #Get file extension
    _, file_ext = os.path.splitext(src_path)

    #Get basename
    basename = os.path.basename(src_path)

    #Get directory to put the file/dir into based on its extension
    dest_dir = search_dir(file_ext)

    #Ignore if the source path is a folder or temporary file (i.e. .CRDOWNLOAD, .tmp)
    if(os.path.isdir(src_path) or (file_ext in tempFileExts)):
      print("Error: Directory or temp file: {}".format(src_path))
      return 

    #If the folder does not exist yet, make it.
    if(not os.path.isdir(os.path.join(path,dest_dir))):
      os.mkdir(os.path.join(path,dest_dir))

    #Creat new destination path
    new_dest_path = os.path.join(path,dest_dir)
    print('{} to {}'.format(src_path,new_dest_path))

    existing_file_path = os.path.join(path,dest_dir,basename)

    #If new destination path does not exist, move it.
    if(not os.path.isfile(existing_file_path)):
      shutil.move(src_path,new_dest_path)
    #Else, move it but as a copy
    else:
      new_dest_path = os.path.join(new_dest_path,''.join([basename,'-Copy-',file_ext]))
      shutil.move(src_path,new_dest_path)

def main():
  print("Running Downloads Folder Organizer Bot..")
  event_handler = FolderOrganizer()
  observer = Observer()
  observer.schedule(event_handler, path, recursive=True)
  observer.start()
  try:
      while True:
          time.sleep(1)
  except KeyboardInterrupt:
      observer.stop()
  observer.join()

if __name__ == "__main__":
  path = "C:/Users/Rgee/Downloads"
  main()
  
