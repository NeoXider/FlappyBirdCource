from PIL import Image, ImageDraw

def create_pipe():
    # Size of the pipe image. 80x600 for high resolution.
    w, h = 80, 600
    img = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)

    # Colors
    border_color = (84, 56, 71, 255) # Dark brown/greenish border
    main_color = (115, 191, 46, 255) # Bright green
    highlight_color = (156, 227, 89, 255)
    shadow_color = (85, 128, 34, 255)

    # 1. Draw the main body
    body_width = w - 10
    body_x1 = 5
    body_x2 = w - 5
    body_y1 = 40 # space for the cap
    body_y2 = h - 2 # goes to the bottom

    # Body border
    d.rectangle([body_x1, body_y1, body_x2, body_y2], fill=border_color)
    # Body fill
    d.rectangle([body_x1+2, body_y1, body_x2-2, body_y2], fill=main_color)
    # Body highlight
    d.rectangle([body_x1+8, body_y1, body_x1+16, body_y2], fill=highlight_color)
    # Body shadow
    d.rectangle([body_x2-12, body_y1, body_x2-4, body_y2], fill=shadow_color)


    # 2. Draw the cap
    cap_x1 = 0
    cap_x2 = w
    cap_y1 = 0
    cap_y2 = 40

    # Cap border
    d.rectangle([cap_x1, cap_y1, cap_x2, cap_y2], fill=border_color)
    # Cap main
    d.rectangle([cap_x1+2, cap_y1+2, cap_x2-2, cap_y2-2], fill=main_color)
    # Cap highlight
    d.rectangle([cap_x1+8, cap_y1+2, cap_x1+16, cap_y2-2], fill=highlight_color)
    # Cap shadow
    d.rectangle([cap_x2-12, cap_y1+2, cap_x2-4, cap_y2-2], fill=shadow_color)
    
    img.save("pipe.png")

if __name__ == "__main__":
    create_pipe()
