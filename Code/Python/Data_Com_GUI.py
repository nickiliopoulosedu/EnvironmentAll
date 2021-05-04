# imports tkinter UI library
import tkinter as tk
# imports serial communication library
import serial
# imports xlsxwriter library to write on excel
import xlsxwriter
# imports datetime to view pc time
from datetime import datetime
# imports sleep function
from time import sleep
# imports windll function for pop up messages
from ctypes import windll
# impoprts floor function
from math import floor
# imports ascii characters
from string import ascii_uppercase as letter_list

# define custom errors
class Error(Exception):
	pass
		
class incorrectDimentions(Error):
	pass

class incorrectColor(Error):
	pass

# constant variable for data send delay
send_delay = 1

# constant variable of scans per cycle the robot makes. Default is 5
scans_per_cycle = 5

# constant flexiblity in meters allowed in the relationship between the field's dimentions and the desired amount of rows
diff = 2

# initialising empty global variables
rows, columns = 0, 0

entries = [[],[]]

y_names, line_color, charts = [[] for i in range(3)]

data, ser, root = [None for i in range(3)]

connect_btn, baudrate_entry, com_port_entry, validate_colors_btn, Start_RW_btn, send_data_btn, row_num_entry, col_num_entry, field_len_entry, field_height_entry = [None for i in range(10)]

# create a workbook
workbook = xlsxwriter.Workbook('Data.xlsx')

# create workbook sheets
worksheet = workbook.add_worksheet('Data')
worksheet_graph = workbook.add_worksheet('Graphs')

# creates bold format
bold_format = workbook.add_format()
bold_format.set_bold()
bold_format.set_align('center')
bold_format.set_align('vcenter')
bold_format.set_font_size(14)

# creates general format
gen_format = workbook.add_format()
gen_format.set_align('center')
gen_format.set_align('vcenter')
gen_format.set_font_size(12)

# creates red text format
red_format = workbook.add_format()
red_format.set_align('center')
red_format.set_align('vcenter')
red_format.set_size(12)
red_format.set_font_color('red')

worksheet.write(0, 0, 'Event Time (ms)', bold_format)

def show_color_table():
	global entries, validate_colors_btn, Start_RW_btn, send_data_btn
	# informs user for successfull data transmission
	tk.Label(root, text='Data Sent', foreground='green', bg='white').grid(row=7, column=2)

	# show labels for color/name table
	tk.Label(root, text='#').grid(row=0, column=3)
	tk.Label(root, text="Name for column").grid(row=0, column=4)
	tk.Label(root, text="Color (Html)").grid(row=0, column=5) 

	for i in range(columns):	
		# create entry fields for name columns
		entries[0].append(tk.Entry(root))
		entries[0][i].grid(row=i+1, column=4)
		
		# create entry fields for graph color
		entries[1].append(tk.Entry(root))
		entries[1][i].insert(10, '000000')
		entries[1][i].grid(row=i+1, column=5)
		
		# show number label
		tk.Label(root, text=i+1).grid(row=i+1, column=3)

	# create check button
	validate_colors_btn = tk.Button(root, text="Validate and Save", command=check_colors)
	validate_colors_btn.grid(row=columns+1, column=4)

	# create start button
	Start_RW_btn = tk.Button(root, text="Start", command=read_write_data)
	Start_RW_btn.grid(row=columns+1, column=5)
	Start_RW_btn['state']='disabled'

	# disable send data button
	send_data_btn['state']='disabled'

def read_data():
	global worksheet
	# transmits initialisation byte
	ser.write(1)

	# reads received data and removes "\r\n" prefix
	for i in range(1, rows):
		
		# writes data per column
		for j in range(columns):

			data = str(ser.readline().decode('ascii')).replace('\r\n', '')
			
			# makes sure to only read data and not empty transmissions
			if data != "":

				# writes data to "Data" sheet
				worksheet.write(i, j + 1, int(data), gen_format)
				worksheet.write(i, 0, datetime.now().strftime('%H:%M:%S'), red_format)
	# closes Serial communication
	ser.close()

