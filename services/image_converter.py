from PIL import Image

class ImageService:
    @staticmethod
    def convert_and_resize_image(image_path, output_path, width=800, height=400, quality=80):
        with Image.open(image_path) as img:
            img.thumbnail((width, height))
            img.save(output_path, 'WEBP', quality=quality)