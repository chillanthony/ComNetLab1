import socket
import json
import threading
import pymysql

# extract data from json and insert legal data to database
def extract_fields(json_data, mac_to_match):

    mmac = json_data.get('mmac', None)
    timestamp = json_data.get('time', None)
    extracted_data = []

    for entry in json_data.get('data', []):
        mac = entry.get('mac', None)
        tmc = entry.get('tmc', None)
        rssi = entry.get('rssi', None)
        range_value = entry.get('range', None)
        

        if mac in mac_to_match:
            extracted_data.append({
                'mmac': mmac,
                'time': timestamp,
                'mac': mac,
                'tmc': tmc,
                'rssi': rssi,
                'range': range_value
            })
            lock.acquire()
            sql = "insert into points (mmac,time,mac,tmc,rssi,range1) values ('%s','%s','%s','%s',%s,%s);" %(mmac, timestamp, mac, tmc, rssi, range_value)
            cursor.execute(sql)
            conn.commit()
            lock.release()

    return extracted_data

# start a new thread for a new connection
def handle_client(client_socket):
    # print(f"正在处理来自{client_socket}的连接")
    t = threading.Thread(target=process_client, args=(client_socket,))
    t.start()

# receive primitive data from client, convert it to json, rip the legal data out
def process_client(client_socket):
    try:
        while True:
            chunk = client_socket.recv(8192)
            if not chunk:
                break
            data = b''
            data += chunk
            json_str = str(data,encoding='utf-8')
            # print(json_str, '\n')

            index = json_str.find('data=')
            if index != -1:
                json_str = json_str[index+5:]
                json_data = eval(json_str)
                device_macs = ["3c:7d:0a:c0:68:ad"]
                extracted_data = extract_fields(json_data,device_macs)
                if extracted_data:
                    print('succesful catched data!\n')
                    print(extracted_data, '\n')

    except Exception as e:
        # print(json_str, '\n')
        print(f"处理客户端时出现错误: {e}")
    finally:
        client_socket.close()    

def main():

    #start server and listening
    server_address = ('192.168.3.11', 8080)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(server_address)
    server_socket.listen(5)
    print(f"服务器开始运行，正在监听 {server_address}\n")

    #accept connection
    try:
        while True:
            # print('defaulttimeout=',socket.getdefaulttimeout())
            client_socket, client_address = server_socket.accept()
            # print(f"接受来自 {client_address} 的连接")
            handle_client(client_socket)

    except KeyboardInterrupt:
        print("服务器被用户中断")

    finally:
        server_socket.close()

# connect to mysql server
conn = pymysql.connect(host = '127.0.0.1', port = 3306, user = 'root', passwd = 'crypto385142', charset = 'utf8')
cursor = conn.cursor()
cursor.execute('use ComNet;')

# lock for sql database
lock = threading.Lock()

# main function
if __name__ == '__main__':
    main()