import socket
import cv2
import threading
import numpy
import pybase64 as base64

class ServerSocket:
    def __init__(self, ip, port):
        self.TCP_IP = ip
        self.TCP_PORT = port
        self.socketOpen()
        self.receiveThread = threading.Thread(target=self.receiveImages)
        self.receiveThread.start()

    def socketClose(self):
        self.sock.close()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is close')

    def socketOpen(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.TCP_IP, self.TCP_PORT))
        self.sock.listen(1)
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is open')
        self.conn, self.addr = self.sock.accept()
        print(u'Server socket [ TCP_IP: ' + self.TCP_IP + ', TCP_PORT: ' + str(self.TCP_PORT) + ' ] is connected with client')

    def receiveImages(self):
        try:
            while True:
                length = self.recvall(self.conn, 64)
                # print(length)
                length1 = length.decode('utf-8')
                print(length1)
                stringData = self.recvall(self.conn, int(length1))
                # print("st : " , stringData)
                data = numpy.frombuffer(base64.b64decode(stringData), dtype = numpy.uint8)
                numpy.save("data2",data)
                print("data",data)
                print(data.shape)
                decimg = cv2.imdecode(data, 1)
                print("dec : ", decimg)
                return decimg
                # cv2.imwrite("image.png", decimg)
                # cv2.waitKey(1)
                
        except Exception as e:
            print(e)
            self.socketClose()
            self.socketOpen()
            self.receiveThread = threading.Thread(target=self.receiveImages)
            self.receiveThread.start()

    def recvall(self, sock, count):
        buf = b''
        while count:
            newbuf = sock.recv(count)
            if not newbuf: return None
            buf += newbuf
            count -= len(newbuf)
        return buf

def main():
    server = ServerSocket('192.168.0.100', 5050)

if __name__ == "__main__":
    main()