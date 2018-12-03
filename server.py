#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket

server_addr = ('127.0.0.1',1060)

def recv_all(sock):
    data = b''
    while data[-2:] != b'\n\r':
        more = sock.recv(512)
        data += more
    return data

def return_file(sock,file_name):
    data = b''
    try:
        with open(file_name,'rb') as f:
            data = f.read()
        length=str(len(data)).encode('utf-8')
        sock.sendall(length+b'.'+data)
    except Exception:
        msg = 'error:19.file dose not exist'
        sock.sendall(msg.encode('utf-8')) #length = 19

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
sock.bind(server_addr)
sock.listen(4)
print('Lisen Start.')
while True:
    try:
        client, client_name = sock.accept()
        while True:
            raw_filename = recv_all(client)
            filename = raw_filename[:-2].decode('utf-8')
            print(filename)
            if filename == 'exit':
                print("Client {} Closed".format(client_name))
                break
            else:
                return_file(client,filename)
    except Exception:
        print("Client {} Closed".format(client_name))
sock.close()