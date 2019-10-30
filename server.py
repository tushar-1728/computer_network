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

def recv_message(serverSocket, text, var, var1):
	data, clientAddress = serverSocket.recvfrom(2048)
	data = dill.loads(data)
	msg = data['msg']
	check_sum = data['check_sum']
	correctness = checkSumServerSideImplementation(check_sum, msg)
	text.insert(tk.INSERT, msg+"\n")
	var.set(check_sum)
	if(correctness):
		var1.set("Correct")
	else:
		var1.set("Incorrect")
	print(msg)
	if(msg != "bye"):
		recv_message(serverSocket, text, var, var1)


def server(text, var, var1):
	serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	serverSocket.bind(('localhost', 12000))
	t1 = threading.Thread(target = recv_message, args = [serverSocket, text, var, var1])
	t1.start()		


root = tk.Tk()
root.title("Working of Checksum")
root.geometry("600x600")

info = tk.Label(root, text = "This is the server side of checksum checking program.", font = "century 15")
info.place(relx = 0.09, rely = 0.03)

label1 = tk.Label(root, text = "Message received\nfrom client", font = "Verdana 10")
label1.place(relx = 0.03, rely = 0.375)

text = tk.Text(root, bg = "white", bd = 3)
text.place(relwidth = 0.5, relheight = 0.3, relx = 0.25, rely = 0.25)

label1 = tk.Label(root, text = "Checksum of received message:", bd = 1, font = "verdana 10")
label1.place(relx = 0.03, rely = 0.65)

var = tk.StringVar()
label2 = tk.Label(root, bg = "white", relief = tk.SUNKEN, textvariable=var, font = "verdana 10")
label2.place(relwidth = 0.5, relx = 0.4, rely = 0.65)

label3 = tk.Label(root, text = "Correctness of checksum:", bd = 1, font = "verdana 10")
label3.place(relx = 0.03, rely = 0.75)

var1 = tk.StringVar()
label4 = tk.Label(root, bg = "white", relief = tk.SUNKEN, textvariable=var1, font = "verdana 10")
label4.place(relwidth = 0.5, relx = 0.4, rely = 0.75)

c_server = tk.Button(root, text = "Create Server", command = lambda: server(text, var, var1), font = "Verdana 10")
c_server.place(relwidth = 0.2, relheight = 0.075, relx = 0.4, rely = 0.1)


root.mainloop()