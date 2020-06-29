import json
from os import scandir, getcwd

def comprobar_mes(num):
    
    if(num == 2):
        return 'febrero'
    elif(num == 1 or num == 3 or num == 5 or num == 7 or 
         num == 8 or num == 10 or num == 12):
        return '31'
    else:
        return '30'
    
def get_mes(i):
    switcher = {
        1: "Enero",
        2: "Febrero",
        3: "Marzo",
        4: "Abril",
        5: "Mayo",
        6: "Junio",
        7: "Julio",
        8: "Agosto",
        9: "Septiembre",
        10: "Octubre",
        11: "Noviembre",
        12: "Diciembre"
    }
    return switcher.get(i)

def get_num_mes(i):
    switcher = {
        "Enero":        1,
        "Febrero":      2,
        "Marzo":        3,
        "Abril":        4,
        "Mayo":         5,
        "Junio":        6,
        "Julio":        7,
        "Agosto":       8,
        "Septiembre":   9,
        "Octubre":      10,
        "Noviembre":    11,
        "Diciembre":    12
    }
    return switcher.get(i)

def get_weekday(i):
    switcher = {
        1: "lunes",
        2: "martes",
        3: "miercoles",
        4: "jueves",
        5: "viernes",
        6: "sabado",
        7: "domingo",
    }
    return switcher.get(i)

def get_dayofweek(i):
    switcher = {
        "lunes":    0,
        "martes":   1,
        "miercoles":2,
        "jueves":   3,
        "viernes":  4,
        "sabado":   5,
        "domingo":  6,
    }
    return switcher.get(i)

def get_dias_restantes(i):
    switcher = {
        'lunes':    6,
        'martes':   5,
        'miercoles':4,
        'jueves':   3,
        'viernes':  2,
        'sabado':   1,
        'domingo':  0,

    }
    return switcher.get(i)

def es_bisiesto(anyo):
    if(anyo%4 == 0 and anyo % 100 != 0):
        return True
    elif(anyo%4 == 0 and anyo%400 == 0):
        return True
    else:
        return False
    
def get_next_weekday(weekday, passed_days):
    if passed_days == 7 or passed_days == 0:
        return weekday
    else:
        return get_weekday((get_dayofweek(weekday)+passed_days)%7+1)

class calendar:
    
    meses = []
    dia_semana = 'lunes'
    anyo = 2000
    convenio = 0
    
    def __init__(self, crear, anyo, convenio = 1, dia_semana = 'lunes'):
        if crear:
            self.create(dia_semana, anyo, convenio)
        else:
            self.load(anyo)
    
    def create(self, dia_semana, anyo, convenio):
        
        self.meses = []
        self.dia_semana = dia_semana
        self.anyo = int(anyo)
        self.convenio = convenio
        next_week = 1
        next_weekday = dia_semana

        for i in range(12):
		
            mes = ""
			
            if(comprobar_mes(i+1) == 'febrero'):
                mes = febrero(next_weekday, es_bisiesto(self.anyo), next_week)
            elif(comprobar_mes(i+1) == '30'):
                mes = dias30(get_mes(i+1), next_weekday, next_week)
            else:
                mes = dias31(get_mes(i+1), next_weekday, next_week)
				
            next_week = mes.next_weeks()
            next_weekday = mes.get_next_month_weekday()
            self.meses.append(mes)
                
        self.save()
                
    def load(self, anyo):
        
        f = open(getcwd()+"\\data\\"+anyo+'.sv', 'r')
        data = json.load(f)
        f.close()
        
        self.create(data[anyo]['dia_semana'], int(anyo), data[anyo]['convenio'])
        
        for mes in self.meses:
            mes.load(data[str(self.anyo)])
            
        self.save()
        
    def to_string(self):
        for mes in self.meses:
            print(mes.to_string())
            
    def get_horas(self):
        aux = 0
        for mes in self.meses:
            aux += mes.get_horas()
        return float(aux)
    
    def get_mes(self, num):
        return self.meses[num]
    
    def get_convenio(self):
        return self.convenio
    
    def set_horas(self, mes, dia, horas):
        dias = 0
        dias_semana = 0
        i = 0
        encontrado = False
        while not encontrado:
            semana = self.meses[get_num_mes(mes)-1].semanas[i]
            dias_semana = semana.get_days()
            if dias + dias_semana < dia:
                i += 1
                dias += dias_semana
            else:
                num_dia = dia - dias -1
                semana.dias[num_dia].set_horas(horas)
                encontrado = True
            
        self.save()
        
    def set_convenio(self, convenio):
        self.convenio = convenio
        self.save()
                
    def save(self):
        data = {self.anyo: {'dia_semana': self.dia_semana, 'convenio': self.convenio}}
        for mes in self.meses:
            data[self.anyo][mes.get_mes()] = mes.save()
        f = open(getcwd()+"\\data\\"+str(self.anyo)+'.sv', 'w+')
        json.dump(data, f, indent = 4)
        f.close()
        
