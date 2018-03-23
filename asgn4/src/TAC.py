class TAC:
    def __init__(self):
        self.code = []
        self.error = False

    def emit(self, instrType, lis):
        if instrType == 'EndOfCode':   # lis = [des, src]
            self.code.append('endOfCode')
        if instrType == 'Assignment':   # lis = [des, src]
            self.code.append('=,'+str(lis[0])+','+str(lis[1]))
        if instrType == 'Arithmetic' or instrType == 'logical': # lis = [op, des, src1, src2]
            self.code.append(str(lis[0])+','+str(lis[1])+','+str(lis[2])+','+str(lis[3]))
        if instrType == 'print':  # lis = [src]
            self.code.append('print,'+str(lis[0]))
        if instrType == 'goto': # lis = [label]
            self.code.append('goto,'+str(lis[0]))
        if instrType == 'ifgoto': # lis = [rel, src1,src2, lablel]
            self.code.append('ifgoto,'+str(lis[0])+ ',' + str(lis[1])+','+str(lis[2])+','+str(lis[3]))
        if instrType == 'label': # lis = [label]
            self.code.append('label,'+str(lis[0]))
        if instrType == 'flabel': # lis = [label]
            self.code.append('flabel,'+str(lis[0]))
        if instrType == 'return': # lis = [src]
            self.code.append('return,'+str(lis[0]))
        if instrType == 'func_arg':   # lis = [src, special_registor_number]
            self.code.append('funcarg,'+str(lis[0])+','+str(lis[1]))
        if instrType == 'param':     # lis = [src]
            self.code.append('param,'+str(lis[0]))
        if instrType == 'call': # lis = [fname, return value]
            if (lis[1]==''):
                self.code.append('call,'+str(lis[0]))
            else:
                self.code.append('call,'+str(lis[0])+','+str(lis[1]))

    def printTAC(self):
        for instr in self.code:
            print instr


        #FUNCTION
