import pygame
import sys
from constants import *
from sprites import Ball, Paddle, Block
from levels import levels, block_properties

class BounceGame:
    def __init__(self):
        # Initialize pygame
        pygame.init()
        pygame.display.set_caption(TITLE)
        
        # Create the screen
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Game state variables
        self.level = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.level_complete = False
        self.paused = False
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()
        
        # Create paddle
        self.paddle = Paddle()
        self.all_sprites.add(self.paddle)
        
        # Create ball
        ball_x = self.paddle.rect.centerx
        ball_y = self.paddle.rect.top - BALL_RADIUS
        self.ball = Ball(ball_x, ball_y)
        self.all_sprites.add(self.ball)
        
        # Load game font
        self.font = pygame.font.Font(None, 36)
        
        # Start the game with the first level
        self.create_level(self.level)
    
    def create_level(self, level_num):
        """Create blocks for the current level"""
        # Clear any existing blocks
        for block in self.blocks:
            block.kill()
        
        # Make sure level_num is valid
        if level_num >= len(levels):
            level_num = 0  # Loop back to first level
        
        # Get the level layout
        layout = levels[level_num]
        
        # Create blocks based on the layout
        for row_index, row in enumerate(layout):
            for col_index, block_type in enumerate(row):
                if block_type > 0:  # If there's a block at this position
                    # Calculate block position
                    x = col_index * (BLOCK_WIDTH + BLOCK_MARGIN)
                    y = row_index * (BLOCK_HEIGHT + BLOCK_MARGIN) + 50  # Start 50 pixels from the top
                    
                    # Get block properties
                    props = block_properties[block_type]
                    
                    # Create the block
                    block = Block(x, y, props["color"], props["points"], props["strength"])
                    self.blocks.add(block)
                    self.all_sprites.add(block)
        
        # Reset ball and set level state
        self.reset_ball()
        self.level_complete = False
    
    def reset_ball(self):
        """Reset ball position to above the paddle"""
        self.ball.reset(self.paddle.rect.centerx, self.paddle.rect.top - BALL_RADIUS)
    
    def handle_events(self):
        """Handle game events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                if event.key == pygame.K_SPACE and not self.ball.active and not self.game_over:
                    self.ball.launch()
                if event.key == pygame.K_r and self.game_over:
                    self.restart_game()
                if event.key == pygame.K_LEFT:
                    self.paddle.move_left()
                if event.key == pygame.K_RIGHT:
                    self.paddle.move_right()
            
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT and self.paddle.direction == -1:
                    self.paddle.stop()
                if event.key == pygame.K_RIGHT and self.paddle.direction == 1:
                    self.paddle.stop()
        
        return True
    
    def update(self):
        """Update game state"""
        if self.paused or self.game_over or self.level_complete:
            return
        
        # Update all sprites
        self.all_sprites.update()
        
        # Check if ball is below the screen (player loses a life)
        if self.ball.rect.top > SCREEN_HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.game_over = True
            else:
                self.reset_ball()
        
        # Check for ball-paddle collision
        if not self.ball.active:  # If ball is attached to paddle
            # Update ball position to follow paddle
            self.ball.exact_x = float(self.paddle.rect.centerx)
            self.ball.exact_y = float(self.paddle.rect.top - BALL_RADIUS)
            self.ball.rect.center = (self.ball.exact_x, self.ball.exact_y)
        else:  # Ball is active, check for collisions
            self.paddle.handle_ball_collision(self.ball)
            
            # Check for ball-block collisions
            block_hit_list = pygame.sprite.spritecollide(self.ball, self.blocks, False)
            for block in block_hit_list:
                # Increase score
                self.score += block.points
                
                # Increase ball speed slightly
                self.ball.increase_speed()
                
                # Hit the block and remove if destroyed
                if block.hit():
                    block.kill()
                
                # Calculate bounce direction based on which side of the block was hit
                if self.ball.rect.centerx < block.rect.left or self.ball.rect.centerx > block.rect.right:
                    self.ball.dx = -self.ball.dx  # Hit from left or right
                else:
                    self.ball.dy = -self.ball.dy  # Hit from top or bottom
                
                # Only process one block collision per frame (prevents multiple bounces)
                break
            
            # Check if level is complete (no blocks left)
            if len(self.blocks) == 0:
                self.level_complete = True
                self.level += 1
                # Small delay before next level
                pygame.time.set_timer(pygame.USEREVENT, 2000)  # 2 second delay
                pygame.event.post(pygame.event.Event(pygame.USEREVENT))  # Post event immediately
    
    def draw(self):
        """Draw the game screen"""
        # Fill the background
        self.screen.fill(BLACK)
        
        # Draw all sprites
        self.all_sprites.draw(self.screen)
        
        # Draw score and lives
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        level_text = self.font.render(f"Level: {self.level + 1}", True, WHITE)
        
        self.screen.blit(score_text, (20, 10))
        self.screen.blit(lives_text, (SCREEN_WIDTH - 120, 10))
        self.screen.blit(level_text, (SCREEN_WIDTH // 2 - 50, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(game_over_text, text_rect)
        
        # Draw level complete message
        if self.level_complete:
            level_complete_text = self.font.render("LEVEL COMPLETE!", True, GREEN)
            text_rect = level_complete_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(level_complete_text, text_rect)
        
        # Draw pause message
        if self.paused:
            pause_text = self.font.render("PAUSED", True, YELLOW)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
            self.screen.blit(pause_text, text_rect)
        
        # If ball is not active, draw launch instruction
        if not self.ball.active and not self.game_over:
            launch_text = self.font.render("Press SPACE to launch ball", True, WHITE)
            text_rect = launch_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 60))
            self.screen.blit(launch_text, text_rect)
        
        # Update the display
        pygame.display.flip()
    
    def restart_game(self):
        """Restart the game from the beginning"""
        self.level = 0
        self.score = 0
        self.lives = 3
        self.game_over = False
        self.create_level(self.level)
    
    def run(self):
        """Main game loop"""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Handle level completion
            for event in pygame.event.get(pygame.USEREVENT):
                if self.level_complete:
                    self.create_level(self.level)
            
            # Update game state
            self.update()
            
            # Draw the screen
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = BounceGame()
    game.run()