class mes:
    
    mes = 'enero'
    semanas = []
    next_month_weekday = 'lunes'
    
    def __init__(self, mes, dia_semana, total, num_semana):
        self.semanas = []
        self.mes = mes
        
        n_weekday = dia_semana
        n_semana = num_semana
        i = 1
        while i <= total:
            week = semana(n_weekday, i, total, n_semana)
            self.semanas.append(week)
            n_semana += 1
            i += week.get_days()
            n_weekday = get_next_weekday(n_weekday, week.get_days())
        
        self.next_month_weekday = n_weekday
        
    def to_string(self):
        aux = "\n"+self.mes
        for semana in self.semanas:
            aux += "\n"+semana.to_string()
        return aux
    
    def next_weeks(self):
        return self.semanas[-1].get_next_week()
    
    def get_next_month_weekday(self):
        return self.next_month_weekday
    
    def get_horas(self):
        aux = 0
        for semana in self.semanas:
            aux += semana.get_horas()
        return float(aux)
    
    def get_semanas(self):
        return self.semanas
    
    def get_mes(self):
        return self.mes
    
    def save(self):
        data = {}
        for semana in self.semanas:
            data[semana.get_num_semana()] = semana.save()
        return data
    
    def load(self, data):
        for semana in self.semanas:
            semana.load(data[self.mes])
    
class dias31(mes):
    
    def __init__(self, mes, dia_semana, num_semana):
        super().__init__(mes, dia_semana, 31, num_semana)
    
class dias30(mes):
    
    def __init__(self, mes, dia_semana, num_semana):
        super().__init__(mes, dia_semana, 30, num_semana)
    
class febrero:
    
    mes = 'Febrero'
    semanas = []
    
    next_month_weekday = 'lunes'
    
    def __init__(self, dia_semana, bisiesto, num_semana):

        self.semanas = []
        
        total = 28
        if bisiesto:
            total = 29
        
        n_weekday = dia_semana
        n_semana = num_semana
        i = 1
        while i <= total:
            week = semana(n_weekday, i, total, n_semana)
            self.semanas.append(week)
            n_semana += 1
            i += week.get_days()
            n_weekday = get_next_weekday(n_weekday, week.get_days())
            
        self.next_month_weekday = n_weekday
        
    def to_string(self):
        aux = "\n"+self.mes
        for semana in self.semanas:
            aux += "\n"+semana.to_string()
        return aux
            
    def next_weeks(self):
        return self.semanas[-1].get_next_week()
    
    def get_next_month_weekday(self):
        return self.next_month_weekday
    
    def get_horas(self):
        aux = 0
        for semana in self.semanas:
            aux += semana.get_horas()
        return float(aux)
    
    def get_semanas(self):
        return self.semanas
    
    def get_mes(self):
        return self.mes
    
    def save(self):
        data = {}
        for semana in self.semanas:
            data[semana.get_num_semana()] = semana.save()
        return data
        
    def load(self, data):
        for semana in self.semanas:
            semana.load(data[self.mes])
            
class semana:
    
    dias = []
    num_semana = 0
    dia_semana = 1
    
    def __init__(self, dia_semana, dia_inicio, dia_final, num_semana):
        self.dias = []
        self.num_semana = num_semana
        self.dia_semana = dia_semana
        
        num_dias = get_dias_restantes(dia_semana)
        
        if(dia_inicio + num_dias < dia_final):
            dia_final = dia_inicio+num_dias
        
        for i in range(dia_inicio, dia_final+1):
            self.dias.append(dia(i))
        
    def to_string(self):
        aux = "Num semana: " + str(self.num_semana)
        aux += "\nDia semana: " + self.dia_semana
        for dia in self.dias:
            aux += "\n" + dia.to_string()
        return aux
    
    def get_next_week(self):
        if len(self.dias) <= get_dias_restantes(self.dia_semana):
            return self.num_semana
        else:
            return self.num_semana+1
        
    def get_days(self):
        return len(self.dias)
    
    def get_dias(self):
        return self.dias
    
    def get_horas(self):
        aux = 0
        for dia in self.dias:
            aux += dia.get_horas()
        return float(aux)
    
    def get_num_semana(self):
        return self.num_semana
    
    def get_dia_semana(self):
        return self.dia_semana
    
    def save(self):
        data = {}
        for dia in self.dias:
            data[dia.get_dia()] = dia.save()
        return data
    
    def load(self, data):
        for dia in self.dias:
            dia.load(data[str(self.num_semana)])
        
class dia:
    
    dia = 1
    horas = 0
    
    def __init__(self, dia):
        
        self.dia = dia
    
    def to_string(self):
        return "Dia: "+str(self.dia)+"    Horas: "+str(self.horas)
    
    def get_horas(self):
        return float(self.horas)
    
    def get_dia(self):
        return self.dia
    
    def set_horas(self, horas):
        self.horas = horas
        
    def save(self):
        return self.horas
    
    def load(self, data):
        self.horas = data[str(self.dia)]

