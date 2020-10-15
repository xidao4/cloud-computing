from bilibili_api import Verify
from bilibili_api import bangumi
import json
import socket
import time
SERVER_IP = 'localhost'
PORT=8081

def socket_client(data):
    # 创建tcp套接字
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 链接服务器
    client_socket.connect((SERVER_IP, PORT))
    print(data)
    client_socket.send(data.encode("UTF-8"))
    client_socket.close()


def get_series():
    #投币 弹幕 追番人数 总播放量
    a=bangumi.get_interact_data(34004)
    a=json.dumps(a,indent=4,ensure_ascii=False)
    print(a)
    verify=Verify(sessdata="ea3912b9%2C1617369404%2C61152*a1",csrf="3acd1173cb6819568856aaeb798d7cbd")
    #长评数量 短评数量
    

if __name__ == "__main__":
    get_series()

