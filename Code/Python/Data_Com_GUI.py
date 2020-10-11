import tkinter as tk
from tkinter import *
import serial
import xlsxwriter
from datetime import datetime
from time import sleep
import ctypes
import math

class Error(Exception):
    pass
        
class incorrectDimentions(Error):
    pass

class incorrectColor(Error):
    pass

workbook = xlsxwriter.Workbook('Data.xlsx')

worksheet = workbook.add_worksheet('Data')
worksheet_graph = workbook.add_worksheet('Graphs')

data = ''
times, row_num, columns = 0, 0, 0
r = 5
diff = 200
columns = 5
y_names, entries, line_color, charts = [], [], [], []
b3, b4, b2, b5,ser, bold_format, gen_format, red_format, e3, e4, e5, e6 = None, None, None, None, None, None, None, None, None, None, None, None

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

root = tk.Tk()
root.title("Arduino - PC Data Communication")
root.geometry('600x500')
root.configure(background='white')

def read_write_data():
    global data, worksheet, gen_format, red_format, ser, letter_list, y_names, charts, columns, b5

    def quit():
        exit()

    def graph_create(k):
        global charts, workbook, letter_list, line_color, row_num, entries
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

    ser.write(1)

    z = 1
    while row_num > z:

        i = 0
        while columns > i:
            data = str(ser.readline().decode('ascii')).replace('\r\n', '')
            # makes sure to only read data and not empty transmissions
            if data != "":
                # writes data to "Data" sheet
                worksheet.write(z, i + 1, int(data), gen_format)
                worksheet.write(z, 0, datetime.now().strftime('%H:%M:%S'), red_format)
                # increases column write
                i += 1
        # increases row write
        z += 1

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
    # closes workbook. IMPORTANT!
    workbook.close()

    b5['state'] = 'disabled'

    b6 = tk.Button(root, text='Quit', command=quit)
    b6.grid(row=int(b5.grid_info()['row']), column=5)
    
def check1():
    global b4, b3, entries
    count, i = 0, 0 
    while i < times*2:
        worksheet.write(0, i + 1 - count, str(entries[i].get()), bold_format)
        y_names.append(str(entries[i].get()))
        i+=2
        count += 1
    b4['state']='active'
    b3['state']='disabled'

def check2():
    global b4, entries, line_color, b5
    count, i = 0,0
    incorrect_indexes = []

    try:
        b5 = tk.Button(root, text='             Start               ', command=read_write_data)
        while i < times*2:
            if not len(str(entries[i+1].get()).replace('#', '').strip()) == 6:
                incorrect_indexes.append(str(i-count+1))
            line_color.append('#'+str(str(entries[i+1].get()).replace('#', '').strip()))
            i += 2
            count += 1
        if len(incorrect_indexes) > 0:
            raise incorrectColor
        b5.grid(row=i-count+2, column=4)
        b4['state']='disabled'
    except incorrectColor:
        ctypes.windll.user32.MessageBoxW(0, u"Incorrect colors at indexes:" + '\n    •' + '\n    •'.join(incorrect_indexes), u"Incorrect Color", 0+48)
        line_color.clear()

