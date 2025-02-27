import os
from PyQt5 import QtCore, QtWidgets

class TriggerOut:
    def __init__(self, new_object=False, additional_parameters={}):
        super().__init__()

        self.new_object = new_object

        self.__additional_parameters=additional_parameters

    def has_additional_parameter(self, name):
        return name in self.__additional_parameters.keys()

    def get_additional_parameter(self, name):
        return self.__additional_parameters[name]

class TriggerIn:
    def __init__(self, new_object=False, interrupt=False, additional_parameters={}):
        super().__init__()

        self.new_object = new_object
        self.interrupt = interrupt

        self.__additional_parameters=additional_parameters

    def has_additional_parameter(self, name):
        return name in self.__additional_parameters.keys()

    def get_additional_parameter(self, name):
        return self.__additional_parameters[name]


class TTYGrabber:
    def __init__(self,  tmpFileName = 'out.tmp.dat'):
        self.tmpFileName = tmpFileName
        self.ttyData = []
        self.outfile = False
        self.save = False

    def start(self):
        self.outfile = os.open(self.tmpFileName, os.O_RDWR|os.O_CREAT)
        self.save = os.dup(1)
        os.dup2(self.outfile, 1)
        return

    def stop(self):
        if not self.save:
            return
        os.dup2(self.save, 1)
        tmpFile = open(self.tmpFileName, "r")
        self.ttyData = tmpFile.readlines()
        tmpFile.close()
        os.close(self.outfile)
        os.remove(self.tmpFileName)

class EmittingStream(QtCore.QObject):
    textWritten = QtCore.pyqtSignal(str)

    def write(self, text):
        self.textWritten.emit(str(text))

    def flush(self):
        pass

import h5py, time

subgroup_name = "surface_file"

def read_surface_file(file_name):
    if not os.path.isfile(file_name): raise ValueError("File " + file_name + " not existing")

    file = h5py.File(file_name, 'r')
    xx = file[subgroup_name + "/X"][()]
    yy = file[subgroup_name + "/Y"][()]
    zz = file[subgroup_name + "/Z"][()]

    return xx, yy, zz

def write_surface_file(zz, xx, yy, file_name, overwrite=True):

    if (os.path.isfile(file_name)) and (overwrite==True): os.remove(file_name)

    if not os.path.isfile(file_name):  # if file doesn't exist, create it.
        file = h5py.File(file_name, 'w')
        # points to the default data to be plotted
        file.attrs['default']          = subgroup_name + '/Z'
        # give the HDF5 root some more attributes
        file.attrs['file_name']        = file_name
        file.attrs['file_time']        = time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime())
        file.attrs['creator']          = 'write_surface_file'
        file.attrs['code']             = 'Oasys'
        file.attrs['HDF5_Version']     = h5py.version.hdf5_version
        file.attrs['h5py_version']     = h5py.version.version
        file.close()

    file = h5py.File(file_name, 'a')

    try:
        f1 = file.create_group(subgroup_name)
    except:
        f1 = file[subgroup_name]

    f1z = f1.create_dataset("Z", data=zz)
    f1x = f1.create_dataset("X", data=xx)
    f1y = f1.create_dataset("Y", data=yy)


    # NEXUS attributes for automatic plot
    f1.attrs['NX_class'] = 'NXdata'
    f1.attrs['signal'] = "Z"
    f1.attrs['axes'] = [b"Y", b"X"]

    f1z.attrs['interpretation'] = 'image'
    f1x.attrs['long_name'] = "X [m]"
    f1y.attrs['long_name'] = "Y [m]"


    file.close()


class ShowTextDialog(QtWidgets.QDialog):

    def __init__(self, title, text, width=650, height=400, parent=None):
        QtWidgets.QDialog.__init__(self, parent)
        self.setModal(True)
        self.setWindowTitle(title)
        layout = QtWidgets.QVBoxLayout(self)

        text_edit = QtWidgets.QTextEdit("", self)
        text_edit.append(text)
        text_edit.setReadOnly(True)

        text_area = QtWidgets.QScrollArea(self)
        text_area.setWidget(text_edit)
        text_area.setWidgetResizable(True)
        text_area.setFixedHeight(height)
        text_area.setFixedWidth(width)

        bbox = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok)

        bbox.accepted.connect(self.accept)
        layout.addWidget(text_area)
        layout.addWidget(bbox)

    @classmethod
    def show_text(cls, title, text, width=650, height=400, parent=None):
        dialog = ShowTextDialog(title, text, width, height, parent)
        dialog.show()


