from PIL import Image
from pytesseract import image_to_string
import re

import cv2

import urllib.request,io

#Image size: 308/20

original_image_path = "/srv/http/ENV3/flask_websockets/banner.png"
image_url = "https://irctclive.nlpcaptcha.in/index.php/media/getTC/M3ZZWG40aTYrd0dCVUo2eStveUpSNlFGdVFtWTVDYUdWSVFFREo1K0kyaEQycUhXYnNhdElDTlBKZ2xiRzcwOGlPaGxRdTIwNEdDVG0vaFBrclJmd1E9PQ==/banner"

original_image_data = io.BytesIO(urllib.request.urlopen(image_url).read())
img1 = Image.open(original_image_data)
img1 = img1.resize((616,40),Image.ANTIALIAS)
img1.save("banner.png",quality=100)

#print(original_image_path)


img = cv2.imread(original_image_path, 0)
ret, thresh = cv2.threshold(img, 10, 255, cv2.THRESH_OTSU)
cv2.imwrite("./banner_final.png", thresh)

#exit()

# img2 = Image.open("/srv/http/ENV3/flask_websockets/banner_low_noise.png")
# img2 = img2.resize((616,40),Image.ANTIALIAS)
# img2.save("banner_final.png",quality=100)

extracted_txt = image_to_string(Image.open("/srv/http/ENV3/flask_websockets/banner_final.png"))
captcha_part = extracted_txt.split(":",1)[1]
captcha = re.sub(' ','',captcha_part)
print(captcha.upper())

#img = Image.open("/srv/http/ENV3/flask_websockets/debug.png")
# box = (150,0,280,20)
# cropped_image = image.crop(box)
# cropped_image.save('cropped_image.jpg')

# img = img.resize((924,120),Image.ANTIALIAS)
# img.save("improved2.png",quality=100)

#import cv2
# img = cv2.imread("/srv/http/ENV3/flask_websockets/banner.png", 0)
# ret, thresh = cv2.threshold(img, 10, 255, cv2.THRESH_OTSU)
# cv2.imwrite("./debug.png", thresh)



# import cv2
# import numpy as np
# from matplotlib import pyplot as plt
#
# img = cv2.imread('/srv/http/ENV3/flask_websockets/improved.png',0)
# blur = cv2.GaussianBlur(img,(5,5),0)
# ret3,th3 = cv2.threshold(blur,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# cv2.imwrite("./debug2.png", th3)
