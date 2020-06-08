
import PIL
from PIL import Image
from PIL import ImageDraw, ImageFont




# read image and convert to RGB
image = Image.open("msi_recruitment.gif")
image = image.convert('RGB')

# Before the code that was used for thsi assignment, here is a much quicker option to use but it means importing the numpy module -
# which I did not use as we technically haven't learned yet. The code below works but it is very slow so give it some time before it
# executes fully
# import numpy
# a = numpy.array(image)
# a[:,:,1] //= 2 - this line reduces 'G' channel intensity in half, last element in the list is the channel (either 0 for R, 1 for G or 2 for B)
# b = Image.fromarray(a)
# Re = Re.convert('RGB')
# Bl = Bl.convert('RGB')
# b.show()

# defining a function which will take an original, make a slightly bigger copy, change the tone and write text on the bottom
def changecolor_inputtext(orimage, channel, intensity):
    # creating a copy as the function is going to keep changing the original, slightly bigger in height to create a black textbox
    copyimg = Image.new(mode = 'RGB', size = (orimage.width, orimage.height+50), color = 'black')
    copyimg.paste(orimage)
    drawtxt = ImageDraw.Draw(copyimg)
    # importing the font we are meant to use
    font = ImageFont.truetype('fanwood-webfont.ttf', 48)
    # inputting text
    drawtxt.text((1, int(0.9*copyimg.height)),("channel: {} intensity: {}".format(channel, intensity)), fill = 'white', font=font)
    # a for loop through all the pixels in the image
    for row in range(copyimg.height):
        for col in range(copyimg.width):
            # editing only ONE element of the tuple with channels to change the tone of the picture
            pix = list(copyimg.getpixel((col,row)))
            pix[channel] = int(pix[channel]*intensity)
            # drawing a pixel with new channel vlaues in the same place
            change = ImageDraw.ImageDraw(copyimg)
            change.point((col,row), fill= tuple(pix))
    return copyimg

channel_list = [0,1,2]
intensity_list = [0.1, 0.5, 0.9]
# running a list comprehension with lists created above - with values of channel and values of intensity, to create a new list of 9 images
changed_pics = [changecolor_inputtext(image, channel, intensity) for channel in channel_list for intensity in intensity_list]

# assigning firstpic a value of first element in changed_pics
firstpic = changed_pics[0]

# the rest is as per code that created a contact_sheet with different brightnesses
collage = PIL.Image.new(firstpic.mode, (firstpic.width * 3, firstpic.height *3))
coord_x = 0
coord_y = 0

for img in changed_pics:
    collage.paste(img, (coord_x,coord_y))
    if coord_x + firstpic.width == collage.width:
        coord_x = 0
        coord_y = coord_y + firstpic.height
    else:
        coord_x = coord_x + firstpic.width

collage = collage.resize((int(collage.width / 2),int(collage.height / 2)))
collage.show()
collage.save('finalcollage.png')







