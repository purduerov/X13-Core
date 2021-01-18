Algo:
test3 is baseline 
tolerance adds tolerance to projections
invert better captures tolerance around nan slopes, redid ortho project in an important way
area has smarter rectangle selection
vid is the video tool

For best results: don't be obnoxious. It's a very specific task, so take a very specific photo.
	As straight on as possible, capturing ideally only the CV target, and it should do the rest.
	It can handle quite a bit of noise, but if you start feeding in bad photos you're going 
	to get bad results. 

There are tons of helper functions and commented out points for you to observe what's happening. Use them before you ask me.
    Especially the ones in show_desired_rect, operate, and get_lines. GLHF

NN:
split splits the video into image frames
a.bash deletes every other .jpg in a folder; adjacent frames are too similar, doesn't help in training an ai
after using https://github.com/tzutalin/labelImg to label images I accidentally reran split, so I made this file to delete every image that I didn't label
show shows me the bounding box on an image to make sure I'm not an idiot
nn is a baby nn I used just to see how it would do. Harsh truths:
    Needs more variety of training data. It converges way too quickly since adjacent frames 
    in each batch are too similar; I should bind images and bounding boxes to a custom generator
    so I can randomize it, and then add in duplicate frames that have been rotated or transposed.
    That being said, it didn't show enough promise to make me think this extra effort was worth it,
    but maybe I can throw a freshman at it to do my dirty work for me + teach them how to build a nn. 