class ElementInFormula(object):
    def __init__(self, element, atomic_number, n_atoms, molecular_weight):
        self._element = element
        self._atomic_number = atomic_number
        self._n_atoms = n_atoms
        self._molecular_weight = molecular_weight

class ChemicalFormulaParser(object):

    @classmethod
    def parse_formula(cls, formula):
        return parse(formula).getsyms()


###################################


# symbol, name, atomic number, molecular weight
_data = r"""'Ac', 'Actinium', 89, 227
'Ag', 'Silver', 47, 107.868
'Al', 'Aluminum', 13, 26.98154
'Am', 'Americium', 95, 243
'Ar', 'Argon', 18, 39.948
'As', 'Arsenic', 33, 74.9216
'At', 'Astatine', 85, 210
'Au', 'Gold', 79, 196.9665
'B', 'Boron', 5, 10.81
'Ba', 'Barium', 56, 137.33
'Be', 'Beryllium', 4, 9.01218
'Bi', 'Bismuth', 83, 208.9804
'Bk', 'Berkelium', 97, 247
'Br', 'Bromine', 35, 79.904
'C', 'Carbon', 6, 12.011
'Ca', 'Calcium', 20, 40.08
'Cd', 'Cadmium', 48, 112.41
'Ce', 'Cerium', 58, 140.12
'Cf', 'Californium', 98, 251
'Cl', 'Chlorine', 17, 35.453
'Cm', 'Curium', 96, 247
'Co', 'Cobalt', 27, 58.9332
'Cr', 'Chromium', 24, 51.996
'Cs', 'Cesium', 55, 132.9054
'Cu', 'Copper', 29, 63.546
'Dy', 'Dysprosium', 66, 162.50
'Er', 'Erbium', 68, 167.26
'Es', 'Einsteinium', 99, 254
'Eu', 'Europium', 63, 151.96
'F', 'Fluorine', 9, 18.998403
'Fe', 'Iron', 26, 55.847
'Fm', 'Fermium', 100, 257
'Fr', 'Francium', 87, 223
'Ga', 'Gallium', 31, 69.735
'Gd', 'Gadolinium', 64, 157.25
'Ge', 'Germanium', 32, 72.59
'H', 'Hydrogen', 1, 1.0079
'He', 'Helium', 2, 4.0026
'Hf', 'Hafnium', 72, 178.49
'Hg', 'Mercury', 80, 200.59
'Ho', 'Holmium', 67, 164.9304
'I', 'Iodine', 53, 126.9045
'In', 'Indium', 49, 114.82
'Ir', 'Iridium', 77, 192.22
'K', 'Potassium', 19, 39.0983
'Kr', 'Krypton', 36, 83.80
'La', 'Lanthanum', 57, 138.9055
'Li', 'Lithium', 3, 6.94
'Lr', 'Lawrencium', 103, 260
'Lu', 'Lutetium', 71, 174.96
'Md', 'Mendelevium', 101, 258
'Mg', 'Magnesium', 12, 24.305
'Mn', 'Manganese', 25, 54.9380
'Mo', 'Molybdenum', 42, 95.94
'N', 'Nitrogen', 7, 14.0067
'Na', 'Sodium', 11, 22.98977
'Nb', 'Niobium', 41, 92.9064
'Nd', 'Neodymium', 60, 144.24
'Ne', 'Neon', 10, 20.17
'Ni', 'Nickel', 28, 58.71
'No', 'Nobelium', 102, 259
'Np', 'Neptunium', 93, 237.0482
'O', 'Oxygen', 8, 15.9994
'Os', 'Osmium', 76, 190.2
'P', 'Phosphorous', 15, 30.97376
'Pa', 'Proactinium', 91, 231.0359
'Pb', 'Lead', 82, 207.2
'Pd', 'Palladium', 46, 106.4
'Pm', 'Promethium', 61, 145
'Po', 'Polonium', 84, 209
'Pr', 'Praseodymium', 59, 140.9077
'Pt', 'Platinum', 78, 195.09
'Pu', 'Plutonium', 94, 244
'Ra', 'Radium', 88, 226.0254
'Rb', 'Rubidium', 37, 85.467
'Re', 'Rhenium', 75, 186.207
'Rh', 'Rhodium', 45, 102.9055
'Rn', 'Radon', 86, 222
'Ru', 'Ruthenium', 44, 101.07
'S', 'Sulfur', 16, 32.06
'Sb', 'Antimony', 51, 121.75
'Sc', 'Scandium', 21, 44.9559
'Se', 'Selenium', 34, 78.96
'Si', 'Silicon', 14, 28.0855
'Sm', 'Samarium', 62, 150.4
'Sn', 'Tin', 50, 118.69
'Sr', 'Strontium', 38, 87.62
'Ta', 'Tantalum', 73, 180.947
'Tb', 'Terbium', 65, 158.9254
'Tc', 'Technetium', 43, 98.9062
'Te', 'Tellurium', 52, 127.60
'Th', 'Thorium', 90, 232.0381
'Ti', 'Titanium', 22, 47.90
'Tl', 'Thallium', 81, 204.37
'Tm', 'Thulium', 69, 168.9342
'U', 'Uranium', 92, 238.029
'Unh', 'Unnilhexium', 106, 263
'Unp', 'Unnilpentium', 105, 260
'Unq', 'Unnilquadium', 104, 260
'Uns', 'Unnilseptium', 107, 262
'V', 'Vanadium', 23, 50.9415
'W', 'Tungsten', 74, 183.85
'Xe', 'Xenon', 54, 131.30
'Y', 'Yttrium', 39, 88.9059
'Yb', 'Ytterbium', 70, 173.04
'Zn', 'Zinc', 30, 65.38
'Zr', 'Zirconium', 40, 91.22"""

