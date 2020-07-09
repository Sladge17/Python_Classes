from copy import copy

class TableError(Exception):
    pass

class Table:
    '''Создание таблицы с одной строкой, и количеством столбцов равных количеству вводимых аргументов.
    Значение элементов таблицы равно значению вводимых аргументов'''

    def __init__(self, *args):
        if len(args)==0:
            raise TableError('Таблица должна содержать минимум один элемент')
        self.table=[list(args)]
        self.lines=len(self.table)
        self.pillars=len(self.table[0])

    def tail_line(self, *args):
        '''Добавление строки в конец существующей таблицы.
        Количество вводимых аргументов не должно превышать, количество элементов в строках существующей таблицы.
        Если количество вводимых аргументов меньше количества элементов в строках существующей таблиы,
        недостающим элементам присваивается нулевое значение и они вставляются в конец строки'''
        args=list(args)
        if len(args)<self.pillars:
            args+=[0]*(self.pillars-len(args))
        if len(args)>self.pillars:
            raise TableError('Количество элементов в строке превышает максимальное, равное '+str(self.pillars))
        #self.table.append(args)
        self.table+=[args]
        self.lines+=1

    def head_line(self, *args):
        '''Добавление строки в начало существующей таблицы.
        Количество вводимых аргументов не должно превышать, количество элементов в строках существующей таблицы.
        Если количество вводимых аргументов меньше количества элементов в строках существующей таблиы,
        недостающим элементам присваивается нулевое значение и они вставляются в конец строки'''
        args=list(args)
        if len(args)<self.pillars:
            args+=[0]*(self.pillars-len(args))
        if len(args)>self.pillars:
            raise TableError('Количество элементов в строке превышает максимальное, равное '+str(self.pillars))
        #self.table.insert(0,args)
        self.table=[args]+self.table
        self.lines+=1

    def tail_pillar(self, *args):
        '''Добавление столбца в конец существующей таблицы.
        Количество вводимых аргументов не должно превышать, количество элементов в столбцах существующей таблицы.
        Если количество вводимых аргументов меньше количества элементов в столбцах существующей таблиы,
        недостающим элементам присваивается нулевое значение и они вставляются в конец столбца'''
        args=list(args)
        if len(args)<self.lines:
            args+=[0]*(self.lines-len(args))
        if len(args)>self.lines:
            raise TableError('Количество элементов в столбце превышает максимальное, равное '+str(self.lines))
        self.table=[self.table[i]+[args[i]] for i in range(self.lines)]
        self.pillars+=1
        
    def head_pillar(self, *args):
        '''Добавление столбца в начало существующей таблицы.
        Количество вводимых аргументов не должно превышать, количество элементов в столбцах существующей таблицы.
        Если количество вводимых аргументов меньше количества элементов в столбцвх существующей таблиы,
        недостающим элементам присваивается нулевое значение и они вставляются в конец столбца'''
        args=list(args)
        if len(args)<self.lines:
            args+=[0]*(self.lines-len(args))
        if len(args)>self.lines:
            raise TableError('Количество элементов в столбце превышает максимальное, равное '+str(self.lines))        
        self.table=[[args[i]]+self.table[i] for i in range(self.lines)]
        self.pillars+=1

    def extract_lines(self, *args):
        '''Выделение из таблицы необходимых строк. Нумерация строк начинается с единицы.
        Номера строк не должны превышать количество строк в существующей таблице'''
        if len(args)>self.lines:
            raise TableError('Количество выделенных строк превышает количество строк в таблице')
        args=sorted(args)
        for i in range(len(args)):
            if args[i]>self.lines:
                raise TableError('Строки '+str(args[i])+' не существует, количество строк в таблице '
                                 +str(self.lines))
            if args[i]!=args[-1] and args[i]==args[i+1]:
                raise TableError('Строка '+str(args[i])+' выделяется несколько раз, это недопустимо')
        self.table=[self.table[i-1] for i in args]
        self.lines=len(self.table)          

    def extract_pillars(self, *args):
        '''Выделение из таблицы необходимых столбцов. Нумерация столбцов начинается с единицы.
        Номера столбцов не должны превышать количество столбцов в существующей таблице'''
        if len(args)>self.pillars:
            raise TableError('Количество выделенных столбцов превышает количество столбцов в таблице')
        args=sorted(args)
        for i in range(len(args)):
            if args[i]>self.pillars:
                raise TableError('Столбца '+str(args[i])+' не существует, количество столбцов в таблице '
                                 +str(self.pillars))
            if args[i]!=args[-1] and args[i]==args[i+1]:
                raise TableError('Столбец '+str(args[i])+' выделяется несколько раз, это недопустимо')
        self.table=[[self.table[i][j-1] for j in args] for i in range(self.lines)]
        self.pillars=len(self.table[0])     

    def replace(self, n_line, n_pillar, value=0):
        '''Изменение значения элемента таблицы.
        В качестве аргумента вводится сначала номер строки заменяемого элемента, затем номер столбца,
        после этого вводится новое значение элемента.
        Нумерация строк и столбцов начинается с единицы.
        Если новое значение не задано, элемент принимает нулевое значение'''
        if n_line<=self.lines and n_pillar<=self.pillars:
            self.table[n_line-1][n_pillar-1]=value
        else:
            if n_line>self.lines:
                raise TableError('Номер строки для вставляемого элемента не должен превышать '
                                  +str(self.lines))
            else:
                raise TableError('Номер столбца для вставляемого элемента не должен превышать '
                                  +str(self.pillars)) 

    def union_lines(self, other):
        '''Объединение двух таблиц, путём последовательной записи их строк.
        Количество элементов в строках присоединаемой таблицы должно быть равно
        количеству элементов в строках присоединяющей таблицы'''
        if self.pillars==other.pillars:
            self.table+=other.table
        else:
            raise TableError('Количество элементов в строках присоединяемой таблицы должно быть равно '
                              +str(self.pillars))
        self.lines+=other.lines

    def union_pillars (self, other):
        '''Объединение двух таблиц, путём последовательной записи их столбцов.
        Количество элементов в столбцах присоединаемой таблицы должно быть равно
        количеству элементов в столбцах присоединяющей таблицы'''        
        if self.lines==other.lines:
            self.table=[self.table[i]+other.table[i] for i in range(self.lines)]
            self.pillars+=other.pillars
        else:
            raise TableError('Количество элементов в столбцах присоединяемой таблице должно быть равно '
                              +str(self.lines))

    def trans(self):
        '''Транспонирование таблицы'''
        self.table=[[line[i] for line in self.table] for i in range(self.pillars)]
        self.lines=len(self.table)
        self.pillars=len(self.table[0])
        
    def __str__(self):
        self.table=[[line[i] for line in self.table] for i in range(len(self.table[0]))]
        len_maxpillar=[max([len(str(j)) for j in i]) for i in self.table]
        self.table=[[line[i] for line in self.table] for i in range(len(self.table[0]))]
        len_style=''.join(['{:<'+str(len_maxpillar[i]+2)+'}' for i in range(len(self.table[0]))])
        str_table=(''.join([len_style.format(*i)+'\n' for i in self.table]))[:-2]
        return 'Созданная таблица с '+str(self.lines)+' строками, и '+str(self.pillars)+' столбцами:\n'+str_table

    def saveinfile(self,name='Problem_1'):
        '''Сохрание таблицы в файл формата txt.
        Если имя файла не указано, таблица сохраняется в файл Problem_1.txt'''
        if type(name)!=str:
            raise TableError('Название файла должно быть строчной переменной')
        with open(name+'.txt','w') as output:
            self.table=[[line[i] for line in self.table] for i in range(len(self.table[0]))]
            len_maxpillar=[max([len(str(j)) for j in i]) for i in self.table]
            self.table=[[line[i] for line in self.table] for i in range(len(self.table[0]))]
            len_style=''.join(['{:<'+str(len_maxpillar[i]+2)+'}' for i in range(len(self.table[0]))])
            str_table=(''.join([len_style.format(*i)+'\n' for i in self.table]))[:-2]
            output.write(str_table)
            print('Созданная таблица сохраненна в файл',name+'.txt')
