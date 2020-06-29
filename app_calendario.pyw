import calendario as cal
from tkinter import font
from tkinter import *
from functools import partial
from os import scandir, getcwd, mkdir
from os.path import abspath, isdir

meses = ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", 
         "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"]
    
def num_dias(mes, anyo):
    if mes == 'Febrero':
        return 28+cal.es_bisiesto(anyo)
    else:
        return int(cal.comprobar_mes(anyo))
    
def add_horas(entry, text, mes, s, dia, resultado_semana_text, 
              resultado_semana, resultado_mes, resultado_mes_text, 
              anyo, anyo_text, event):
    
    res = entry.get()
    if res == "":
         calendario.set_horas(cal.get_mes(mes+1), dia, 0)
    else:
        calendario.set_horas(cal.get_mes(mes+1), dia, float(res))
   
    
    anyo_text.set(calendario.get_horas())
    anyo.update()
    
    resultado_mes_text[mes].set(calendario.get_mes(mes).get_horas())
    resultado_mes[mes].update()
    
    i = 0
    for semana in calendario.get_mes(mes).get_semanas():
        if i == s:
            resultado_semana_text[mes][i].set(semana.get_horas())
            resultado_semana[mes][i].update()
        i += 1
        
    update_total()
    
def set_convenio(convenio, convenio_text, event):
    calendario.set_convenio(int(convenio.get()))
    
    update_total()
    
def update_total():
    total_text.set(calendario.get_horas()-calendario.get_convenio())
    total.update()
    
