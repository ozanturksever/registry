#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import threading

try:
    import zmq
except:
    import zmqpy as zmq
try:
    import msgpack
except:
    import msgpack_pure as msgpack
import time


class MsgThread(threading.Thread):
    _exit = False

    def __init__(self, registry, name):
        self.registry = registry
        self.thread_name = name
        threading.Thread.__init__(self)

    def run(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
#        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.socket.bind('tcp://127.0.0.1:10000')
#        self.socket.bind('ipc:///tmp/10000')
        self.count = 0
        while not self._exit:
            try:
                msg = self.socket.recv()
                unpacked = msgpack.unpackb(msg)
                if unpacked.get('action') == 'stat':
                    print self.thread_name, self.count
                    break
                if unpacked.get('action') == 'set':
                    self.registry.set(unpacked.get('params', {}).get('key'), unpacked.get('params', {}).get('value'))
#                print self.registry.get(unpacked.get('params', {}).get('key'))
                self.socket.send(msgpack.packb(self.registry.get(unpacked.get('params', {}).get('key'))))
                self.count+=1
            except zmq.ZMQError, err:
                pass
        self._close_socket()

    def _close_socket(self):
        if not self.socket.closed:
            self.socket.close()
        if not self.context.closed:
            self.context.term()
        pass

    def exit(self):
        self._exit = True

class Registry(object):
    data = {}
    server_started = False
    _stop_server = False

    def __init__(self):
        self.msgThread = MsgThread(self,name='first')
        self.msgThread.daemon = True
        self.msgThread.start()
        while True:
            time.sleep(1)

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def stop_server(self):
        self.msgThread.exit()
        pass

    def __del__(self):
        if self.msgThread.is_alive:
            self.msgThread.exit()
