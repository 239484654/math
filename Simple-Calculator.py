'''
Function:
	tkinter计算器
Author:
	Charlie
'''
import math
import tkinter


root = tkinter.Tk()
root.resizable(width=False, height=False)
'''hypeparameter'''
# 是否按下了运算符
IS_CALC = False
# 存储数字
STORAGE = []
# 显示框最多显示多少个字符
MAXSHOWLEN = 11
# 当前显示的数字
CurrentShow = tkinter.StringVar()
CurrentShow.set('0')


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
			# 直接舍去不考虑四舍五入问题
			result = result[:MAXSHOWLEN]
	return result


'''按下运算符'''
def pressOperator(operator):
	global STORAGE
	global IS_CALC
	if operator == '+/-':
		if CurrentShow.get().startswith('-'):
			CurrentShow.set(CurrentShow.get()[1:])
		else:
			CurrentShow.set('-'+CurrentShow.get())
	elif operator == '1/x':
		try:
			result = 1 / float(CurrentShow.get())
		except:
			result = 'illegal operation'
		result = modifyResult(result)
		CurrentShow.set(result)
		IS_CALC = True
	elif operator == 'sqrt':
		try:
			result = math.sqrt(float(CurrentShow.get()))
		except:
			result = 'illegal operation'
		result = modifyResult(result)
		CurrentShow.set(result)
		IS_CALC = True
	elif operator == 'MC':
		STORAGE.clear()
	elif operator == 'MR':
		if IS_CALC:
			CurrentShow.set('0')
		STORAGE.append(CurrentShow.get())
		expression = ''.join(STORAGE)
		try:
			result = eval(expression)
		except:
			result = 'illegal operation'
		result = modifyResult(result)
		CurrentShow.set(result)
		IS_CALC = True
	elif operator == 'MS':
		STORAGE.clear()
		STORAGE.append(CurrentShow.get())
	elif operator == 'M+':
		STORAGE.append(CurrentShow.get())
	elif operator == 'M-':
		if CurrentShow.get().startswith('-'):
			STORAGE.append(CurrentShow.get())
		else:
			STORAGE.append('-' + CurrentShow.get())
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
		# 除以0的情况
		except:
			result = '除数不能为0'
		result = modifyResult(result)
		CurrentShow.set(result)
		STORAGE.clear()
		IS_CALC = True


