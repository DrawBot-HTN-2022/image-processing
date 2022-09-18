from PIL import Image
from svgpathtools import Path, Line, CubicBezier
import numpy as np
import potrace
import time
import cv2
    
# Opening the image (R prefixed to string
# in order to deal with '\' in paths)
image = Image.open('car.jpg')
  
# Converting the image to grayscale, as edge detection 
# requires input image to be of mode = Grayscale (L)
image = image.convert("L")
image = image.resize((128, 128))

canny=cv2.bitwise_not(cv2.Canny(np.asarray(image),70,140))

# print(image)
  
# Displaying the image
cv2.imshow("plot", canny)
if cv2.waitKey(1) == ord('q'):
    raise Exception()
time.sleep(5)

# Create a bitmap from the array
bmp = potrace.Bitmap(image)

# Trace the bitmap to a path
path = bmp.trace(opttolerance=0.5)

print(path)

iy, ix = image.size
print(ix, iy)
plotter = np.zeros((ix, iy, 3), dtype=np.uint8)
plotter.fill(255)

print(plotter)

NUM_SAMPLES = 10

def draw():
    cv2.imshow("plot", plotter)
    if cv2.waitKey(1) == ord('q'):
        raise Exception()
    # time.sleep(0.00001)

# Iterate over path curves
for curve in path:
    draw()
    current_point_x = curve.start_point.x
    current_point_y = curve.start_point.y
    for segment in curve:
        end_point_x = segment.end_point.x
        end_point_y = segment.end_point.y
        if segment.is_corner:
            c_x = segment.c.x
            c_y = segment.c.y
            # print("corner", c_x, c_y)
        else:
            c1_x = segment.c1.x
            c1_y = segment.c1.y
            c2_x = segment.c2.x
            c2_y = segment.c2.y
            # print("bezier", c1_x, c1_y, c2_x, c2_y)
            bezier_curve = CubicBezier(
                start=complex(current_point_x, current_point_y), 
                control1=complex(c1_x, c1_y), 
                control2=complex(c2_x, c2_y), 
                end=complex(end_point_x, end_point_y)
            )
            bezier_path = Path(bezier_curve)
            for i in range(NUM_SAMPLES):
                raw_point = bezier_path.point(i/NUM_SAMPLES)
                draw_x = int(raw_point.real)
                draw_y = int(raw_point.imag)
                # print(draw_x, draw_y)
                cv2.circle(plotter, (draw_x, draw_y), 1, (0,0,0), 2)
                draw()
        current_point_x = end_point_x
        current_point_y = end_point_y

while True:
    print("end")
    time.sleep(5)
    draw()
            
cv2.destroyAllWindows()
