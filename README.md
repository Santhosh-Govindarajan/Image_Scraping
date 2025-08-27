# Image_Scraping
Facebook Image Scraper with Selenium

This project came from a simple need: downloading images from a Facebook group without saving them one by one. Imagine sitting for hours, right-clicking and saving each photo. It’s tiring. That’s where this script comes in as your digital assistant.

The journey starts when you run the Python file. A Chrome browser opens, almost like a blank canvas, and takes you straight to Facebook’s login page. Here, nothing tricky happens. You enter your login details yourself, keeping everything safe and private. Once you’re logged in, the script is ready to take over.

You direct it to a Facebook group’s media section, and that’s where the magic begins. Just like you would scroll endlessly through posts, the script does this for you. It scrolls repeatedly, pausing each time to give Facebook enough time to load all those hidden images waiting below.

When the page is filled with pictures, the script carefully searches for links that open the full image viewer. It collects them like a treasure map, one by one, until it knows where all the high-quality photos are stored. Then, it shifts gears and starts opening those images in a separate tab. Each photo is inspected, and its tiny thumbnail is replaced with the largest, clearest version possible, often upgraded to 1080px resolution.

Once the real gems are found, the script saves them into a folder. If the folder doesn’t exist, it creates one, preparing a little gallery just for you. The files are named and organized neatly, avoiding duplicates so you won’t waste space. Slowly, image by image, your collection begins to take shape.

By the time the browser closes, you are left with a tidy folder full of memories, resources, or research material—whatever those images meant to you. And it all happened without the endless clicking, dragging, and waiting you’d normally face.

This script isn’t just code. It’s a helping hand for anyone who needs to gather visual content from Facebook responsibly. It saves time, effort, and patience, wrapping the whole process in a simple story: open, scroll, collect, and save.

When it finally says “DONE: All images saved,” you’ll know that the job you dreaded is now finished.
