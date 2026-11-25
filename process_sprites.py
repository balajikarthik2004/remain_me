import os
import numpy as np
from PIL import Image
from collections import deque

def cutout_white_background(src_path, dest_path, white_thresh=238, color_diff_thresh=20):
    print(f"Processing: {src_path} -> {dest_path}")
    im = Image.open(src_path).convert('RGB')
    w, h = im.size
    arr = np.array(im, dtype=np.int32)

    # Detect white/off-white background
    is_white = (arr[:, :, 0] > white_thresh) & (arr[:, :, 1] > white_thresh) & (arr[:, :, 2] > white_thresh) & \
               (np.abs(arr[:, :, 0] - arr[:, :, 1]) < color_diff_thresh) & \
               (np.abs(arr[:, :, 1] - arr[:, :, 2]) < color_diff_thresh)

    # Flood fill ONLY from the 4 outer image boundaries
    # This prevents white areas inside the character (such as Spidey's eyes) from becoming transparent!
    visited = np.zeros((h, w), dtype=bool)
    q = deque()

    for x in range(w):
        if is_white[0, x] and not visited[0, x]: 
            q.append((0, x)); visited[0, x] = True
        if is_white[h-1, x] and not visited[h-1, x]: 
            q.append((h-1, x)); visited[h-1, x] = True

    for y in range(h):
        if is_white[y, 0] and not visited[y, 0]: 
            q.append((y, 0)); visited[y, 0] = True
        if is_white[y, w-1] and not visited[y, w-1]: 
            q.append((y, w-1)); visited[y, w-1] = True

    while q:
        y, x = q.popleft()
        for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            ny, nx = y + dy, x + dx
            if 0 <= ny < h and 0 <= nx < w and not visited[ny, nx]:
                if is_white[ny, nx]:
                    visited[ny, nx] = True
                    q.append((ny, nx))

    # visited == True is outer background
    rgba = np.zeros((h, w, 4), dtype=np.uint8)
    rgba[:, :, :3] = np.array(im)
    rgba[:, :, 3] = np.where(visited, 0, 255)

    # Soften outer edge boundary slightly to avoid jagged pixel artifacts
    # Crop to non-empty bounding box
    non_empty = np.where(rgba[:, :, 3] > 0)
    if len(non_empty[0]) == 0:
        print("Warning: image became empty!")
        return False
        
    min_y, max_y = np.min(non_empty[0]), np.max(non_empty[0])
    min_x, max_x = np.min(non_empty[1]), np.max(non_empty[1])

    # Add 4px margin
    min_y = max(0, min_y - 4)
    min_x = max(0, min_x - 4)
    max_y = min(h, max_y + 4)
    max_x = min(w, max_x + 4)

    cropped = Image.fromarray(rgba).crop((min_x, min_y, max_x, max_y))
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    cropped.save(dest_path)
    print(f"Saved {dest_path}: size {cropped.size}, alpha mode RGBA")
    return True

if __name__ == "__main__":
    spidey_idle_src = r"C:\Users\BalajiKrishnan\.gemini\antigravity\brain\e20049d2-a124-403d-af17-977037b027b5\chibi_spiderman_pet_1794828114278.jpg"
    spidey_action_src = r"C:\Users\BalajiKrishnan\.gemini\antigravity\brain\e20049d2-a124-403d-af17-977037b027b5\chibi_spiderman_action_sprite_1794828103276.jpg"

    cutout_white_background(spidey_idle_src, "assets/shadow_soldiers/spiderman_hq.png")
    cutout_white_background(spidey_action_src, "assets/shadow_soldiers/spiderman_action_hq.png")
    print("ALL SPRITES CUT OUT AND SAVED SUCCESSFULLY!")
