import socket
import requests
import sys
import argparse
import json
import time


def sendFile(host, port, file_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    s.send(bytes(file_name, encoding='UTF-8'))
    data = s.recv(1000000)

    _f = open(file_name, 'rb')
    _time = time.time()
    speed = None
    data_len = 0
    if str(data, 'UTF-8') == '1':
        while True:
            _data = _f.read(1024 * 1024)
            s.send(_data)
            if not _data:
                s.send(b'')
                s.close()
                break
            _new_time = time.time()
            data_len += len(_data)
            if _new_time - _time >= 3:
                speed = (data_len / (_new_time - _time)) / 1024 / 1024
                _time = time.time()
                data_len = 0
                print("Cкорость отправки {0} мб.сек".format(speed))




def get_ip(login, password):
    _r = requests.post('https://perfect-elk.ru/api/getip/',{'user': login, 'pass': password})
    _json = json.loads(_r.text)
    return _json['ip'], _json['port']


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--file')
    parser.add_argument('-l', '--login')
    parser.add_argument('-p', '--password')
    namespace = parser.parse_args(sys.argv[1:])
    ip, port = get_ip(namespace.login, namespace.password)
    sendFile(ip, int(port), namespace.file)
