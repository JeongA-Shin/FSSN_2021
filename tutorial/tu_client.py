# Asynchronous Client/Server Pattern
# Reference: https://zguide.zeromq.org/docs/chapter3/#The-Asynchronous-Client-Server-Pattern
# author of original code: Felipe Cruz <felipecruz@loogica.net>
# license of original code: MIT/X11

import pygame
import random
from time import sleep

import zmq
import sys
import threading
import json


WHITE = (255,255,255)
BLACK = (  0,  0,  0)

RED   = (255,  0,  0)
GREEN = (  0,255,  0)
BLUE  = (  0,  0,255)

YELLOW = (255,255, 0)


def button_create(text, rect, inactive_color, active_color, action):

    font = pygame.font.Font(None, 40)

    button_rect = pygame.Rect(rect)

    text = font.render(text, True, BLACK)
    text_rect = text.get_rect(center=button_rect.center)

    return [text, text_rect, button_rect, inactive_color, active_color, action, False]

def button_check(info, event):

    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if event.type == pygame.MOUSEMOTION:
        # hover = True/False   
        info[-1] = rect.collidepoint(event.pos)

    elif event.type == pygame.MOUSEBUTTONDOWN:
        if hover and action:      
            action()

def button_draw(screen, info):

    text, text_rect, rect, inactive_color, active_color, action, hover = info

    if hover:
        color = active_color
    else:
        color = inactive_color

    pygame.draw.rect(screen, color, rect)
    screen.blit(text, text_rect)

def on_click_button_1():
    global stage
    stage = '1'
    global select
    select=False
    print('1 Player')

def on_click_button_2():
    global stage
    global select
    select=False
    stage = '2'
    print('2 Player')

def on_click_button_3():
    global stage
    #global running
    global select
    select=False
    stage = '3'
    stage_data[2]+=1
    #running = False

    print('3 player')



screen_height=0
screen_width=0
screen=pygame.display.set_mode((screen_width,screen_height))
enemy=pygame.image.load('./picture/peng.png')
enemy_size=enemy.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
enemy_width=enemy_size[0] #가로크기
enemy_height=enemy_size[1] #세로크기
enemy_x_pos=(screen_width/2)-(enemy_width/2)+20 #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
enemy_y_pos=screen_height-enemy_height-6 #화면은 아래쪽으로 갈 수록 +임 #y좌표
enemy2=pygame.image.load('./picture/peng.png')
enemy2_size=enemy2.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
enemy2_width=enemy2_size[0] #가로크기
enemy2_height=enemy2_size[1] #세로크기
enemy2_x_pos=(screen_width/2)-(enemy2_width/2)+20 #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
enemy2_y_pos=screen_height-enemy2_height-6 #화면은 아래쪽으로 갈 수록 +임 #y좌표
is_enemy=False
is_enemy2=False
stage_data=[0,0,0] #각 인덱스는 stage-1, value들은 그 stage를 선택한만큼의 수


#게임에 쓸 폰트
#font=pygame.font.Font('./font/비트로 코어 TTF.ttf',30)