def graph_create(i):
	
	charts.append(workbook.add_chart({'type': 'line'}))
	# sets x axis
	charts[i].set_x_axis({'name': 'Time (HMS)'})
	# sets y axis accordingly to user input
	charts[i].set_y_axis({'name': y_names[i]})
	# removes legend
	charts[i].set_legend({'none': True})
	# adds a data series
	charts[i].add_series({
		'name': '=Data!$' + str(letter_list[i + 1]) + '$1',
		'categories': '=Data!$A$2:$A$' + str(int(rows) - 1),
		'values': '=Data!$' + str(letter_list[i + 1]) + '$2:$' + str(letter_list[i + 1]) + '$' + str(int(rows) - 1),
		'line': {'color': line_color[i]}
	})

def read_write_data():
	global worksheet, charts
	
	read_data()
	# creates and saves graph to excel
	x = 1
	for i in range(columns):
		graph_create(i)
		worksheet_graph.insert_chart(str(letter_list[1]) + str(x), charts[i])
		x += 16

	# closes workbook. IMPORTANT!
	workbook.close()

	# creates a quit button
	quit_btn = tk.Button(root, text='Quit', command=exit)
	quit_btn.grid(row=int(Start_RW_btn.grid_info()['row']) + 1, column=4)
	
def check_colors():
	global Start_RW_btn, validate_colors_btn, line_color

	# list for incorrect colors
	incorrect_indexes = []
	try:
		for i in range(columns):
			# reads color from entry
			color = str(entries[1][i].get()).replace('#', '').strip()

			# adds color to color list
			line_color.append('#'+ color)

			#checks color validity
			if not len(color) == 6:
				# appends incorrect color to list
				incorrect_indexes.append(str(i+1))
				
		# tests if incorrect colors exist
		if len(incorrect_indexes) > 0:
			# raises incorrectColor error
			raise incorrectColor

		for i in range(columns):
			# appends name and names column after inputed name
			y_names.append(str(entries[0][i].get()))
			worksheet.write(0, i + 1, y_names[i], bold_format)
		
		# disables validate button
		validate_colors_btn['state']='disabled'

		# enbles start button 
		Start_RW_btn['state']='active'
		
	# handles case of incorrect color
	except incorrectColor:
		# shows pop up with incorrecr indexes to user
		windll.user32.MessageBoxW(0, u"Incorrect colors at indexes:'\n    •" + '\n    •'.join(incorrect_indexes), u"Incorrect Color", 0+48)
		
		# clears list of colors
		line_color.clear()

def check_and_send_data():
	global rows, columns
	
	try:
		# get specifications from input fields and store them as int
		x = int(str(field_len_entry.get()).strip())
		y = int(str(field_height_entry.get()).strip())
		columns = int(str(col_num_entry.get()).strip())
		rows = int(str(row_num_entry.get()).strip())

		# finds how many field rows the robot has to scan to get the required number of measurements
		required_field_rows = floor(rows/scans_per_cycle)

		# test if values are physically possible
		if required_field_rows > 0 and y/scans_per_cycle >= diff and x/required_field_rows >= diff:
			pass
		elif required_field_rows > 0 and x/scans_per_cycle >= diff and y/required_field_rows >= diff:
			pass
		else:
			# raisee error to inform the user of inpossible values
			raise incorrectDimentions

		tk.Label(root, text='                                                   ', bg='white').grid(row=7, column=2)
		
		try:
			# send data to robot
			sleep(send_delay)
			ser.write(str(x).encode())
			sleep(send_delay)
			ser.write(str(y).encode())
			sleep(send_delay)
			ser.write(str(rows).encode())
			sleep(send_delay)
			ser.write(str(scans_per_cycle).encode())
			sleep(send_delay)
			ser.write(required_field_rows)
			show_color_table()
		except:
			# handles errors during data transmission
			tk.Label(root, text='Data not Sent', foreground='red', bg='white').grid(row=7, column=2)
	except incorrectDimentions:
		# pop up informing user of impossible values
		windll.user32.MessageBoxW(0, u"Make sure you are following these rules! \n"
			f"\n•Field Height / vertical scans ({scans_per_cycle}) >= {diff}" +
			f"\n•Field Lenght / required_field_rows (rows ({rows}) / scans_per_cycle ({scans_per_cycle}) = {required_field_rows}) >= {diff}" +
			f"\n•rows ({rows}) / scans_per_cycle ({scans_per_cycle}) > 0" +
			"\n\nAlternatively:" +
			f"\n•Field Lenght / vertical scans ({scans_per_cycle}) >= {diff}" +
			f"\n•Field Height / required_field_rows (rows ({rows}) / scans_per_cycle ({scans_per_cycle}) = {required_field_rows}) >= {diff}"  +
			f"\n•rows ({rows}) / scans_per_cycle({scans_per_cycle}) > 0" 
			f"\n\nYou can edit the code to modify these limitations.", u"Incorrect Dimentions", 0+48)
		tk.Label(root, text='   Wrong Input        ', foreground='red', bg='white').grid(row=7, column=2)
	except:
		# handles invalid input
		tk.Label(root, text='   Wrong Input        ', foreground='red', bg='white').grid(row=7, column=2)

