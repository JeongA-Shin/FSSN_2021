import zmq
import sys
import threading
import time
from random import randint, random
import json

clientNum=0
stage_data={'s1':0,'s2':0,'s3':0}
first=''
second=''
third=''
#점수들은 100점부터 시작한다
score_data_2={'1':100,'2':100}
score_data_3={'1':100,'2':100,'3':100}

rank_2={'first':'1','second':'2'}
rank_3={'first':'1','second':'2','third':'3'}

relay_info={'relay_info':''}
prevment='넵'
count=0

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self, num_server):
        threading.Thread.__init__ (self)
        self.num_server = num_server

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER)
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER) 
        backend.bind('inproc://backend')

        publisher=context.socket(zmq.PUB) 
        publisher.bind("tcp://*:5557") 

        workers = [] #worker들
        for i in range(self.num_server): #num_server는 사용자가 입력한 숫자
            worker = ServerWorker(context, i,publisher) #각 woker에 serverWorker가 들어가는 거임
            worker.start() #serverworker클래스의 run함수 동작
            workers.append(worker)

        zmq.proxy(frontend, backend) 

        frontend.close()
        backend.close()
        context.term()

class ServerWorker(threading.Thread):
    """ServerWorker"""
    def __init__(self, context, id,publisher):
        threading.Thread.__init__ (self)
        self.context = context
        self.id = id
        self.publisher=publisher

    def run(self):
        global clientNum
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        print('Worker#{0} started'.format(self.id))
        global stage_data
        global first
        global second
        global third
        global relay_info
        global is_prevment
        global prevment
        global count
        global rank_2
        global rank_3

        while True:
            ident, msg = worker.recv_multipart() #클라이언트로부터 받은 메시지들
            
            if(msg.decode()[0]=='s'): #s로 시작하면 stage 정보임
                if(msg.decode()=='s1'):
                    stage_data['s1']+=1
                elif(msg.decode()=='s2'):
                    stage_data['s2']+=1
                elif(msg.decode()=='s3'):
                    stage_data['s3']+=1
                self.publisher.send(json.dumps(stage_data).encode())
            elif(msg.decode()[0]=='j'): #j로 시작되면 점수 정보임 #one player모드에서는 점수 비교 필요 없음-점수 관련 정보는 publisher로 뿌림
                if(stage_data['s2']==2): #2 player mode 시작이면
                    if(str(ident.decode())=='1'):
                        score_data_2['1']=int(msg.decode()[1:])
                    elif(str(ident.decode())=='2'):
                        score_data_2['2']=int(msg.decode()[1:])
                    first=(max(score_data_2, key=score_data_2.get))
                    second=(min(score_data_2, key=score_data_2.get))
                    rank_2['first']=first
                    rank_2['second']=second
                    if((score_data_2[first]-score_data_2[second])>=30): 
                        text1=str("{}플레이어님, 분발하세요!".format(second))
                        if(prevment !=text1):
                            prevment=text1
                            relay_info['relay_info']=text1
                            self.publisher.send(json.dumps(relay_info).encode())
                    elif((score_data_2[first]-score_data_2[second])>=20):
                        text2=str("{}플레이어님이 앞서고 있습니다!".format(first))
                        if(prevment != text2):
                            prevment=text2
                            relay_info['relay_info']=text2
                            self.publisher.send(json.dumps(relay_info).encode())
                    elif((score_data_3[first]-score_data_3[second])<=10):  
                        text3=str('아직 1등이 확실하지 않습니다!')
                        count+=1#충돌될 때마다 클라이언트에서 점수를 보내는데, 1등이 확실하지 않다는 멘트를 충돌이 적어도 3번보다 많을 때 중계 시작 위해서
                        if(prevment !=text3 and count>3): 
                            prevment=text3
                            relay_info['relay_info']=text3
                            self.publisher.send(json.dumps(relay_info).encode())
                    self.publisher.send(json.dumps(rank_2).encode())
                elif(stage_data['s3']==3): #3 player mode 시작이면
                    if(str(ident.decode())=='1'):
                        score_data_3['1']=int(msg.decode()[1:])
                    elif(str(ident.decode())=='2'):
                        score_data_3['2']=int(msg.decode()[1:])
                    elif(str(ident.decode())=='3'):
                        score_data_3['3']=int(msg.decode()[1:])
                    first=(max(score_data_3, key=score_data_3.get))
                    third=(min(score_data_3, key=score_data_3.get))
                    for keey in score_data_3.keys():
                        if(keey != first and keey != third):
                            second=keey
                    rank_3['first']=first
                    rank_3['second']=second
                    rank_3['third']=third
                    if((score_data_3[first]-score_data_3[third])>=30):
                        text1=str("{}플레이어님, 분발하세요!".format(third))
                        if(prevment !=text1):
                            prevment=text1
                            relay_info['relay_info']=text1
                            self.publisher.send(json.dumps(relay_info).encode())
                    elif((score_data_3[first]-score_data_3[second])>=20):
                        text2=str("{}플레이어님이 앞서고 있습니다!".format(first))
                        if(prevment != text2):
                            prevment=text2
                            relay_info['relay_info']=text2
                            self.publisher.send(json.dumps(relay_info).encode())
                    elif((score_data_3[first]-score_data_3[second])<=10):
                        text3=str('아직 1등이 확실하지 않습니다!')
                        count+=1
                        if(prevment !=text3 and count>3): 
                            prevment=text3
                            relay_info['relay_info']=text3
                            self.publisher.send(json.dumps(relay_info).encode())
                    self.publisher.send(json.dumps(rank_3).encode())
            elif(msg==b'Connected'): #연결되었다고 왔으면
                clientNum+=1
                clientNum_data={"ident":ident.decode(),"clientNum":str(clientNum)}
                self.publisher.send(json.dumps(clientNum_data).encode())
            else: #위치정보임
                pos_data={"ident":ident.decode(),"msg":msg.decode()}
                payload=json.dumps(pos_data).encode()
                self.publisher.send(payload)


        worker.close() # useless

def main(argv):
    """main function"""
    server = ServerTask(int(argv[1]))
    server.start()
    server.join() 

if __name__ == "__main__":
    main(sys.argv)