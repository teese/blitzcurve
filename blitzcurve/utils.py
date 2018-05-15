import numpy as np

def exp_func(x, a, b, c):
    y = a * np.exp(-b * x) + c
    return y

class FlourescentColours():
    def __init__(self):
        self.red = "#FF355E"
        self.watermelon = "#FD5B78"
        self.orange = "#FF6037"
        self.tangerine = "#FF9966"
        self.carrot = "#FF9933"
        self.sunglow = "#FFCC33"
        self.lemon = "#FFFF66"
        self.yellow = "#FFFF66"
        self.lime = "#CCFF00"
        self.green = "#66FF66"
        self.mint = "#AAF0D1"
        self.blue = "#50BFE6"
        self.pink = "#FF6EFF"
        self.rose = "#EE34D2"
        self.magenta = "#FF00CC"
        self.pizzazz = "FF00CC"


def get_fluorescent_colours():
    # get dict and list of fluorescent colours
    #https://www.w3schools.com/colors/colors_crayola.asp
    fc_dict = {"Red":"#FF355E","Watermelon":"#FD5B78","Orange":"#FF6037","Tangerine":"#FF9966","Carrot":"#FF9933","Sunglow":"#FFCC33","Lemon":"#FFFF66","Yellow":"#FFFF66","Lime":"#CCFF00","Green":"#66FF66","Mint":"#AAF01","Blue":"#50BFE6","Pink":"#FF6EFF","Rose":"#EE34D2","Magenta":"#FF00CC","Pizzazz":"FF00CC"}
    fl_col_keys = sorted(fc_dict)
    fl_col_list = [fc_dict[k] for k in fl_col_keys]
    return fc_dict, fl_col_keys, fl_col_list