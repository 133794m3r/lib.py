#!/usr/bin/python3
"""
Base32 Encoder/Decoder Module
By Macarthur Inbody
License AGPLv3 or Later
(C) 2020
Functions \n
b32_encode; b32_decode
Both functions take in a string or bytes object and will return a string.

b32_encode will encode any string given to it with zb32 alphabet.
b32_decode will decode any string encoded with zb32 alphabet into it's original form.
"""


def b32_decode(src):
	"""b32_decode
	arguments:
	{string|bytes} src -- The source string to encode.
	\n
	This program will decode a zb32 encoded string. Aka Zooko-Base32 alphabet.
	"""
	#bunch of variables.
	i=0;j=0;a=0;b=0;c=0;d=0;e=0;f=0;g=0;h=0;
	#get the original length.
	orig_len=len(src);
	#replace all of the = signs with blanks.
	src=src.replace("=","")
	#get the new source length.
	src_len=len(src);
	#our proper length is the difference between the two.
	orig_len=orig_len - src_len;
	dest=""
	
	#RFC Table
	#table='ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
	
	#our table to utilize.
	table="ybndrfg8ejkmcpqxot1uwisza345h769";
	byte=0;
	#while we're less than the src length.
	while i < src_len:
		'''
		do all of the following. 
		To keep it simple I'm only going to explain one line because they're all the same.
		OK time to unwrap some code.
		1) First I see if our value for i is less than the src_len variable.
			a) If it is then we find the index of the charater in our table.
			b) If it's not we set the index to be 0.
		2) We take i and add a value to it.
			a) If it's i is less than the max we set the value to 1.
			b) otherwise it's 0.
			Either way it's added to the value of i.
		If Python was a real language and included ++ the lines below would be way simpler.
		For example the first one that sets the variable a would be as follows.
		a=(table.find(src[i++]) if i < src_len else 0)
		that's it. That's all I would have to do. If i was not less than src_len then we
		would just set the value to 0 and wouldn't increment i.
		'''
		a=( table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)
		b=(table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)
		c=(table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)
		d=(table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)
		e=(table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)
		f=(table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)						
		g=(table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)
		h=(table.find(src[i]) if i < src_len else 0); i=i+( 1 if i < src_len else 0)
		'''
		Same thing here one line will be explained the rest won't.
		Since Python doesn't support signed values for variables I have to do the last bit.
		But first what I'm doing. I'll just explain the first line.
		
		1)I take the value of a shift all bits left by 3,
		2)I take the value of b shift all bits right by 2.
		3) Or the final value of a and b.
		4) Take that resulting value and bitwise AND it with 0xff.
		
		This will make any negative value suchas -1 and convert it to 255. It does this via
		the binary values given below.
		-1 = 11111111 Because the left-most bit is the sign bit if it's set the value is negative.
		255 = 11111111 Because it is unsigned the leftmost bit is just used as a normal value.
		Now back to your regularly scheduled program.
		
		5) I then take this decimal value and get the character pointed to by it's codepoint.
		6) I then append this to the dest string.
		'''
		dest+= chr(( a << 3 | b >> 2) & 0xff)
		dest+= chr(( b << 6 | c << 1 | d >> 4) &0xff)
		dest+= chr((d <<4 | e >> 1) & 0xff)
		dest+= chr(( e << 7 | f << 2 | g >> 3) &0xff)
		dest+= chr( (g << 5 | h ) & 0xff)
	#if the difference is more than 0 that means we'll have null bytes.
	if orig_len > 0:
		#I just remove all null bytes from the string.
		dest=dest.replace('\x00','')
	#then I return the destination string.
	return dest
	

def b32_encode(src):
	"""b32_encode
	arguments:
	{string|bytes} src -- The source string to encode.
	\n
	This program will encode a string into a b32 encoded string utilizing zb32 alphabet.
	"""
	i=0;j=0;a=0;b=0;c=0;d=0;e=0;
	src_len=len(src);
	#leftover bytes is the remainder or padding we have to do.
	leftover_bytes=(src_len % 5)
	
	#RFC Table
	#table='ABCDEFGHIJKLMNOPQRSTUVWXYZ234567'
	
	#our alphabet.
	table="ybndrfg8ejkmcpqxot1uwisza345h769";
	padding="="
	'''
	the output length we're going to have.
	OK so to depack this one. It'll give us the exact length of the output value.
	1) Take 5 - leftover_bytes giving us how many bytes we are away from a full set of 5.
	2) Take src_len add it to this value so that we get the value with the remainder.
	3) Take this resulting value and divide it by 5 with the floor operator to get us 
	how many sets of 5 we've got.
	4) Then we multiply it by 8.
	5) This gives us the size of our output.
	E.g. src_len = 7. leftover_bytes = 7 % 5 => 2.
	7 + (5 -2) = 10. 
	10 // 5 = 2.
	2 << 3(or times 8) = 16. Output is thus 16 bytes including padding.
	'''
	out_len =  ((src_len + (5 - leftover_bytes)) //5) << 3
	replace_bytes=0
	dest='';
	#while i is less than src_len
	while i < src_len:
		'''
		Like before I'm only going to explain one line.
		1) If i is less than src_len get the codepoint of the character at the index of 
		i. Otherwise we make the value be 0.
		2) Set this value to the variable.
		3) Then I increment i by one value.
		If python supported ++ it'd be just the following line.
		a=(ord(src[i++]) if i < src_len else 0)
		'''
		a=(ord(src[i]) if i < src_len else 0);i+=1
		b=(ord(src[i]) if i < src_len else 0);i+=1
		c=(ord(src[i]) if i < src_len else 0);i+=1
		d=(ord(src[i]) if i < src_len else 0);i+=1
		e=(ord(src[i]) if i < src_len else 0);i+=1
		#like above one line only and it'll be the second one since it's more complex.
		dest+=table[(a >> 3)];j+=1
		'''
		1) I take the value of a bitwise AND it with the value 0x07.
		2) Then shift all bits left by 2(faster than multiply)
		3) take the value of b shift all bits right by 6.
		4) bitwise OR both of the previous two values.
		5) use this value as the index to the character of the table.
		6) Add this character to the destination.
		7) increment j by one.
		'''
		dest+=table[( ((a & 0x07) << 2) | (b >> 6))];j+=1
		dest+=table[( ((b & 0x3F) >> 1) )];j+=1
		dest+=table[( ((b & 0x01) << 4) | (c >> 4))];j+=1
		dest+=table[( ((c & 0x0F) << 1) | (d >> 7))];j+=1
		dest+=table[( ((d & 0x7F) >> 2))];j+=1
		dest+=table[( ((d & 0x03) << 3) | (e >> 5))];j+=1
		dest+=table[( ((e & 0x1F) ))];j+=1

	#This is to handle the amount of leftover bytes we need to pad it with.
	if leftover_bytes == 1: replace_bytes = 6;
	elif leftover_bytes == 2: replace_bytes = 4;
	elif leftover_bytes == 3: replace_bytes = 3;
	elif leftover_bytes == 4: replace_bytes = 1;
	i=0;

	#if replaces bytes is greater than or equal to 1.
	if replace_bytes >=1:
		#create padding of this many bytes.
		padding=("=" * replace_bytes)
		'''
		We slice the string dest up from the first index 0, and all but the replace_bytes
		bytes from the string. Then we append the padding to it.
		Then we set the value of dest to this new string.
		'''		
		dest=dest[0:-replace_bytes]+padding
	#reeturn the destination string.
	return dest;
