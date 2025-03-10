import pygame
import math
import random
from constants import *

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([BALL_RADIUS * 2, BALL_RADIUS * 2], pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (BALL_RADIUS, BALL_RADIUS), BALL_RADIUS)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = INITIAL_BALL_SPEED
        # Initialize with a random angle between 45 and 135 degrees (upward)
        angle = random.randint(45, 135)
        self.dx = self.speed * math.cos(math.radians(angle))
        self.dy = -self.speed * math.sin(math.radians(angle))
        self.exact_x = float(x)
        self.exact_y = float(y)
        self.active = False  # Ball starts inactive (attached to paddle)

    def update(self):
        if not self.active:
            return
            
        # Update position based on velocity
        self.exact_x += self.dx
        self.exact_y += self.dy
        self.rect.x = int(self.exact_x - BALL_RADIUS)
        self.rect.y = int(self.exact_y - BALL_RADIUS)
        
        # Check for wall collisions
        if self.rect.left <= 0:
            self.exact_x = BALL_RADIUS
            self.dx = abs(self.dx)  # Bounce right
        
        if self.rect.right >= SCREEN_WIDTH:
            self.exact_x = SCREEN_WIDTH - BALL_RADIUS
            self.dx = -abs(self.dx)  # Bounce left
        
        if self.rect.top <= 0:
            self.exact_y = BALL_RADIUS
            self.dy = abs(self.dy)  # Bounce down

    def reset(self, x, y):
        """Reset ball to initial position and state"""
        self.rect.center = (x, y)
        self.exact_x = float(x)
        self.exact_y = float(y)
        self.speed = INITIAL_BALL_SPEED
        angle = random.randint(45, 135)
        self.dx = self.speed * math.cos(math.radians(angle))
        self.dy = -self.speed * math.sin(math.radians(angle))
        self.active = False
    
    def launch(self):
        """Activate the ball movement"""
        self.active = True

    def increase_speed(self):
        """Increase ball speed with each block hit"""
        if self.speed < MAX_BALL_SPEED:
            self.speed += BALL_ACCELERATION
            # Maintain direction while increasing speed
            angle = math.atan2(-self.dy, self.dx)
            self.dx = self.speed * math.cos(angle)
            self.dy = -self.speed * math.sin(angle)

class Paddle(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.width = PADDLE_WIDTH
        self.height = PADDLE_HEIGHT
        self.image = pygame.Surface([self.width, self.height])
        self.image.fill(CYAN)
        
        # Position the paddle at the bottom center of the screen
        x = (SCREEN_WIDTH - self.width) // 2
        y = SCREEN_HEIGHT - PADDLE_MARGIN_BOTTOM - self.height
        self.rect = self.image.get_rect(topleft=(x, y))
        
        self.speed = PADDLE_SPEED
        self.direction = 0  # 0: stationary, -1: left, 1: right

    def update(self):
        # Move the paddle based on direction
        self.rect.x += self.speed * self.direction
        
        # Keep paddle within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
    
    def move_left(self):
        self.direction = -1
    
    def move_right(self):
        self.direction = 1
    
    def stop(self):
        self.direction = 0
        
    def handle_ball_collision(self, ball):
        """Handle ball collision with the paddle with realistic physics"""
        if ball.rect.bottom >= self.rect.top and ball.rect.top <= self.rect.bottom:
            if ball.rect.right >= self.rect.left and ball.rect.left <= self.rect.right:
                # Calculate where on the paddle the ball hit (0 to 1, from left to right)
                hit_pos = (ball.rect.centerx - self.rect.left) / self.width
                
                # Map hit position to an angle between 150 (left) and 30 (right) degrees
                angle = 150 - hit_pos * 120
                
                # Set new ball direction based on where it hit the paddle
                ball.exact_y = float(self.rect.top - BALL_RADIUS)
                ball.speed = min(ball.speed + 0.1, MAX_BALL_SPEED)  # Slight speed increase
                ball.dx = ball.speed * math.cos(math.radians(angle))
                ball.dy = -ball.speed * math.sin(math.radians(angle))
                
                # Add a little variation based on paddle movement
                if self.direction != 0:
                    ball.dx += self.direction * 0.5
                
                return True
        return False

class Block(pygame.sprite.Sprite):
    def __init__(self, x, y, color, points=SCORE_PER_BLOCK, strength=1):
        super().__init__()
        self.image = pygame.Surface([BLOCK_WIDTH, BLOCK_HEIGHT])
        self.image.fill(color)
        self.rect = self.image.get_rect(topleft=(x, y))
        self.points = points
        self.strength = strength  # How many hits needed to break the block
        self.color = color
        self.original_color = color
    
    def hit(self):
        """Process a hit on the block, return True if block is destroyed"""
        self.strength -= 1
        
        # If block is not destroyed, change its appearance
        if self.strength > 0:
            # Make the block slightly darker
            r, g, b = self.color
            self.color = (max(r-30, 0), max(g-30, 0), max(b-30, 0))
            self.image.fill(self.color)
            return False
        return True  # Block destroyed
