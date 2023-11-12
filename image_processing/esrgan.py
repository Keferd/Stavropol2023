import torch
from PIL import Image
from RealESRGAN import RealESRGAN


def image_proccessing(image_path):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=4)
    model.load_weights('weights/RealESRGAN_x8.pth', download=True)
    path_to_image = image_path
    image = Image.open(path_to_image).convert('RGB')
    shape = (int(image.size[0] / 2), int(image.size[1] / 2))
    low_res_img = image.resize(shape)
    sr_image = model.predict(low_res_img)
    sr_image.save(image_path)