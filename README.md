### Sprite Builder

###### version 1.0.0 - Alpha

This is a broader attempt at a sprite builder similar to my Denzi Character Builder project which I've stopped working on in favor of this project.

The Sprite Builder is being designed to work with sprites from 16x16 to 64x64, though in it's current state it is hard coded to only work with 16x16 images.

Dependencies
```
pygame
```

#### Usage

Launch using the `main.py` file.  Prior to launching you can change colors and some other settings within the `local.py` file.

For images to actually show up, you'll want to add individual sprites to the `/images/list` directory.  This currently only supports png files though I plan to make the loading much more robust in the future.

Once images are loaded, they will appear in the lower image area.  There is not hard limit to the number of images you can put in the list directory.  They will appear in the order they are loaded.

Image previews are provided in 16x16, 32x32 and 64x64, though the image is only saved as a 16x16 image currently.

Add images by clicking on them, hovering over an image gives you a larger preview of the image itself.  You're able to add multiple images to create a layered image.  If you need to go back, use the `Undo Last` button to take a step back, this can be repeated until the image is empty.  Use the `Clear` button to complete remove the image.  Use the `Save` button to save the image to the `/images/created` directory.  They're stored in a `time.random.png` format.  Lastly, you can close the program with the `Quit` button or by closing the window.

#### The To-Do's

- [ ] Allow size selection before save
- [ ] Allow image to be named
- [ ] Dynamic loading of images
- [ ] Sprite sheet parsing
- [ ] Custom image saving (e.g compound images saved as bin format for reloading)
- [ ] Improved layout
- [ ] Image/color editor
- [ ] Figure out the rest of the To-Do's