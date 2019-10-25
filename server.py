import tkinter as tk
import threading
import socket
import dill
import math


global serverSocket
global clientSocket

def add_binary_nums(x, y):
    max_len = max(len(x), len(y))

    x = x.zfill(max_len)
    y = y.zfill(max_len)
    result = ''  # initialize the result
    carry = 0   # initialize the carry
    for i in range(max_len - 1, -1, -1):   # Traverse the string
        r = carry
        r += 1 if x[i] == '1' else 0
        r += 1 if y[i] == '1' else 0
        result = ('1' if r % 2 == 1 else '0') + result
        carry = 0 if r < 2 else 1  # Compute the carry.

    if carry != 0: result = '1' + result

    return result.zfill(max_len)

def checkSumServerSideImplementation(checksum,string):
    sixteenBitArr = []
    binString = ''.join(format(ord(x),'b') for x in string)
    adtZero = math.ceil(len(binString)/16)* 16 - len(binString)
    appZero = '0'*adtZero
    binString = appZero + binString
    print(binString,len(binString))
    for i in range(0,len(binString),16):
        sixteenBitArr.append(binString[i:i+16])
    sixteenBitArr = map(lambda string:'0b'+string ,sixteenBitArr)
       
    sumOfBnos = ""
    for i in sixteenBitArr:
        print(i)
        sumOfBnos = add_binary_nums(sumOfBnos,i[2:])
        print(sumOfBnos,len(sumOfBnos))


    if (len(sumOfBnos) >= 17):
        while (len(sumOfBnos)!=16):
            sumOfBnos = add_binary_nums(sumOfBnos[1:], '0000000000000001')

    print(checksum,sumOfBnos,len(sumOfBnos))
    sumOfBnos = add_binary_nums(sumOfBnos,checksum)
    print(checksum, sumOfBnos)

    for i in sumOfBnos:
        if i=='0':
            print("error")
            return 0
    print("no error")
    return 1

def recv_message(c_check_sum, text, serverSocket):
	data, clientAddress = serverSocket.recvfrom(2048)
	data = dill.loads(data)
	msg = data['msg']
	check_sum = data['check_sum']
	correctness = checkSumServerSideImplementation(check_sum, msg)
	text.insert("1.0", msg+"\n")
	if(correctness):
		c_check_sum.insert(0, "Checksum is correct")
	else:
		c_check_sum.insert(0, "Checksum is incorrect")
	print(msg)
	if(msg != "bye"):
		recv_message(c_check_sum, text, serverSocket)


def server(c_check_sum, text):
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSocket.bind(('localhost', 12000))
	t1 = threading.Thread(target = recv_message, args = [c_check_sum,text, serverSocket])
	t1.start()
	# t1.join()
		


root = tk.Tk()
root.title("Working of Checksum")
root.geometry("600x600")


c_check_sum = tk.Entry(root, bg = "grey", bd = 3)
text = tk.Text(root, bg = "grey", bd = 3)
# action_arg = partial(action, text)
c_server = tk.Button(root, text = "Create Server", command = lambda: server(c_check_sum, text), font = "Verdana 10")
# c_sendMessage = tk.Button(root, text = "Send Message", command = lambda: action(text))
text1 = """Message received
from client"""
label1 = tk.Label(root, text = text1, font = "Verdana 10")


c_server.place(relwidth = 0.17, relheight = 0.075, relx = 0.415, rely = 0.05)
text.place(relwidth = 0.375, relheight = 0.225, relx = 0.3125, rely = 0.15)
# c_sendMessage.place(relx = 0.375, rely = 0.6)
c_check_sum.place(relx = 0, rely = 0.75, relwidth = 0.5)
label1.place(relwidth = 0.26, relx = 0.025, rely = 0.23)

root.mainloop()