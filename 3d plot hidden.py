import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Set up display
width, height = 1024, 768
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('3D Function Plot')

# Constants
scale = 30  # Base scale for the x, y, and z axes
fov = 500  # Field of view
step_size = 0.01  # How much x and y increase between each point
angle_shift = math.pi / 18  # Angle shift per key press (10 degrees)
zoom_factor = 1.1  # Zoom factor per key press
light_direction = pygame.math.Vector3(1, -1, 1).normalize()  # Example light direction

# Initial parameters
angle_x = math.pi / 4  # Initial x-axis rotation
angle_y = math.pi / 4  # Initial y-axis rotation
current_scale = scale

def perspective_project(x, y, z):
    # Rotate and project coordinates as before
    y_rotated = y * math.cos(angle_x) - z * math.sin(angle_x)
    z_rotated = y * math.sin(angle_x) + z * math.cos(angle_x)
    x_rotated = x * math.cos(angle_y) + z_rotated * math.sin(angle_y)
    z_final = z_rotated * math.cos(angle_y) - x * math.sin(angle_y)
    factor = fov / (fov + z_final)
    x_proj = x_rotated * factor
    y_proj = y_rotated * factor
    return x_proj, y_proj

def calculate_normal(x, y, func):
    # Calculate the normal vector at the point (x, y) by using nearby points
    h = 0.01
    z_center = func(x, y)
    z_xplus = func(x + h, y)
    z_yplus = func(x, y + h)
    normal = pygame.math.Vector3(h, 0, z_xplus - z_center).cross(pygame.math.Vector3(0, h, z_yplus - z_center)).normalize()
    return normal

def func(x, y):
    # This function needs to match the one used in the main loop
    
    return math.sin(10 * (x**2 + y**2)) / 10
	#return (x**2+y**2)**.5
	#return (math.sin(5*x)*math.cos(5*y))/5
	#return (0.4**2-(0.6-(x**2+y**2)**0.5)**2)**0.5
	#return x*y**3-y*x**3
	#return 1/(15*-(x**2+y**2))
	#return (x**2+3*y**2)*math.e**(-x**2-y**2)
	#return math.cos(abs(x)+abs(y))
	#return -1/(x**2+y**2)
    #return math.cos(abs(x) + abs(y)) * (abs(x) + abs(y))
    

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                angle_y -= angle_shift
            elif event.key == pygame.K_RIGHT:
                angle_y += angle_shift
            elif event.key == pygame.K_UP:
                angle_x += angle_shift
            elif event.key == pygame.K_DOWN:
                angle_x -= angle_shift
            elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                current_scale *= zoom_factor
            elif event.key == pygame.K_MINUS:
                current_scale /= zoom_factor

    screen.fill((0, 0, 0))  # Fill the screen with black

    # Generate points and plot them with shading based on lighting
    x = -1
    while x <= 1:
        y = -1
        while y <= 1:
            z = func(x, y)
            normal = calculate_normal(x, y, func)
            light_intensity = max(0, normal.dot(light_direction))  # Ensure non-negative intensity
            color_intensity = int(128 + 127 * light_intensity)  # Scale color from 128 to 255
            color = (color_intensity, 0, color_intensity)  # Purple shades

            x_scaled, y_scaled, z_scaled = x * current_scale, y * current_scale, z * current_scale
            x2d, y2d = perspective_project(x_scaled, y_scaled, z_scaled)

            x_screen = int(width / 2 + x2d)
            y_screen = int(height / 2 - y2d)

            pygame.draw.circle(screen, color, (x_screen, y_screen), 2)

            y += step_size
        x += step_size

    pygame.display.flip()
    pygame.time.wait(10)

pygame.quit()
sys.exit()
