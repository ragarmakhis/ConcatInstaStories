import os
import shutil
import sys

import ffmpeg

TIME_SEC = '3'
SIZE = '720x1280'

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
for item in listOfFiles:
    if item[-3:] == 'mp4':
        probe = ffmpeg.probe(item)
        video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        width = str(video_stream['width'])
        height = str(video_stream['height'])
        SIZE = width + 'x' + height
        break
listTempFiles = []
for i, item in enumerate(listOfFiles):
    if item[-3:] == 'jpg':
        new_item = item[:-3] + 'mp4'
        (
            ffmpeg
            .input(item, loop='1')
            .output(new_item, vcodec='libx264', t=TIME_SEC, pix_fmt='yuv420p', s=SIZE)
            .run()
        )
        item = new_item
    outputTempFile = outputFile + str(i) + '.ts'
    (
        ffmpeg
        .input(item)
        .output(outputTempFile, vcodec='copy', acodec='copy', vbsf='h264_mp4toannexb', f='mpegts')
        .run()
    )
    listTempFiles.append(outputTempFile)

destinationFile = open(outputFile + '.ts', 'wb')
for file in listTempFiles:
    otherFile = open(os.path.join(workDir, file), "rb")
    shutil.copyfileobj(otherFile, destinationFile)
    otherFile.close()
destinationFile.close()

(
    ffmpeg
    .input(outputFile + '.ts')
    .output(os.path.join(baseDir, outputFile + '.mp4'), vcodec='copy', acodec='copy')
    .run()
)

for item in listTempFiles:
    os.remove(item)
os.remove(outputFile + '.ts')
