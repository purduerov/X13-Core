To run a proper test feed: 
  on one terminal, run: ffserver -f /etc/ffserver.conf 
  on the other, run: ffmpeg -i <./path/to/.mp4> -c:v libvpx -cpu-used 4 -threads 8 http://localhost:8090/stream.ffm
  This throws up a camera feed from an old video that you may now consume

    
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

yeet:
  idk honestly something I tried with contouring 

photomosaics:
  my starting take on Hunter's work
  tester: test driver


hist:
  puts pixel values into a histogram, makes a palette out of the most occurring colors, then 
  quantizes all other colors into these on a frame 
  based on an idea from scott 
  very naive; to demonstrate:   
    say I have 6 common frequencies 
    I'm looking for 4 colors so I quant down to 4 
    3 of my most frequent colors are shades of blue 
    congrats you just turned the picture mostly blue 
  additionally:
    these frequencies are [r,g,b], so adjacent pixels may differ a lot, and your results may be a little nonsensical 
    to fix it should be done in a continuous color spectra 


dynamic_quant:
  ^^ but less naive; however it's unuseably slow. much optimization would be needed to work 
  it uses HSV since hue is a continuous [0,360] spectra 
  instead of choosing the most frequent colors, it chooses local maxima of frequencies; to demonstrate:
    if there are 4 blues but one blue is most common, then 6 reds and one is most common, all of which are 
      together in a list, and I'm looking for 2 maxima, ideally it should choose one blue and one red 
        (I said less naive, not infallible) 
  since the reassignment of hues to this palette of maxima colors is manual and in python, it's ludicrously slow 
  all of the runtime is spent in the quantize function 
  GLHF 

the_one_algo_to_rule_them_all:
  I hate how simple it is, but it works very consistently. Some of these ideas are Hunter's from photomosaics.py. 


rov ffserver.conf for reference:

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




my ffserver.conf: 

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

