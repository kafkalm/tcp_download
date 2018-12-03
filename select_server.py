#!/usr/bin/env python
#-*- coding:utf-8 -*-
import select
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
#设置为非阻塞模式
sock.setblocking(False)
sock.listen(4)

inputs = [sock,]

while True:
    readable,writeable,exceptional = select.select(inputs,[],[])
    try:
        for s in readable:
            #是服务器套接字 则监听一个客户端请求 并将新的套接字加入读队列
            if s == sock:
                client,client_name = sock.accept()
                inputs.append(client)
            #与客户端连接的套接字 接收消息
            else:
                raw_filename = recv_all(s)
                filename = raw_filename[:-2].decode('utf-8')
                print("Client:",filename)
                #客户端退出 将套接字移出队列
                if filename == 'exit':
                    inputs.remove(s)
                    print("Client {} Closed".format(client_name))
                else:
                    return_file(s, filename)
    except Exception:
        inputs.remove(s)
        print("Client {} Closed".format(client_name))

sock.close()
























"""
def all_events_forever(poll_object):
    while True:
        for fd,event in poll_object.poll():
            yield fd,event

def serve(listener):
    sockets = {listener.fileno():listener}
    addresses = {}
    bytes_received = {}
    bytes_to_send = {}

    poll_object = select.poll()
    poll_object.register(listener,select.POLLIN)
    for fd,event in all_events_forever(poll_object):
        sock = sockets[fd]
        if event & (select.POLLHUP | select.POLLERR | select.POLLNVAL):
            address = addresses.pop(sock)
            rb = bytes_received.pop(sock,b'')
            sb = bytes_to_send.pop(sock,b'')
            if rb:
                print('Client {} sent {} but then closed'.format(address,rb))
            elif sb:
                print('Client {} closed before we sent {}'.format(address,sb))
            else:
                print('Client {} closed socket normally'.format(address))
            poll_object.unregister(fd)
            del sockets[fd]

        elif sock is listener:
            sock,address = sock.accept()
            print('Accepted connection from {}'.format(address))
            sock.setblocking(False)
            sockets[sock.fileno()] = sock
            addresses[sock] = address
            poll_object.register(sock,select.POLLIN)
        elif event & select.POLLIN:

"""