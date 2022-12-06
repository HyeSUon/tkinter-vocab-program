from tkinter import filedialog
from tkinter import messagebox
import tkinter as tk
from tkinter import ttk
import os
import csv
import random

fileName = None
file = None
dictionary = {}
double_dict = {}
word_count = 0
question_count = 0
settingWindow = None

question_list = []
entry_list = []
label_list = []

def openFile():
    global dictionary, word_count, question_count
    fileName = filedialog.askopenfilenames(initialdir="/",\
        title = "파일을 선택 해 주세요", \
            filetypes = [("Excel Files", "*csv"), ("Text Files", "*txt"), ("All Files", "*.*")])
    if fileName == '':
        lbl_status['fg'] = "red"
        lbl_status['text'] = "file open failed: please select a file"
        return
    ext = os.path.splitext(fileName[0])[1]
    if ext == '.txt':
        with open(fileName[0], 'r', encoding='UTF-8') as file:
            lines = file.readlines()
            for line in lines:
                pair = line.split(' ')
                dictionary[pair[0]] = pair[1].strip()
                double_dict[pair[0]] = pair[1].strip()
                double_dict[pair[1].strip()] = pair[0]
    elif ext == '.csv':
        with open(fileName[0], 'r') as file:
            dictionary = dict(csv.reader(file))
        for key,value in dictionary.items():
            double_dict[key] = value
            double_dict[value] = key
    else:
        lbl_status['fg'] = "red"
        lbl_status['text'] = "file open failed: 지원하지 않는 파일 형식"
        return
    for key,value in dictionary.items():
        word_count += 1
        lst_vocab.insert('end', str(word_count) + ". " + key + ": " + value)
    question_count = word_count
    lbl_status['fg'] = "green"
    lbl_status['text'] = "file open success"

def exitSettingWindow(settingWindow, ent_input):
    num = int(ent_input.get()) # 예외처리 x
    if num < 0 or num > word_count:
        messagebox.showerror("에러", "유효한 값을 입력해주세요.") # 취소 구현 x
    question_count = num
    lbl_status['fg'] = "green"
    lbl_status['text'] = "setting saved!"
    settingWindow.destroy()


def saveSetting(settingWindow, ent_input):
    global var_vocab, question_count
    num = int(ent_input.get())
    if num < 0 or num > word_count:
        messagebox.showerror("에러", "유효한 값을 입력해주세요.")
        return

    question_count = num
    lbl_status['fg'] = "green"
    lbl_status['text'] = "setting saved!"
    settingWindow.destroy()

def setting():
    settingWindow = tk.Toplevel(window)
    settingWindow.title("Setting")

    frm_radio = tk.LabelFrame(settingWindow, text="문제 유형 선택", relief=tk.GROOVE, bd=2)
    rdo_g1 = tk.Radiobutton(frm_radio, value=0, text="단어 뜻 빈칸", variable=var_vocab) # default
    rdo_g2 = tk.Radiobutton(frm_radio, value=1, text="단어 스펠링 빈칸", variable=var_vocab)
    rdo_g3 = tk.Radiobutton(frm_radio, value=2, text="랜덤", variable=var_vocab)

    frm_input = tk.Frame(settingWindow, bd=2)
    chk_c1 = tk.Checkbutton(settingWindow, text="단어 섞기", variable=wordShuffle)
    lbl_number = tk.Label(frm_input, text="출제 수(max:"+ str(word_count)+"): ")
    ent_input = tk.Entry(frm_input, width=3)
    btn_enter = tk.Button(frm_input, text="확인", width=10, command= lambda: saveSetting(settingWindow, ent_input))

    settingWindow.rowconfigure(0, minsize=100, weight=1)
    settingWindow.columnconfigure(0, minsize=50, weight=1)

    rdo_g1.grid(row=0, column=0, sticky='w', pady=5)
    rdo_g2.grid(row=1, column=0, sticky='w')
    rdo_g3.grid(row=2, column=0, sticky='w', pady=5)
    frm_radio.grid(row=0, column=0,sticky='n', padx=5, pady=5)

    chk_c1.grid(row=1, column=0, sticky='n')
    lbl_number.grid(row=0, column=0, sticky='w')
    ent_input.grid(row=0, column=1, sticky='w')
    btn_enter.grid(row=1, column=0, columnspan=2, pady=5)
    frm_input.grid(row=2, column=0, sticky='n', padx=5, pady=5)

    ent_input.insert(0, str(question_count))
    settingWindow.protocol('WM_DELETE_WINDOW', lambda: exitSettingWindow(settingWindow, ent_input))

