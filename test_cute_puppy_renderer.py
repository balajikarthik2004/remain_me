import os
from PIL import Image
import sys

# Test importing or running PuppyRenderer
from desktop_puppy import PuppyRenderer

renderer = PuppyRenderer(96, 88, "#FF00FF")
print("PuppyRenderer initialized successfully!")
img_sit = renderer.draw_sit(0)
print("draw_sit OK:", type(img_sit))
img_walk = renderer.draw_walk(0)
print("draw_walk OK:", type(img_walk))
img_wag = renderer.draw_wag(0)
print("draw_wag OK:", type(img_wag))
img_sleep = renderer.draw_sleep(0)
print("draw_sleep OK:", type(img_sleep))
