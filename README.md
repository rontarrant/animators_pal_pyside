# Animator's Pal

## Refactored with PySide6 & moviepy

### What it is

Animator's Pal does one simple job: given a series of images, it builds an MP4 video file. Animator's Pal will always order the images alphabetically/numerically. In other words, in the order they appear in a file browser. This should be universal across all operating systems (if you run the Python version, not the PyInstaller version built for Windows, naturally). (Note: File order is different in UNIX than it is in Windows. UNIX uses ASCII order — numbers, then uppercase, then lowercase) whereas Windows mixes uppercase and lowercase.)

### Along the Way

You can set these:

- frames per second (18, 24, 0r 30)
- output resolution (8k, 4k, 1080p, or 720p)
- order the images to play forward or in reverse in the final video
- set the framehold (also called shooting on 1's, 2's, 3's, etc.) anywhere from 1's to 9's

### Other Features

The images can be of random sizes and shapes and they will all be resized to fit the selected output resolution.

If an image is narrower than 16:9 (also known as Full HD TV) it will be pillarboxed (black will show on either side of the image).

If it's wider than 16:9, it'll be letterboxed (black will show above and below the image).

Images for varying aspect ratios can be combined into a single video file. Why anyone might want to do that is a very good question, but Animator's Pal will.

### Current Status

I've wanted something like Animator's Pal for a while, but every application I tried either didn't have all the features I wanted or used jargon that really didn't translate well to the language found books about classical animation such as those written by (in no particular order) Preston Blair, Chris Webster, Richard Williams, Tony White, Harold Whitaker, and John Halas.

As of September 23, 2024, it's about as complete as I need it to be for now.

If you're using Windows 10 or 11:
- navigate to the dist folder,
- grab the contents of the main folder (or just the entire folder),
- put them somewhere on your computer, and
- run animators_pal.exe.

No need for installation. 

If you're using Linux, one of the BSD's, or any other OS where Python can be installed, do this:

1) grab these files/directories:
- all the .py files
- the images folder
2) install these:
- PySide6
- moviepy
3) type: python main.py

PySide6 is fast enough so page-flipping will run at full speed on (I'm pretty sure) most computers that are less than 10 years old. I have an old gaming laptop from 2015 and it runs fine on that.

If you want a sample series of 75 images to test this out, I've included an ancient flipbook I did (probably) circa 1985. You'll find them in the sequence directory/folder.

### Why the Refactor?

A rewrite of the Animator's Pal animation tool using the *PySide6* GUI library came about because *Tkinter* simply isn't fast enough to do 30 fps page-flipping... which shouldn't have taken a year to work out, but it did.

Prototyping and the first proof took far longer than I'd planned (or liked, for that matter) but when I was faced with a ground-up rewrite using yet another GUI toolkit (the fourth one for this project) and a new video handling library, I decided to enslave a chat-bot to do the coding.

So, I wrote up a comprehensive product requirements doc (see: Application Requirements and Design in the docs directory) and fed it to the AI bots one at a time.

I had the best results with Perplexity, not just because it didn't cut me off after 10 questions, but because it went a step further and made interesting (and, as it turned out, helpful) suggestions.

Over the course of six days I coached Perplexity through several versions of a monolithic file, then further coached it through breaking that up into easier-to-maintain modules, and finally ended up with a product that was close enough to spec that I declared it done.

There were hiccups along the way, but also some interesting interactions. As far as hiccups go, Tuesday September 17, 2024 was a full moon. Now, from a logical point of view, that shouldn't matter to an AI, but they were *all* going nuts that day. And for the entire day. Seriously. I kept checking back and they were all giving nonsense answers.

Needless to say, I took the day off.

So much for science v. whatever.

On the interesting side, at one point I handed Perplexity a list of image files I wanted to use for buttons. (I never use standard buttons because my education is in art and I like colourful UIs. Anyway...) In the requirements doc, I'd listed seven video control buttons I wanted for the on-screen video player, but there were 18 file names on the list of image files. Perplexity made an assumption and wrote the logic for nine buttons ('up' and 'down' images for 9 buttons equals 18 image files).

There were a few setbacks, too. If I didn't word my instructions very carefully, Perplexity would add in a feature I'd asked for, but remove another one that I'd not mentioned at all. And it wasn't like these features were mutually exclusive. Perplexity just took it upon itself to yank them for what I can only assume was a reason that made sense to Perplexity itself.

But, with further coaching, all the features I'd planned ended up in the application.

I just finished initial testing and it looks pretty solid. I'm impressed with Perplexity and I'll probably use it for my next project, too. I mean, why bother writing my own code if I can do the design and requirements and then hand off the coding to a bot?

AI may not change the world overnight, but the writing is on the wall for coders. Programmers, no, but I can see coders being laid off in droves within the next few years. Sorry to be the bearer of that bit of news, but maybe Guaranteed Basic Income will pass parliament and you guys can get trained for other work.

Good luck!

 