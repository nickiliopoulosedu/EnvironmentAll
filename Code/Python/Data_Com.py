# imports Serial Communication library
import serial

# imports xlsxwirter library to write on excel
import xlsxwriter

# imports datetime to view pc time
from datetime import datetime

#imports sleep function
from time import sleep

#imports ascii characters
from string import ascii_uppercase as letter_list

# declares number of rows variable
rows = 0
# declares number of columns variable
columns = 0

# creates empty list for color of graph lines
line_color = []
# creates empty object list for charts
charts = []
# creates empty list for y names
y_names = []

# creates dictionary of Html basic color codes
color_list = {
	"black": "000000", 
	"blue": "0000FF",
	"brown": "800000",
	"cyan": "00FFFF",
	"gray": "808080",
	"green": "008000",
	"lime": "00FF00",
	"magenta": "FF00FF",
	"navy": "000080",
	"orange": "FF6600",
	"pink": "FF00FF",
	"purple": "800080",
	"red": "FF0000",
	"silver": "C0C0C0",
	"white": "FFFFFF",
	"yellow": "FFFF00"
}

# creates or overwrites a workbook
workbook = xlsxwriter.Workbook('Data.xlsx')
#  adds sheets to the workbook
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

def input_values():
	global ser, columns, rows
	# asks serial port number
	while True:
		try:
			com_num = int(input('Enter COM Input Port Number: '))
		except ValueError:
			print('Not a number, try again')
			continue
		break

	# asks serial port bauds number
	while True:
		try:
			bauds = int(input('Enter Baud Rate: '))
		except ValueError:
			print('Not a number, try again')
			continue
		break

	# establishes connection with serial port
	while True:

		try:
			com_port = 'COM' + str(com_num)
			ser = serial.Serial(com_port, baudrate=bauds, timeout=1)
		except serial.serialutil.SerialException:
			print('Not connected')
			input('Press any key to try again')
			continue
		print('Connected')
		break

	# asks for row number without the title
	while True:
		try:
			rows = input('Enter Number of Rows (Except the Title): ')
			int(rows)
		except ValueError:
			print('Not a number, try again')
			continue
		rows = int(rows) + 1
		break

	# asks for column number without the time
	while True:
		try:
			columns = int(input('Enter Number of Columns (Except the Time): '))	
		except ValueError:
			print('Not a number, try again')
			continue
		break

	# asks for column number without the time
	while True:
		try:
			x = int(input('Enter Field Length: '))
		except ValueError:
			print('Not a number, try again')
			continue
		ser.write(x)
		break
	sleep(1)
	# asks for column number without the time
	while True:
		try:
			y = int(input('Enter Field Height: '))
		except ValueError:
			print('Not a number, try again')
			continue
		ser.write(y)
		break

def column_customise():
	# writes title for time column
	worksheet.write(0, 0, 'Event Time (ms)', bold_format)

	# asks for personalised row information
	for i in range(columns):

		# asks name for columns
		worksheet.write(0, i + 1, input('Name the column no ' + str(i + 1) + ' '), bold_format)

		# asks for title for each y axis
		y_names.append(input('Name the axis for graph created by column no ' + str(i + 1) + ' '))

		# asks for graph line color for each row
		cin = input('Enter an Htlm color value without "#" to set the color of the line for column ' + str(i + 1)
			+ ' or leave blank to show a list o basic colors ').upper()

		show = True
		while True:	
			if len(cin) != 6:
				if show:
					# displays html basic color list and waits for valid response
					for j in range(len(color_list)):
						print("{:<10}is    {:<8}".format(list(color_list)[j], list(color_list.values())[j]))
					cin = '#' + input('Select a color from the "list" or enter one you like without the "#" ')
					show = False
				else:
					cin = input('You have to enter an Html, 6 digit, color without "#" ')
			else:
				break

		# saves selected color to list
		line_color.append('#' + cin)

def read_data():

	# waiting for user input
	input('Press any key to start')

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

def graph_save():
	# creates and saves graph to excel
	x = 1
	for i in range(columns):
		graph_create(i)
		worksheet_graph.insert_chart(str(letter_list[1]) + str(x), charts[i])
		x += 16

def main():
	input_values()
	column_customise()
	read_data()
	graph_save()

	print('Finished')
	# closes workbook. IMPORTANT!
	workbook.close()

main()

# closes the program
exit()	