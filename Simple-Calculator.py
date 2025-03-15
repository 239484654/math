import math
import tkinter
import tkinter as tk
import cmath
from fractions import Fraction
from decimal import Decimal
import threading
import time

try:
    import darkdetect
    model = 1 if darkdetect.isDark() else 0
except ImportError:
    model = 0

color = [["#979d9f", "#d3e7f3", "#f9f9f9", "#ffffff", "#0067c0", "black", "white"],
         ["#979d9f", "#202020", "#323232", "#3b3b3b", "#76b9ed", "white", "black"]]
m = color[model][0]

root = tk.Tk()
root.resizable(width=False, height=False)

IS_CALC = False
STORAGE = []
MAXSHOWLEN = 10
CurrentShow = tk.StringVar()
CurrentShow.set('0')

def add_fraction(num, reg=1):
    tmp = ""
    lst = [0, 0]
    apk = [["Decimal('", "(Fraction(Decimal('"][reg], [")*1j)", "'))*1j)"][reg]]
    for i in num:
        if i in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "j", "i", "."]:
            if i in ["j", "i"]:
                if lst[0] == 1:
                    tmp += apk[1]
                    lst[0], lst[1] = 0, 0
                else:
                    tmp += "1j"
            else:
                if reg == 1 and i != "." and lst[0] == 0:
                    tmp += apk[0]
                    lst[0], lst[1] = 1, 1
                tmp += i
        else:
            if lst[0] == 1:
                if lst[1] == 1:
                    tmp += "'))"
                    lst[1] = 0
                tmp += ")"
            lst[0] = 0
            tmp += i
    if lst[0] == 1:
        tmp += "')"
        if lst[1] == 1:
            tmp += "))"
    return tmp


def calculate_expression(expression):
    try:
        expression = add_fraction(expression, reg=0)
        product = eval(expression)

        if isinstance(product, complex):
            real_part = product.real
            imag_part = product.imag

            if real_part == 0 and imag_part == 0:
                result = '0'
            elif real_part == 0:
                if imag_part == 1:
                    result = 'i'
                elif imag_part == -1:
                    result = '-i'
                else:
                    result = f"{imag_part}i"
            elif imag_part == 0:
                result = str(real_part)
            else:
                real_str = str(real_part)
                if real_str.endswith('.0'):
                    real_str = real_str[:-2]
                if imag_part == 1:
                    imag_str = 'i'
                elif imag_part == -1:
                    imag_str = '-i'
                else:
                    imag_str = f"{imag_part}i"
                    if imag_part > 0:
                        imag_str = f"+{imag_str}"
                result = f"{real_str}{imag_str}"
        else:
            result = str(product)
            if result.endswith('.0'):
                result = result[:-2]
        return result
    except Exception:
        return 'Error'


def Int(num):
    if str(num)[-1] == "0":
        return int(num)
    return num


def pressNumber(number):
    global IS_CALC
    if IS_CALC:
        CurrentShow.set('0')
        IS_CALC = False
    if CurrentShow.get() == '0':
        CurrentShow.set(number)
    else:
        if len(CurrentShow.get()) < MAXSHOWLEN:
            CurrentShow.set(CurrentShow.get() + number)


def pressDP():
    global IS_CALC
    if IS_CALC:
        CurrentShow.set('0')
        IS_CALC = False
    if len(CurrentShow.get().split('.')) == 1:
        if len(CurrentShow.get()) < MAXSHOWLEN:
            CurrentShow.set(CurrentShow.get() + '.')


def clearAll():
    global STORAGE
    global IS_CALC
    STORAGE.clear()
    IS_CALC = False
    CurrentShow.set('0')


def clearCurrent():
    CurrentShow.set('0')


def delOne():
    global IS_CALC
    if IS_CALC:
        CurrentShow.set('0')
        IS_CALC = False
    if CurrentShow.get() != '0':
        if len(CurrentShow.get()) > 1:
            CurrentShow.set(CurrentShow.get()[:-1])
        else:
            CurrentShow.set('0')


