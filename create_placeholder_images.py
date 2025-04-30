from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder_image(product_id, size=(400, 300), bg_color=(200, 200, 200)):
    # Create a new image with a gray background
    image = Image.new('RGB', size, bg_color)
    draw = ImageDraw.Draw(image)
    
    # Add text
    text = f"Product ID:\n{product_id}"
    text_color = (50, 50, 50)  # Dark gray
    
    # Calculate text position (center)
    text_bbox = draw.textbbox((0, 0), text)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    text_x = (size[0] - text_width) // 2
    text_y = (size[1] - text_height) // 2
    
    # Draw text
    draw.text((text_x, text_y), text, fill=text_color)
    
    # Ensure directory exists
    os.makedirs('data/images', exist_ok=True)
    
    # Save image
    image.save(f'data/images/{product_id}.jpg')

if __name__ == '__main__':
    # Create placeholder images for each product
    product_ids = ['WA70A4002GS', 'WA90T5260BV']
    for product_id in product_ids:
        create_placeholder_image(product_id)
        print(f"Created placeholder image for {product_id}")
