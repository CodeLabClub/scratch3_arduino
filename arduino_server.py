'''
arduino nano
requirement:
    pip3 install pymata-aio --user
'''
import zmq
from time import sleep

from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants

# zmq socket
port = 38782
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:%s" % port)


def main():
    ConnectedToArduino = False
    while True:
        if not ConnectedToArduino:
            try:
                board = PyMata3()
            except:
                pass
            else:
                ConnectedToArduino = True
                board.set_pin_mode(13, Constants.OUTPUT)
                board.digital_write(13, 1)

        arduino_code = socket.recv_json().get("arduino_code")

        if not arduino_code:
            socket.send_json({"result": {
                "pin_2_state": board.get_pin_state(2),
                "pin_3_state": board.get_pin_state(3),
                "pin_4_state": board.get_pin_state(4),
                "pin_5_state": board.get_pin_state(5),
                "pin_6_state": board.get_pin_state(6),
                "pin_7_state": board.get_pin_state(7),
                "pin_8_state": board.get_pin_state(8),
                "pin_9_state": board.get_pin_state(9),
                "pin_10_state": board.get_pin_state(10),
                "pin_11_state": board.get_pin_state(11),
                "pin_12_state": board.get_pin_state(12),
                "pin_13_state": board.get_pin_state(13),
                "digital_pin_2": board.digital_read(2),
                "digital_pin_3": board.digital_read(3),
                "digital_pin_4": board.digital_read(4),
                "digital_pin_5": board.digital_read(5),
                "digital_pin_6": board.digital_read(6),
                "digital_pin_7": board.digital_read(7),
                "digital_pin_8": board.digital_read(8),
                "digital_pin_9": board.digital_read(9),
                "digital_pin_10": board.digital_read(10),
                "digital_pin_11": board.digital_read(11),
                "digital_pin_12": board.digital_read(12),
                "digital_pin_13": board.digital_read(13),
                "analog_pin_0": board.analog_read(0),
                "analog_pin_1": board.analog_read(1),
                "analog_pin_2": board.analog_read(2),
                "analog_pin_3": board.analog_read(3),
                "analog_pin_4": board.analog_read(4),
                "analog_pin_5": board.analog_read(5),
                "analog_pin_6": board.analog_read(6),
                "analog_pin_7": board.analog_read(7),
            }})
            sleep(0.05)
            continue

        if arduino_code == "quit!":
            output = eval("board.shutdown()", {}, {
                          "board": board, "Constants": Constants})
            socket.send_json({"result": "quit!"})
            break
        else:
            try:
                output = eval(arduino_code, {}, {
                              "board": board, "Constants": Constants})
                # output = exec(arduino_code) # 安全性问题
            except Exception as e:
                output = e
        socket.send_json({
            "result": {
                "output": str(output),
                "pin_2_state": board.get_pin_state(2),
                "pin_3_state": board.get_pin_state(3),
                "pin_4_state": board.get_pin_state(4),
                "pin_5_state": board.get_pin_state(5),
                "pin_6_state": board.get_pin_state(6),
                "pin_7_state": board.get_pin_state(7),
                "pin_8_state": board.get_pin_state(8),
                "pin_9_state": board.get_pin_state(9),
                "pin_10_state": board.get_pin_state(10),
                "pin_11_state": board.get_pin_state(11),
                "pin_12_state": board.get_pin_state(12),
                "pin_13_state": board.get_pin_state(13),
                "digital_pin_2": board.digital_read(2),
                "digital_pin_3": board.digital_read(3),
                "digital_pin_4": board.digital_read(4),
                "digital_pin_5": board.digital_read(5),
                "digital_pin_6": board.digital_read(6),
                "digital_pin_7": board.digital_read(7),
                "digital_pin_8": board.digital_read(8),
                "digital_pin_9": board.digital_read(9),
                "digital_pin_10": board.digital_read(10),
                "digital_pin_11": board.digital_read(11),
                "digital_pin_12": board.digital_read(12),
                "digital_pin_13": board.digital_read(13),
                "analog_pin_0": board.analog_read(0),
                "analog_pin_1": board.analog_read(1),
                "analog_pin_2": board.analog_read(2),
                "analog_pin_3": board.analog_read(3),
                "analog_pin_4": board.analog_read(4),
                "analog_pin_5": board.analog_read(5),
                "analog_pin_6": board.analog_read(6),
                "analog_pin_7": board.analog_read(7),
            }})
        sleep(0.05)

    socket.close()
    context.term()


if __name__ == '__main__':
    main()