def modifyResult(result):
    result = str(result)
    if len(result) > MAXSHOWLEN:
        if len(result.split('.')[0]) > MAXSHOWLEN:
            result = 'Error'
        else:
            if "e" in result:
                reu = result.split("e+")
                reu_0 = str(Int(float(reu[0][:10 - len(reu[1]) - 2])))
                result = reu_0 + "e+" + reu[1]
            if result[-1] == "i":
                if "+" in result:
                    res = result[:-1].split("+")
                    res_1 = "+" + str(Int(float(res[1][:4]))) + "i"
                    res_0 = str(Int(float(res[0][:4])))
                    result = str(res_0 + res_1)
                elif "-" in result:
                    res = result[:-1].split("-")
                    res_1 = "-" + str(Int(float(res[1][:4]))) + "i"
                    res_0 = str(Int(float(res[0][:4])))
                    result = str(res_0 + res_1)
                else:
                    result = result[:(MAXSHOWLEN - 1)] + "i"
            else:
                result = result[:MAXSHOWLEN]
    return result


def pressOperator(operator):
    global STORAGE
    global IS_CALC
    global m
    if operator == '+/-':
        CurrentShow.set(calculate_expression('-(' + CurrentShow.get() + ")"))
    elif operator == '1/x':
        result = calculate_expression("1/(" + CurrentShow.get() + ")")
        result = modifyResult(result)
        CurrentShow.set(result)
        IS_CALC = True
    elif operator == 'sqrt':
        result = calculate_expression("cmath.sqrt(" + CurrentShow.get() + ")")
        result = modifyResult(result)
        CurrentShow.set(result)
        IS_CALC = True
    elif operator == 'x2':
        result = calculate_expression("pow(" + CurrentShow.get() + ",2)")
        result = modifyResult(result)
        CurrentShow.set(result)
        IS_CALC = True
    elif operator == 'MC':
        m = color[model][0]
        Demo()
        STORAGE.clear()
    elif operator == 'MR':
        if IS_CALC:
            CurrentShow.set('0')
        STORAGE.append(CurrentShow.get())
        expression = ''.join(STORAGE)
        result = calculate_expression(expression)
        result = modifyResult(result)
        CurrentShow.set(result)
        IS_CALC = True
    elif operator == 'MS':
        STORAGE.clear()
        STORAGE.append(CurrentShow.get())
        m = color[model][5]
        Demo()
    elif operator == 'M+':
        m = color[model][5]
        Demo()
        STORAGE.append(CurrentShow.get())
    elif operator == 'M-':
        if CurrentShow.get().startswith('-'):
            STORAGE.append(CurrentShow.get())
        else:
            STORAGE.append('-' + CurrentShow.get())
        m = color[model][5]
        Demo()
    elif operator in ['+', '-', '*', '/', '%']:
        STORAGE.append(CurrentShow.get())
        STORAGE.append(operator)
        IS_CALC = True
    elif operator == '=':
        if IS_CALC:
            CurrentShow.set('0')
        STORAGE.append(CurrentShow.get())
        expression = ''.join(STORAGE)
        result = calculate_expression(expression)
        result = modifyResult(result)
        CurrentShow.set(result)
        STORAGE.clear()
        IS_CALC = True


