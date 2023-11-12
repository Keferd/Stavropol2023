import torch
from PIL import Image
from RealESRGAN import RealESRGAN


def image_proccessing(image_path):
    print(1)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(21)
    model = RealESRGAN(device, scale=4)
    print(31)
    model.load_weights('weights/RealESRGAN_x8.pth', download=True)
    print(41)
    path_to_image = image_path
    print(51)
    image = Image.open(path_to_image).convert('RGB')
    print(61)
    shape = (int(image.size[0] / 2), int(image.size[1] / 2))
    print(71)
    low_res_img = image.resize(shape)
    print(81)
    sr_image = model.predict(low_res_img)
    print(91)
    sr_image.save(image_path)