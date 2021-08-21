# X13-Core
Codebase for the the X13 version of the ROV

Software Versions
Ubuntu 18
Raspbian Buster
ROS Melodic

Hardware
Raspberry Pi 4


## Philosophy ##
We designed the comms interfaces between front end and backend to include potential for CV in two fundamental ways:

### Back end agnostic ###
This is for the tasks that don't need to occupy the backend's processing at all; when the frontend would like to do some computations that don't involve controls. <br />
This is the simpler task, and we left a lot of room for integrating; for a task that's just operating on 5 pictures, Ivan and I set it up s.t. frontend saves screencaps on a button press from a given feed, and then a child proc is spawned to do the CV, much as you might do for comms between a ROS node. If the rules didn't stipulate that the CV couldn't have any input besides taking the pictures then we would have integrated fully into tsx for retakes / validation. The capturing could have been implicit to the CV functionality - rules stopped us from doing it that way, but in the future if rules allow I definitely encourage that design. That's why we left you flexibility here. 

### Feed Forward ###
ROV_main.py expects to know who is talking to it in the message type; you can send a flag to let it know to swap which set of ingress controls it should listen to. This enables you to hot swap feeds that control drones. We took this account in our design but never saw it fully through to fruition - this should be someone's focus this next year. This is a universal design so it isn't exclusive to CV via frontend taking over; anything that can generate controls can send this message format, CV was just the most obvious. 


To rerun a video to imitate a proper test feed: <br />
  on one terminal, run: ffserver -f /etc/ffserver.conf <br />
  on the other, run: ffmpeg -i <./path/to/.mp4> -c:v libvpx -cpu-used 4 -threads 8 http://localhost:8090/stream.ffm <br />
  This throws up a camera feed from an old video that you may now consume<br />


#### Eric's Wack Math ####

This section operates off a weird math conceept I stumbled upon on SO. It's about colinear projection; a very simple concept but I didn't really see it much on the google, but think about orthogonal projection from calc 1 but for the dot product component instead of the cross product component. 

This approach is about redefining a rectangle in the loosest possible terms; two sets of parallel lines that are orthogonal to each other, and their colinear projections have overlap on each other (they aren't just any random two sets of parallel lines, they need to make some what of a box). This was developed in response to poor ability to isolate hard edges to form lines in blurry underwater pictures in an effort to make it more tolerant. 

Algo: <br />
test3 is baseline <br />
tolerance adds angle tolerance to projections; for instance: in doing orthogonal projection, you can be a % tolerance from orthogonal to still get  the desired projection <br />
invert better captures tolerance around nan slopes due to numpy vectorizing flaw, redid ortho project in an important way
area has smarter rectangle selection <br />
vid is the video tool <br />
Orthodemo and Parademo were simple proof of concepts to show to the midterm design review <br />
<br />
For best results: don't be obnoxious. It's a very specific task, so take a very specific photo.
	As straight on as possible, capturing ideally only the CV target, and it should do the rest.
	It can handle quite a bit of noise, but if you start feeding in bad photos you're going 
	to get bad results. It's best to take the extra 2 seconds per capture in the middle of a mission run, so talk to your pilot about what your ideal capture is and make sure you get it.  <br />
There are tons of helper functions and commented out points for you to observe what's happening. Use them before you ask me. 
    Especially the ones in show_desired_rect, operate, and get_lines. GLHF <br />
<br />

### Neural net proof of concept ###

Don't take this seriously, this was just a viability test. Needs MUCH more work to actually work. 
This is a classifier; you must have a tremendous training set for it to be able to classify correctly, let alone identifying square / rect and colors. Way too much effort to be worth it, I just wanted to see if it would take a lot of work or an unsurmountable amount. Looked like the last. <br />
<br />
NN:<br />
split: splits the video into image frames<br />
a.bash: deletes every other .jpg in a folder; adjacent frames are too similar, doesn't help in training an ai<br />
fix: after using https://github.com/tzutalin/labelImg to label images I accidentally reran split, so I made this file to delete every image that I didn't label<br />
show: shows me the bounding box on an image to make sure I'm not an idiot<br />
nn: a baby nn I used just to see how it would do. Harsh truths:
    Needs volumes of training data. It converges way too quickly since adjacent frames are too similar and unsimilar frames are really unsimilar and the order is implicit to batch determination; I should bind images and bounding boxes to a custom generator
    so I can randomize it, and then add in duplicate frames that have been rotated/transposed/sheared/etc.
    That being said, it didn't show enough promise to make me think this extra effort was worth it,
    but maybe I can throw a freshman at it to do my dirty work for me + teach them how to build a simple nn. <br />


### Other stuff ### 

yeet:<br />
  idk honestly, something I tried with contouring. If it was easier to capture hard lines in blurry underwater images this would be the go to, but instead it sucks. Maybe spend some time next effort trying to see if you can capture them better than I did and return to contouring. <br />


photomosaics:<br />
  my starting take on Hunter's work. Made it fault tolerant and work with real target images, but very far from perfect. Simplified in the one algo.
  tester: test driver<br />


hist:<br />
  puts pixel values into a histogram, makes a palette out of the most occurring colors, then 
  quantizes all other colors into these on a frame 
  based on an idea from scott 
  very naive; to demonstrate:   <br />
    say I have 6 common frequencies <br />
    I'm looking for 4 colors so I quant down to 4 <br />
    3 of my most frequent colors are shades of blue <br />
    congrats you just turned the picture mostly blue <br />
  additionally, 
    these frequencies are [r,g,b], so adjacent pixels may differ a lot, and your results may be a little nonsensical.
    To fix, it should be done in a continuous color spectra like hue in hsv <br />

  drawback: everything is blue, so if I want the 4 highest freqs I'll get 4 shades of blue. Make a simple algo that identifies the 4 peaks in        frequency over 4 highest freqs and this will function much much better - this one is well worth your time working on. <br />


dynamic_quant:<br />
  ^^ but less naive; however it's unuseably slow. much optimization would be needed to work <br />
  it uses HSV since hue is a continuous [0,360] spectra <br />
  instead of choosing the most frequent colors, it chooses local maxima of frequencies; to demonstrate:<br />
    if there are 4 blues but one blue is most common, then 6 reds and one is most common, all of which are 
      together in a list, and I'm looking for 2 maxima, ideally it should choose one blue and one red 
        (I said less naive, not infallible) <br />
  since the reassignment of hues to this palette of maxima colors is manual and in python, it's ludicrously slow, 
  all of the runtime is spent in the quantize function 
  GLHF <br />


the_one_algo_to_rule_them_all:<br />
  I hate how simple it is, but it works very consistently. Some of these ideas are Hunter's from photomosaics.py. 

simple.py:<br />
  ^^ but simpler, more fault tolerant 

no_crop.py:<br />
  ^^ simpler still. The dumbest algo I've ever written, but a judge at comp told me it was judges' discretion of what's good output; over-zealous cropping of a single color band could get it disqualified, so don't even crop at all for insurance. I hate it but it was our best shot at the time. 
<br />

rov pi ffserver.conf for reference, since they live in /etc/ where git doesn't track them:

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

