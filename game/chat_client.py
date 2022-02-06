import zmq
import sys

def main(argv):
    context=zmq.Context()
    #서버가 뿌리는 정보 받아오는 소켓(SUB 역할을 하는 소켓)
    subscriber=context.socket(zmq.SUB)
    subscriber.setsockopt(zmq.SUBSCRIBE,b'')
    subscriber.connect("tcp://localhost:5557") # 클라이언트이므로 bind가 아니라 connect

    #서버쪽에 클라이언트 정보 주는 소켓(PUSH 역할을 하는 소켓)
    publisher=context.socket(zmq.PUSH)
    publisher.connect("tcp://localhost:5558")#pub-sub와는 다른 통로로 데이터가 오감

    clientID=sys.argv[1]
    
    while True:
        if(subscriber.poll(100)&zmq.POLLIN):
            print(clientID," receives from server : ",subscriber.recv())#서버로부터 받은 메세지 출력
        else:
            msg=input("enter your message here: ")
            publisher.send_string(msg+" from client "+str(clientID)) #서버에 클라이언트가 쓴 메세지 보냄
            print(clientID," sent ",msg) #내가 쓴 메세지 출력
        print('')


if __name__=='__main__':
    main(sys.argv)





