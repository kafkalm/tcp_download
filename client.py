#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket

server_addr = ('127.0.0.1',1060)
#error flag
error = 0

def recv_all(sock):
    raw_data = b''
    global error
    #接收数据长度信息
    while str(raw_data).split('.',1)[0] == "b''":
        more = sock.recv(1024)
        raw_data +=more
    #文件不存在时提示错误信息
    if str(raw_data).split('.',1)[0][:8] == "b'error:":
        error = 1
        length = 19
        data = raw_data[9:]
    else:
        error = 0
        length = int(str(raw_data).split('.',1)[0][2:]) #正文长度
        data = raw_data[len(str(length))+1:]    #已经接收的正文

    length = length - len(data) #剩余长度

    while length:
        more = sock.recv(length)
        length -= len(more)
        data+=more
    return data

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.connect(server_addr)

while True:
    t = input('input file name:')
    sock.sendall(t.encode('utf-8')+b'\n\r')
    if t == 'exit':
        break
    data = recv_all(sock)
    if error:
        print(data.decode('utf-8'))
    else:
        with open('pythontest\\' + t, 'wb') as f:
            f.write(data)

sock.close()
