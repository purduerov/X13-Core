Untracked: 
    yeet
    hist
    lightspeed 
    tester
    photomosaics
    vid_streamer


Algo:
test3 is baseline 
tolerance adds tolerance to projections
invert better captures tolerance around nan slopes due to numpy vectorizing flaw, redid ortho project in an important way
area has smarter rectangle selection
vid is the video tool

For best results: don't be obnoxious. It's a very specific task, so take a very specific photo.
	As straight on as possible, capturing ideally only the CV target, and it should do the rest.
	It can handle quite a bit of noise, but if you start feeding in bad photos you're going 
	to get bad results. 

There are tons of helper functions and commented out points for you to observe what's happening. Use them before you ask me.
    Especially the ones in show_desired_rect, operate, and get_lines. GLHF

Orthodemo and Parademo were proof of concepts to show to the midterm design review

NN:
split: splits the video into image frames
a.bash: deletes every other .jpg in a folder; adjacent frames are too similar, doesn't help in training an ai
fix: after using https://github.com/tzutalin/labelImg to label images I accidentally reran split, so I made this file to delete every image that I didn't label
show: shows me the bounding box on an image to make sure I'm not an idiot
nn: a baby nn I used just to see how it would do. Harsh truths:
    Needs more variety of training data. It converges way too quickly since adjacent frames 
    in each batch are too similar; I should bind images and bounding boxes to a custom generator
    so I can randomize it, and then add in duplicate frames that have been rotated or transposed.
    That being said, it didn't show enough promise to make me think this extra effort was worth it,
    but maybe I can throw a freshman at it to do my dirty work for me + teach them how to build a nn. 



rov ffserver.conf:

HTTPPort 8090
HTTPBindAddress 0.0.0.0
MaxHTTPConnections 100
MaxClients 50
MaxBandwidth 10000000

<Feed cam0.ffm>
File /tmp/cam0.ffm
FileMaxSize 15M
Launch ./ffmpeg -input_format mjpeg -i /dev/video2 -c:v copy -override_ffserver
</Feed>

<Feed cam1.ffm>
File /tmp/cam1.ffm
FileMaxSize 15M
Launch ./ffmpeg -input_format mjpeg -i /dev/video0 -c:v copy -override_ffserver
</Feed>

<Stream cam0>
Feed cam0.ffm
Format mpjpeg
VideoSize 1920x1080
VideoFrameRate 30
VideoBitRate 20000
VideoQMin 1
VideoQMax 10
NoAudio
</Stream>

<Stream cam1>
Feed cam1.ffm
Format mpjpeg
VideoSize 1920x1080
VideoFrameRate 30
VideoBitRate 20000
VideoQMin 1
VideoQMax 10
NoAudio
</Stream>

<Stream status>
Format status
</Stream>






HTTPPort 8090
HTTPBindAddress 0.0.0.0
MaxHTTPConnections 2000
MaxClients 1000
MaxBandwidth 100000

<Feed streamwebm.ffm>
  File /tmp/streamwebm.ffm
  FileMaxSize 50M
</Feed>

<Stream streamwebm>
#in command line run : ffmpeg -i yourvideo.mp4 -c:v libvpx -cpu-used 4 -threads 8    http://localhost:8090/streamwebm.ffm
Feed streamwebm.ffm
Format webm

VideoFrameRate 30
VideoSize 624x368

MaxTime 0

</Stream>


<Feed streamflv.ffm>
  File /tmp/streamflv.ffm
  FileMaxSize 50M
</Feed>

<Stream streamflv>
  Feed streamflv.ffm
  Format flv

  VideoCodec libx264
  VideoFrameRate 30
  VideoSize 640x360
  VideoBitRate 1000

  MaxTime 0
</Stream>

<Stream stat.html>
  Format status
</Stream>

