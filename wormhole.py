import pygame
import math
import colorsys
import random

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 400
FPS = 60
NUM_LAYERS = 30
MAX_RADIUS = 300

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class WormholeVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Wormhole Visualizer")
        self.clock = pygame.time.Clock()
        
        # Wormhole properties
        self.shapes = ["circle", "square", "triangle", "hexagon", "octagon", "star"]
        self.current_shape = 0
        self.base_hue = 0.5  # Starting hue (cyan)
        self.time_offset = 0
        self.mouse_x = WINDOW_SIZE // 2
        self.mouse_y = WINDOW_SIZE // 2
        
        # Animation properties
        self.layer_speeds = [i * 0.5 for i in range(NUM_LAYERS)]
        self.layer_rotations = [0] * NUM_LAYERS
        
    def get_shape_points(self, shape_type, center_x, center_y, radius, rotation=0):
        """Generate points for different shapes"""
        points = []
        
        if shape_type == "circle":
            # For circles, we'll use pygame.draw.circle instead
            return None
            
        elif shape_type == "square":
            half_size = radius * 0.7
            corners = [
                (-half_size, -half_size),
                (half_size, -half_size),
                (half_size, half_size),
                (-half_size, half_size)
            ]
            
        elif shape_type == "triangle":
            angles = [0, 120, 240]
            corners = []
            for angle in angles:
                rad = math.radians(angle)
                x = radius * math.cos(rad)
                y = radius * math.sin(rad)
                corners.append((x, y))
                
        elif shape_type == "hexagon":
            angles = [i * 60 for i in range(6)]
            corners = []
            for angle in angles:
                rad = math.radians(angle)
                x = radius * math.cos(rad)
                y = radius * math.sin(rad)
                corners.append((x, y))
                
        elif shape_type == "octagon":
            angles = [i * 45 for i in range(8)]
            corners = []
            for angle in angles:
                rad = math.radians(angle)
                x = radius * math.cos(rad)
                y = radius * math.sin(rad)
                corners.append((x, y))
                
        elif shape_type == "star":
            angles = []
            for i in range(10):
                angle = i * 36
                if i % 2 == 0:
                    r = radius
                else:
                    r = radius * 0.5
                rad = math.radians(angle)
                x = r * math.cos(rad)
                y = r * math.sin(rad)
                angles.append((x, y))
            corners = angles
            
        # Apply rotation and translation
        cos_rot = math.cos(math.radians(rotation))
        sin_rot = math.sin(math.radians(rotation))
        
        for x, y in corners:
            rotated_x = x * cos_rot - y * sin_rot
            rotated_y = x * sin_rot + y * cos_rot
            points.append((center_x + rotated_x, center_y + rotated_y))
            
        return points
        
    def hue_to_rgb(self, hue):
        """Convert HSV hue to RGB color"""
        rgb = colorsys.hsv_to_rgb(hue, 1.0, 1.0)
        return tuple(int(c * 255) for c in rgb)
        
    def draw_wormhole_layer(self, layer_index):
        """Draw a single layer of the wormhole"""
        # Calculate layer properties
        progress = layer_index / NUM_LAYERS
        base_radius = MAX_RADIUS * (1 - progress)
        
        # Add pulsing effect
        pulse = math.sin(self.time_offset * 3 + layer_index * 0.5) * 0.2
        radius = base_radius * (1 + pulse)
        
        # Skip if radius is too small
        if radius < 2:
            return
            
        # Calculate position offset based on mouse position
        center_offset_x = (self.mouse_x - WINDOW_SIZE // 2) * progress * 0.3
        center_offset_y = (self.mouse_y - WINDOW_SIZE // 2) * progress * 0.3
        
        center_x = WINDOW_SIZE // 2 + center_offset_x
        center_y = WINDOW_SIZE // 2 + center_offset_y
        
        # Calculate color with hue shift
        hue_shift = progress * 0.3 + self.time_offset * 0.1
        current_hue = (self.base_hue + hue_shift) % 1.0
        
        # Add some brightness variation
        brightness = 0.7 + 0.3 * math.sin(self.time_offset * 2 + layer_index * 0.3)
        rgb = colorsys.hsv_to_rgb(current_hue, 1.0, brightness)
        color = tuple(int(c * 255) for c in rgb)
        
        # Update rotation for this layer
        self.layer_rotations[layer_index] += self.layer_speeds[layer_index]
        
        # Draw the shape
        shape_name = self.shapes[self.current_shape]
        
        if shape_name == "circle":
            pygame.draw.circle(self.screen, color, (int(center_x), int(center_y)), int(radius), 2)
        else:
            points = self.get_shape_points(
                shape_name, center_x, center_y, radius, self.layer_rotations[layer_index]
            )
            if points and len(points) > 2:
                pygame.draw.polygon(self.screen, color, points, 2)
                
    def draw_ui(self):
        """Draw user interface elements"""
        font = pygame.font.Font(None, 36)
        
        # Shape name
        shape_text = font.render(f"Shape: {self.shapes[self.current_shape].capitalize()}", True, WHITE)
        self.screen.blit(shape_text, (10, 10))
        
        # Controls
        controls = [
            "SPACE: Change shape",
            "R/G/B: Change base color",
            "Mouse: Guide wormhole"
        ]
        
        small_font = pygame.font.Font(None, 24)
        for i, control in enumerate(controls):
            text = small_font.render(control, True, WHITE)
            self.screen.blit(text, (10, WINDOW_SIZE - 80 + i * 25))
            
    def handle_events(self):
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.current_shape = (self.current_shape + 1) % len(self.shapes)
                    
                elif event.key == pygame.K_r:
                    self.base_hue = 0.0  # Red
                    
                elif event.key == pygame.K_g:
                    self.base_hue = 0.33  # Green
                    
                elif event.key == pygame.K_b:
                    self.base_hue = 0.66  # Blue
                    
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_x, self.mouse_y = event.pos
                
        return True
        
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            running = self.handle_events()
            
            # Clear screen
            self.screen.fill(BLACK)
            
            # Update time
            self.time_offset += 0.02
            
            # Draw wormhole layers from back to front
            for layer in range(NUM_LAYERS - 1, -1, -1):
                self.draw_wormhole_layer(layer)
                
            # Draw UI
            self.draw_ui()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(FPS)
            
        pygame.quit()

if __name__ == "__main__":
    visualizer = WormholeVisualizer()
    visualizer.run()
