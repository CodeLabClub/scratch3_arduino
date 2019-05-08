
'''
Arduino
requirement:
    pip3 install pymata-aio --user
'''
import zmq
import subprocess
import pathlib
import platform
import time
import threading

from codelab_adapter import settings
from codelab_adapter.core_extension import Extension


def get_python3_path():
    # If it is not working,  Please replace python3_path with your local python3 path. shell: which python3
    if (platform.system() == "Darwin"):
        # which python3
        # 不如用PATH python
        # 不确定
        path = "/usr/local/bin/python3"
    if platform.system() == "Windows":
        path = "python3"
    if platform.system() == "Linux":
        path = "/usr/bin/python3"
    return path


python3_path = get_python3_path()


class arduinoExtension(Extension):
    def __init__(self):
        name = type(self).__name__  # class name
        super().__init__(name)
        self.scratch3_message = {}
        self.TOPIC = "eim/arduino"
        self.first_start = 1


    def run(self):
        # 抽象掉这部分 Class
        port = 38782  # todo 随机分配
        context = zmq.Context.instance()
        socket = context.socket(zmq.REQ)
        socket.connect("tcp://localhost:%s" % port)

        codelab_adapter_server_dir = pathlib.Path.home(
        ) / "codelab_adapter" / "servers"
        script = "{}/arduino_server.py".format(codelab_adapter_server_dir)

        cmd = [python3_path, script]
        arduino_server = subprocess.Popen(cmd)
        settings.running_child_procs.append(arduino_server)

        lock = threading.Lock()

        def request():
            while self._running:
                lock.acquire()
                self.scratch3_message = self.read()
                lock.release()

        bg_task = threading.Thread(target=request)
        self.logger.debug("thread start")
        bg_task.daemon = True
        bg_task.start()

        while self._running:
            scratch3_message = self.scratch3_message
            self.logger.debug("scratch3_message {}".format(scratch3_message))
            self.scratch3_message = {}
            if scratch3_message == {}:
                scratch3_message = {"topic": self.TOPIC, "payload": ""}

            topic = scratch3_message.get('topic')
            arduino_code = scratch3_message.get("payload")

            if  topic == self.TOPIC:
                socket.send_json({"arduino_code": arduino_code})

            result = socket.recv_json().get("result")

            if self.first_start == 1:
                self.publish({"topic": "eim/arduino/init","payload": ""})
                self.first_start = 0

            # 发往scratch3.0
            self.publish({"topic": self.TOPIC,"payload": result})
            time.sleep(0.05)




        # release socket
        socket.send_json({"arduino_code": "quit!"})
        result = socket.recv_json().get("result")
        arduino_server.terminate()
        arduino_server.wait()
        socket.close()
        context.term()


export = arduinoExtension