def serial_connect():
	global ser, send_data_btn, row_num_entry, col_num_entry, field_len_entry, field_height_entry     
	
	try:
		# read and validate com port and baud rate inputs
		com_port = int(str(com_port_entry.get()).strip())
		bauds = int(str(buadrate_entry.get()).strip())
		tk.Label(root, text='                                                   ', bg='white').grid(row=2, column=2)
		
		# try connecting to com port
		ser = serial.Serial("COM"+str(com_port), baudrate=bauds, timeout=10)
		
		# verify connection to user
		tk.Label(root, text='Connected', foreground='green', bg='white').grid(row=2, column=2)
		
		# show labels for field specifications
		tk.Label(root, text="# of Rows:").grid(row=3, column=1, sticky=tk.E)
		tk.Label(root, text="Columns:").grid(row=4, column=1, sticky=tk.E)
		tk.Label(root, text="Field Lenght (m):").grid(row=5, column=1, sticky=tk.E)
		tk.Label(root, text="Field Height (m):").grid(row=6, column=1, sticky=tk.E)

		# create entry fields for field secifications
		row_num_entry = tk.Entry(root)
		col_num_entry = tk.Entry(root)
		field_len_entry = tk.Entry(root)
		field_height_entry = tk.Entry(root)
		
		# incert default values to fields
		row_num_entry.insert(10, '100')
		col_num_entry.insert(10, '3')
		field_len_entry.insert(10, '100')
		field_height_entry.insert(10, '100')

		# align fields to grid
		row_num_entry.grid(row=3, column=2)
		col_num_entry.grid(row=4, column=2)
		field_len_entry.grid(row=5, column=2)
		field_height_entry.grid(row=6, column=2)  

		#show send data button
		send_data_btn = tk.Button(root, text='Send Data', command=check_and_send_data)
		send_data_btn.grid(row=7, column=1, sticky=tk.E, pady=4)
		tk.Label(root, text='                                                   ', bg='white').grid(row=7, column=2)

		# disable connect button
		connect_btn["state"] = "disabled"
	except ValueError:
		# print invalid input error
		tk.Label(root, text='   Wrong Input        ', foreground='red', bg='white').grid(row=2, column=2)
	except:
		# print connection Error
		tk.Label(root, text='Could Not Connect', foreground='red', bg='white').grid(row=2, column=2)
	sleep(2)

def main():
	global com_port_entry, buadrate_entry, connect_btn
	# configure windows title and size
	root = tk.Tk()
	root.title("Arduino - PC Data Communication")
	root.geometry('600x500')
	root.configure(background='white')
	
	# show labels for com info
	tk.Label(root, text="Serial Port").grid(row=0, column=1, sticky=tk.E)
	tk.Label(root, text="Baud Rate").grid(row=1, column=1, sticky=tk.E)

	# create empy entry fields for com info
	com_port_entry = tk.Entry(root)
	buadrate_entry = tk.Entry(root)

	# set default values for com info fields
	com_port_entry.insert(10, '3')
	buadrate_entry.insert(10, '9600')

	# align fields to grid 
	com_port_entry.grid(row=0, column=2)
	buadrate_entry.grid(row=1, column=2)

	# create connect button
	connect_btn = tk.Button(root, text='Connect', command=serial_connect)
	connect_btn.grid(row=2, column=1, sticky=tk.E, pady=4)
	tk.Label(root, text='                                                   ', bg='white', ).grid(row=2, column=2)

	root.mainloop()

main()
