import pygame


pygame.init()#초기화하는 작업- 반드시 필요

#게임 화면 크기 설정
screen_width=480 
screen_height=640
screen=pygame.display.set_mode((screen_width,screen_height)) #화면 크기 설정


#화면 타이틀 설정
pygame.display.set_caption("My Game") #게임 이름


#이벤트루프 - 사용자가 입력하기 전에 꺼지는 등 종료되지 않고 기다리도록 설정
running=True #현재 게임ㅁ이 진행중인지
while running:
    for event in pygame.event.get(): #사용자 입력- 마우스나 키보드 입력이 들어오는지 계속 체크함
        if event.type==pygame.QUIT: #우측 상단의 x버튼 눌렀을 때
            running=False
        


#그리고 while문 벗어나면 - 즉 running이 false이면 pygame 종료
pygame.quit()