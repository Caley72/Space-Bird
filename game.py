import pygame
import random
import os
import time

# Initialize pygame
pygame.init()

# Define constants
WIDTH, HEIGHT = 800, 600
FPS = 60
GRAVITY = 0.5
SPACESHIP_SPEED = 10
METEOR_SPEED = 5
METEOR_FREQUENCY = 25  # Every 25 frames a meteor will appear

# Load fonts
font = pygame.font.SysFont("Arial", 30)

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger - SpaceShip")

# Load images (You need to have these images)
background = pygame.image.load('Images/space.jpg')  # Your space background
spaceship_img = pygame.image.load('Images/circle-ship.png')  # Your spaceship image
meteor_img = pygame.image.load('Images/asteroid.png')  # Your meteor image

# Scale the images
spaceship_img = pygame.transform.scale(spaceship_img, (50, 50))
meteor_img = pygame.transform.scale(meteor_img, (50, 50))

# Space ship class
class Spaceship:
    def __init__(self):
        self.x = 100
        self.y = HEIGHT // 2
        self.vel_y = 0
        self.rect = spaceship_img.get_rect(center=(self.x, self.y))
    
    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.vel_y = -SPACESHIP_SPEED
        else:
            self.vel_y += GRAVITY
        self.y += self.vel_y
        self.rect.y = self.y
    
    def draw(self):
        screen.blit(spaceship_img, self.rect.topleft)

# Meteor class
class Meteor:
    def __init__(self):
        self.x = random.randint(WIDTH, WIDTH + 100)
        self.y = random.randint(50, HEIGHT - 50)
        self.rect = meteor_img.get_rect(center=(self.x, self.y))
    
    def move(self):
        self.x -= METEOR_SPEED
        self.rect.x = self.x
    
    def draw(self):
        screen.blit(meteor_img, self.rect.topleft)

# Score and Highscore handling
def load_high_score():
    if os.path.exists("high_score.txt"):
        with open("high_score.txt", "r") as f:
            return int(f.read())
    return 0

def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

# Game loop
def game_loop():
    spaceship = Spaceship()
    meteors = []
    clock = pygame.time.Clock()
    score = 0
    high_score = load_high_score()

    run_game = True
    while run_game:
        screen.fill((0, 0, 0))  # Clear screen with black
        screen.blit(background, (0, 0))  # Draw background
        
        spaceship.move()  # Move the spaceship
        spaceship.draw()  # Draw the spaceship
        
        # Meteor spawning
        if random.randint(1, METEOR_FREQUENCY) == 1:
            meteors.append(Meteor())
        
        # Move and draw meteors
        for meteor in meteors[:]:
            meteor.move()
            meteor.draw()
            if meteor.rect.right < 0:
                meteors.remove(meteor)
            # Collision detection
            if spaceship.rect.colliderect(meteor.rect):
                run_game = False
        
        # Increase score
        score += 1
        
        # Draw score and highscore
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))
        
        high_score_text = font.render(f"High Score: {high_score}", True, (255, 255, 255))
        screen.blit(high_score_text, (WIDTH - 200, 10))
        
        # Update the high score if needed
        if score > high_score:
            high_score = score
        
        # Check for quit events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run_game = False
        
        pygame.display.update()  # Update screen
        clock.tick(FPS)  # Set the game frame rate

    # Save high score if needed
    if score > high_score:
        save_high_score(score)

    # Game over screen
    game_over_text = font.render("GAME OVER", True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - 100, HEIGHT // 2 - 30))
    pygame.display.update()
    time.sleep(2)  # Show game over screen for a moment

# Main entry point
if __name__ == "__main__":
    game_loop()
    pygame.quit()
