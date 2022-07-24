#! /usr/bin/python3
from PIL import Image
import os
import sys
import errno

def drawProgressBar(percent, barLen = 20):
    # percent float from 0 to 1.
    sys.stdout.write("\r")
    sys.stdout.write("[{:<{}}] {:.0f}%".format("=" * int(barLen * percent), barLen, percent * 100))
    sys.stdout.flush()

def createPath(dirToBeCreated):
    if not os.path.exists(os.path.dirname(dirToBeCreated)):
        try:
            os.makedirs(os.path.dirname(dirToBeCreated))
        except OSError as exc: # Guard against race condition
            if exc.errno != errno.EEXIST:
                raise

if(len(sys.argv) < 2):
    print("Please provide source path")
    exit(errno.EFAULT)

sourceDir = sys.argv[1]
destPath = sourceDir + "../" + list(filter(None, sourceDir.split('/')))[-1] + "Compressed/"
createPath(destPath)
total_files = len([name for name in os.listdir(sourceDir) if os.path.isfile(os.path.join(sourceDir, name))])
i = 1
#Iterating Recursively through the source path
for root, dirs, files in os.walk(sourceDir):
    for file in files:
        img_path = os.path.abspath(os.path.join(root, file))
        try:
            image = Image.open(img_path)
            size = os.path.getsize(img_path)
            qual = int((1024/size) * 100)
            # Preserve exif Data
            exif = image.info['exif']
            image.save(destPath + file,quality=qual,optimize=True, exif=exif)
        except Exception as e:
            sys.stdout.write("\r" + "  "*30)
            sys.stdout.flush()
            print("\n" + str(e))
        drawProgressBar(i/total_files)
        i += 1
print("\nFinished...!!!")