def saveResult():
    pass

def nextFunc(page):
    page+= 1
    if len(question_list) < page * 10:
        for i in range((page-1)*10, (page-1)*10 + len(question_list) % 10):
            label_list[i-(page-1)*10]["text"] = question_list[i]
    else:
        for i in range((page-1)*10, page*10):
            label_list[i-(page-1)*10]["text"] = question_list[i]
    

def startQuiz():
    quizWindow = tk.Toplevel(window)
    quizWindow.title("Quiz")
    frm_form = tk.Frame(quizWindow, relief=tk.SUNKEN, borderwidth=3)
    frm_form.pack()

    question_list.clear()
    entry_list.clear()
    label_list.clear()
    page = 1

    num_vocab = var_vocab.get()
    if num_vocab == 0:
        for key in dictionary:
            question_list.append(key)
    elif num_vocab == 1:
        for key in dictionary:
            question_list.append(dictionary[key])
    elif num_vocab == 2:
        for key in dictionary:
            if random.randint(0, 1):
                question_list.append(dictionary[key])
            else:
                question_list.append(key)

    if wordShuffle:
        random.shuffle(question_list)

    if len(question_list) < page * 10:
        for i in range((page-1)*10, (page-1)*10 + len(question_list) % 10):
            label_list.append(tk.Label(master=frm_form, text=question_list[i]))
            entry_list.append(tk.Entry(master=frm_form,width=50))
            label_list[i].grid(row=i, column=0, sticky='e')
            entry_list[i].grid(row=i, column=1)
    else:
        for i in range((page-1)*10, page*10):
            label_list.append(tk.Label(master=frm_form, text=question_list[i]))
            entry_list.append(tk.Entry(master=frm_form,width=50))
            label_list[i].grid(row=i, column=0, sticky='e')
            entry_list[i].grid(row=i, column=1)


    frm_progress = tk.Frame(quizWindow, bg='red', height=30)
    frm_progress.pack(fill=tk.X)


    frame1 = tk.Frame(quizWindow, width=100, height=50)
    frame1.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    
    frame2 = tk.Frame(quizWindow, width=100, height=50)
    frame2.pack(fill=tk.BOTH, side=tk.LEFT, expand = True)

    frame3 = tk.Frame(quizWindow, width=100, height=50)
    frame3.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)
    btn_back = tk.Button(master=frame1, text="Back",width=10)
    btn_back.pack()

    btn_submit = tk.Button(master=frame2, text="Submit", width=10)
    btn_submit.pack()

    btn_next = tk.Button(master=frame3, text="Next", width=10, command=lambda: nextFunc(page))
    btn_next.pack()


window = tk.Tk()
window.title("English Vocab Editor")

window.rowconfigure(0, minsize=600, weight=1)
window.columnconfigure(1, minsize=800, weight=1)

var_vocab = tk.IntVar()
wordShuffle = tk.IntVar()
wordShuffle.set(1)

lst_vocab = tk.Listbox(window, height=5)
vsc_vocab = ttk.Scrollbar(window, orient=tk.VERTICAL, command=lst_vocab.yview)

frm_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
btn_open = tk.Button(frm_buttons, text="Open", command=openFile)
btn_setting = tk.Button(frm_buttons, text="Setting...", command=setting)
btn_start = tk.Button(frm_buttons, text="Start", command=startQuiz)
lbl_status = tk.Label(window, text="Status message", anchor="w")

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_setting.grid(row=1, column=0, sticky="ew", padx=5)
btn_start.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
lst_vocab.grid(row=0, column=1, sticky="nsew")
vsc_vocab.grid(row=0, column=2, sticky="ns")
lbl_status.grid(column=0, columnspan=2, row=1, sticky="we")

lst_vocab['yscrollcommand'] = vsc_vocab.set
    
window.mainloop()