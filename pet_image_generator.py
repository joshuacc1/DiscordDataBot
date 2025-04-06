from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import math
import os

def tile_images(self, ctx):
    """Tiles images from the local drive and sends the result."""

    # Folder where your images are stored
    # folder_path = "images"
    # filenames = ["image1.png", "image2.png", "image3.png"]
    # image_paths = [os.path.join(folder_path, f) for f in filenames]
    image_paths = self.get_files_in_folder("Data/Pets")
    image_paths = image_paths
    try:
        tile_size = 100
        font_size = 12
        label_height = 15  # extra space under each tile for the label

        # Load font (fallback to default if unavailable)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        labeled_images = []
        for path in image_paths:
            # Open and resize
            img = Image.open(path).resize((tile_size, tile_size))
            
            # Create a new image with space for the label
            labeled = Image.new("RGB", (tile_size, tile_size + label_height), color=(255, 255, 255))
            labeled.paste(img, (0, 0))

            # Add the label
            draw = ImageDraw.Draw(labeled)
            img_info = path.split("%%")
            petname = img_info[1]
            label = os.path.splitext(os.path.basename(petname))[0]  # filename without extension
            text_width = draw.textlength(label, font=font)
            text_x = (tile_size - text_width) // 2
            draw.text((text_x, tile_size), label, fill=(0, 0, 0), font=font)

            labeled_images.append(labeled)

        num_images = len(labeled_images)
        columns = math.ceil(math.sqrt(num_images))
        rows = math.ceil(num_images / columns)

        grid_width = columns * tile_size
        grid_height = rows * (tile_size + label_height)
        tiled = Image.new("RGB", (grid_width, grid_height), color=(255, 255, 255))

        for index, img in enumerate(labeled_images):
            x = (index % columns) * tile_size
            y = (index // columns) * (tile_size + label_height)
            tiled.paste(img, (x, y))

        buffer = BytesIO()
        tiled.save(buffer, format="PNG")
        #buffer.seek(0)
        tiled.show()
        #file = discord.File(buffer, filename="labeled_grid.png")

    except Exception as e:
        print(f"Error: {e}")

def pictures_into_tiles_all(image_paths, size):
    # image_paths = self.get_files_in_folder("Data/Pets")
    # image_paths = image_paths
    try:
        tile_size = 100
        font_size = 12
        label_height = 15  # extra space under each tile for the label

        # Load font (fallback to default if unavailable)
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
        except:
            font = ImageFont.load_default()

        labeled_images = []
        for path in image_paths:
            # Open and resize
            img = Image.open(path).resize((tile_size, tile_size))
            
            # Create a new image with space for the label
            labeled = Image.new("RGB", (tile_size, tile_size + 2*label_height), color=(0, 0, 0))
            labeled.paste(img, (0, 15))

            # Add the label
            draw = ImageDraw.Draw(labeled)
            img_info = path.split("/")[-1]
            img_info = img_info.split("%%")
            petname = img_info[1]
            username = img_info[0]
            label = os.path.splitext(os.path.basename(petname))[0]  # filename without extension
            text_width_petname = draw.textlength(label, font=font)
            text_width_username = draw.textlength(username, font=font)
            text_x_petname = (tile_size - text_width_petname) // 2
            text_x_username = (tile_size - text_width_username) // 2
            draw.text((text_x_petname, tile_size+label_height), label, fill=(255, 255, 255), font=font)
            draw.text((text_x_username, 0),username, fill=(255, 255, 255), font=font)
            labeled_images.append(labeled)

        num_images = len(labeled_images)
        columns = math.ceil(math.sqrt(num_images))
        rows = math.ceil(num_images / columns)

        grid_width = columns * tile_size
        grid_height = rows * (tile_size + 2*label_height)
        tiled = Image.new("RGB", (grid_width, grid_height), color=(255, 255, 255))

        for index, img in enumerate(labeled_images):
            x = (index % columns) * tile_size
            y = (index // columns) * (tile_size + 2*label_height)
            tiled.paste(img, (x, y))

        buffer = BytesIO()
        tiled.save(buffer, format="PNG")
        buffer.seek(0)

        tiled.show()
        return buffer
    
    except Exception as e:
        print(f"{e}")

def pictures_into_tiles_owner(owner_name, picture_data, size = 200, show_image = False):
    image_paths = picture_data
    try:
        tile_size = size
        font_size = 14
        label_height = 18  # extra space under each tile for the label
        border_thickness = 5  # Thickness of the border around each tile

        # Load font (fallback to default if unavailable)
        font_path = "/usr/share/fonts/truetype/noto/NotoSans-Regular.ttf"  # Adjust path as needed
        
        try:
            font = ImageFont.truetype("arial.ttf", font_size)
            font = load_font(font_path, font_size)
        except:
            font = ImageFont.load_default()

        labeled_images = []
        for path in image_paths:
            # Open and resize
            fimg = Image.open(path)
            original_width, original_height = fimg.size

            # Calculate the new dimensions
            if original_height > original_width:
                percentage = size/original_height
                new_height = size
                new_width = int(original_width * percentage)
            else:
                percentage = size/original_height
                new_height = int(original_height * percentage)
                new_width = size
            
            img = fimg.resize((new_width - 2 * border_thickness, new_height - 2* border_thickness))
            
            # Create a new image with space for the label and border
            framed = Image.new(
                "RGB",
                (new_width, new_height),
                color=(230, 230, 230),
            )

            framed.paste(img, (border_thickness, border_thickness))

            labeled = Image.new(
                "RGB",
                (tile_size, tile_size + label_height),
                color=(0, 0, 0),
            )

            if original_height > original_width:
                labeled.paste(framed, (int(size/2 - new_width/2), 0))
            else:
                labeled.paste(framed, (0, int(size/2 - new_height/2)))

            # Add the label
            draw = ImageDraw.Draw(labeled)
            img_info = path.split("%%")
            petname = img_info[1]
            label = petname # os.path.splitext(os.path.basename(petname))[0]  # filename without extension
            text_width = draw.textlength(label, font=font)
            text_x = (tile_size - text_width) // 2
            draw.text((text_x, tile_size), label, fill=(255, 255, 255), font=font)

            labeled_images.append(labeled)

        num_images = len(labeled_images)
        columns = math.ceil(math.sqrt(num_images))
        rows = math.ceil(num_images / columns)

        grid_width = columns * tile_size
        grid_height = rows * (tile_size + 2*label_height)
        tiled = Image.new("RGB", (grid_width, grid_height), color=(0, 0, 0))
        

        for index, img in enumerate(labeled_images):
            x = (index % columns) * tile_size
            y = (index // columns) * (tile_size + label_height) + label_height
            tiled.paste(img, (x, y))

        # # Add a label over the entire tiled image
        final_image = Image.new("RGB", (grid_width, grid_height + label_height), color=(0, 0, 0))

        # Paste the tiled image below the label
        final_image.paste(tiled, (0, 0))

        buffer = BytesIO()
        final_image.save(buffer, format="PNG")
        buffer.seek(0)
        if show_image:
            final_image.show()
        return buffer
    except Exception as e:
        print(f"{e}")

def load_font(font_path, font_size):
    """Loads a font with the specified size."""
    try:
        return ImageFont.truetype(font_path, font_size)
    except Exception as e:
        print(f"Error loading font: {e}")
        return ImageFont.load_default()  # Fallback to default font

def get_files_in_folder(folder_path):
    """Returns a list of all files in the specified folder."""
    try:
        # List all files in the folder
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        return files
    except FileNotFoundError:
        print(f"Folder not found: {folder_path}")
        return []



image_paths = get_files_in_folder("Data/Pets")
image_paths = [x for x in image_paths if "720142714103922738" in x]
# # #pictures_into_tiles(image_paths[4:8],(100,100))
pictures_into_tiles_owner("Owner_name",image_paths,400)