def colocar_dias(frame, num, horas_dia, horas_dia_text, resultado_semana, resultado_semana_text):
    dias = []
    dias_semana = []
    
    y = 0
    j = 0
    
    for i in "LMXJVSD":
        
        dias_semana.append(Label(frame, text=i, fg = 'red'))
        dias_semana[j//2].grid(column = j, row = y+1)
        
        j+=2
    
    for semana in calendario.get_mes(num).get_semanas():
        
        horas_dia.append([])
        horas_dia_text.append([])
        dia_semana = cal.get_dayofweek(semana.get_dia_semana())*2
        
        y+=1
        
        for dia in semana.get_dias():
            
            dias.append(Label(frame, text=str(dia.get_dia())))
            dias[len(dias)-1].grid(column = dia_semana,row = y+1)
            
            horas_dia_text[y-1].append(StringVar())
            
            index  = len(horas_dia_text[y-1])-1
            horas = dia.get_horas()
            
            if horas == 0:
                horas = ""
            else:
                horas = str(horas)
                
            horas_dia_text[y-1][index].set(horas)
            horas_dia[y-1].append(Entry(frame, textvariable = horas_dia_text[y-1][index], width = 3))
            
            i = len(horas_dia[y-1])-1
            horas_dia[y-1][i].grid(column = dia_semana+1,row = y+1)
            dia_semana += 2
        
        resultado_semana_text.append(StringVar())
        resultado_semana_text[len(resultado_semana_text)-1].set(str(semana.get_horas()))
        resultado_semana.append(Label(frame, 
            textvariable = resultado_semana_text[len(resultado_semana_text)-1], 
            bg = 'black', fg = 'white', width  = 3))
        resultado_semana[len(resultado_semana)-1].grid(column = 14, row = y+1) 
        
def colocar_mes(frame, resultado_mes, resultado_mes_text, i):
    resultado_mes_text.append(StringVar())
    resultado_mes_text[i].set(str(calendario.get_mes(i).get_horas()))
    resultado_mes.append(Label(frame, 
    textvariable = resultado_mes_text[i], 
    bg = 'black', fg = 'white', width  = 4))
    resultado_mes[i].grid(column = 14, row = y+1)
        
def salir(entry1, entry2, entry3):
    global LOOP_ACTIVE
    global anyo
    global dia_semana
    global convenio
    
    anyo = entry1.get()
    dia_semana = entry2.get().lower()
    convenio = entry3.get()
    
    if anyo != "" and comprobar_existencia(anyo):
        LOOP_ACTIVE = False
    elif anyo != "" and convenio != "" and dia_semana != "":
        LOOP_ACTIVE = False
        
def comprobar_existencia(anyo):
    ruta = getcwd()+"\\data"
    encontrado = False

    if not isdir(ruta):
        mkdir(ruta)
        return
    
    archivos = scandir(ruta)
    
    for archivo in archivos:
        print(archivo.is_file(), anyo+".sv" == archivo.name)
        encontrado = archivo.is_file() and archivo.name == anyo+".sv"
        if encontrado:
            break;
            
    return encontrado
    
def crear(anyo, convenio, dia_semana):
                
    if comprobar_existencia(anyo) and (convenio == "" or dia_semana == ""):
        print("Load")
        return cal.calendar(False, anyo)
    else:
        print("Create")
        convenio = int(convenio)
        return cal.calendar(True, anyo, convenio, dia_semana)
    
def definir_menu(mainframe):
    
    widgets = []
    
    widgets.append(Label(mainframe,
                          text = "Año"))
    fecha = Entry(mainframe)
    widgets.append(fecha)
    
    widgets.append(Label(mainframe,
                          text = "Convenio\nSolo al crear un calendario"))
    convenio = Entry(mainframe)
    widgets.append(convenio)
    
    widgets.append(Label(mainframe,
                          text = "Dia de la semana en que empiza\n(Solo al crear un calendario)"))
    weekday = Entry(mainframe, text="Solo para crear")
    widgets.append(weekday)
    
    
    for i in widgets:
        i.pack(pady = 5)
        
    widgets.append(Button(mainframe, command=partial(salir, fecha, weekday, convenio), 
                          text = "Start", width = 25, bg = 'white', pady = 5))
    widgets[-1].pack()
    
    return widgets, fecha


# MAIN CODE

root = Tk()

x = root.winfo_screenwidth()
y = root.winfo_screenheight()
root.title("Calendario")
#root.bind("<Return>",lambda e: print("Click"))


mainframe = Frame(root)
#mainframe.pack_propagate(0)

LOOP_ACTIVE = True

widgets = definir_menu(mainframe)
    
while LOOP_ACTIVE:
    root.update()
    mainframe.pack()

LOOP_ACTIVE = True

root.title("Calendario "+anyo)
calendario = crear(anyo, convenio, dia_semana)

mainframe.destroy()
mainframe = Frame(root)

meses = []
meses_text=[]

horas_dia = []
resultado_semana = []
horas_dia_text = []
resultado_semana_text = []
resultado_mes = []
resultado_mes_text = []

f = font.Font(weight= 'bold')
f.configure(underline = True)

for i in range(12):
    col = i%4
    row = i//4
    meses.append(Frame(mainframe, width = x//4, height = y//3))
    meses[i].grid(column = col, row = row, sticky ='NW')
    meses_text.append(Label(meses[i], text=cal.get_mes(i+1).upper()))
    meses_text[i].configure(font = f)
    meses_text[i].grid(column = 0, row = 0, columnspan = 7, sticky ='NW')
    horas_dia.append([])
    horas_dia_text.append([])
    resultado_semana.append([])
    resultado_semana_text.append([])
    colocar_dias(meses[i], i, horas_dia[i], horas_dia_text[i], resultado_semana[i], resultado_semana_text[i])
    colocar_mes(meses[i], resultado_mes, resultado_mes_text, i)
    
total_frame = Frame(mainframe)
total_frame.grid(column = 3, row = 3, sticky ='E')

anyo = Label(total_frame, text = "TOTAL AÑO: ")
anyo.grid(column = 0, row = 0)    
anyo_text = StringVar()
anyo_text.set(str(calendario.get_horas()))
anyo = Label(total_frame, textvariable = anyo_text, width = 7)
anyo.grid(column = 1, row = 0)    


convenio = Label(total_frame, text= "HORAS CONVENIO: ")
convenio.grid(column = 0, row = 1)
convenio_text=StringVar()
convenio_text.set(calendario.get_convenio())
convenio = Entry(total_frame, textvariable=convenio_text)
convenio.bind("<Return>", partial(set_convenio, convenio, convenio_text))
convenio.grid(column = 1, row = 1)

total_text = StringVar()
total = Label(total_frame, text = "HORAS TOTALES: ")
total.grid(column = 0, row = 2)
total_text.set(calendario.get_horas()-calendario.get_convenio())
total = Label(total_frame, textvariable = total_text)
total.grid(column = 1, row = 2)

for i in range(12):
    s = 0
    dia = 1
    for semana in horas_dia[i]:
        j= 0
        for horas in semana:
            horas.bind("<Return>", partial(add_horas, 
                                           horas, horas_dia_text[i][s][j], 
                                           i, s, dia, resultado_semana_text,
                                           resultado_semana, resultado_mes,
                                           resultado_mes_text, anyo, anyo_text))
            j += 1
            dia += 1
        s += 1
    j = 1
    


while LOOP_ACTIVE:
    
    mainframe.pack(expand = 'yes', fill='both')
    root.update()
    
