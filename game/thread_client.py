# Asynchronous Client/Server Pattern
# Reference: https://zguide.zeromq.org/docs/chapter3/#The-Asynchronous-Client-Server-Pattern
# author of original code: Felipe Cruz <felipecruz@loogica.net>
# license of original code: MIT/X11

import zmq
import sys
import threading
import json

import time
from random import randint, random

#클라이언트 쓰레드
class ClientTask(threading.Thread):
    """ClientTask"""
    def __init__(self, id):
        self.id = id
        threading.Thread.__init__ (self) #쓰레드를 클래스로 정의할 경우에는 __init__ 함수에서 부모 클래스의 생성자 threading.Thread.__init__(self)를 반드시 호출 !!

    def recvHandler(self):
        while True:
            sockets = dict(self.poll.poll(1000)) #1000은 이벤트를 기다리는 시간 제한(밀리초)입니다.
            if self.socket in sockets:
                msg = self.socket.recv() #서버로부터 받은 메세지
                print('{0} received: {1}'.format(self.identity, msg))

    def run(self):
        self.context = zmq.Context()
        #DEALER 소켓을 생성
        self.socket = self.context.socket(zmq.DEALER)
        self.identity = u'%s' % self.id
        self.socket.identity = self.identity.encode('ascii')
        #DEALER는 CONNECT함
        self.socket.connect('tcp://localhost:5570')
        print('Client %s started' % (self.identity))
        #Poller는 두 개 이상의 소켓을 등록하여두면 소켓들로부터의 입력을 감지하여 (소켓, 이벤트)의 리스트를 리턴해준다. 
        #이를 이용해서 각각의 소켓을 동시에 수신하면서 소켓별로 구분된 메시지를 얻을 수 있다.
        self.poll = zmq.Poller()#self.poll은 Poller
        self.poll.register(self.socket, zmq.POLLIN) #POLLER 등록 - Dealer 소켓을 통해 각 클라이언트들의 데이터를 받아옴
        reqs = 0

        clientThread = threading.Thread(target=self.recvHandler)
        clientThread.daemon = True
        clientThread.start() #쓰레드 시작(recvHandler 시작)
        
        while True:
            reqs = reqs + 1
            print('Req #%d sent..' % (reqs))
            self.socket.send_string(u'request #%d' % (reqs))
            time.sleep(1)

        self.socket.close() #useless
        self.context.term() #useless

def main(argv):
    """main function"""
    client = ClientTask(argv[1])#client는 쓰레드의 인스턴스
    client.start() #Thread의 instance의 start 함수를 실행하면 MyThread 클래스의 run 함수가 자동 실행

# usage: python 08-dealer-router-async-client.py client_id
if __name__ == "__main__":
    main(sys.argv)