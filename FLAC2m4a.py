#!/usr/bin/python
# my first from scratch personal python program!
# It's supposed to find all of my FLAC files and convert them
# to lossless alac files and it's going to be awesome.

""" the command to convert the files is:

  from http://tech.moosaico.com/blog/2012/05/15/audio-conversion-between-flac-and-alac-in-ubuntu/

  avconv -i audio.flac -acodec alac audio.m4a
  avconv -i audio.m4a -acodec flac audio.flac

  e.g.
  avconv -i 7.\ Flying\ Whales.flac -acodec alac 
  /media/ServyData/steve/m4a/Gojira/From\ Mars\ To\ Sirius//7.\ Flying\ Whales.m4a
"""

import os
import time
import re
import sys
import commands
import subprocess

#  Build a list of the files to convert (and leave out the 
#  ones which can be skipped.  
def find_files_to_convert(source_dir):
  files_to_convert = {}
  source_artists = os.listdir(source_dir)
  for artist in source_artists:
    artist_path = os.path.join(source_dir, artist)
    if os.path.isdir(artist_path) == True:
      source_albums = os.listdir(artist_path)
      for album in source_albums:
        album_path = os.path.join(artist_path, album)
        if os.path.isdir(album_path) == True:
          source_files = os.listdir(album_path) 
          # Assuming that all of our flac files end in .flac
          #
          for song in source_files:
            match = re.search(r'\.flac', song)
            if match:
              dest_dir = album_path.replace("FLAC","m4a")
              dest_file = song.replace("flac","m4a")
  
              cmd_source_file = os.path.join(album_path, song)

              cmd_dest_file = os.path.join(dest_dir, dest_file)

              # check to see if the dest dirs exist and create them 
              # if they don't
              if not os.path.exists(dest_dir):
                print "creating directory: " + dest_dir
                os.makedirs(dest_dir)

              # Check to see if the destination file exists
              # if it doesn't then add to the convert list
              if not os.path.exists(cmd_dest_file):
                files_to_convert[cmd_source_file] = cmd_dest_file
                print "Cannot find dest file, adding to list: " + cmd_source_file
              else:
                # Check to see if the source file is newer than 
                # the destination file
                if ((os.path.getmtime(cmd_source_file)) > (os.path.getmtime(cmd_dest_file))):
                  files_to_convert[cmd_source_file] = cmd_dest_file
                  print "Source file: " + cmd_source_file + ": " + (str(os.path.getmtime(cmd_source_file)))
                  print "Destination file: " + cmd_dest_file + ": " + (str(os.path.getmtime(cmd_dest_file)))
                  print "Source file is newer, adding to list: " + cmd_source_file
                  print "Removing destination file: " + cmd_dest_file
                  os.remove(cmd_dest_file)

    # print files_to_convert
    # would be nice to put a check in here to provide some info
    # see http://stackoverflow.com/questions/12165735/how-to-refer-to-empty-dict-value-in-python
    # if files_to_convert == {}
    # print "No new FLAC files to convert."
    # MAINT would be nice to sort these guys, but this isn't working with the 
    # for loop below
    # return sorted(files_to_convert)
  return files_to_convert



def convert_files(files_to_convert):
  for source_file in files_to_convert:
    dest_file = files_to_convert[source_file]

    # from dperttula @ https://github.com/drewp/photo/blob/master/mediaresource.py#L177
    # Need to read this at some point:
    #   http://jimmyg.org/blog/2009/working-with-python-subprocess.html
    # Possibly also this:
    #   http://stackoverflow.com/questions/1007855/popen-and-python
    
    # convert = subprocess.Popen(['ls', source_file, '-la'], shell=False)
    # this is all of the business right here vvvv
    convert = subprocess.Popen(['avconv', '-i', source_file,  '-acodec', 'alac', dest_file], shell=False)
    # MAINT gonna use wait instead of poll because to keep it from mega threading until
    # i get that figured out later
    convert.wait()
    # print convert.returncode

  
def main():

  # Making a list of the command line arguments, other than the [0] element
  args = sys.argv[1:]

  if not args:
    # print 'usage: [--sourcepath] path_to_source_FLAC [--destpath] path_to_desired_m4a'
    print 'usage: [--source_path] path_to_source_FLAC'
    sys.exit[1:]

  # Look for the source_path flag and pull it from args if found
  if args[0] == '--source_path':
    del args[0]
    source_path = args[0]

  # Look for the dest_path flag and pull it from args if found
  # if args[0] == '--dest_path':
    # del args[0]
    # dest_path = args[0]


  # source_path = '/home/steve/Scripts/FLAC2m4a/test/data/FLAC/'
  # source_path = '/media/ServyData/sxb/FLAC/'
  
  # Find the source files which are newer than the dest files
  files_to_convert = find_files_to_convert(source_path)
  # Convert them
  convert_files(files_to_convert)

if __name__ == '__main__':
  main()

