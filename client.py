import tkinter as tk
import math
import dill
import socket


serverSocket = 0
clientSocket = 0

def send_message(text):
	global clientSocket
	msg = str(text.get("1.0", "end-1c"))
	check_sum = checkSumClientSideImplementation(msg);
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

    if carry != 0: result = '1' + result

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
root.geometry("400x400")

text = tk.Text(root, bg = "grey", bd = 3)
text.place(relwidth = 0.5, relheight = 0.3, relx = 0.25, rely = 0.25)

c_client = tk.Button(root, text = "Create Client", command = client)
c_client.place(relwidth = 0.2, relheight = 0.1, relx = 0.7, rely = 0.1)

c_sendMessage = tk.Button(root, text = "Send Message", command = lambda: send_message(text))
c_sendMessage.place(relx = 0.375, rely = 0.6)


root.mainloop()