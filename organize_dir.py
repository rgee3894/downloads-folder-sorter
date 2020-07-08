# A program that organizes files of a specified directory (Downloads folder by default)
# into subdirectories


import shutil
import sys
import os
import argparse
import string

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
  "Other Folders":[]
}

def search_dir(ext):
  for k, v in fileTypeDict.items():
    if(ext in v):
      return k
  return "Others"

def make_dirs(path):
  for dir_name in fileTypeDict.keys():
    dir_path = os.path.join(path,dir_name)
    if (not os.path.isdir(dir_path)): os.mkdir(dir_path)

def organize_files(path):
  subdirs = list(fileTypeDict.keys())
  for entry in os.scandir(path):

    #Get path of source file/dir (C:/Users/user/Downloads/file.ext) to be moved
    src_path = entry.path

    #Get _ (C:/Users/user/Downloads/file) and ext (.ext)
    _, ext = os.path.splitext(src_path)

    #Get filename (file.ext)
    basename = os.path.basename(src_path)
    # print(basename)

    #If the basename is a file called 'desktop.ini' (This file should NOT be moved)
    #Or if the basename is one of the made subdirectories, skip it.
    if((basename.lower()=='desktop.ini') or basename in subdirs): continue

    #Get directory to put the file/dir into based on its extension
    dest_dir = search_dir(ext)

    #If it's a dir
    if(os.path.isdir(entry)):
      dest_dir = "Other Folders"
    #Else if it's a file
    else:
      existing_file_path = os.path.join(path,dest_dir,basename)
      #If a file already exists in the destination path
      if(os.path.isfile(existing_file_path)):
        #Rename the file such that it has '-Copy-' in its filename
        dest_dir = os.path.join(dest_dir,''.join([basename,'-Copy-',ext]))

    #Create destination path
    dest_path = os.path.join(path,dest_dir)
    print("From {} to {}".format(src_path,dest_path))

    shutil.move(src_path,dest_path)


def main():
  ag = argparse.ArgumentParser('Parser for directory to organize files in',)
  ag.add_argument('--path', help='Path of directory to organize the files in', type=str, default="C:/Users/Rgee/Downloads")
  args = ag.parse_args()

  dir_path = args.path

  if(not os.path.isdir(dir_path)): raise Exception('Path specified is not a directory')

  make_dirs(dir_path)
  organize_files(dir_path)



if __name__ == "__main__":
  main()