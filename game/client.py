import pygame
import random
from time import sleep
import zmq
import sys
import threading
import json

pygame.init()#초기화하는 작업- 반드시 필요
#게임 화면 크기로 줄 변수들
screen_width=780
screen_height=443


#화면 타이틀 설정
pygame.display.set_caption("My Game") #게임 이름



#배경화면 정하기- 배경 이미지 불러오기
background=pygame.image.load('./picture/background.png')

#처음에는 100점에서 출발
score=100

#적 캐릭터 불러오기
enemy=pygame.image.load('./picture/lion.png')
enemy_size=enemy.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
enemy_width=enemy_size[0] #가로크기
enemy_height=enemy_size[1] #세로크기

enemy_x_pos=(screen_width/2)-(enemy_width/2) #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
enemy_y_pos=screen_height-enemy_height-6 #화면은 아래쪽으로 갈 수록 +임 #y좌표

#이동할 위치(좌표)
to_x=0


#적 위치 조작
def consoles(): 
    global enemy_x_pos,enemy_y_pos
    #fps에 맞추기 위한 이동속도
    enemy_speed=0.6
    while True:
        msg=client.recv(1024) #연결된 클라이언트로부터 1024 바이트 데이터 받음
        if(msg.decode()=='right'): #소켓으로부터 받은 데이터가 right면 오른쪽으로 옮김
            enemy_x_pos+=enemy_speed
        elif(msg.decode()=='left'):
            enemy_x_pos-=enemy_speed

def acceptC():
    global client
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    client.bind(('0.0.0.0',5557))
    

    thr=threading.Thread(target=consoles,args=()) #쓰레드가 실행할 함수, 그 함수의 파라미터
    thr.Daemon=True #메인 쓰레드가 종료되면 즉시 종료되는 쓰레드임
    thr.start()

