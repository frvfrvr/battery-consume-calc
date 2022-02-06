
# ! Battery Consumption Calculator
# ! Author: @frvfrvr (github.com/frvfrvr)
# ! v0.1 Development Time and Date: Jan-30-2022 6:23 PM - Jan-31-2022 6:34 PM

import os, subprocess, platform
import psutil
from datetime import *
from tkinter import *
from tkinter.filedialog import asksaveasfile


# ? initiliaze the tkinter window

twodgts = lambda x: x > 9 and f'{x}' or f'0{x}' # so the number is formmated as a 2 digit number
currtoday = datetime.now().strftime("bcc-%I%M%p-%B-%d-%Y")
filestore = []

batthr = []
battmin = []
battsec = []
battpercent = []

def convert(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    x = lambda x: x > 1 and "s" or "" # lambda function to check if x > 1 and return "s" or "" - makes word plural
    comma = lambda comma: bool(comma) and ", " or "" # lambda function to check if comma > 0 and return "," or "". add comma if > 0. adds comma if there's another number after it
    minsec = True if (bool(min) == bool(sec) == True) else False if (bool(min) == bool(sec) == False) else False # if min and sec are both true or both false, return False
    hourmin = True if (bool(hour) == bool(min) == True) else False if (bool(hour) == bool(min) == False) else False # checks if hour > 0 or min > 0
    return f"{(lambda hr: hr > 0 and f'{hr} ' or '')(hour)}{(lambda hr: hr > 0 and 'hour' or '')(hour)}{x(hour)}{comma(hourmin)}{(lambda m: m > 0 and f'{m} ' or '')(min)}{(lambda m: m > 0 and 'minute' or '')(min)}{x(min)}{comma(minsec)}{(lambda s: s > 0 and f'{s} ' or '')(sec)}{(lambda s: s > 0 and 'second' or '')(sec)}{x(sec)}"

def batteryConsumption(dt, batthr, battmin, battsec, battpercent, simple=False, multilog=False):
    # requires datetime, battery hours, battery minutes, battery seconds, battery percentage    
    global twodgts
    battery = psutil.sensors_battery()
    dthr = int(dt.strftime("%H"))
    dtmin = int(dt.strftime("%M"))
    dtsec = int(dt.strftime("%S"))
    if simple == True:
        # Manually append the new time and battery percentage in case of simple mode
        batthr.append(dthr)
        battmin.append(dtmin)
        battsec.append(dtsec)
        battpercent.append(battery.percent)
    else:
        if battery.power_plugged == False:
            if (battpercent == []) or (len(battpercent) < 2):
                battpercent.append(battery.percent)
                battsec.append(dtsec)
                batthr.append(dthr)
                battmin.append(dtmin)
                return "Calculating... Current battery percentage: " + str(battery.percent) + "%"
            elif (battpercent != []) or (battery.percent < battpercent[-1]):
                if battpercent[-1] != battery.percent:
                    battpercent.append(battery.percent)
                    battsec.append(dtsec) 
                    batthr.append(dthr) 
                    battmin.append(dtmin)
                s1 = str(twodgts(batthr[-2])) + ':' + str(twodgts(battmin[-2])) + ':' + str(twodgts(battsec[-2])) # before previous time
                s2 = str(twodgts(batthr[-1])) + ':' + str(twodgts(battmin[-1])) + ':' + str(twodgts(battsec[-1])) # current time
                FMT = '%H:%M:%S'
                tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
                if tdelta.days < 0:
                    tdelta = timedelta(
                        days=0,
                        seconds=tdelta.seconds,
                        microseconds=tdelta.microseconds
                    )
                hourminsec = int(tdelta.total_seconds())
                if multilog == False:
                    if len(battpercent) > 3:
                        del battpercent[:-3]
                        del batthr[:-3]
                        del battmin[:-3]
                        del battsec[:-3]
                return "Battery consumes 1% every " + convert(hourminsec)
            return "Data invalid. Anyway here's the current battery percentage: " + str(battery.percent) + "%"
        else:
            #return "Battery is plugged in, can't calculate consumption"
            # will calculate the 1% recharge every x hours, minutes, seconds
            # "Battery charges 1% every x hours, minutes, seconds"
            if (battpercent == []) or (len(battpercent) < 2):
                battpercent.append(battery.percent)
                battsec.append(dtsec)
                batthr.append(dthr)
                battmin.append(dtmin)
                return "Calculating... Current battery percentage: " + str(battery.percent) + "%"
            elif (battpercent != []) or (battery.percent > battpercent[-1]):
                if battpercent[-1] != battery.percent:
                    battpercent.append(battery.percent)
                    battsec.append(dtsec) 
                    batthr.append(dthr) 
                    battmin.append(dtmin) 
                twodgts = lambda x: x > 9 and f'{x}' or f'0{x}' # so the number is formmated as a 2 digit number
                s1 = str(twodgts(batthr[-2])) + ':' + str(twodgts(battmin[-2])) + ':' + str(twodgts(battsec[-2])) # before previous time
                s2 = str(twodgts(batthr[-1])) + ':' + str(twodgts(battmin[-1])) + ':' + str(twodgts(battsec[-1])) # current time
                FMT = '%H:%M:%S'
                tdelta = datetime.strptime(s2, FMT) - datetime.strptime(s1, FMT)
                if tdelta.days < 0:
                    tdelta = timedelta(
                        days=0,
                        seconds=tdelta.seconds,
                        microseconds=tdelta.microseconds
                    )
                hourminsec = int(tdelta.total_seconds())
                if multilog == False:
                    if len(battpercent) > 3:
                        del battpercent[:-3]
                        del batthr[:-3]
                        del battmin[:-3]
                        del battsec[:-3]
                return "Battery charges 1% every " + convert(hourminsec)
            return "Battery is plugged in, will try to calculate recharging or consumption later"

# ? window appearnce
window = Tk()
var = IntVar()

window.resizable(0,0)
window.title("Avg. Battery Consumption")

window.geometry('475x100') # 475x50, x100 only for testing
window.configure(bg='black', highlightbackground='black', highlightthickness=0)
window.attributes('-topmost',True) # window will always be on top for benchmark purposes

def coutput(radio):
    global twodgts
    try:
        file = asksaveasfile(defaultextension=".txt", initialfile=f"{currtoday}.txt")
        filestore.append(file.name)
        dt = datetime.now()
        battstat = batteryConsumption(dt, batthr, battmin, battsec, battpercent)
        logtime = f"{twodgts(batthr[-2])}:{twodgts(battmin[-2])}:{twodgts(battsec[-2])} {battpercent[-2]}%\n{twodgts(batthr[-1])}:{twodgts(battmin[-1])}:{twodgts(battsec[-1])} {battpercent[-1]}% - {battstat}\n"
        file.write(logtime)
        writeappend(filestore[0])
        B = Button(window, text="Open Log", command= openlog, bd=0, relief=SUNKEN, bg='black', fg='black', font=(None, 6, 'bold'))
        B.pack(side=BOTTOM, anchor=SE)
        selection = "Logging to " + file.name
        ti.config(text = selection)
        radio.pack_forget()
    except:
        return

def writeappend(filepath, simple=False):
    global twodgts
    battery = psutil.sensors_battery()
    if filepath != "":
        with open(filepath, "r") as file:
            lines = [line.strip() for line in file]
            battp = []
            for line in lines:
                battnum = line.split(" ")
                if "%" in battnum[1]:
                    # latest line in file with battery percentage as second element in the sentence
                    battp = battnum[1].split("%")
                    battp = [var for var in battp if var]
                    battp = int(battp[0]) # battery percentage becomes a number instead of a string. battp is now integer.
                    #ti.configure(text = "Logging to: " + filepath)
                    tinone(1, filepath)
                else:
                    #ti.configure(text = "Error writing in log file, retrying... last line: " + line)
                    tinone(2, line)
        with open(filepath, "a") as f:
            dt = datetime.now()
            battstat = batteryConsumption(dt, batthr, battmin, battsec, battpercent)
            stuff = f"{twodgts(batthr[-1])}:{twodgts(battmin[-1])}:{twodgts(battsec[-1])} {battpercent[-1]}% - {battstat}\n"
            f.write(stuff) if simple == True else f.write("")
            f.write(stuff) if (battery.percent != battp) else None
            window.after(1000, writeappend, filepath)
    else:
        tinone(3)
        file = asksaveasfile(defaultextension=".txt", initialfile=f"{currtoday}.txt")
        filepath = file.name
        tinone(1, file.name)
        window.after(1000, writeappend, filepath)

def tinone(msg=0, arg=None):
    # orignally tinone "ti none" was used to render nothing in label named "ti" but later expanded
    msgs = ["",
            "Logging to: " + arg,
            "Error writing in log file, retrying... last line: " + arg, # arg is the last line in the file
            "No log file found, please create one.",
            "No log file found, try save continous output first."]
    ti.configure(text = msgs[msg])

def openlog():
    try:
        filename = filestore[0]
        if platform.system() == 'Darwin':       # macOS
            subprocess.call(('open', filename))
        elif platform.system() == 'Windows':    # Windows
            os.startfile(filename)
        else:                                   # linux variants
            subprocess.call(('xdg-open', filename))
    except Exception:
        tinone(4)
        window.after(4000, tinone)

lbl = Label(window, fg='#01ff48', bg='black', justify='center') # placeholder: text="Battery consumes 1% every XXX hours, XXX minutes, XXX seconds"
lbl.place(relx=.5, rely=.2, anchor="center") # default very center: relx=.5, rely=.5, anchor="center"

timelog =  Label(window, fg='#808080', bg='black', justify='center')
timelog.place(relx=.5, rely=.60, anchor="center")

ti = Label(window, fg='#808080', bg='black', justify='center', font=(None, 8), bd=1, relief=SUNKEN, anchor=W)
ti.pack(side=BOTTOM, fill=X) # relx=.5, rely=.75, anchor="center"

R1 = Radiobutton(window, text="Save continuous output", variable=var, value=1,
                    font=(None, 6, 'bold'), command=lambda: coutput(R1), bg='black')
R1.pack( anchor = SE, side = 'bottom' )

def mmainloop():
    global twodgts
    dt = datetime.now()
    battstat = batteryConsumption(dt, batthr, battmin, battsec, battpercent)
    lbl.configure(text=battstat)
    if len(battpercent) > 1:
        logtime = f"{twodgts(batthr[-1])}:{twodgts(battmin[-1])}:{twodgts(battsec[-1])} {battpercent[-1]}%\n{twodgts(batthr[-2])}:{twodgts(battmin[-2])}:{twodgts(battsec[-2])} {battpercent[-2]}%"
        timelog.configure(text=logtime)    
    window.after(1000, mmainloop)    

window.after(1000, mmainloop)


window.mainloop()
