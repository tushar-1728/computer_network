import tkinter as tk
import math
import dill
import socket


serverSocket = 0
clientSocket = 0

def send_message(text, var):
	global clientSocket
	msg = str(text.get("1.0", "1.100"))
	text.insert("1.0", "\n")
	check_sum = checkSumClientSideImplementation(msg);
	var.set(check_sum)
	dict_msg_checksum ={
		'msg': msg,
		'check_sum':check_sum
	}
	dict_msg_checksum = dill.dumps(dict_msg_checksum)
	clientSocket.sendto(dict_msg_checksum,('localhost', 12000))


def client():
	global clientSocket
	clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

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
	if carry != 0:
		result = '1' + result

	return result.zfill(max_len)

def checkSumClientSideImplementation(string):
	sixteenBitArr = []
	binString = ''.join(format(ord(x),'b') for x in string)
	adtZero = math.ceil(len(binString)/16)* 16 - len(binString)
	appZero = '0'*adtZero
	binString = appZero + binString
	print(binString,len(binString))
	for i in range(0,len(binString),16):
		sixteenBitArr.append(binString[i:i+16])
	sixteenBitArr = map(lambda string:'0b'+string ,sixteenBitArr)
	   
	sumOfBnos = '0b0'
	for i in sixteenBitArr:
		 sumOfBnos = bin(int(sumOfBnos[2:], 2) + int(i[2:], 2))

	if(len(sumOfBnos[2:])<16):
		sumOfBnos = '0b' + str(0*(16 - len(sumOfBnos[2:]))) + sumOfBnos[2:]

	print(sumOfBnos,2)

	temp = sumOfBnos[2:]
	if(len(sumOfBnos[2:])>=17):
		while(len(temp)!= 16):
			temp = add_binary_nums(temp[1:],'0000000000000001')
			#print(sumOfBnos,type(sumOfBnos))
		#sumOfBnos = sumOfBnos[3:]

	comp = ""
	for i in temp:
		if(i=='1'):
			comp = comp+'0'
		else:
			comp+='1'
	print(comp)

	return comp

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
	   
	sumOfBnos = '0b0'
	for i in sixteenBitArr:
		sumOfBnos = bin(int(sumOfBnos[2:],2) + int(i[2:],2))
		
	while(len(sumOfBnos)!=18):
		sumOfBnos = bin(int(sumOfBnos[3:],2) + int(1,2))
	
	
	sumOfBnos += checksum
	
	for i in sumOfBnos[2:]:
		if i=='0':
			print("error")
			return
	print("no error")



root = tk.Tk()
root.title("Working of Checksum")
root.geometry("600x600")

info = tk.Label(root, text = "This is the client side of checksum checking program.", font = "century 15")
info.place(relx = 0.09, rely = 0.03)

text = tk.Text(root, bg = "white", bd = 3)
text.place(relwidth = 0.5, relheight = 0.3, relx = 0.25, rely = 0.25)

label = tk.Label(root, text = "Enter your\ntext here:", bd = 1, font = "verdana 10")
label.place(relx = 0.07, rely = 0.375)

c_client = tk.Button(root, text = "Create Client", command = client, font = "verdana 10")
c_client.place(relwidth = 0.2, relheight = 0.075, relx = 0.4, rely = 0.1)

label1 = tk.Label(root, text = "Checksum of sent message:", bd = 1, font = "verdana 10")
label1.place(relx = 0.05, rely = 0.75)

var = tk.StringVar()
label2 = tk.Label(root, bg = "white", relief = tk.SUNKEN, textvariable=var, font = "verdana 10")
label2.place(relwidth = 0.5, relx = 0.4, rely = 0.75)

c_sendMessage = tk.Button(root, text = "Send Message", command = lambda: send_message(text, var))
c_sendMessage.place(relwidth = 0.2, relheight = 0.075, relx = 0.375, rely = 0.6)

root.mainloop()