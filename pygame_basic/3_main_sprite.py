import pygame


pygame.init()#초기화하는 작업- 반드시 필요

#게임 화면 크기 설정
screen_width=580
screen_height=640
screen=pygame.display.set_mode((screen_width,screen_height)) #화면 크기 설정

#화면 타이틀 설정
pygame.display.set_caption("My Game") #게임 이름

#배경화면 정하기- 배경 이미지 불러오기
background=pygame.image.load('./background.png')

#캐릭터 불러오기
character=pygame.image.load('./main.png')
character_size=character.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
character_width=character_size[0] #가로크기
character_height=character_size[1] #세로크기

character_x_pos=(screen_width/2)-(character_width/2) #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
character_y_pos=screen_height-character_height #화면은 아래쪽으로 갈 수록 +임 #y좌표

#이벤트루프 - 사용자가 입력하기 전에 꺼지는 등 종료되지 않고 기다리도록 설정
running=True #현재 게임이 진행중인지
while running:
    for event in pygame.event.get(): #사용자 입력- 마우스나 키보드 입력이 들어오는지 계속 체크함
        if event.type==pygame.QUIT: #우측 상단의 x버튼 눌렀을 때
            running=False
    
    #screen.fill(0,0,25) #r,g,b를 이용해서 색으로 채울 수도 있음
    screen.blit(background,(0,0)) #blit: 배경을 그리는 역할
    screen.blit(character,(character_x_pos,character_y_pos)) #캐릭터 그리기
    pygame.display.update() #얘를 통해 화면을 계속 새롭게(?) 그림, 게임 화면 다시 그리기

#그리고 while문 벗어나면 - 즉 running이 false이면 pygame 종료
pygame.quit()