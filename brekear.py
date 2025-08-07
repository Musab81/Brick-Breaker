import pygame, sys, random

class Block(pygame.sprite.Sprite):
	def __init__(self,path,x_pos,y_pos):
		super().__init__()
		self.image = pygame.image.load(path)
		self.rect = self.image.get_rect(center = (x_pos,y_pos))
		
class Paddle(Block):
    def __init__(self, path, x_pos, y_pos,speed,movement):
        super().__init__(path, x_pos, y_pos)
        original_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (140, 15))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed =speed
        self.movement = movement
    def screen_constrain(self):
        if self.rect.left <= 0:
            self.rect.left = 0
        if self.rect.right >= screen_width:
            self.rect.right = screen_width
    def update(self):
        self.rect.x += self.movement
        self.screen_constrain()

class Ball(Block):
    def __init__(self, path, x_pos, y_pos,speed,paddles,bricks_group):
        super().__init__(path, x_pos, y_pos)
        original_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (30,30))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
        self.speed = speed
        self.movement_x = 0
        self.movement_y = 0
        self.paddles = paddles
        self.bricks_group=bricks_group
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.active = False
        self.p_time = 0
    def ball_reset(self):
        if self.rect.bottom >= screen_height:
            self.active = False
            self.p_time = pygame.time.get_ticks()
    def ball_restart(self):
        current_time = pygame.time.get_ticks()
        countdown_number = 3
        if not(self.active): 
            if current_time - self.p_time < 700:
                countdown_number = 3
            elif current_time - self.p_time <1400:
                countdown_number = 2
            elif current_time - self.p_time<2100:
                countdown_number = 1
            if current_time - self.p_time <2100:
                self.rect.center = (self.x_pos,self.y_pos)
                self.movement_x = 0
                self.movement_y = 0
            else:
                self.movement_x = self.speed * random.choice((-1,1))
                self.movement_y = -self.speed
                self.active = True
            time_counter = basic_font.render(str(countdown_number),True,accent_color)
            screen.blit(time_counter,(screen_width/2,screen_height/2))
    def collisions(self):
        if self.rect.top <= 0:
            self.movement_y *= -1
        if self.rect.left <=0 or self.rect.right >= screen_width:
            self.movement_x *= -1
        
        if (pygame.sprite.spritecollide(self,self.paddles,False)):
            collision_paddle = pygame.sprite.spritecollide(self,self.paddles,False)[0].rect
            if abs(self.rect.left - collision_paddle.right) < 15 and self.movement_x > 0:
                self.movement_x *= -1
            if abs(self.rect.right - collision_paddle.left) < 15 and self.movement_x < 0 :
                self.movement_x *= -1
            if abs(self.rect.bottom - collision_paddle.top) < 15 and self.movement_y > 0:
                self.movement_y *= -1
            if abs(self.rect.top - collision_paddle.bottom) < 15 and self.movement_y < 0:
                self.movement_y *= -1 
        if (pygame.sprite.spritecollide(self,self.bricks_group,True)):
            self.movement_y *= -1
    

    def update(self):
        if self.rect.top > screen_height:
            self.ball_reset()
        self.ball_restart()
        self.collisions()
        self.rect.x += self.movement_x
        self.rect.y += self.movement_y
        

class Bricks(Block):
    def __init__(self, path, x_pos, y_pos):
        super().__init__(path, x_pos, y_pos)
        original_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (50, 32))
        self.rect = self.image.get_rect(center=(x_pos, y_pos))
    def update(self):
        pass
            
class lives(Block):
    def __init__(self, path, x_pos, y_pos,lives):
        super().__init__(path, x_pos, y_pos)
        original_image = pygame.image.load(path).convert_alpha()
        self.image = pygame.transform.scale(original_image, (40, 40))
        # self.lives=lives
        # self.deaths=0
    def update(self):
        # if self.deaths >0:
        #     self.lives -= self.deaths
        #     self.deaths=0
        pass


class GameManager():
    def __init__(self,paddle_group,ball_group,lives_group,brick_group):
        self.paddle_group = paddle_group
        self.ball_group = ball_group
        self.lives_group = lives_group
        self.brick_group = brick_group
        self.ball= self.ball_group.sprite
        self.p_time=0

    def handle_lives(self):
        self.current_time = pygame.time.get_ticks()

        if self.ball.rect.bottom >= screen_height:
            if not self.flag:
                # First time ball touches bottom
                self.p_time = pygame.time.get_ticks()
                self.flag = True

                if len(self.lives_group) > 0:
                    self.lives_group.remove(list(self.lives_group)[-1])
            else:
                # Ball is still at the bottom, wait before quitting
                if len(self.lives_group) == 0:
                    pygame.quit()
                    sys.exit()
        else:
            # Reset flag once ball is above screen again
            self.flag = False


    def run_game(self):
        self.brick_group.draw(screen)
        self.lives_group.draw(screen)
        self.paddle_group.draw(screen)
        self.ball_group.draw(screen)

        self.brick_group.update()
        # self.lives_group.update(screen)
        self.paddle_group.update()
        self.ball_group.update()
        self.handle_lives()


#----------------------------
pygame.init()
clock=pygame.time.Clock()

screen_width = 1000
screen_height = 600
screen=pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("Brick Breaker")
#----------------------------
basic_font = pygame.font.Font('freesansbold.ttf', 100)
accent_color = (27,35,43)
col=64


#Game objects
paddle=Paddle("brick breaker/paddle.png",screen_width/2,screen_height-50,7,0)
paddle_group = pygame.sprite.GroupSingle()
paddle_group.add(paddle)

brick_group = pygame.sprite.Group()
brick=[[None for _ in range(20)] for _ in range(6)]
for i in range(6):
    for j in range(4):
        brick[i][j]=Bricks("brick breaker/brick(blue).png",(j+0.5)*50,col+(32*i))
        brick_group.add(brick[i][j])

        brick[i][j+4]=Bricks("brick breaker/brick(Green).png",(j+4.5)*50,col+(32*i))
        brick_group.add(brick[i][j+4])

        brick[i][j+8]=Bricks("brick breaker/brick(orange).png",(j+8.5)*50,col+(32*i))
        brick_group.add(brick[i][j+8])

        brick[i][j+12]=Bricks("brick breaker/brick(purple).png",(j+12.5)*50,col+(32*i))
        brick_group.add(brick[i][j+12])

        brick[i][j+16]=Bricks("brick breaker/brick(red).png",(j+16.5)*50,col+(32*i))
        brick_group.add(brick[i][j+16])

ball=Ball("brick breaker/Ball.png",screen_width/2-50,screen_height-150,4,paddle_group,brick_group)
ball_group = pygame.sprite.GroupSingle()
ball_group.add(ball)

lives_group = pygame.sprite.Group()
live=[None for _ in range(3)]
for i in range(3):
    live[i] = lives("brick breaker/lives.jpeg",50*(i+1.7),70,3)
    lives_group.add(live[i])

Game_manager = GameManager(paddle_group,ball_group,lives_group,brick_group)

while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                paddle.movement += 7
            if event.key == pygame.K_LEFT:
                paddle.movement -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                paddle.movement -=7
            if event.key == pygame.K_LEFT:
                paddle.movement += 7
    

    screen.fill((0,0,0))

    Game_manager.run_game()
    pygame.display.flip()
    clock.tick(60)
