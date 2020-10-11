# imports Serial Communication library
import serial
# imports xlsxwirter library to write on excel
import xlsxwriter
# imports datetime to view pc time
from datetime import datetime
from time import sleep

# declares number of rows variable
row_num = 0
# declares number of columns variable
columns = 0
# declares bauds rate variable
bauds = 0
# declares COM port number variable
com_num = 0
# declares serial monitor variable
ser = 0

cin = 0

# creates empty list for color of graph lines
line_color = []
# creates empty object list for charts
charts = []
# creates empty list for y names
y_names = []
# creates the list of alphabet letters
letter_list = [
    'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H',
    'I', 'J', 'K', 'L',
    'M', 'N', 'O', 'P',
    'Q', 'R', 'S', 'T',
    'U', 'V', 'W', 'X',
    'Y', 'Z']
# creates list of Html basic color codes
color_list = [
    ['black   is 000000'],
    ['blue    is 0000FF'],
    ['brown   is 800000'],
    ['cyan    is 00FFFF'],
    ['gray    is 808080'],
    ['green   is 008000'],
    ['lime    is 00FF00'],
    ['magenta is FF00FF'],
    ['navy    is 000080'],
    ['orange  is FF6600'],
    ['pink    is FF00FF'],
    ['purple  is 800080'],
    ['red     is FF0000'],
    ['silver  is C0C0C0'],
    ['white   is FFFFFF'],
    ['yellow  is FFFF00']]

# creates or overwriting a workbook
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

# asks serial port number
while True:
    try:
        com_num = input('Enter COM Input Port Number: ')
        int(com_num)
    except ValueError:
        print('Not a number, try again')
        continue
    com_num = int(com_num)
    break

# asks serial port bauds number
while True:
    try:
        bauds = input('Enter Baud Rate: ')
        int(bauds)
    except ValueError:
        print('Not a number, try again')
        continue
    bauds = int(bauds)
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
        row_num = input('Enter Number of Rows (Except the Title): ')
        int(row_num)
    except ValueError:
        print('Not a number, try again')
        continue
    row_num = int(row_num) + 1

    break

# asks for column number without the time
while True:
    try:
        columns = input('Enter Number of Columns (Except the Time): ')
        int(columns)
    except ValueError:
        print('Not a number, try again')
        continue
    columns = int(columns)
    break

# asks for column number without the time
while True:
    try:
        x = input('Enter Field Length: ')
        int(x)
    except ValueError:
        print('Not a number, try again')
        continue
    x = int(x)
    ser.write(x)
    break
sleep(1)
# asks for column number without the time
while True:
    try:
        y = input('Enter Field Height: ')
        int(y)
    except ValueError:
        print('Not a number, try again')
        continue
    y = int(y)
    ser.write(y)
    break

# writes title for time column
worksheet.write(0, 0, 'Event Time (ms)', bold_format)


def color_retry():
    cin2 = '#' + input('You have to enter an Html, 6 digit, color without "#" ')
    return cin2


# asks for personalised row information
i = 0
while columns > i:

    # asks name for columns
    worksheet.write(0, i + 1, input('Name the column no ' + str(i + 1) + ' '), bold_format)

    # asks for title for each y axis
    y_names.append(input('Name the axis for graph created by column no ' + str(i + 1) + ' '))

    # asks for graph line color for each row
    cin = str('#' + (input('Enter an Htlm color value without "#" to set the color of the line for column ' + str(i + 1)
                           + ' or leave blank to show a list o basic colors ')).upper())

    show = True
    stoploop = False
    while True:
        if len(cin) < 7 or len(cin) > 7:
            if show:
                # displays html basic color list and waits for valid response
                z = 0
                while len(color_list) > z:
                    print(color_list[z])
                    z += 1
                cin = '#' + input('Select a color from the "list" or enter one you like without the "#" ')
                show = False
            else:
                cin = (color_retry())
        elif len(cin) == 7:
            break

    # saves selected color to list
    line_color.append(str(cin))
    i += 1

# waiting for user input
input('Press any key to start')

# transmits data to source
ser.write(1)

# reads received data and removes "\r\n" prefix
z = 1
while row_num > z:

    # writes data per column
    i = 0
    while columns > i:
        data_raw = str(ser.readline().decode('ascii'))
        data = data_raw.replace('\r\n', '')
        # makes sure to only read data and not empty transmissions
        if data != "":
            # writes data to "Data" sheet
            worksheet.write(z, i + 1, int(data), gen_format)
            worksheet.write(z, 0, datetime.now().strftime('%H:%M:%S'), red_format)
            # increases column write
            i += 1
    # increases row write
    z += 1


# creates a graph
def graph_create(k):
    charts.append('chart' + str(k))
    # sets graph type
    charts[k] = (workbook.add_chart({'type': 'line'}))
    # sets x axis
    charts[k].set_x_axis({'name': 'Time (HMS)'})
    # sets y axis accordingly to user input
    charts[k].set_y_axis({'name': y_names[k]})
    # removes legend
    charts[k].set_legend({'none': True})
    # adds a data series
    charts[k].add_series({
        'name': '=Data!$' + str(letter_list[k + 1]) + '$1',
        'categories': '=Data!$' + 'A$2:$' + 'A$' + str(int(row_num) - 1),
        'values': '=Data!$' + str(letter_list[k + 1]) + '$2:$' + str(letter_list[k + 1]) + '$' + str(int(row_num) - 1),
        'line': {'color': line_color[k]}
    })


# closes Serial communication
ser.close()

# creates and prints graph to excel
i = 0
x = 1
while True:
    if columns > i:
        graph_create(i)
        worksheet_graph.insert_chart(str(letter_list[1]) + str(x), charts[i])
        i += 1
        x += 16
    else:
        break

print('Finished')
# closes workbook. IMPORTANT!
workbook.close()
# closes the program
exit()
