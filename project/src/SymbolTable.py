label_no = 0
temp_no = 0
class Symtable:

    def __init__(self, scope):
        self.vardict = {}
        self.funcdict = {}
        if(scope == "local"):
            self.label_prefix = 'l_'
        else:
            self.label_prefix = ''

    def varlookup(self, var):
        if var in self.vardict.keys():
            return self.vardict[var]
        else:
             return False

    def funclookup(self, func):
        if func in self.funcdict.keys():
            return self.funcdict[func]
        else:
             return False

    def varinsert(self, var, dic):
        self.vardict[var] = dic

    def funcinsert(self, func, dic):
        self.funcdict[func] = dic

    def newtemp(self, dic):
        global temp_no
        temp_no += 1
        dic["declare"] = True
        temp_name = "temp"+str(temp_no)
        self.varinsert(temp_name, dic)
        return temp_name

    def update(self, var, key, value):
        self.vardict[var][key] = value

    def newlabel(self):
        global label_no
        label_no += 1
        label_name = self.label_prefix + "label" + str(label_no)
        return label_name
