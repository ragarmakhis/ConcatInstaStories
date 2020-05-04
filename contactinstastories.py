import os
import shutil
import subprocess
import sys

TIME_SEC = '3'
SIZE = '720x1280'  # TODO: Get size from neighboring videos

workDir = baseDir = os.path.join(os.environ['HOME'], 'Pictures')
os.chdir(workDir)
outputFile = sys.argv[-1]
listOfFiles = []
if len(sys.argv) < 3:
    listOfFiles.append(sys.argv[-1])
else:
    listOfFiles.extend(sys.argv[1:-1])
if len(listOfFiles) == 1:
    workDir = os.path.join(workDir, listOfFiles[0])
    os.chdir(workDir)
    listOfFiles = os.listdir(workDir)
    listOfFiles.sort()
listTempFiles = []
for i, item in enumerate(listOfFiles):
    if item[-3:] == 'jpg':
        new_item = item[:-3] + 'mp4'
        subprocess.call(['ffmpeg', '-loop', '1', '-i', item, '-c:v', 'libx264', '-t', TIME_SEC,
                         '-pix_fmt', 'yuv420p', '-s', SIZE, new_item])
        item = new_item
    outputTempFile = outputFile + str(i) + '.ts'
    subprocess.call(['ffmpeg', '-i', item, '-acodec', 'copy', '-vcodec', 'copy',
                     '-vbsf', 'h264_mp4toannexb', '-f', 'mpegts', outputTempFile])
    listTempFiles.append(outputTempFile)

destinationFile = open(outputFile + '.ts', 'wb')
for file in listTempFiles:
    otherFile = open(os.path.join(workDir, file), "rb")
    shutil.copyfileobj(otherFile, destinationFile)
    otherFile.close()
destinationFile.close()

subprocess.call(['ffmpeg', '-i', outputFile + '.ts', '-vcodec', 'copy', '-acodec', 'copy',
                 os.path.join(baseDir, outputFile + '.mp4')])

for item in listTempFiles:
    os.remove(item)
os.remove(outputFile + '.ts')
