from PIL import Image
import numpy as np
import os

def cycle_hues(image_path, output_path, num_frames=30, frame_duration=100):
    """
    Create a GIF from a PNG image by cycling through hues.
    
    Args:
        image_path (str): Path to input PNG image.
        output_path (str): Path to save output GIF.
        num_frames (int): Number of frames in the GIF (default: 30).
        frame_duration (int): Duration per frame in milliseconds (default: 100).
    
    Raises:
        FileNotFoundError: If input image doesn't exist.
        ValueError: If num_frames is invalid or output path is not a GIF.
    """
    # Validate inputs
    if not os.path.isfile(image_path):
        raise FileNotFoundError(f"Input image {image_path} not found.")
    if not output_path.lower().endswith('.gif'):
        raise ValueError("Output path must have a .gif extension.")
    if num_frames < 1:
        raise ValueError("Number of frames must be at least 1.")

    # Load the PNG image
    try:
        img = Image.open(image_path)
    except Exception as e:
        raise ValueError(f"Failed to open image: {e}")

    # Convert to RGB if necessary
    img = img.convert("RGB")

    # Initialize GIF writer
    gif_frames = []

    # Convert to HSV once (optimization)
    hsv_img = img.convert('HSV')
    hsv_array = np.array(hsv_img, dtype=np.uint8)  # Use uint8 for clarity

    # Cycle through hues
    for i in range(num_frames):
        # Create a copy of the HSV array to avoid modifying the original
        frame_array = hsv_array.copy()

        # Shift hue channel
        hue_shift = (255 * i // num_frames) % 255  # Integer division for smoother steps
        frame_array[:, :, 0] = (frame_array[:, :, 0] + hue_shift) % 255

        # Convert back to RGB and append to frames
        new_img = Image.fromarray(frame_array, 'HSV').convert('RGB')
        gif_frames.append(new_img)

    # Save the GIF
    try:
        gif_frames[0].save(
            output_path,
            save_all=True,
            append_images=gif_frames[1:],
            loop=0,  # Infinite loop
            duration=frame_duration
        )
    except Exception as e:
        raise RuntimeError(f"Failed to save GIF: {e}")

# Example usage
if __name__ == "__main__":
    try:
        cycle_hues("tone.png", "tone.gif", num_frames=15, frame_duration=100)
        print("GIF created successfully!")
    except Exception as e:
        print(f"Error: {e}")