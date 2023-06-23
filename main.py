import pygame
import random
import math

# Initialize Pygame
pygame.init()

# Game window dimensions
WIDTH = 800
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game window
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tower Defense")


# Player class
class Player:
    def __init__(self):
        self.lives = 1
        self.gold = 20
        self.font = pygame.font.Font(None, 30)

    def draw(self):
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        gold_text = self.font.render(f"Gold: {self.gold}", True, WHITE)
        win.blit(lives_text, (10, 10))
        win.blit(gold_text, (10, 40))


# Enemy class
class Enemy:
    def __init__(self):
        self.x = 0
        self.y = HEIGHT // 2
        self.width = 20
        self.height = 20
        self.vel = 1  # Slower movement speed
        self.health = 10
        self.max_health = self.health
        self.y_direction = 0  # Initialize y-coordinate direction
        self.y_change_timer = random.uniform(1, 3)  # Random initial change timer
        self.y_change_delay = random.uniform(1, 3)  # Random initial change delay
        self.cooldown = 0

    def move(self):
        self.x += self.vel

        # Update y-coordinate direction and timer
        self.y_change_timer += clock.get_time() / 1000.0  # Convert milliseconds to seconds
        if self.y_change_timer >= self.y_change_delay:
            self.y_direction = random.uniform(-1, 1)  # Randomize y-coordinate direction
            self.y_change_timer = 0  # Reset the timer
            self.y_change_delay = random.uniform(1, 3)  # Randomize the change delay

        self.y += self.y_direction * self.vel

        # Ensure enemy stays within the screen boundaries
        self.y = max(self.y, 0)
        self.y = min(self.y, HEIGHT - self.height)

    def shoot(self, towers, bullets):
        if self.cooldown <= 0:
            nearest_tower = self.get_nearest_tower(towers)
            if nearest_tower:
                bullet = Bullet(self.x + self.width / 2, self.y + self.height / 2, nearest_tower,
                                10)  # Change the damage to 5 or any other value you want
                bullets.append(bullet)
                self.cooldown = 60  # Reset the cooldown
        else:
            self.cooldown -= 1

    def get_nearest_tower(self, towers):
        nearest_tower = None
        shortest_distance = float('inf')
        for tower in towers:
            distance = ((self.x - tower.x) ** 2 + (self.y - tower.y) ** 2) ** 0.5
            if distance < shortest_distance:
                shortest_distance = distance
                nearest_tower = tower
        return nearest_tower

    def draw(self):
        pygame.draw.rect(win, RED, (self.x, self.y, self.width, self.height))
        self.draw_health_bar()

    def reached_end(self):
        return self.x >= WIDTH

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 5
        health_bar_x = self.x
        health_bar_y = self.y - 10

        fill_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(win, GREEN, (health_bar_x, health_bar_y, fill_width, bar_height))
        pygame.draw.rect(win, WHITE, (health_bar_x, health_bar_y, bar_width, bar_height), 1)


class Bullet:
    def __init__(self, x, y, target, damage):
        self.x = x
        self.y = y
        self.target = target
        self.damage = damage
        self.vel = 5
        self.radius = 5

    def draw(self):
        pygame.draw.circle(win, BLUE, (int(self.x), int(self.y)), self.radius)

    def move(self):
        direction = (self.target.x - self.x, self.target.y - self.y)
        distance = math.hypot(direction[0], direction[1])
        direction = (direction[0] / distance, direction[1] / distance)
        self.x += direction[0] * self.vel
        self.y += direction[1] * self.vel

    def hit(self):
        return math.hypot(self.target.x - self.x, self.target.y - self.y) < self.radius


