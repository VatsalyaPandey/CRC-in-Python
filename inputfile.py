import socket		

def xor(a, b):

	
	result = []

	
	for i in range(1, len(b)):
		if a[i] == b[i]:
			result.append('0')
		else:
			result.append('1')

	return ''.join(result)


def mod2div(dividend, divisor):

	#numberofbitstobeXOR'ed
	pick = len(divisor)

	tmp = dividend[0 : pick]

	while pick < len(dividend):

		if tmp[0] == '1':

			# replace the divident by the result
			# of XOR and pull 1 bit down
			tmp = xor(divisor, tmp) + dividend[pick]

		else: # If leftmost bit is '0'

			# If the leftmost bit of the dividend (or the
			# part used in each step) is 0, the step cannot
			# use the regular divisor; we need to use an
			# all-0s divisor.
			tmp = xor('0'*pick, tmp) + dividend[pick]

		# increment pick to move further
		pick += 1

	# For the last n bits, we have to carry it out
	# normally as increased value of pick will cause
	# Index Out of Bounds.
	if tmp[0] == '1':
		tmp = xor(divisor, tmp)
	else:
		tmp = xor('0'*pick, tmp)

	checkword = tmp
	return checkword

# Function used at the sender side to encode
# data by appending remainder of modular division
# at the end of data.
def encodeData(data, key):

	l_key = len(key)

	# Appends n-1 zeroes at end of data
	appended_data = data + '0'*(l_key-1)
	remainder = mod2div(appended_data, key)

	# Append remainder in the original data
	codeword = data + remainder
	return codeword
	
s = socket.socket()	

port = 12345		

s.connect(('127.0.0.1', port))



inp = input("Enter data you want to send->")
data =(''.join(format(ord(x), 'b') for x in inp))
print("Entered data in binary format :",data)
key = "1001"

ans = encodeData(data,key)
print("Encoded data to be sent to server in binary format :",ans)
s.sendto(ans.encode(),('127.0.0.1', 12345))


print("Received feedback from server :",s.recv(1024).decode())

s.close()
