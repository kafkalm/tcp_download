#!/usr/bin/env python
#-*- coding:utf-8 -*-
import socket
import asyncio

server_addr = ('127.0.0.1',1060)

async def handle_conversation(reader,writer):
    address = writer.get_extra_info('peername')
    print('Accepted connection from {}'.format(address))
    while True:
        try:
            raw_filename = b''
            while raw_filename[-2:] != b'\n\r':
                more = await reader.read(512)
                raw_filename += more
            filename = raw_filename[:-2].decode('utf-8')
            if filename == 'exit':
                print('Client {} Closed'.format(address))
                break
            else:
                try:
                    with open(filename, 'rb') as f:
                        data = f.read()
                    length = str(len(data)).encode('utf-8')
                    writer.write(length + b'.' + data)
                except Exception:
                    msg = 'error:19.file dose not exist'
                    writer.write(msg.encode('utf-8'))  # length = 19
        except Exception:
            print('Client {} Closed'.format(address))
            break

#创建一个事件
loop = asyncio.get_event_loop()
#创建一个协程
coroutine = asyncio.start_server(handle_conversation,server_addr[0],server_addr[1])
#协程加入事件循环
server = loop.run_until_complete(coroutine)
try:
    loop.run_forever()
finally:
    server.close()
    loop.close()