'''Demo'''
def Demo():
	root.minsize(320,470)
	root.title('计算器')
	root.configure(bg="#202020")
	# 布局
	# --文本框
	label = tkinter.Label(root, textvariable=CurrentShow, bg='#202020', anchor='e', bd=5, fg='white', font=('Microsoft YaHei UI', 33))
	label.place(x=20, y=75, width=280, height=50)
	# --第一行
	# ----Memory clear
	button1_1 = tkinter.Button(text='MC', bg='#202020', bd=0, command=lambda:pressOperator('MC'),fg='#717171')
	button1_1.place(x=5, y=147, width=51, height=25)
	# ----Memory read
	button1_2 = tkinter.Button(text='MR', bg='#202020', bd=0, command=lambda:pressOperator('MR'),fg='#717171')
	button1_2.place(x=58, y=147, width=51, height=25)
	# ----Memory save
	button1_3 = tkinter.Button(text='MS', bg='#202020', bd=0, command=lambda:pressOperator('MS'),fg="white")
	button1_3.place(x=217, y=147, width=51, height=25)
	# ----Memory +
	button1_4 = tkinter.Button(text='M+', bg='#202020', bd=0, command=lambda:pressOperator('M+'),fg="white")
	button1_4.place(x=111, y=147, width=51, height=25)
	# ----Memory -
	button1_5 = tkinter.Button(text='M-', bg='#202020', bd=0, command=lambda:pressOperator('M-'),fg="white")
	button1_5.place(x=164, y=147, width=51, height=25)
	# ----Memory -
	button1_5 = tkinter.Button(text='M∨', bg='#202020', bd=0, command=lambda:pressOperator('M∨'),fg='#717171')
	button1_5.place(x=270, y=147, width=51, height=25)
	# --第二行
	# ----删除单个数字
	button2_1 = tkinter.Button(text='del', bg='#323232', bd=0, command=lambda:delOne(),font=('楷体', 13),fg="white")
	button2_1.place(x=241, y=176, width=75, height=45)
	# ----清除当前显示框内所有数字
	button2_2 = tkinter.Button(text='CE', bg='#323232', bd=0, command=lambda:clearCurrent(),font=('楷体', 13),fg="white")
	button2_2.place(x=83, y=176, width=75, height=45)
	# ----清零(相当于重启)
	button2_3 = tkinter.Button(text='C', bg='#323232', bd=0, command=lambda:clearAll(),font=('楷体', 13),fg="white")
	button2_3.place(x=162, y=176, width=75, height=45)
	# ----取反
	button2_4 = tkinter.Button(text='+/-', bg='#3b3b3b', bd=0, command=lambda:pressOperator('+/-'),font=('黑体', 15),fg="white")
	button2_4.place(x=4, y=421, width=75, height=45)
	# ----开根号
	button2_5 = tkinter.Button(text='√￣', bg='#323232', bd=0, command=lambda:pressOperator('sqrt'),fg="white")
	button2_5.place(x=162, y=225, width=75, height=45)
	# --第三行
	# ----7
	button3_1 = tkinter.Button(text='7', bg='#3b3b3b', bd=0, command=lambda:pressNumber('7'),font=('黑体', 15),fg="white")
	button3_1.place(x=4, y=372, width=75, height=45)
	# ----8
	button3_2 = tkinter.Button(text='8', bg='#3b3b3b', bd=0, command=lambda:pressNumber('8'),font=('黑体', 15),fg="white")
	button3_2.place(x=83, y=372, width=75, height=45)
	# ----9
	button3_3 = tkinter.Button(text='9', bg='#3b3b3b', bd=0, command=lambda:pressNumber('9'),font=('黑体', 15),fg="white")
	button3_3.place(x=162, y=372, width=75, height=45)
	# ----除
	button3_4 = tkinter.Button(text='÷', bg='#323232', bd=0, command=lambda:pressOperator('/'),font=('Juice ITC', 15),fg="white")
	button3_4.place(x=241, y=225, width=75, height=45)
	# ----取余
	button3_5 = tkinter.Button(text='%', bg='#323232', bd=0, command=lambda:pressOperator('%'),fg="white")
	button3_5.place(x=4, y=176, width=75, height=45)
	# --第四行
	# ----4
	button4_1 = tkinter.Button(text='4', bg='#3b3b3b', bd=0, command=lambda:pressNumber('4'),font=('黑体', 15),fg="white")
	button4_1.place(x=4, y=323, width=75, height=45)
	# ----5
	button4_2 = tkinter.Button(text='5', bg='#3b3b3b', bd=0, command=lambda:pressNumber('5'),font=('黑体', 15),fg="white")
	button4_2.place(x=83, y=323, width=75, height=45)
	# ----6
	button4_3 = tkinter.Button(text='6', bg='#3b3b3b', bd=0, command=lambda:pressNumber('6'),font=('黑体', 15),fg="white")
	button4_3.place(x=162, y=323, width=75, height=45)
	# ----乘
	button4_4 = tkinter.Button(text='×', bg='#323232', bd=0, command=lambda:pressOperator('*'),font=('Juice ITC', 15),fg="white")
	button4_4.place(x=241, y=274, width=75, height=45)
	# ----取导数
	button4_5 = tkinter.Button(text='1/x', bg='#323232', bd=0, command=lambda:pressOperator('1/x'),fg="white")
	button4_5.place(x=4, y=225, width=75, height=45)
	# ----取导数
	button4_5 = tkinter.Button(text='x²', bg='#323232', bd=0, command=lambda:pressOperator('x²'),fg="white")
	button4_5.place(x=83, y=225, width=75, height=45)
	# --第五行
	# ----3
	button5_1 = tkinter.Button(text='3', bg='#3b3b3b', bd=0, command=lambda:pressNumber('3'),font=('黑体', 15),fg="white")
	button5_1.place(x=162, y=274, width=75, height=45)
	# ----2
	button5_2 = tkinter.Button(text='2', bg='#3b3b3b', bd=0, command=lambda:pressNumber('2'),font=('黑体', 15),fg="white")
	button5_2.place(x=83, y=274, width=75, height=45)
	# ----1
	button5_3 = tkinter.Button(text='1', bg='#3b3b3b', bd=0, command=lambda:pressNumber('1'),font=('黑体', 15),fg="white")
	button5_3.place(x=4, y=274, width=75, height=45)
	# ----减
	button5_4 = tkinter.Button(text='-', bg='#323232', bd=0, command=lambda:pressOperator('-'),font=('幼圆', 15),fg="white")
	button5_4.place(x=241, y=323, width=75, height=45)
	# ----等于
	button5_5 = tkinter.Button(text='=', bg='#76b9ed', bd=0, command=lambda:pressOperator('='),fg="black",font=('Juice ITC', 17))
	button5_5.place(x=241, y=421, width=75, height=45)
	# --第六行
	# ----0
	button6_1 = tkinter.Button(text='0', bg='#3b3b3b', bd=0, command=lambda:pressNumber('0'),font=('黑体', 15),fg="white")
	button6_1.place(x=83, y=421, width=75, height=45)
	# ----小数点
	button6_2 = tkinter.Button(text='.', bg='#3b3b3b', bd=0, command=lambda:pressDP(),font=('黑体', 15),fg="white")
	button6_2.place(x=162, y=421, width=75, height=45)
	# ----加
	button6_3 = tkinter.Button(text='+', bg='#323232', bd=0, command=lambda:pressOperator('+'),font=('Juice ITC', 15),fg="white")
	button6_3.place(x=241, y=372, width=75, height=45)


	
	root.mainloop()


if __name__ == '__main__':
	Demo()
