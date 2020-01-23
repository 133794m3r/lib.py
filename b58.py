from math import *
'''
#C conversion doesn't work.
def b58_fast2(b58):
	i=j=0;
	tmp=0
	b58_len=len(b58)
	out_len=b58_len * 3 /4
	out = [ 0] * out_len
	while i < b58_len:
		c=ord(b58[i])
		
		if b58[i] < 58:
			c -=49
		elif b58[i] < 73:
			c-=56;
		elif b58[i] < 79:
			c-=57;
		elif b58[i] <91:
			c-=58
		elif b58[i] < 108:
			c-=64
		else:
			c-=65
			
		j=out_len-1
		while j >=0:
			tmp = ((out[j] * 58) + c) & 0xffff
			c = ((tmp & (~0xff)) >> 8) & 0xffff
			out[j] = tmp & 0xff	
			j-=1
			
		i+=1
	
	return out
	
def b58_fast(b58):
	b58_digits_mapped=[0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0x00, 0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0x09, 0x0A, 0x0B, 0x0C, 0x0D, 0x0E, 0x0F, 0x10, 0xFF, 0x11, 0x12, 0x13, 0x14, 0x15, 0xFF,
    0x16, 0x17, 0x18, 0x19, 0x1A, 0x1B, 0x1C, 0x1D, 0x1E, 0x1F, 0x20, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF,
    0xFF, 0x21, 0x22, 0x23, 0x24, 0x25, 0x26, 0x27, 0x28, 0x29, 0x2A, 0x2B, 0xFF, 0x2C, 0x2D, 0x2E,
0x2F, 0x30, 0x31, 0x32, 0x33, 0x34, 0x35, 0x36, 0x37, 0x38, 0x39, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
	b58_len=len(b58)
	out=[0] * ((b58_len *3) /4)
	i=0
	while i < b58_len:
		if b58[i] != '1':
			break;
		i+=1

	j=0;
	i=0;
	t=0;
	c=0;
	z=i
	h=(b58_len //4) -1
	l=h
	while i < b58_len:
		c = b58_digits_mapped[ord(b58[i])]
		j=h
	 	while j > 0:
			if j == l:
				if c:
					l-=1
				else:
					break;
			else:
				c+=out[j]*58
			j-=1
	
			out[j] = c &0xff
			c >>=32 & 0xffff
		
		i+=1
	
	 		
	print(out)
'''
def b58_encode(string,text=True):
	i=0;j=0;digits=[0]
	string_len=len(string)
	digit_len=1;
	carry=0;
	alphabet="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz";	
	while i < string_len:
		j=0;
		while j < digit_len:
			digits[j] <<=8
			j+=1

		digits[0]+=ord(string[i])
		carry=0;
		j=0;
		while j < digit_len:
			digits[j] += carry
			carry=(digits[j] // 58)
			digits[j] %= 58
			j+=1
		while carry:
			digits.append(carry % 58)
			carry = (carry // 58)
			digit_len+=1
		i+=1;
	zeroes=ceil( (string_len * 8 ) / 5.857980995127572) - digit_len
	while i < zeroes:
		digits.append(0)
		i+=1

	return	''.join(map(lambda x: alphabet[x],digits[::-1]))
			

def b58_decode(string,text=True):
	alphabet_map={"1":0,"2":1,"3":2,"4":3,"5":4,"6":5,"7":6,"8":7,"9":8,"A":9,"B":10,"C":11,"D":12,"E":13,"F":14,"G":15,"H":16,"J":17,"K":18,"L":19,"M":20,"N":21,"P":22,"Q":23,"R":24,"S":25,"T":26,"U":27,"V":28,"W":29,"X":30,"Y":31,"Z":32,"a":33,"b":34,"c":35,"d":36,"e":37,"f":38,"g":39,"h":40,"i":41,"j":42,"k":43,"m":44,"n":45,"o":46,"p":47,"q":48,"r":49,"s":50,"t":51,"u":52,"v":53,"w":54,"x":55,"y":56,"z":57}
	alphabet="123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"
	import re
	bytes='';c=0;carry=0;j=0;
	i=0;
	
	string_len=len(string)
	bytes_len=1
	if(string_len ==0):
		raise ValueError("String must be at least 1 character long.")
	pattern='[^{}]'.format(alphabet_map)
	if re.findall(pattern,string):
		raise ValueError("Your string '{}' doesn't contain valid characters.".format(string))
	bytes=[0]
	while i < string_len:
		c=string[i]
		j=0		
		while j < bytes_len:
			bytes[j] *= 58
			j+=1

		bytes[0]+=alphabet_map[c]
		carry=0
		j=0
		while j<bytes_len:
			bytes[j] +=carry
			carry = bytes[j] >> 8
			bytes[j] &= 0xff
			j+=1			
		while carry:
			bytes.append( carry & 0xff)
			carry >>=8
			bytes_len+=1
			
		i+=1
	i=0
	while string[i] == "1" and i < string_len -1:
		bytes.append(0)
		i+=1
	bytes=bytes[::-1]
	if text:
		bytes=''.join([ chr(byte) for byte in bytes ])
		
	return bytes

b58_str="NVCijF7n6peM7a7yLYPZrPgHmWUHi97LCAzXxSEUraKme"
print(b58_decode("NVCijF7n6peM7a7yLYPZrPgHmWUHi97LCAzXxSEUraKme"))
