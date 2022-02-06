# Asynchronous Client/Server Pattern
# Reference: https://zguide.zeromq.org/docs/chapter3/#The-Asynchronous-Client-Server-Pattern
# author of original code: Felipe Cruz <felipecruz@loogica.net>
# license of original code: MIT/X11

import zmq
import sys
import threading
import time
from random import randint, random

class ServerTask(threading.Thread):
    """ServerTask"""
    def __init__(self, num_server):
        threading.Thread.__init__ (self)
        self.num_server = num_server

    def run(self):
        context = zmq.Context()
        frontend = context.socket(zmq.ROUTER) #router 소켓- 얘를 통해 서버로 클라이언트들의 요청들이 전달됨
        frontend.bind('tcp://*:5570')

        backend = context.socket(zmq.DEALER) #Dealer 소켓 - 클라이언트들의 요청 결과가 처리되어 전달됨
        backend.bind('inproc://backend')#zmq inproc: zmq 스레드간 통신 전송
        #.bind('inproc://{프로세스 이름})

        publisher=context.socket(zmq.PUB) 
        publisher.bind("tcp://*:5557") #서버이므로 connect가 아니라 bind임

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
        worker = self.context.socket(zmq.DEALER)
        worker.connect('inproc://backend')
        print('Worker#{0} started'.format(self.id))

        while True:
            ident, msg = worker.recv_multipart() #클라이언트로부터 받은 메시지들
            print('Worker#{0} received {1} from client #{2}'.format(self.id, msg, ident))
            #worker.send_multipart([ident, msg]) #해당 메세지를 보낸 각 클라이언트에 보냄
            
            smsg=("Hello, I'm Server") #서버가 뿌릴 메세지
            #worker.send_string(smsg)#클라이언트들에게 메세지들을 뿌림
            self.publisher.send_string(smsg)#subscriber에게 메세지들을 뿌림

            print('')
            #멀티파트 메시지는 하나의 메시지 프레임 내부에 여러 개의 독립적인 메시지 프레임이 들어 있는 것

        worker.close() # useless

def main(argv):
    """main function"""
    server = ServerTask(int(argv[1]))
    server.start()
    server.join() #쓰레드 클래스의 run 함수 

# usage: python 07-dealer-router-async-server.py n
if __name__ == "__main__":
    main(sys.argv)