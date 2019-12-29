#!/usr/bin/python3

def swap_dict(input_dict):
	input_dict_items=input_dict.items()
	dict( (value,key) for key,value in input_dict_items )