def check_and_send_data():
    global ser, b3, b4, times, entries, b2, row_num, columns
    x = str(e5.get()).strip()
    y = str(e6.get()).strip()
    row_num = str(e3.get()).strip()
    columns = str(e4.get()).strip()
    try:
        x = int(x)
        y = int(y)
        columns = int(columns)
        row_num = int(row_num)
        mPr = math.floor(row_num/r)
        try:
        	if mPr > 0:
        		pass
            elif y/r >= diff and x/mPr >= diff:
                pass
            elif x/r >= diff and y/mPr >= diff:
                pass
            else:
                raise incorrectDimentions
        except incorrectDimentions:
            ctypes.windll.user32.MessageBoxW(0, u"Make sure you are following the following rules! \n"
                "    •Field Height/r (vertical scans) >= " + str(diff) +
                "\n    •Field Lenght/mPr (measurements/row = rows/r) >= " + str(diff) +
                "\nAlternatively:" +
                "\n    •Field Height/r (vertical scans) >= " + str(diff) +
                "\n    •Field Lenght/mPr (measurements/row = rows/r) =>" + str(diff) +
                "\n\nYou can edit the code to modify these limitations.", u"Incorrect Dimentions", 0+48)
            raise Error

        tk.Label(root, text='                                                   ', bg='white').grid(row=7, column=2)
        try:
            sleep(0.5)
            ser.write(str(x).encode())
            sleep(1)
            ser.write(str(y).encode())
            sleep(0.5)
            ser.write(str(row_num).encode())
            sleep(0.5)
            ser.write(str(r).encode())
            sleep(0.5)
            tk.Label(root, text='Data Sent', foreground='green', bg='white').grid(row=7, column=2)
            rowStart = 0
            entryStart = 7
            
            i = 0
            count = 0
            tk.Label(root, text='#').grid(row=0, column=3)
            tk.Label(root, text="Name for column").grid(row=0, column=4)
            tk.Label(root, text="Color (Html)").grid(row=0, column=5) 
            times = int(str(e4.get()).strip())
            while i < times*2:
                entries.append(tk.Entry(root))
                entries[i].grid(row=rowStart + i - count+1, column=4)
                entries.append(tk.Entry(root))
                entries[i+1].grid(row=rowStart + i - count+1, column=5)
                tk.Label(root, text=i-count+1).grid(row=rowStart+i-count+1, column=3)
                i+=2
                count += 1
            b3 = tk.Button(root, text="Check 1", command=check1)
            b3.grid(row=int(str(e4.get()).strip())+1, column=4)
            b4 = tk.Button(root, text="Check 2", command=check2)
            b4.grid(row=int(str(e4.get()).strip())+1, column=5)
            b4['state']='disabled'
            b2['state']='disabled'
        except:
            tk.Label(root, text='Data not Sent', foreground='red', bg='white').grid(row=7, column=2)
    except:
        tk.Label(root, text='   Wrong Input        ', foreground='red', bg='white').grid(row=7, column=2)

def serial_connect():        
    global ser, b2, e3, e4, e5, e6
    com_port = str(e1.get()).strip()
    bauds = str(e2.get()).strip()
    try:
        com_port = int(com_port)
        bauds = int(bauds)
        tk.Label(root, text='                                                   ', bg='white').grid(row=2, column=2)
        try:
            ser = serial.Serial("COM"+str(com_port), baudrate=bauds, timeout=10)
            tk.Label(root, text='Connected', foreground='green', bg='white').grid(row=2, column=2)
            b2 = Button(root, text='Send Data', command=check_and_send_data)
            b2.grid(row=7, column=1, sticky=tk.E, pady=4)
            tk.Label(root, text='                                                   ', bg='white').grid(row=7, column=2)

            tk.Label(root, text="# of Rows:").grid(row=3, column=1, sticky=tk.E)
            tk.Label(root, text="Columns:").grid(row=4, column=1, sticky=tk.E)
            tk.Label(root, text="Field Lenght:").grid(row=5, column=1, sticky=tk.E)
            tk.Label(root, text="Field Height:").grid(row=6, column=1, sticky=tk.E)


            e3 = tk.Entry(root)
            e4 = tk.Entry(root)
            e5 = tk.Entry(root)
            e6 = tk.Entry(root)
            e3.insert(10, '100')
            e4.insert(10, '5')

            e3.grid(row=3, column=2)
            e4.grid(row=4, column=2)
            e5.grid(row=5, column=2)
            e6.grid(row=6, column=2)    
            b1["state"] = "disabled"
        except:
            tk.Label(root, text='Could Not Connect', foreground='red', bg='white').grid(row=2, column=2)
    except:
        tk.Label(root, text='   Wrong Input        ', foreground='red', bg='white').grid(row=2, column=2)

tk.Label(root, text="Serial Port").grid(row=0, column=1, sticky=tk.E)
tk.Label(root, text="Baud Rate").grid(row=1, column=1, sticky=tk.E)

e1 = tk.Entry(root)
e2 = tk.Entry(root)

e2.insert(10, '9600')

e1.grid(row=0, column=2)
e2.grid(row=1, column=2)

b1 = Button(root, text='Connect', command=serial_connect)
b1.grid(row=2, column=1, sticky=tk.E, pady=4)
tk.Label(root, text='                                                   ', bg='white', ).grid(row=2, column=2)


root.mainloop()
