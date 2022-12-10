#some useful things
def stringadd(x,y):
    return str(int(x) + int(y))

def stringmult(x,y):
    return str(int(x) * int(y))

def removedigit(num,place):
    stri = str(num)
    stri = str[:place - 1]
    num = int(stri)
    return num

def insert_str(string, str_to_insert, index):
    return string[:index] + str_to_insert + string[index:]

def adddigit(num,digit,index):
    string = str(num)
    str_ins = str(digit)
    num = insert_str(string, str_ins, index)
    return int(num)

def split(string_to_split, index):
    string1, string2 =  string_to_split[:index], string_to_split[index:]
    return string1, string2

#big numbers
class bignum():
    def __init__(self, man__int = "0", man_dec = "0", expo = "0"):
        self.mantissa_int = man__int
        self.mantissa_dec = man_dec
        self.exponant = expo

    def printn(self,x):
        str = f"{x.mantissa_int}.{x.mantissa_dec}E{x.exponant}"
        print(str)

    def Bignum(string):
        E_index = string.find("E")
        dec_index = string.find(".")
        res = bignum()
        res.mantissa_int = string[:dec_index]
        res.mantissa_dec = string[dec_index + 1:E_index]
        res.exponant = string[E_index + 1:]
        while int(res.mantissa_int) > 10:
            res.mantissa_dec += res.mantissa_int[len(res.mantissa_int)]
            res.mantissa_int = res.mantissa_int[:-1]
            res.exponant = stringadd(res.exponant, "1")
        res.printn(res)
        return res

    def mult(self,y):
        res = bignum()
        res_num_str = ""
        res_dec_len = 0
        res.exponant = stringadd(self.exponant, y.exponant)
        res_dec_len = len(self.mantissa_dec) + len(y.mantissa_dec)
        res_num_str = stringmult(self.mantissa_int+self.mantissa_dec, y.mantissa_int+y.mantissa_dec)
        res.mantissa_dec = res_num_str[res_dec_len:]
        if len(res_num_str) == res.mantissa_dec:
            res.mantissa_int = "0"
        else:
            res.mantissa_int = res_num_str[:len(res_num_str) - res_dec_len]

        while int(res.mantissa_int) > 10:
            res.mantissa_dec += res.mantissa_int[len(res.mantissa_int)-1]
            res.mantissa_int = res.mantissa_int.rstrip(res.mantissa_int[-1])
            res.exponant = stringadd(res.exponant, "1")
            res.mantissa_dec = res.mantissa_dec[:-1]

        return res

a = bignum.Bignum("2.2E3")
b = bignum.Bignum("3.34E4")
a.printn(a.mult(b))