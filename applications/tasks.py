import base64
from PIL import Image
import random
from io import BytesIO


def task_generate_shares_from_color(image):
    width, height = image.size
    share1 = Image.new('RGB', (width, height))
    share2 = Image.new('RGB', (width, height))
    share1_pixels = share1.load()
    share2_pixels = share2.load()

    for x in range(0, width):
        for y in range(0, height):
            pixel = image.getpixel((x, y))
            random_vals = tuple(random.randint(0, 255) for _ in range(3))
            share1_pixels[x, y] = random_vals
            share2_pixels[x, y] = tuple(pixel[i] ^ random_vals[i] for i in range(3))

    share1_buffered = BytesIO()
    share1.save(share1_buffered, format="PNG")
    share1 = base64.b64encode(share1_buffered.getvalue())

    share2_buffered = BytesIO()
    share2.save(share2_buffered, format="PNG")
    share2 = base64.b64encode(share2_buffered.getvalue())

    return share1, share2


def task_combine_shares_from_color(share1, share2):
    """Kết hợp hai ảnh shares để tái tạo ảnh gốc"""
    width, height = share1.size
    combined_image = Image.new('RGB', (width, height))
    share1_pixels = share1.load()
    share2_pixels = share2.load()
    combined_pixels = combined_image.load()
    for x in range(0, width):
        for y in range(0, height):
            share1_rgb_pixel = share1_pixels[x, y]
            share2_rgb_pixel = share2_pixels[x, y]
            combined_rgb_pixel = tuple(share1_rgb_pixel[i] ^ share2_rgb_pixel[i] for i in range(3))
            combined_pixels[x, y] = combined_rgb_pixel
    combined_image_buffered = BytesIO()
    combined_image.save(combined_image_buffered, format="PNG")
    combined_image = base64.b64encode(combined_image_buffered.getvalue())
    return combined_image


def task_generate_shares_from_binary(image):
    width, height = image.size
    share1 = Image.new('1', (width*2, height*2))
    share2 = Image.new('1', (width*2, height*2))
    patterns = [[1, 1, 0, 0], [1, 0, 1, 0], [1, 0, 0, 1],
                [0, 1, 1, 0], [0, 1, 0, 1], [0, 0, 1, 1]]

    for x in range(0, width):
        for y in range(0, height):
            pixel = image.getpixel((x, y))
            pat = random.choice(patterns)

            share1.putpixel((x*2, y*2), pat[0])
            share1.putpixel((x*2+1, y*2), pat[1])
            share1.putpixel((x*2, y*2+1), pat[2])
            share1.putpixel((x*2+1, y*2+1), pat[3])

            if pixel == 0:
                share2.putpixel((x*2, y*2), 1 - pat[0])
                share2.putpixel((x*2+1, y*2), 1 - pat[1])
                share2.putpixel((x*2, y*2+1), 1 - pat[2])
                share2.putpixel((x*2+1, y*2+1), 1 - pat[3])
            else:
                share2.putpixel((x*2, y*2), pat[0])
                share2.putpixel((x*2+1, y*2), pat[1])
                share2.putpixel((x*2, y*2+1), pat[2])
                share2.putpixel((x*2+1, y*2+1), pat[3])

    share1 = share1.convert("RGBA")
    data1 = share1.getdata()
    new_data1 = []
    for item in data1:
        if item[:3] == (255, 255, 255):
            new_data1.append((255, 255, 255, 0))
        else:
            new_data1.append(item)

    share1.putdata(new_data1)

    share2 = share2.convert("RGBA")
    data2 = share2.getdata()
    new_data2 = []
    for item in data2:
        if item[:3] == (255, 255, 255):
            new_data2.append((255, 255, 255, 0))
        else:
            new_data2.append(item)

    share2.putdata(new_data2)

    share1_buffered = BytesIO()
    share1.save(share1_buffered, format="PNG")
    share1 = base64.b64encode(share1_buffered.getvalue())

    share2_buffered = BytesIO()
    share2.save(share2_buffered, format="PNG")
    share2 = base64.b64encode(share2_buffered.getvalue())
    return share1, share2