'''Demo'''
def Demo():
    root.minsize(320,502)
    root.title('计算器')
    root.configure(bg=color[model][1])
    try:
        root.iconbitmap('favicon.ico')
    except:
        pass
    # 布局
    # --文本框
    label = tkinter.Label(root, textvariable=CurrentShow, bg=color[model][1], anchor='e', bd=5, fg=color[model][5], font=('Cascadia Mono', 33))
    label.place(x=20, y=75, width=280, height=50)

    # --第一行
    # ----Memory clear
    button1_1 = tkinter.Button(text='', bg=color[model][1], bd=0, command=lambda:pressOperator('MC'),font=('Calculator Fluent Icons',12),fg=m)
    button1_1.place(x=5, y=147, width=51, height=25)
    # ----Memory read
    button1_2 = tkinter.Button(text='', bg=color[model][1], bd=0, command=lambda:pressOperator('MR'),font=('Calculator Fluent Icons',12),fg=m)
    button1_2.place(x=58, y=147, width=51, height=25)
    # ----Memory +
    button1_4 = tkinter.Button(text='', bg=color[model][1], bd=0, command=lambda:pressOperator('M+'),font=('Calculator Fluent Icons',12),fg=color[model][5])
    button1_4.place(x=111, y=147, width=51, height=25)
    # ----Memory -
    button1_5 = tkinter.Button(text='', bg=color[model][1], bd=0, command=lambda:pressOperator('M-'),font=('Calculator Fluent Icons',12),fg=color[model][5])
    button1_5.place(x=164, y=147, width=51, height=25)
    # ----Memory save
    button1_3 = tkinter.Button(text='', bg=color[model][1], bd=0, command=lambda:pressOperator('MS'),font=('Calculator Fluent Icons',12),fg=color[model][5])
    button1_3.place(x=217, y=147, width=51, height=25)
    # ----Memory v
    button1_5 = tkinter.Button(text='', bg=color[model][1], bd=0, command=lambda:pressOperator('MV'),font=('Calculator Fluent Icons',12),fg=m)
    button1_5.place(x=270, y=147, width=51, height=25)

    # --第二行
    # ----取余
    button3_5 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator(''),font=('Calculator Fluent Icons',11),fg=color[model][5])
    button3_5.place(x=4, y=182, width=77, height=51)
    # ----清除当前显示框内所有数字
    button2_2 = tkinter.Button(text='CE', bg=color[model][2], bd=0, command=lambda:clearCurrent(),font=('Cascadia Mono', 13),fg=color[model][5])
    button2_2.place(x=83, y=182, width=76, height=51)
    # ----清零(相当于重启)
    button2_3 = tkinter.Button(text='C', bg=color[model][2], bd=0, command=lambda:clearAll(),font=('楷体', 13),fg=color[model][5])
    button2_3.place(x=161, y=182, width=77, height=51)
    # ----删除单个数字
    button2_1 = tkinter.Button(text='', bg=color[model][2],bd=0,command=lambda:delOne(),font=('Calculator Fluent Icons', 12),fg=color[model][5])
    button2_1.place(x=240, y=182, width=76, height=51)

    # --第三行
    # ----取导数
    button4_5 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator('1/x'),font=('Calculator Fluent Icons',12),fg=color[model][5])
    button4_5.place(x=4, y=235, width=77, height=51)
    # ----平方
    button4_5 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator('x2'),font=('Calculator Fluent Icons',12),fg=color[model][5])
    button4_5.place(x=83, y=235, width=76, height=51)
    # ----开根号
    button2_5 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator('sqrt'),font=('Calculator Fluent Icons',12),fg=color[model][5])
    button2_5.place(x=161, y=235, width=77, height=51)
    # ----除
    button3_4 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator('/'),font=('Calculator Fluent Icons', 11),fg=color[model][5])
    button3_4.place(x=240, y=235, width=76, height=51)

    # --第四行
    # ----1
    button5_3 = tkinter.Button(text='1', bg=color[model][3], bd=0, command=lambda:pressNumber('1'),font=('黑体', 15),fg=color[model][5])
    button5_3.place(x=4, y=288, width=77, height=51)
    # ----2
    button5_2 = tkinter.Button(text='2', bg=color[model][3], bd=0, command=lambda:pressNumber('2'),font=('黑体', 15),fg=color[model][5])
    button5_2.place(x=83, y=288, width=76, height=51)
    # ----3
    button5_1 = tkinter.Button(text='3', bg=color[model][3], bd=0, command=lambda:pressNumber('3'),font=('黑体', 15),fg=color[model][5])
    button5_1.place(x=161, y=288, width=77, height=51)
    # ----乘
    button4_4 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator('*'),font=('Calculator Fluent Icons', 11),fg=color[model][5])
    button4_4.place(x=240, y=288, width=76, height=51)

    # --第五行
    # ----4
    button4_1 = tkinter.Button(text='4', bg=color[model][3], bd=0, command=lambda:pressNumber('4'),font=('黑体', 15),fg=color[model][5])
    button4_1.place(x=4, y=341, width=77, height=51)
    # ----5
    button4_2 = tkinter.Button(text='5', bg=color[model][3], bd=0, command=lambda:pressNumber('5'),font=('黑体', 15),fg=color[model][5])
    button4_2.place(x=83, y=341, width=76, height=51)
    # ----6
    button4_3 = tkinter.Button(text='6', bg=color[model][3], bd=0, command=lambda:pressNumber('6'),font=('黑体', 15),fg=color[model][5])
    button4_3.place(x=161, y=341, width=77, height=51)
    # ----减
    button5_4 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator('-'),font=('Calculator Fluent Icons', 11),fg=color[model][5])
    button5_4.place(x=240, y=341, width=76, height=51)

    # --第六行
    # ----7
    button3_1 = tkinter.Button(text='7', bg=color[model][3], bd=0, command=lambda:pressNumber('7'),font=('黑体', 15),fg=color[model][5])
    button3_1.place(x=4, y=394, width=77, height=51)
    # ----8
    button3_2 = tkinter.Button(text='8', bg=color[model][3], bd=0, command=lambda:pressNumber('8'),font=('黑体', 15),fg=color[model][5])
    button3_2.place(x=83, y=394, width=76, height=51)
    # ----9
    button3_3 = tkinter.Button(text='9', bg=color[model][3], bd=0, command=lambda:pressNumber('9'),font=('黑体', 15),fg=color[model][5])
    button3_3.place(x=161, y=394, width=77, height=51)
    # ----加
    button6_3 = tkinter.Button(text='', bg=color[model][2], bd=0, command=lambda:pressOperator('+'),font=('Calculator Fluent Icons', 11),fg=color[model][5])
    button6_3.place(x=240, y=394, width=76, height=51)

    # --第七行
    # ----取反
    button2_4 = tkinter.Button(text='', bg=color[model][3], bd=0, command=lambda:pressOperator('+/-'),font=('Calculator Fluent Icons', 15),fg=color[model][5])
    button2_4.place(x=4, y=447, width=77, height=51)
    # ----0
    button6_1 = tkinter.Button(text='0', bg=color[model][3], bd=0, command=lambda:pressNumber('0'),font=('黑体', 15),fg=color[model][5])
    button6_1.place(x=83, y=447, width=76, height=51)
    # ----小数点
    button6_2 = tkinter.Button(text='.', bg=color[model][3], bd=0, command=lambda:pressDP(),font=('黑体', 15),fg=color[model][5])
    button6_2.place(x=161, y=447, width=77, height=51)
    # ----等于
    button5_5 = tkinter.Button(text='', bg=color[model][4], bd=0, command=lambda:pressOperator('='),fg=color[model][6],font=('Calculator Fluent Icons', 11))
    button5_5.place(x=240, y=447, width=76, height=51)

    root.mainloop()

# 启动检查系统颜色的线程
def check_system_color():
    global model
    try:
        while True:
            import darkdetect
            new_model = 1 if darkdetect.isDark() else 0
            if new_model != model:
                model = new_model
                root.after(0,Demo)
            time.sleep(0.5)
    except:
        pass
color_thread = threading.Thread(target=check_system_color, daemon=True)
color_thread.start()

if __name__ == '__main__':
    Demo()
