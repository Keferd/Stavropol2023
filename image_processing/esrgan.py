import torch
from PIL import Image
from RealESRGAN import RealESRGAN


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

model = RealESRGAN(device, scale=4)
model.load_weights('weights/RealESRGAN_x8.pth', download=True)

path_to_image = '/content/Pgp-com2-K-1-0-9-36.jpg'
image = Image.open(path_to_image).convert('RGB')
shape = (int(image.size[0] / 2), int(image.size[1] / 2))
low_res_img = image.resize(shape)

sr_image = model.predict(low_res_img)

sr_image.save('/content/sr_image.png')