import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
import numpy as np
import math
from matplotlib.image import imread
from skimage.transform import resize

x0, y0 = 100, 100

R_outer = 90
R_inner = 20
R_inner_dash = 17

A1, B1, C1 = (60, 130), (100, 50), (140, 130)
A2, B2, C2 = (56, 133), (100, 45), (144, 133)

fig, ax = plt.subplots()
ax.set_aspect('equal')

def draw_line_points(x1, y1, x2, y2, color=(0, 0, 0), thickness=1.5, style='solid'):
    if style == 'dashed':
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy)
        position = 0.0
        dash_length = 8
        gap_length = 4
        while position < length:
            end = min(position + dash_length, length)
            t1 = position / length
            t2 = end / length
            x_start = x1 + dx * t1
            y_start = y1 + dy * t1
            x_end = x1 + dx * t2
            y_end = y1 + dy * t2
            ax.plot([x_start, x_end], [y_start, y_end],
                    color=color, linewidth=thickness)
            position += dash_length + gap_length
    else:
        ax.plot([x1, x2], [y1, y2], color=color, linewidth=thickness)

def draw_circle_points(xc, yc, r, color=(0, 0, 0), thickness=1.2):
    angles = np.linspace(0, 2 * np.pi, 300)
    x_points = xc + r * np.cos(angles)
    y_points = yc + r * np.sin(angles)
    ax.plot(x_points, y_points, color=color, linewidth=thickness)

def draw_arc_points(xc, yc, r, start_angle, end_angle, color=(0, 0, 0), thickness=1.2):
    start_angle_rad = math.radians(start_angle)
    end_angle_rad = math.radians(end_angle)
    angles = np.linspace(start_angle_rad, end_angle_rad, 100)
    x_points = xc + r * np.cos(angles)
    y_points = yc + r * np.sin(angles)
    ax.plot(x_points, y_points, color=color, linewidth=thickness)

def insert_image_into_triangle(image_path, triangle_vertices):
    img = imread(image_path)
    if img.dtype != np.uint8 and img.max() > 1.0:
        img = img / 255.0

    A, B, C = triangle_vertices
    x_coords = [A[0], B[0], C[0]]
    y_coords = [A[1], B[1], C[1]]

    min_x, max_x = min(x_coords), max(x_coords)
    min_y, max_y = min(y_coords), max(y_coords)

    width = max_x - min_x
    height = max_y - min_y

    if width > 0 and height > 0:
        img_corrected = np.fliplr(img)
        img_resized = resize(img_corrected, (int(height), int(width)), anti_aliasing=True)

        triangle_poly = Polygon(triangle_vertices, closed=True, transform=ax.transData)
        ax.imshow(img_resized, extent=[min_x, max_x, max_y, min_y],
            clip_path=triangle_poly, clip_on=True, alpha=0.7)

draw_arc_points(x0, y0, R_outer, 0, 225, thickness=1.5)

draw_circle_points(x0, y0, R_inner, thickness=1.2)

for angle_degrees in range(0, 360, 60):
    start_angle = angle_degrees
    end_angle = angle_degrees + 30
    draw_arc_points(x0, y0, R_inner_dash, start_angle, end_angle, thickness=1.2)

def create_triangle(vertices, style='solid', thickness=1.5):
    A, B, C = vertices
    if style == 'dashed':
        draw_line_points(A[0], A[1], B[0], B[1], thickness=thickness, style='dashed')
        draw_line_points(B[0], B[1], C[0], C[1], thickness=thickness, style='dashed')
        draw_line_points(C[0], C[1], A[0], A[1], thickness=thickness, style='dashed')
    else:
        draw_line_points(A[0], A[1], B[0], B[1], thickness=thickness)
        draw_line_points(B[0], B[1], C[0], C[1], thickness=thickness)
        draw_line_points(C[0], C[1], A[0], A[1], thickness=thickness)

create_triangle([A1, B1, C1], style='solid', thickness=1.5)
create_triangle([A2, B2, C2], style='dashed', thickness=1.2)

image_path = "/Users/onyx/Desktop/Screenshot.jpeg"
insert_image_into_triangle(image_path, [A1, B1, C1])

def create_slanted_line(start_x, start_y, end_x, end_y, thickness=1.5):
    draw_line_points(start_x, start_y, end_x, end_y, thickness=thickness)

create_slanted_line(0, 6.5, 200, 110, thickness=1.5)

ax.invert_yaxis()
ax.set_xlim(0, 250)
ax.set_ylim(250, 0)
ax.axis('off')

plt.show()