class Element:
    def __init__(self, symbol, name, atomicnumber, molweight):
        self.sym = symbol
        self.name = name
        self.ano = atomicnumber
        self.mw = molweight

    def getweight(self):
        return self.mw

    def addsyms(self, weight, result):
        result[self.sym] = result.get(self.sym, 0) + weight

def build_dict(s):
    answer = {}
    for line in s.split("\n"):
        symbol, name, num, weight = eval(line)
        answer[symbol] = Element(symbol, name, num, weight)
    return answer

sym2elt = build_dict(_data)
del _data

class ElementSequence:
    def __init__(self, *seq):
        self.seq = list(seq)
        self.count = 1

    def append(self, thing):
        self.seq.append(thing)

    def getweight(self):
        sum = 0.0
        for thing in self.seq:
            sum = sum + thing.getweight()
        return sum * self.count

    def set_count(self, n):
        self.count = n

    def __len__(self):
        return len(self.seq)

    def addsyms(self, weight, result):
        totalweight = weight * self.count
        for thing in self.seq:
            thing.addsyms(totalweight, result)

    def displaysyms(self):
        result = {}
        self.addsyms(1, result)
        #items = sorted(result.items())

        for sym, count in result.items():
            print (sym, "(" + sym2elt[sym].name + "):", count)

    def getsyms(self):
        result = {}
        self.addsyms(1, result)
        items = sorted(result.items())

        result = []
        for sym, count in items:
            result.append (ElementInFormula(sym, sym2elt[sym].ano, count, sym2elt[sym].mw))

        return result

NAME, NUM, LPAREN, RPAREN, EOS = range(5)
import re
_lexer = re.compile(r"[A-Z][a-z]*|\d+|[()]|<EOS>").match
del re

class Tokenizer:
    def __init__(self, input):
        self.input = input + "<EOS>"
        self.i = 0

    def gettoken(self):
        global ttype, tvalue
        self.lasti = self.i
        m = _lexer(self.input, self.i)
        if m is None:
            self.error("unexpected character")
        self.i = m.end()
        tvalue = m.group()
        if tvalue == "(":
            ttype = LPAREN
        elif tvalue == ")":
            ttype = RPAREN
        elif tvalue == "<EOS>":
            ttype = EOS
        elif "0" <= tvalue[0] <= "9":
            ttype = NUM
            tvalue = int(tvalue)
        else:
            ttype = NAME

    def error(self, msg):
        emsg = msg + ":\n"
        emsg = emsg + self.input[:-5] + "\n"  # strip <EOS>
        emsg = emsg + " " * self.lasti + "^\n"

        raise ValueError(emsg)

def parse(s):
    global t, ttype, tvalue
    t = Tokenizer(s)
    t.gettoken()
    seq = parse_sequence()
    if ttype != EOS:
        t.error("expected end of input")
    return seq

def parse_sequence():
    global t, ttype, tvalue
    seq = ElementSequence()
    while ttype in (LPAREN, NAME):
        # parenthesized expression or straight name
        if ttype == LPAREN:
            t.gettoken()
            thisguy = parse_sequence()
            if ttype != RPAREN:
                t.error("expected right paren")
            t.gettoken()
        else:
            assert ttype == NAME
            if tvalue in sym2elt:
                thisguy = ElementSequence(sym2elt[tvalue])
            else:
                t.error("'" + tvalue + "' is not an element symbol")
            t.gettoken()
        # followed by optional count
        if ttype == NUM:
            thisguy.set_count(tvalue)
            t.gettoken()
        seq.append(thisguy)
    if len(seq) == 0:
        t.error("empty sequence")
    return seq