#클라이언트 쓰레드
class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__ (self) #쓰레드를 클래스로 정의할 경우에는 __init__ 함수에서 부모 클래스의 생성자 threading.Thread.__init__(self)를 반드시 호출 !!

    def recvHandler(self):
        global screen
        global screen_height
        global screen_width
        global enemy
        global enemy_size
        global enemy_width
        global enemy_height
        global enemy_x_pos
        global enemy_y_pos
        global enemy2
        global enemy2_size
        global enemy2_width
        global enemy2_height
        global enemy2_x_pos
        global enemy2_y_pos
        global is_enemy
        global is_enemy2
        ident_standard=self.identity 
        while True:
            if(self.subscriber.poll(100)&zmq.POLLIN):
                message=json.loads(self.subscriber.recv())
                if('clientNum' in message):
                    global clientNum
                    clientNum=message['clientNum'] 
                elif ('s1' in message):
                    global stage_data
                    stage_data[0]=message['s1']
                    stage_data[1]=message['s2']
                    stage_data[2]=message['s3']
                else:
                    if(message['ident'] != self.identity): #해당 클라이언트가 아닌 다른 클라이언트의 위치 정보임
                        if(is_enemy == False):
                            ident_standard=message['ident']
                        if(message['ident']==ident_standard):
                            is_enemy=True
                            #print(message['ident'],message['msg'])
                            enemy=pygame.image.load('./picture/peng.png')
                            enemy_size=enemy.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
                            enemy_width=enemy_size[0] #가로크기
                            enemy_height=enemy_size[1] #세로크기
                            enemy_x_pos=(screen_width/2)-(enemy_width/2)+20 #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
                            enemy_y_pos=screen_height-enemy_height-6 #화면은 아래쪽으로 갈 수록 +임 #y좌표
                            enemy_x_pos=float(message['msg'])
                        elif(message['ident']!=ident_standard):
                            is_enemy2=True
                            #print(message['ident'],message['msg'])
                            enemy2=pygame.image.load('./picture/peng.png')
                            enemy2_size=enemy2.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
                            enemy2_width=enemy2_size[0] #가로크기
                            enemy2_height=enemy2_size[1] #세로크기
                            enemy2_x_pos=(screen_width/2)-(enemy2_width/2)+20 #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
                            enemy2_y_pos=screen_height-enemy_height-6 #화면은 아래쪽으로 갈 수록 +임 #y좌표
                            enemy2_x_pos=float(message['msg'])
                

           

    def run(self):
        global screen
        global screen_height
        global screen_width
        global enemy
        global enemy_size
        global enemy_width
        global enemy_height
        global enemy_x_pos
        global enemy_y_pos
        global enemy2
        global enemy2_size
        global enemy2_width
        global enemy2_height
        global enemy2_x_pos
        global enemy2_y_pos
        global is_enemy
        global is_enemy2

        self.context = zmq.Context()
        #DEALER 소켓을 생성
        self.socket = self.context.socket(zmq.DEALER)
        self.identity = u'%s' % self.id #id값은 사용자가 입력
        self.socket.identity = self.identity.encode('ascii')
        #DEALER는 CONNECT함
        self.socket.connect('tcp://localhost:5570')
        #self.socket.send(b'Connected') #서버에 클라이언트가 쓴 메세지 보냄

        
        print('Client %s started' % (self.identity))
        #Poller는 두 개 이상의 소켓을 등록하여두면 소켓들로부터의 입력을 감지하여 (소켓, 이벤트)의 리스트를 리턴해준다. 
        #이를 이용해서 각각의 소켓을 동시에 수신하면서 소켓별로 구분된 메시지를 얻을 수 있다.
        self.poll = zmq.Poller()#self.poll은 Poller
        self.poll.register(self.socket, zmq.POLLIN) #POLLER 등록 - Dealer 소켓을 통해 각 클라이언트들의 데이터를 받아옴

        self.subscriber=self.context.socket(zmq.SUB)
        self.subscriber.setsockopt(zmq.SUBSCRIBE,b'')
        self.subscriber.connect("tcp://localhost:5557") # 클라이언트이므로 bind가 아니라 connect

        clientThread = threading.Thread(target=self.recvHandler)
        clientThread.daemon = True
        clientThread.start() #쓰레드 시작(recvHandler 시작)- 서버가 클라이언트 쪽으로 보내는 것 있으면 받기 위해

        pygame.init()#초기화하는 작업- 반드시 필요

        #게임 화면 크기 설정
        screen_width=780
        screen_height=443
        screen=pygame.display.set_mode((screen_width,screen_height)) #화면 크기 설정
        screen_rect=screen.get_rect()

        global stage
        stage = 'menu'
        button_1 = button_create("1 PLAYER", (300, 100, 200, 75), RED, GREEN, on_click_button_1)
        button_2 = button_create("2 PLAYER", (300, 200, 200, 75), RED, GREEN, on_click_button_2)
        button_3 = button_create("3 PLAYER", (300, 300, 200, 75), RED, GREEN, on_click_button_3)

        #화면 타이틀 설정
        pygame.display.set_caption("My Game") #게임 이름

        #fps - 프레임 수가 많으면 좀 더 부드러움
        clock=pygame.time.Clock()

        #배경화면 정하기- 배경 이미지 불러오기
        background=pygame.image.load('./picture/background.png')

        #처음에는 100점에서 출발
        score=100

        #캐릭터 불러오기
        character=pygame.image.load('./picture/lion.png')
        character_size=character.get_rect().size #이미지 크기를 구해옴 #배열 형태로 반환됨 [가로크기, 세로크기]
        character_width=character_size[0] #가로크기
        character_height=character_size[1] #세로크기

        character_x_pos=(screen_width/2)-(character_width/2) #화면 가로의 절반에 해당하는 곳에 위치 #x좌표
        character_y_pos=screen_height-character_height-6 #화면은 아래쪽으로 갈 수록 +임 #y좌표

        #이동할 위치(좌표)
        to_x=0

        #fps에 맞추기 위한 이동속도
        character_speed=0.6


        #적 (rock)) 캐릭터
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

        font=pygame.font.Font('./font/비트로 코어 TTF.ttf',30)


        #총 시간 - 제한시간
        total_time=50

        global select
        select=True
        while select:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    waiting = False 

                if stage == 'menu':
                    button_check(button_1, event)
                    button_check(button_2, event)
                    button_check(button_3, event)
                
            screen.fill(BLACK)

            if stage == 'menu':
                button_draw(screen, button_1)
                button_draw(screen, button_2)
                button_draw(screen, button_3)
           
            pygame.display.update()
        
        self.socket.send_string('s'+stage) #서버에 선택한 stage정보 보냄

        #이제 모드에 맞게 클라이언트들 접속하는 것 기다려야 함
        waiting=True
        global clientNum
        #clientNum=0
        global stage_data
        while waiting:
            if(int(stage) == stage_data[int(stage)-1]):
                #print("stage: ",stage)
                #print("clientNum: ",clientNum)
                waiting=False
            else:
                font1 = pygame.font.Font(None, 40)
                img1 = font1.render('Wait To Connect',True,BLUE)
                screen.fill(BLACK)
                screen.blit(img1, (screen_width/2-100,screen_height/2))
                pygame.display.update()


        start_ticks=0
        if(stage == '1'):
            print("1 카운트다운 시작")
            start_ticks=pygame.time.get_ticks() #시작(현재의) tick 정보
        
             
        start_ticks_start=False #2번째 애가 그려졌는지
        start_ticks_start2=False #3번째 애가 그려졌는지


        #이벤트루프 - 사용자가 입력하기 전에 꺼지는 등 종료되지 않고 기다리도록 설정

        running=True #현재 게임이 진행중인지
        while running:
            dt=clock.tick(85)#원하는 화면의 초당 프레임 수 설정
            for event in pygame.event.get(): #사용자 입력- 마우스나 키보드 입력이 들어오는지 계속 체크함
                if event.type==pygame.QUIT: #우측 상단의 x버튼 눌렀을 때
                    running=False

                if event.type == pygame.KEYDOWN: #키가 눌러졌는지 확인
                    if event.key==pygame.K_LEFT: #캐릭터를 왼쪽으로
                        to_x-=character_speed
                    elif event.key==pygame.K_RIGHT:
                        to_x+=character_speed

                if event.type==pygame.KEYUP: #방향키를 떼면 멈춤
                    if event.key == pygame.K_LEFT or event.key==pygame.K_RIGHT: #즉 왼쪽키나 오른쪽 키를 누르고 있다가 뗀 거면
                        to_x=0
            #게임 캐릭터의 움직인 위치 정의        
            character_x_pos+=to_x*dt
            self.socket.send_string(str(character_x_pos))

            #가로 경계값의 처리
            if character_x_pos < 0:#화면의 왼쪽 밖으로 나가면
                character_x_pos=0
            elif character_x_pos > screen_width-character_width : #화면 오른쪽 밖으로 나가게 되면
                character_x_pos=screen_width-character_width

            #돌 캐릭터의 움직이는 위치 정의
            rock1_y_pos+=rock1_speed
            rock2_y_pos+=rock2_speed
            rock3_y_pos+=rock3_speed

            #가로 경계값의 처리
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
            character_rect=character.get_rect()
            character_rect.left=character_x_pos
            character_rect.top=character_y_pos

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
            if character_rect.colliderect(rock1_rect):
                print("충돌했습니다!")
                rock1_y_pos=0 #다시 화면 맨 위로 올림
                rock1_x_pos=random.randint(0,screen_width-rock1_width)
                is_collision1=True
                score-=5
            elif(character_rect.colliderect(rock2_rect)):
                print("충돌했습니다!")
                rock2_y_pos=0 #다시 화면 맨 위로 올림
                rock2_x_pos=random.randint(0,screen_width-rock1_width)
                is_collision2=True
                score-=5
            elif(character_rect.colliderect(rock3_rect)):
                print("충돌했습니다!")
                rock3_y_pos=0 #다시 화면 맨 위로 올림
                rock3_x_pos=random.randint(0,screen_width-rock1_width)
                is_collision3=True
                score-=5
                

            collision1=font.render(("충돌했습니다!"),True,(255,0,0))
            collision2=font.render(("점수: "+str(score)),True,(0,0,255))
           

            
            screen.blit(background,(0,0)) #blit: 배경을 그리는 역할
            screen.blit(character,(character_x_pos,character_y_pos)) #캐릭터 그리기
            screen.blit(rock1,(rock1_x_pos,rock1_y_pos)) 
            screen.blit(rock2,(rock2_x_pos,rock2_y_pos)) 
            screen.blit(rock3,(rock3_x_pos,rock3_y_pos))

            if(is_enemy):
                if(stage == '2' and start_ticks_start==False):
                    start_ticks=pygame.time.get_ticks()
                    start_ticks_start=True
                if(stage == '3' and start_ticks_start==False):
                    start_ticks_start=True
                screen.blit(enemy,(enemy_x_pos,enemy_y_pos))

            if(is_enemy2):
                if(stage == '3' and start_ticks_start2==False):
                    start_ticks=pygame.time.get_ticks()
                    start_ticks_start2=True
                screen.blit(enemy2,(enemy2_x_pos,enemy2_y_pos))
            
            

            #타이머 집어넣기
            #경과 시간 계산
            elapsed_time=(pygame.time.get_ticks()-start_ticks) /1000 
            timer=font.render(str(int(total_time-elapsed_time)),True,(225,0,0)) #글자로 써줌, 정수 단위로만 가능하도록 int형을 씌어줌
            #render안에는 str형이 들어와야함
            #redner(출력할 글자, true, rgb형 색)
            #이제 그려주기
            if(stage == '1' and start_ticks_start==False and start_ticks_start2==False):
                screen.blit(timer,(10,10))
            elif(stage == '2' and start_ticks_start==True and start_ticks_start2==False):
                screen.blit(timer,(10,10))
            elif(stage == '3' and start_ticks_start==True and start_ticks_start2==True):
                screen.blit(timer,(10,10))
                
            #만약 남은 시간이 0이 되면 종료
            if total_time-elapsed_time<=0:
                print("타임아웃")
                is_timeout=True
                running=False

            timeout=font.render("최종 점수: "+(str(score)),True,(0,0,255))
            
            if(is_collision1 or is_collision2 or is_collision3):
                self.socket.send_string(str(score)) #서버에 클라이언트가 쓴 메세지 보냄
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
        

        self.socket.close() #useless
        self.context.term() #useless

def main(argv):
    """main function"""
    client = ClientTask(argv[1])#client는 쓰레드의 인스턴스
    client.start() #Thread의 instance의 start 함수를 실행하면 MyThread 클래스의 run 함수가 자동 실행

# usage: python 08-dealer-router-async-client.py client_id
if __name__ == "__main__":
    main(sys.argv)