# Tower class
class Tower:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 35
        self.range = 150
        self.damage = 1
        self.health = 100
        self.max_health = self.health
        self.cooldown = 0

    def draw(self):
        pygame.draw.rect(win, GREEN, (self.x, self.y, self.width, self.height))
        self.draw_health_bar()

    def draw_health_bar(self):
        bar_width = self.width
        bar_height = 5
        health_bar_x = self.x
        health_bar_y = self.y - 10

        fill_width = (self.health / self.max_health) * bar_width
        pygame.draw.rect(win, GREEN, (health_bar_x, health_bar_y, fill_width, bar_height))
        pygame.draw.rect(win, WHITE, (health_bar_x, health_bar_y, bar_width, bar_height), 1)

    def shoot(self, enemies, bullets):
        if self.cooldown <= 0:
            for enemy in enemies:
                if self.is_within_range(enemy):
                    bullet = Bullet(self.x + self.width / 2, self.y + self.height / 2, enemy, self.damage)
                    bullets.append(bullet)
                    self.cooldown = 30
                    break
        else:
            self.cooldown -= 1

    def is_within_range(self, enemy):
        distance = ((self.x - enemy.x) ** 2 + (self.y - enemy.y) ** 2) ** 0.5
        return distance <= self.range


# Create objects
player = Player()
enemies = [Enemy()]
towers = []
bullets = []
# Game loop
running = True
clock = pygame.time.Clock()
# Enemy spawn timer
enemy_spawn_timer = 0
enemy_spawn_delay = 500  # Delay in milliseconds (2 seconds)

game_over = False

while running:
    clock.tick(60)  # Frame rate

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if game_over and event.key == pygame.K_y:
                # Restart the game by re-initializing all objects
                player = Player()
                enemies = [Enemy()]
                towers = []
                bullets = []
                game_over = False
        elif event.type == pygame.MOUSEBUTTONDOWN and player.gold >= 10 and not game_over:
            mouse_pos = pygame.mouse.get_pos()
            tower = Tower(mouse_pos[0], mouse_pos[1])
            towers.append(tower)
            player.gold -= 10

    if not game_over:
        # Enemies actions
        for enemy in enemies:
            enemy.move()
            enemy.shoot(towers, bullets)

            # Check if enemy reaches the right wall
            if enemy.reached_end():
                player.lives -= 1
                enemies.remove(enemy)

        # Shoot bullets from towers
        for tower in towers:
            tower.shoot(enemies, bullets)

        # Move bullets and check for collisions
        for bullet in bullets:
            bullet.move()
            if bullet.hit():
                bullet.target.health -= bullet.damage
                bullets.remove(bullet)

        # Remove defeated enemies
        enemies = [enemy for enemy in enemies if enemy.health > 0]

        # Remove defeated towers
        towers = [tower for tower in towers if tower.health > 0]

        # Check if all enemies are defeated or player's lives are depleted
        if player.lives <= 0:
            game_over = True

        # Spawn new enemy
        if not game_over:
            enemy_spawn_timer += clock.get_rawtime()
            if enemy_spawn_timer >= enemy_spawn_delay:
                enemy = Enemy()
                enemies.append(enemy)
                enemy_spawn_timer = 0

                # Randomize enemy spawn delay for the next enemy
                enemy_spawn_delay = random.randint(20, 600)  # Random delay between 2 to 5 seconds (in milliseconds)

    # Draw the game window
    win.fill((0, 0, 0))  # Clear the screen

    # Draw enemies
    for enemy in enemies:
        enemy.draw()

    # Draw towers
    for tower in towers:
        tower.draw()

    # Move bullets and check for collisions
    for bullet in bullets:
        bullet.draw()
        bullet.move()
        if bullet.hit():
            bullet.target.health -= bullet.damage
            if bullet.target.health <= 0:
                player.gold += 10  # Increase gold count for each enemy kill
            bullets.remove(bullet)

    # Draw player stats
    player.draw()

    # Draw result text
    font = pygame.font.Font(None, 50)
    result_text = "YOU LOSE" if game_over else ""
    result_surface = font.render(result_text, True, WHITE)
    result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    win.blit(result_surface, result_rect)

    if game_over:
        font = pygame.font.Font(None, 30)
        restart_text = "Press Y to restart"
        restart_surface = font.render(restart_text, True, WHITE)
        restart_rect = restart_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 40))
        win.blit(restart_surface, restart_rect)

    # Update the game window
    pygame.display.update()
