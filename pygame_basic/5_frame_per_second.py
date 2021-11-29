import pygame

pygame.init()#초기화하는 작업- 반드시 필요

#게임 화면 크기 설정
screen_width=580
screen_height=640
screen=pygame.display.set_mode((screen_width,screen_height)) #화면 크기 설정

#화면 타이틀 설정
pygame.display.set_caption("My Game") #게임 이름

#fps - 프레임 수가 많으면 좀 더 부드러움
clock=pygame.time.Clock()

#배경화면 정하기- 배경 이미지 불러오기
background=pygame.image.load('./background.png')

#캐릭터 불러오기
character=pygame.image.load('./main.png')
character_size=character.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
character_width=character_size[0] #가로크기
character_height=character_size[1] #세로크기

character_x_pos=(screen_width/2)-(character_width/2) #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
character_y_pos=screen_height-character_height #화면은 아래쪽으로 갈 수록 +임 #y좌표

#이동할 좌표
to_x=0
to_y=0

#fps에 맞추기 위한 이동속도
character_speed=0.6

#이벤트루프 - 사용자가 입력하기 전에 꺼지는 등 종료되지 않고 기다리도록 설정
running=True #현재 게임이 진행중인지
while running:
    dt=clock.tick(60)#원하는 화면의 초당 프레임 수 설정
    for event in pygame.event.get(): #사용자 입력- 마우스나 키보드 입력이 들어오는지 계속 체크함
        if event.type==pygame.QUIT: #우측 상단의 x버튼 눌렀을 때
            running=False

        if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
            if event.key==pygame.K_LEFT: #캐릭터를 왼쪽으로
                to_x-=character_speed
            elif event.key==pygame.K_RIGHT:
                to_x+=character_speed
            elif event.key==pygame.K_UP:
                to_y-=character_speed
            elif event.key==pygame.K_DOWN:
                to_y+=character_speed

        if event.type==pygame.KEYUP: #방향키를 떼면 멈춤
            if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT: #즉 왼쪽키나 오른쪽 키를 누르고 있다가 뗀 거면
                to_x=0
            elif event.key == pygame.K_DOWN or event.key==pygame.K_UP:
                to_y=0
    
    character_x_pos+=to_x *dt
    character_y_pos+=to_y *dt

    #가로 경계값의 처리
    if character_x_pos < 0:#화면의 왼쪽 밖으로 나가면
        character_x_pos=0
    elif character_x_pos > screen_width-character_width : #화면 오른쪽 밖으로 나가게 됨
        character_x_pos=screen_width-character_width

    #세로 경계값 처리
    if character_y_pos < 0: #화면 위 밖으로 나가면
        character_y_pos=0
    elif character_y_pos>screen_height-character_height: #화면 아래 밖으로 나가면
        character_y_pos=screen_height-character_height



    
    #screen.fill(0,0,25) #r,g,b를 이용해서 색으로 채울 수도 있음
    screen.blit(background,(0,0)) #blit: 배경을 그리는 역할
    screen.blit(character,(character_x_pos,character_y_pos)) #캐릭터 그리기
    pygame.display.update() #얘를 통해 화면을 계속 새롭게(?) 그림, 게임 화면 다시 그리기

#그리고 while문 벗어나면 - 즉 running이 false이면 pygame 종료
pygame.quit()