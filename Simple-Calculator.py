
'''
Function:
    tkinter计算器
Author:
    Charlie
'''
import math
import tkinter
import tkinter as tk
import cmath

model = 0
try:
    import darkdetect
    if darkdetect.isDark():
        model = 1
except:
    pass
color = [["#979d9f","#d3e7f3","#f9f9f9","#ffffff","#0067c0","black","white"],["#979d9f","#202020","#323232","#3b3b3b","#76b9ed","white","black"]]
m = color[model][0]

root = tkinter.Tk()
root.resizable(width=False, height=False)
'''hypeparameter'''
# 是否按下了运算符
IS_CALC = False
# 存储数字
STORAGE = []
# 显示框最多显示多少个字符
MAXSHOWLEN = 10
# 当前显示的数字
CurrentShow = tkinter.StringVar()
CurrentShow.set('0')

def Int(num):
    if str(num)[-1] == "0":
        return int(num)
    return num

'''按下数字键(0-9)'''
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


'''按下小数点'''
def pressDP():
    global IS_CALC
    if IS_CALC:
        CurrentShow.set('0')
        IS_CALC = False
    if len(CurrentShow.get().split('.')) == 1:
        if len(CurrentShow.get()) < MAXSHOWLEN:
            CurrentShow.set(CurrentShow.get() + '.')


'''清零'''
def clearAll():
    global STORAGE
    global IS_CALC
    STORAGE.clear()
    IS_CALC = False
    CurrentShow.set('0')


'''清除当前显示框内所有数字'''
def clearCurrent():
    CurrentShow.set('0')


'''删除显示框内最后一个数字'''
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


'''计算答案修正'''
def modifyResult(result):
    result = str(result)
    if len(result) > MAXSHOWLEN:
        if len(result.split('.')[0]) > MAXSHOWLEN:
            result = 'Overflow'
        else:
            if "e" in result:
                reu = result.split("e+")
                reu_0 = str(Int(float(reu[0][:10-len(reu[1])-2])))
                result = reu_0+"e+"+reu[1]
        # 直接舍去不考虑四舍五入问题
            if result[-1] == "j":
                if "+" in result:
                    res = result[:-1].split("+")
                    res_1 = "+"+str(Int(float(res[1][:4])))+"i"
                    if res_1 == "+0i":
                        res_0 = str(Int(float(res[0][:10])))
                        res_1 = ""
                    else:
                        res_0 = str(Int(float(res[0][:4])))
                    result = str(res_0+res_1)
                else:
                    result = result[:(MAXSHOWLEN-1)]+"i"
            else:
                print(result[:8])
                result = result[:MAXSHOWLEN]
    else:
        if result[-1] == "j":
            result = result[:-1]+"i"
    if result == "0.99999999":
        result = "1"

    return result

'''按下运算符'''
def pressOperator(operator):
    global STORAGE
    global IS_CALC
    global m
    if operator == '+/-':
        if CurrentShow.get().startswith('-'):
            CurrentShow.set(CurrentShow.get()[1:])
        elif CurrentShow.get() == "Error":
            CurrentShow.set(CurrentShow.get())
        else:
            CurrentShow.set('-'+CurrentShow.get())
    elif operator == '1/x':
        try:
            result = 1 / float(CurrentShow.get())
            result = round(result,8)
            result = '%.10g'%result
        except:
            result = 'Error'
        result = modifyResult(result)
        CurrentShow.set(result)
        IS_CALC = True
    elif operator == 'sqrt':
        result = CurrentShow.get()
        if result == "Error":
            return "Error"
        def resultcr(result):
            if "i" not in result and "-" not in result:
                return math.sqrt(float(result))
            else:
                if "+" in result:
                    num = result.split("+")
                    if num[1] == "i":
                        num[1] = "1i"
                    return cmath.sqrt(float(num[0])+float(num[1][:-1])*cmath.sqrt(-1))
                elif "i" in result:
                    if result == "i":
                        result = "1i"
                    return cmath.sqrt(float(result[:-1])*cmath.sqrt(-1))
                else:
                    return cmath.sqrt(float(result))
        def resultck(a):
            if str(a)[0] == "(":
                a = str(a)[1:-1]
            return a
        result = resultck(resultcr(result))
        if str(result)[-1] != "j":
            result = round(result,8)
            result = '%.10g'%result
        else:
            if result == "1j":
                result = "j"
            elif result == "0j":
                result = "0"
        result = modifyResult(result)
        CurrentShow.set(result)
        IS_CALC = True
    elif operator == 'x2':
        result = CurrentShow.get()
        try:
            def resultcr(result):
                if "i" not in result and "-" not in result:
                    return pow(float(result), 2)
                else:
                    if "+" in result:
                        num = result.split("+")
                        if num[1] == "i":
                            num[1] = "1i"
                        return pow(float(num[0])+float(num[1][:-1])*cmath.sqrt(-1), 2)
                    elif "i" in result:
                        if result == "i":
                            result = "1i"
                        return pow(float(result[:-1])*cmath.sqrt(-1), 2)
                    else:
                        return pow(float(result),2)
            def resultck(a):
                if str(a)[0] == "(":
                    a = str(a)[1:-1]
                return a
            result = resultck(resultcr(result))
            if str(result)[-1] != "j":
                result = round(result,8)
                result = '%.10g'%result
            else:
                if result == "1j":
                    result = "j"
                elif result == "0j":
                    result = "0"
        except:
            result = "Error"
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
        try:
            result = eval(expression)
            result = round(result,8)
            result = '%.10g'%result
        except:
            result = 'Error'
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
        try:
            result = eval(expression)
            result = round(result,8)
            result = '%.10g'%result
        # 除以0的情况
        except:
            result = 'Error'
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

if __name__ == '__main__':
    Demo()
