import zmq

def main():
    context=zmq.Context()
    #클라이언트쪽에 정보를 뿌리는 소켓(PUB)
    publisher=context.socket(zmq.PUB) 
    publisher.bind("tcp://*:5557") #서버이므로 connect가 아니라 bind임
    #클라이언트의 상태들(클라이언트 쪽에서 보내는 정보들)을 받는 소켓
    collector=context.socket(zmq.PULL)
    collector.bind("tcp://*:5558")
    
    while True:
        msg=collector.recv() #클라이언트로부터 서버 소켓이 받은 메세지들
        print('From client: ',msg) #서버 측에 표시

        smsg=input("enter your message here: ") #서버가 뿌릴 메세지
        publisher.send_string(smsg)#클라이언트들에게 메세지들을 뿌림
        print('')


if __name__=='__main__':
    main()


