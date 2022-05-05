from random import randint
import socket
import threading
import signal
import sys
import encode

from numpy import byte, rad2deg
default_user_agent = ['1'] * 8
user_agent = 'User-Agent: Mozilla/5.{0} (X{1}0; Linux x86_64; rv:9{2}.0) Gecko/{3}20{4}00{5}00{6} Firefox/9{7}.0'
cookie = 'Cookie: b3st={0}.{1}.{2}.{3}.{4}.{5}'

n = 2 # n część Antygony z 5 (0-4)
antygona_text = encode.part_of_Antygona("Antygona.txt", n)
print(f'len anygona = {len(antygona_text)}')
antygona_index = 0

config =  {
            "HOST_NAME" : "0.0.0.0",
            "BIND_PORT" : 12345,
            "MAX_REQUEST_LEN" : 1024,
            "CONNECTION_TIMEOUT" : 5
          }
          
def generate_random_cookie():
    cookie = []
    for i in range(3):
        cookie.append(randint(1111111,9999999))
    cookie.append(randint(111,999))
    cookie.append(randint(111,999))
    cookie.append(randint(0,9))
    return cookie


def inject_data(http_request):
    global antygona_index
    global antygona_text
    data = encode.list_of_bits(antygona_text,antygona_index)
    data = list(map(lambda x: x.replace('0', 'l'), data))
    #data = default_user_agent  # remove secret message
    lines = http_request.split(b'\r\n')
    text = b''
    for i in range(len(lines)):
        if lines[i].find(b'User-Agent') != -1:
            lines[i] = bytes(user_agent.format(*data), 'UTF-8')
        if lines[i].find(b'Accept-Encoding') != -1:
            lines[i] = bytes(cookie.format(*generate_random_cookie()), 'UTF-8')
        text += lines[i] + b'\r\n'
    antygona_index+=1
    if antygona_index == len(antygona_text):
        print('KONIEC')
        exit()
    return text[:-2]


class Server:
    def __init__(self, config):
        signal.signal(signal.SIGINT, self.shutdown)
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.serverSocket.bind((config['HOST_NAME'], config['BIND_PORT']))
        self.serverSocket.listen(10)
        self.__clients = {}



    def listenForClient(self):
        while True:
            (clientSocket, client_address) = self.serverSocket.accept()
            d = threading.Thread(name=self._getClientName(client_address), target=self.proxy_thread, args=(clientSocket, client_address))
            d.setDaemon(True)
            d.start()
        self.shutdown(0,0)


    def proxy_thread(self, conn, client_addr):

        request_from_browser = conn.recv(config['MAX_REQUEST_LEN'])
        request_from_proxy = request_from_browser

        # if host == malicious:
        request_from_proxy = inject_data(request_from_proxy)

        first_line = request_from_browser.split(b'\n')[0]  
        print(first_line[:50])
        try :                
            url = first_line.split(b' ')[1]   
        except IndexError :
            url = b""                    
        print(url[:50])

        http_pos = url.find(b"://")         
        if (http_pos==-1):
            temp = url
        else:
            temp = url[(http_pos+3):]

        port_pos = temp.find(b":") 

        webserver_pos = temp.find(b"/")
        if webserver_pos == -1:
            webserver_pos = len(temp)

        webserver = ""
        port = -1
        if (port_pos==-1 or webserver_pos < port_pos):
            port = 80
            webserver = temp[:webserver_pos]
        else:                                              
            port = int((temp[(port_pos+1):])[:webserver_pos-port_pos-1])
            webserver = temp[:port_pos]

        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(config['CONNECTION_TIMEOUT'])
            s.connect((webserver, port))
            s.sendall(request_from_proxy)                          

            while 1:
                data_from_server = s.recv(config['MAX_REQUEST_LEN'])
                data_from_proxy = data_from_server
                if (len(data_from_proxy) > 0):
                    conn.send(data_from_proxy)
                else:
                    break
            s.close()
            conn.close()
        except socket.error as error_msg:
            print('ERROR: ',client_addr,error_msg)
            if s:
                s.close()
            if conn:
                conn.close()


    def _getClientName(self, cli_addr):
        return "Client"


    def shutdown(self, signum, frame):
        self.serverSocket.close()
        sys.exit(0)


if __name__ == "__main__":
    print("proxy online")
    server = Server(config)
    server.listenForClient()