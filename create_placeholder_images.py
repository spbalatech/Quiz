import os
from PIL import Image, ImageDraw, ImageFont
import json

def create_placeholder_image(text, output_path, width=800, height=600):
    # Create new image with white background
    image = Image.new('RGB', (width, height), 'white')
    draw = ImageDraw.Draw(image)
    
    # Draw gray rectangle as product placeholder
    draw.rectangle([50, 50, width-50, height-50], outline='gray', width=2)
    
    # Add product text
    try:
        font = ImageFont.truetype("arial.ttf", 40)
    except:
        font = ImageFont.load_default()
        
    # Split text into lines
    words = text.split()
    lines = []
    current_line = []
    
    for word in words:
        current_line.append(word)
        text_width = draw.textlength(" ".join(current_line), font=font)
        if text_width > width - 100:
            if len(current_line) > 1:
                lines.append(" ".join(current_line[:-1]))
                current_line = [word]
            else:
                lines.append(word)
                current_line = []
                
    if current_line:
        lines.append(" ".join(current_line))
    
    # Draw text
    total_text_height = len(lines) * 50
    y = (height - total_text_height) // 2
    
    for line in lines:
        text_width = draw.textlength(line, font=font)
        x = (width - text_width) // 2
        draw.text((x, y), line, fill='black', font=font)
        y += 50
    
    # Create directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Save the image
    image.save(output_path)

def main():
    # Load products data
    with open('data/products.json', 'r') as f:
        data = json.load(f)
    
    # Create placeholder images for each product
    for product in data['products']:
        category = product['category']
        product_id = product['id']
        output_path = f'data/images/{category}/{product_id}.jpg'
        
        # Only create image if it doesn't exist
        if not os.path.exists(output_path):
            create_placeholder_image(product['name'], output_path)
            print(f"Created placeholder image for {product['name']}")

if __name__ == "__main__":
    main()
