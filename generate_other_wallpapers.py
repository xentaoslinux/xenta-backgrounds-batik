#!/usr/bin/python2

import os, commands, sys

class Wallpaper:
	def __init__ (self, name):
		self.name = name
		self.filename = None
		self.artist = None

CODENAME = "Arok"
wallpapers = []

# MAKE GNOME/MATE Wallpapers
os.system("sed \"s/cinnamon-wp/gnome-wp/\" cinnamon-background-properties/xentaos-%s.xml > gnome-background-properties/xentaos-%s.xml" % (CODENAME.lower(), CODENAME.lower()))
os.system("sed \"s/cinnamon-wp/mate-wp/\" cinnamon-background-properties/xentaos-%s.xml > mate-background-properties/xentaos-%s.xml" % (CODENAME.lower(), CODENAME.lower()))

#MAKE Xfce Wallpapers
os.chdir("xfce4-backdrops")
os.system("rm -f *")
os.system("ln -s /usr/share/backgrounds/xentaos-%s/*.* ./" % CODENAME.lower())
os.system("rename 's/^/%s_/' *" % CODENAME.lower())
os.chdir("..")

# MAKE KDE Wallpapers
with open ("cinnamon-background-properties/xentaos-%s.xml" % CODENAME.lower(), "r") as metadata_file:
	for line in metadata_file:
		line = line.strip()
		if line.startswith("<name>"):
			name = line.replace("<name>", "").replace("</name>", "")
			wallpaper = Wallpaper(name)
			wallpapers.append(wallpaper)
		elif line.startswith("<filename>"):
			wallpaper.filename = line.replace("<filename>", "").replace("</filename>", "")
		elif line.startswith("<artist>"):
			wallpaper.artist = line.replace("<artist>", "").replace("</artist>", "")

os.system("rm -rf kde-wallpapers/*")
os.chdir("kde-wallpapers")
for wallpaper in wallpapers:
	print "WALL: ", wallpaper.name
	os.system("mkdir -p '%s %s'/contents/images" % (wallpaper.name, CODENAME))
	os.system("convert %s -resize 400x250 '%s %s'/contents/screenshot.jpg" % (wallpaper.filename, wallpaper.name, CODENAME))
	dimensions = commands.getoutput("identify %s | awk {'print $3'}" % wallpaper.filename)
	if not "x" in dimensions:
		print "Erroneous dimensions: %s for %s" % (dimensions, wallpaper.filename)
		sys.exit(1)
	suffix = "jpg"
	if (wallpaper.filename.endswith(".png")):
		suffix = "png"
	os.system("ln -s %s '%s %s'/contents/images/%s.%s" % (wallpaper.filename, wallpaper.name, CODENAME, dimensions, suffix))
	os.system("sed \"s/NAME/%s/g; s/ARTIST/%s/g\" ../kde-desktop.template > '%s %s/metadata.desktop'" % (wallpaper.name, wallpaper.artist, wallpaper.name, CODENAME))
