import pygame,sys,random

def player_animation():
    player.x += player_speed
    if player.right >=screen_width:
        player.right = screen_width
    if player.left <= 0:
        player.left = 0

def ball_animation():
    global ball_speed_x,ball_speed_y,score,timer_time,lives
    ball.x += ball_speed_x
    ball.y += ball_speed_y
    if ball.colliderect(player) and ball_speed_y>0:
        pygame.mixer.Sound.play(paddle_sound)
        if abs(player.left - ball.right) <15:
            ball_speed_x *= -1
        elif abs(player.right-ball.left)<15:
            ball_speed_x *= -1      
        else:
            ball_speed_y *= -1  
    collision = False

    for i in range(6):
        for o in range(20):
            if brick[i][o] and ball.colliderect(brick[i][o]):
 
                ball_speed_y *= -1
                collision = True
                score +=1000
                break
        if collision:
            break 
    if ball.right >= screen_width or ball.left <= 0:
        pygame.mixer.Sound.play(paddle_sound)
        ball_speed_x *= -1
    if ball.top <= 0 :
        pygame.mixer.Sound.play(paddle_sound)
        ball_speed_y *= -1
    if ball.bottom >= screen_height:

        timer_time=pygame.time.get_ticks()
        ball.center=(screen_width/2-15,screen_height/2-15)
        ball_speed_x = 4*random.choice((-1,1))
        ball_speed_y = -4
        lives -= 1
def ball_restart():
    global ball_speed_x,ball_speed_y,lives,timer_time
    current_time=pygame.time.get_ticks()
    if lives >0:
        if current_time - timer_time <700:
            number_three = timer_font.render("3",True,p_color)
            screen.blit(number_three,(screen_width/2-60,screen_height/2+25))
        elif current_time -timer_time <1400:
            number_two = timer_font.render("2",True,p_color)
            screen.blit(number_two,(screen_width/2-60,screen_height/2+25))
        elif current_time -timer_time <2100:
            number_one = timer_font.render("1",True,p_color)
            screen.blit(number_one,(screen_width/2-60,screen_height/2+25))
        if current_time -timer_time <2100:
            ball.center=(screen_width/2-15,screen_height/2-15)
            ball_speed_x,ball_speed_y = 0,0
        else:
            timer_time=None
            ball_speed_x,ball_speed_y=4*random.choice((-1,1)),-4
def brick_animation():
    for i in range(6):
        for o in range(20):
            if brick[i][o]:
                if ball.colliderect(brick[i][o]):
                        pygame.mixer.Sound.play(brick_sound)
                        brick[i][o]=None
            if brick[i][o]:
                pygame.draw.rect(screen,add_colors[o],brick[i][o])

def lives_animation():
    if lives >= 0:
        if lives == 3:
            pygame.draw.ellipse(screen,p_color,circle_1)
            pygame.draw.ellipse(screen,p_color,circle_2)
            pygame.draw.ellipse(screen,p_color,circle_3)
        if lives ==2:
            pygame.draw.ellipse(screen,p_color,circle_1)
            pygame.draw.ellipse(screen,p_color,circle_2)
        if lives == 1:
            pygame.draw.ellipse(screen,p_color,circle_1)
    if not(lives >0):
        current_time = pygame.time.get_ticks()
        game_over= timer_font.render("GAME OVER !!!!",True,p_color)
        screen.blit(game_over,(screen_width/2-420,screen_height/2+25))
        pygame.mixer.Sound.play(game_over_sound)
        if current_time - timer_time >2100:
            pygame.quit()
            sys.exit()




brick = [[None for _ in range(20)] for _ in range(6)]
add_colors = [None for _ in range(20)]

col=64


c=pygame.Color
colors=[
    c('red'),
    c('green'),
    c('blue'),
    c('yellow'),
    c('purple'),
    c('brown'),
    c('red'),
    c('cyan'),
    c('pink'),
    c('white')
]
for i in range(10):
    add_colors[i]=colors[i]
    add_colors[i+10]=colors[i]




p_color=c('gray61')
for i in range(6):
    for o in range(20):
        brick[i][o]=pygame.Rect(o*50,col+(32*i),50,32)

player = pygame.Rect(screen_width/2-80,screen_height-50,140,15)
ball = pygame.Rect(screen_width/2-50,screen_height/2-15,30,30)
circle_1 =pygame.Rect(0,17,40,40) 
circle_2 =pygame.Rect(50,17,40,40) 
circle_3 =pygame.Rect(100,17,40,40) 

player_speed = 0
ball_speed_x = 4*random.choice((-1,1))
ball_speed_y = -4

lives = 3 
score = 000000
score_font = pygame.font.Font("freesansbold.ttf",75)
timer_font = pygame.font.Font("freesansbold.ttf",100)
timer_time = True

brick_sound=pygame.mixer.Sound("brick breaker/brick.mp3")
paddle_sound=pygame.mixer.Sound("brick breaker/paddle.mp3")
game_over_sound=pygame.mixer.Sound("brick breaker/game_over.mp3")


while True:
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player_speed += 7
            if event.key == pygame.K_LEFT:
                player_speed -= 7
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                player_speed -=7
            if event.key == pygame.K_LEFT:
                player_speed += 7

    player_animation()
    if lives>0:
        ball_animation()
   
    

    screen.fill((0,0,0))
    brick_animation()
    for i in range(1,7):
        pygame.draw.line(screen,(0,0,0),(0,(i*32)+32),(screen_width,(i*32)+32),3)
    pygame.draw.rect(screen,(p_color),player)
    pygame.draw.ellipse(screen,p_color,ball)
    if timer_time:
        ball_restart()
    
    lives_animation()

    score_text = score_font.render(f"{score}",True,p_color)
    screen.blit(score_text,(screen_width/2-130,0))
    pygame.display.flip()
    clock.tick(60)
