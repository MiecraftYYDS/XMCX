import tkinter as tk
from tkinter import messagebox
import random
import os
import datetime

# 读取xm.txt文件中的名字
def read_names():
    with open('xm.txt', 'r', encoding='utf-8') as file:
        names = file.readlines()
    return [name.strip() for name in names]

# 检查 data.txt 文件的日期
def check_date():
    if os.path.exists('data.txt'):
        with open('data.txt', 'r', encoding='utf-8') as file:
            first_line = file.readline().strip()
        if first_line == datetime.datetime.now().strftime('%Y-%m-%d'):
            return True
    return False

# 删除 data.txt 文件的内容或新建文件
def reset_data_file():
    with open('data.txt', 'w', encoding='utf-8') as file:
        file.write(datetime.datetime.now().strftime('%Y-%m-%d') + '\n')

# 从 data.txt 文件中读取已记录的名字
def read_skipped_names():
    skipped_names = []
    if os.path.exists('data.txt'):
        with open('data.txt', 'r', encoding='utf-8') as file:
            skipped_names = file.readlines()[1:]
    return [name.strip() for name in skipped_names]

# 更新 data.txt 文件中的名字
def write_skipped_name(name):
    with open('data.txt', 'a', encoding='utf-8') as file:
        file.write(name + '\n')

# 抽选一个名字
def draw_name():
    global names
    global current_name
    if not names:
        names = read_names()  # 重新读取名字并移除请假的人
        names = [name for name in names if name not in skipped_names]
    while True:
        current_name = random.choice(names)
        if current_name not in skipped_names:
            break
    name_label.config(text=current_name)

# 对勾按钮点击事件
def confirm_name():
    with open('cx.txt', 'a', encoding='utf-8') as file:
        if file.tell() == 0:
            file.write(f"启动时间: {datetime.datetime.now()}\n")
        file.write(current_name + '\n')
    names.remove(current_name)
    draw_name()

# 叉号按钮点击事件
def skip_name():
    names.remove(current_name)  # 从名字列表中移除当前名字
    draw_name()

# 问号按钮点击事件
def mark_absent():
    write_skipped_name(current_name)  # 记录名字到 data.txt
    skipped_names.append(current_name)  # 更新内存中的请假名单
    names.remove(current_name)  # 从名字列表中移除当前名字
    draw_name()

# 初始化名字列表和当前选中的名字
names = read_names()
current_name = ""

# 每次启动时处理 data.txt
if not check_date():
    reset_data_file()

skipped_names = read_skipped_names()
names = [name for name in names if name not in skipped_names]

# 创建主窗口
root = tk.Tk()
root.title("抽选工具")
root.attributes("-topmost", True)  # 设置窗口置顶
root.geometry("200x150")  # 设置窗口的默认大小为 200x150

# 创建一个框架来放置按钮和标签
frame = tk.Frame(root)
frame.pack(expand=True, fill='both')

# 显示抽选的名字
name_label = tk.Label(frame, text="", font=("Arial", 20))
name_label.pack(pady=20)

# 设置框架使其随着窗口调整大小
frame.pack_propagate(False)

# 创建开始抽选按钮
def start_drawing():
    start_button.pack_forget()  # 隐藏开始按钮
    name_label.pack_forget()  # 隐藏最初的空标签
    name_label.pack(pady=20)  # 显示标签
    confirm_button.pack(side='left', padx=10, expand=True, fill='both')
    skip_button.pack(side='right', padx=10, expand=True, fill='both')
    mark_button.pack(side='top', padx=10, pady=10, expand=True, fill='both')  # 添加问号按钮
    draw_name()

start_button = tk.Button(frame, text="开始抽选", command=start_drawing, font=("Arial", 20))
start_button.pack(pady=20, expand=True, fill='both')

# 创建对勾按钮和叉号按钮，但初始时不显示
confirm_button = tk.Button(frame, text="✔", command=confirm_name, font=("Arial", 20))
skip_button = tk.Button(frame, text="✖", command=skip_name, font=("Arial", 20))
mark_button = tk.Button(frame, text="?", command=mark_absent, font=("Arial", 20))

# 运行主循环
root.mainloop()
