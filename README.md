# WikiPlus

WikiPlus is my final project for CSCI E-33a.
It is an extension to Project 1, Wiki. 

## Overview

In my final project proposal, I outlined how I planned to build upon Wiki to create something that me and my friends would find useful.
The design goal was to create a quickly-editable wiki to facilitate internal collaboration on creative projects for teams that are separated by distance and must work online.
I prioritized keeping things fast and intuitive wherever possible.
A key part of this goal was realized through the absence of a login feature, as having one would greatly slow down the writing and editing process; The wiki is intended to be shared only amongst members of the team.

Wiki entries are stored as Django models. While it took quite some effort to set this up, the payoff was totally worth it, as having the entries represented by models made them very easy to work with and elucidated the process by which I was to add additional features.

Each wiki page contains two tabs. One tab displays text information about the entry and the other shows a gallery of photos related to the entry. The tabs are controlled using JavaScript and JQuery.

Photos are "uploaded" using links to elsewhere online that the photos are being hosted. The "image gallery" itself is actually a TextField wherein each line contains the URL to a different image.
This is by design, as the gallery is intended to be used as a "mood board."
By copy-pasting URLs, this saves users the time and effort of needing to download and then upload the actual files one-by-one into each entry.
It also prevents the common inconvenience of downloading an image from online only to find that it is in svg or webp format.

There is a "Find & Replace" function that will replace every instance of a given word with another given word across ALL pages. This is for naming and re-naming characters and places (a common occurence when outlining/world-building).

Some CSS was also implemented to make the site visually appealing to me. I just really like the Gaegu font.

## Changes

The files I edited and/or added are as follows:

# addpage.html & editpage.html

- Added a section for the user to copy-and-paste image links for display in the gallery/mood board

# index.html

- Now provides a count of all pages as well as a "lifetime" count of edits made

# layout.html

- Includes a link to the "Find & Replace" page
- Added a Favicon

# replace.html

- Provides an interface by which a user can search for instances of a given word across all pages and replace that word with a new one

# wikipage.html

- Now contains both a "content view" and a "gallery view"; one is for text and the other is for images

# models.py

- Created a "WikiEntry" model to store information about a page's title, content, image gallery, and total number of edits made

# urls.py

- Edited to facilitate the "replace" view

# view.py

- Where all of the app's logic takes place
- Just about everything was changed, including the fixing up of some bugs that existed in my original implementation of this project
- Added the "replace" view
- Parses the images in the image gallery so that they can display properly on wikipage.html
- Handles searching, finding, and replacing
- Counts and displays total number of pages and edits
- And more