def GameMain():
    global enemy_x_pos,enemy_y_pos,to_x,score
    screen=pygame.display.set_mode((screen_width,screen_height)) #화면 크기 설정
    #fps - 프레임 수가 많으면 좀 더 부드러움
    #fps=pygame.time.Clock()

    img_speed=0.6
    img=pygame.image.load('./picture/lion.png')
    img_size=enemy.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
    img_width=img_size[0] #가로크기
    img_height=img_size[1] #세로크기

    img_x_pos=(screen_width/2)-(enemy_width/2) #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
    img_y_pos=screen_height-enemy_height-6 #화면은 아래쪽으로 갈 수록 +임 #y좌표
    

    #(rock)) 캐릭터
    rock1=pygame.image.load('./picture/rock1.png')
    rock1_size=rock1.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
    rock1_width=rock1_size[0] #가로크기
    rock1_height=rock1_size[1] #세로크기
    #처음에 나타나는 위치
    rock1_x_pos=random.randint(0,screen_width-rock1_width)
    rock1_y_pos=0
    rock1_speed=3.3 #떨어지는 속도
    
    rock2=pygame.image.load('./picture/rock2.png')
    rock2_size=rock2.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
    rock2_width=rock1_size[0] #가로크기
    rock2_height=rock1_size[1] #세로크기

    rock2_x_pos=random.randint(0,screen_width-rock1_width)
    rock2_y_pos=0
    rock2_speed=1 #떨어지는 속도

    rock3=pygame.image.load('./picture/rock3.png')
    rock3_size=rock3.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
    rock3_width=rock3_size[0] #가로크기
    rock3_height=rock3_size[1] #세로크기

    rock3_x_pos=random.randint(0,screen_width-rock1_width)
    rock3_y_pos=0
    rock3_speed=2 #떨어지는 속도

    #게임에 쓸 폰트
    font=pygame.font.Font('./font/비트로 코어 TTF.ttf',30)

    #총 시간 - 제한시간
    total_time=15
    #시작 시간 
    start_ticks=pygame.time.get_ticks() #시작(현재의) tick 정보
    
    clock=pygame.time.Clock()

    #이벤트루프 - 사용자가 입력하기 전에 꺼지는 등 종료되지 않고 기다리도록 설정
    running=True #현재 게임이 진행중인지
    while running:
        dt=clock.tick(85)#원하는 화면의 초당 프레임 수 설정
        for event in pygame.event.get(): #사용자 입력- 마우스나 키보드 입력이 들어오는지 계속 체크함
            if event.type==pygame.QUIT: #우측 상단의 x버튼 눌렀을 때
                running=False
            if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
                if event.key==pygame.K_LEFT: #캐릭터를 왼쪽으로
                    to_x-=img_speed
                    msg="left"
                    client.sendall(msg.encode()) #클라이언트에게 내가 내린 명령 전송
                elif event.key==pygame.K_RIGHT:
                    to_x+=img_speed
                    msg="right"
                    client.sendall(msg.encode())
            if event.type==pygame.KEYUP: #방향키를 떼면 멈춤
                if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT: #즉 왼쪽키나 오른쪽 키를 누르고 있다가 뗀 거면
                    to_x=0
                    #msg="keyup"
                    #client.sendall(msg.encode())

        #게임 캐릭터의 움직인 위치 정의        
        img_x_pos+=to_x*dt

        #가로 경계값의 처리
        if img_x_pos < 0:#화면의 왼쪽 밖으로 나가면
            img_x_pos=0
        elif img_x_pos > screen_width-img_width : #화면 오른쪽 밖으로 나가게 되면
            img_x_pos=screen_width-img_width

        #돌 캐릭터의 움직이는 위치 정의
        rock1_y_pos+=rock1_speed
        rock2_y_pos+=rock2_speed
        rock3_y_pos+=rock3_speed

        #돌의 경계값의 처리
        if rock1_y_pos >screen_height - 70:
            rock1_y_pos=0 #다시 화면 맨 위로 올림
            rock1_x_pos=random.randint(0,screen_width-rock1_width) 
        if rock2_y_pos >screen_height - 70:
            rock2_y_pos=0 #다시 화면 맨 위로 올림
            rock2_x_pos=random.randint(0,screen_width-rock1_width)
        if rock3_y_pos >screen_height - 70:
            rock3_y_pos=0 #다시 화면 맨 위로 올림
            rock3_x_pos=random.randint(0,screen_width-rock1_width)

        #충돌처리를 위한 rect 정보 업데이트
        #게임 객체 (Rect): 크기 정보 + 좌표 정보 가지고 있음, 게임 형체에 따른 상세한 좌표값 부여가 불가능하므로 그냥 사각형모양이라고 퉁치는 거임
        #그리고 이 가상의 사각형에 좌표 정보들을 부여함
        img_rect=img.get_rect()
        img_rect.left=img_x_pos
        img_rect.top=img_y_pos

        rock1_rect=rock1.get_rect()
        rock1_rect.left=rock1_x_pos
        rock1_rect.top=rock1_y_pos

        rock2_rect=rock2.get_rect()
        rock2_rect.left=rock2_x_pos
        rock2_rect.top=rock2_y_pos

        rock3_rect=rock3.get_rect()
        rock3_rect.left=rock3_x_pos
        rock3_rect.top=rock3_y_pos

        is_collision1=False
        is_collision2=False
        is_collision3=False
        is_timeout=False

        #충돌 체크 - colliderect : 사각형을 기준으로 충돌이 있는지ㅣ 확인
        if img_rect.colliderect(rock1_rect):
            print("충돌했습니다!")
            rock1_y_pos=0 #다시 화면 맨 위로 올림
            rock1_x_pos=random.randint(0,screen_width-rock1_width)
            is_collision1=True
            score-=5
        elif(img_rect.colliderect(rock2_rect)):
            print("충돌했습니다!")
            rock2_y_pos=0 #다시 화면 맨 위로 올림
            rock2_x_pos=random.randint(0,screen_width-rock1_width)
            is_collision2=True
            score-=5
        elif(img_rect.colliderect(rock3_rect)):
            print("충돌했습니다!")
            rock3_y_pos=0 #다시 화면 맨 위로 올림
            rock3_x_pos=random.randint(0,screen_width-rock1_width)
            is_collision3=True
            score-=5
            

        collision1=font.render(("충돌했습니다!"),True,(255,0,0))
        collision2=font.render(("점수: "+str(score)),True,(0,0,255))
        
        screen.blit(background,(0,0)) #blit: 배경을 그리는 역할
        screen.blit(img,(img_x_pos,img_y_pos)) #캐릭터 그리기
        screen.blit(rock1,(rock1_x_pos,rock1_y_pos)) 
        screen.blit(rock2,(rock2_x_pos,rock2_y_pos)) 
        screen.blit(rock3,(rock3_x_pos,rock3_y_pos)) 
        

        #타이머 집어넣기
        #경과 시간 계산
        elapsed_time=(pygame.time.get_ticks()-start_ticks) /1000 
        timer=font.render(str(int(total_time-elapsed_time)),True,(225,0,0)) #글자로 써줌, 정수 단위로만 가능하도록 int형을 씌어줌
        #render안에는 str형이 들어와야함
        
        screen.blit(timer,(10,10))
        #만약 남은 시간이 0이 되면 종료
        if total_time-elapsed_time<=0:
            print("타임아웃")
            is_timeout=True
            running=False

        timeout=font.render("최종 점수: "+(str(score)),True,(0,0,255))

        
        if(is_collision1 or is_collision2 or is_collision3):
            screen.blit(collision1,(screen_width/2-85,screen_height/3))
            screen.blit(collision2,(screen_width/2-60,screen_height/2)) #score
        

        if(is_timeout):
            screen.blit(timeout,(screen_width/2-94,screen_height/2+6))


        pygame.display.update()
        if(is_collision1 or is_collision2 or is_collision3):
            sleep(0.3)

    #종료가 너무 빨리 되니까 종료 전 조금 시간 주기
    pygame.time.delay(2000) #2초 정도 대기

    #그리고 while문 벗어나면 - 즉 running이 false이면 pygame 종료
    pygame.quit()     

            

if __name__=='__main__':
    acceptC()
    GameMain()
            
