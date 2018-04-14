class TAC:
    def __init__(self):
        self.code = []
        self.error = False

    def emit(self, instrType, lis):
        if instrType == 'EndOfCode':
            self.code.append('endOfCode')
        if instrType == 'Assignment':
            self.code.append('=,'+str(lis[0])+','+str(lis[1]))
        if instrType == 'Arithmetic' or instrType == 'logical':
            self.code.append(str(lis[0])+','+str(lis[1])+','+str(lis[2])+','+str(lis[3]))
        if instrType == 'LogicalNOT':
            self.code.append(str(lis[0])+','+str(lis[1])+','+str(lis[2]))
        if instrType == 'print':
            self.code.append('print,'+str(lis[0]))
        if instrType == 'goto':
            self.code.append('goto,'+str(lis[0]))
        if instrType == 'ifgoto':
            self.code.append('ifgoto,'+str(lis[0])+ ',' + str(lis[1])+','+str(lis[2])+','+str(lis[3]))
        if instrType == 'label':
            self.code.append('label,'+str(lis[0]))
        if instrType == 'flabel':
            self.code.append('function,'+str(lis[0]))
        if instrType == 'return':
            self.code.append('return,'+str(lis[0]))
        if instrType == 'func_arg':
            self.code.append('funcarg,'+str(lis[0])+','+str(lis[1]))
        if instrType == 'param':
            self.code.append('param,'+str(lis[0]))
        if instrType == 'pop':
            self.code.append('pop,'+str(lis[0]))
        if instrType == 'retval':
            self.code.append('retval,'+str(lis[0]))
        if instrType == 'vector':
            self.code.append('vector,'+str(lis[0]) + ',' + str(lis[1]))
        if instrType == 'member':
            self.code.append('member,'+str(lis[0]) + ',' + str(lis[1]) + ',' + str(lis[2]))
        if instrType == 'update':
            self.code.append('update,'+str(lis[0]) + ',' + str(lis[1]) + ',' + str(lis[2]))
        if instrType == 'call':
            if (lis[1]==''):
                self.code.append('call,'+str(lis[0]))
            else:
                self.code.append('call,'+str(lis[0])+','+str(lis[1]))

    def printTAC(self):
        f = open('out.ir','w+')
        i = 1
        for instr in self.code:
            f.write(str(i)+ ',' + instr)
            f.write('\n')
            i = i + 1
            # print instr
        f.close()