import tkinter as tk
import os
import csv
import random
from tkinter import ttk
from tkinter import font as tkfont
from tkinter import filedialog
from tkinter import messagebox
from ScrollableFrame import *

# 프레임 전환 구현 - 같은 위치에 여러 프레임을 겹쳐놓고 선택한 프레임을 맨 위로 올림.
# 채점 - dict에 1대1 대응하는 double_dict를 만들어 영어, 한글 두개의 key값을 아무거나 줘도 일정한 value값이 나오도록 구현

class SampleApp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.title_font = tkfont.Font(family='Helvetica', size=18, weight="bold", slant="italic")
        self.title("영단어 암기 프로그램")
        # 다른 클래스(onePage, twoPage..)에서 참조 가능하도록 만든 data
        self.app_data = {"dict": {},
                         "double_dict": {},
                         "question_count": 0,
                         "word_count": 0,
                         "var_vocab": tk.IntVar(),
                         "word_shuffle": tk.IntVar(),
                         "question_list": [],
                         "name_list": [],
                         "entries": [],
                         "result_list": [],
        }

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageOne, PageTwo): #각 클래스를 튜플로 묶어서 하나씩 실행
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame

            # 모든 페이지를 같은 위치에 넣기
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("StartPage")
    def get_page(self, classname):
        for page in self.frames.values():
            if str(page.__class__.__name__) == classname:
                return page
        return None
    def show_frame(self, page_name): 
        '''Show a frame for the given page name'''
        frame = self.frames[page_name]
        frame.update()
        frame.tkraise() # 선택한 프레임을 맨 위로 올리는 함수


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.rowconfigure(0, minsize=300, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)

         # 버튼 frame
        self.frm_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)

        # open 버튼
        self.btn_open = tk.Button(self.frm_buttons, text="Open", command=self.openFile)
        self.btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

        # setting 버튼
        self.btn_setting = tk.Button(self.frm_buttons, text="Setting...", command=lambda: controller.show_frame("PageOne"))
        self.btn_setting.grid(row=1, column=0, sticky="ew", padx=5)

        # start 버튼
        self.btn_start = tk.Button(self.frm_buttons, text="Start", command=lambda: controller.show_frame("PageTwo"))
        self.btn_start.grid(row=2, column=0, sticky="ew", padx=5, pady=5)

        self.frm_buttons.grid(row=0, column=0, sticky="ns")

        # 단어 리스트 박스
        self.lst_vocab = tk.Listbox(self, height=5)
        self.lst_vocab.grid(row=0, column=1, sticky="nsew")

        # 단어 리스트 박스 스크롤바
        self.vsc_vocab = ttk.Scrollbar(self, orient=tk.VERTICAL, command=self.lst_vocab.yview)
        self.vsc_vocab.grid(row=0, column=2, sticky="ns")
        self.lst_vocab['yscrollcommand'] = self.vsc_vocab.set

        # 상태 메세지
        self.lbl_status = tk.Label(self, text="Status message", anchor="w")
        self.lbl_status.grid(column=0, columnspan=2, row=1, sticky="we")


    def openFile(self):
        # 기존에 있던 값들 모두 초기회
        self.controller.app_data["dict"].clear()
        self.controller.app_data["word_count"] = 0
        self.lst_vocab.delete(0, tk.END)

        fileName = filedialog.askopenfilenames(initialdir="/",\
            title = "파일을 선택 해 주세요", \
                filetypes = [("Excel Files", "*csv"), ("Text Files", "*txt"), ("All Files", "*.*")])
        if fileName == '':
            self.lbl_status['fg'] = "red"
            self.lbl_status['text'] = "file open failed: please select a file"
            return
        ext = os.path.splitext(fileName[0])[1]
        if ext == '.txt':
            with open(fileName[0], 'r', encoding='UTF-8') as file:
                lines = file.readlines()
                for line in lines:
                    pair = line.split(' ')
                    self.controller.app_data["dict"][pair[0]] = pair[1].strip()
                    self.controller.app_data["double_dict"][pair[0]] = pair[1].strip()
                    self.controller.app_data["double_dict"][pair[1].strip()] = pair[0]
        elif ext == '.csv':
            with open(fileName[0], 'r') as file:
                self.controller.app_data["dict"] = dict(csv.reader(file))
            for key,value in self.controller.app_data["dict"].items():
                self.controller.app_data["double_dict"][key] = value
                self.controller.app_data["double_dict"][value] = key
        else:
            self.lbl_status['fg'] = "red"
            self.lbl_status['text'] = "file open failed: 지원하지 않는 파일 형식"
            return
        for key,value in self.controller.app_data["dict"].items():
            self.controller.app_data["word_count"] += 1
            self.lst_vocab.insert('end', str(self.controller.app_data["word_count"]) + ". " + key + ": " + value)
        self.controller.app_data["question_count"] = self.controller.app_data["word_count"]
        print(self.controller.app_data["word_count"])
        self.lbl_status['fg'] = "green"
        self.lbl_status['text'] = "file open success"
    def update(self):
        pass

class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.rowconfigure(0, minsize=300, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)

        # 버튼 frame
        self.frm_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)

        # 확인 버튼
        self.btn_enter = tk.Button(self.frm_buttons, text="확인", width=10, command=lambda: controller.show_frame("StartPage"))
        self.btn_enter.grid(row=1, column=0, columnspan=2, pady=5)

        self.frm_buttons.grid(row=0, column=0, sticky="ns")

        # 셋팅 frame
        self.frm_settings = tk.Frame(self, height=5)

        # 라디오 버튼 frame 
        self.frm_radio = tk.LabelFrame(self.frm_settings, text="문제 유형 선택", relief=tk.GROOVE, bd=2)

        # 라디오 버튼 3개
        self.rdo_g1 = tk.Radiobutton(self.frm_radio, value=0, text="단어 뜻 빈칸", variable=self.controller.app_data["var_vocab"]) # default
        self.rdo_g2 = tk.Radiobutton(self.frm_radio, value=1, text="단어 스펠링 빈칸", variable=self.controller.app_data["var_vocab"])
        self.rdo_g3 = tk.Radiobutton(self.frm_radio, value=2, text="랜덤", variable=self.controller.app_data["var_vocab"])

        self.rdo_g1.grid(row=0, column=0, sticky='w', pady=5)
        self.rdo_g2.grid(row=1, column=0, sticky='w')
        self.rdo_g3.grid(row=2, column=0, sticky='w', pady=5)

        self.frm_radio.grid(row=0, column=0,sticky='n', padx=5, pady=5)

        # 체크박스
        self.chk_c1 = tk.Checkbutton(self.frm_settings, text="단어 섞기", variable=self.controller.app_data["word_shuffle"])
        self.chk_c1.grid(row=1, column=0, sticky='n')

        # input 프레임
        self.frm_input = tk.Frame(self.frm_settings, bd=2)

        # 출제 수 입력
        self.lbl_number = tk.Label(self.frm_input, text="출제 수(max:"+ str(self.controller.app_data["word_count"])+"): ")
        self.ent_input = tk.Entry(self.frm_input, width=3)
        self.lbl_number.grid(row=0, column=0, sticky='w')
        self.ent_input.grid(row=0, column=1, sticky='w')

        self.frm_input.grid(row=2, column=0, sticky='n', padx=5, pady=5)

        self.frm_settings.grid(row=0, column=1, sticky="nsew")
        # 상태 메세지
        self.lbl_status = tk.Label(self, text="Status message", anchor="w")
        self.lbl_status.grid(column=0, columnspan=2, row=1, sticky="we")

    def update(self):
        self.lbl_number["text"] = "출제 수(max:"+ str(self.controller.app_data["word_count"])+"): "
        self.ent_input.insert(0, str(self.controller.app_data["question_count"]))

class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller

        self.rowconfigure(0, minsize=300, weight=1)
        self.columnconfigure(1, minsize=400, weight=1)

        # 버튼 frame
        self.frm_buttons = tk.Frame(self, relief=tk.RAISED, bd=2)

        # 뒤로가기 버튼
        self.btn_enter = tk.Button(self.frm_buttons, text="뒤로가기", width=10, command=lambda: controller.show_frame("StartPage"))
        self.btn_enter.grid(row=1, column=0, columnspan=2, pady=5)

        #제출하기 버튼
        self.btn_enter = tk.Button(self.frm_buttons, text="Submit", width=10, command=self.save)
        self.btn_enter.grid(row=2, column=0, columnspan=2, pady=5)

        self.frm_buttons.grid(row=0, column=0, sticky="ns")

        # 셋팅 frame
        self.frm_scroll = ScrollableFrame(self)

        self.frm_scroll.grid(row=0, column=1, sticky="nsew")

        # 상태 메세지
        self.lbl_status = tk.Label(self, text="Status message", anchor="w")
        self.lbl_status.grid(column=0, columnspan=2, row=1, sticky="we")

    def save(self):
        result = messagebox.askquestion("Submit", "정말로 제출하시겠습니까?")
        answer = self.controller.app_data["double_dict"]
        result_list = self.controller.app_data["result_list"]
        question_list = self.controller.app_data["question_list"]
        result_list.clear()
        if result == 'yes':
            entries = self.controller.app_data["entries"]
            for idx,entry in enumerate(entries):
                try:
                    if answer[question_list[idx]] == entry.get():
                        result_list.append("O")
                    else:
                        result_list.append("X")
                except:
                    result_list.append("X")
            self.controller.show_frame("StartPage")
        else:
            return
        
        print(result_list)

    def update(self):
        question_list = self.controller.app_data["question_list"]
        question_list.clear()
        var_vocab = self.controller.app_data["var_vocab"].get()
        dict = self.controller.app_data["dict"]

        for widgets in self.frm_scroll.scrollable_frame.winfo_children():
            widgets.destroy()

        if var_vocab == 0:
            for key in dict:
                question_list.append(key)
        elif var_vocab == 1:
            for key in dict:
                question_list.append(dict[key])
        else:
            for key in dict:
                if random.randint(0, 1):
                    question_list.append(dict[key])
                else:
                    question_list.append(key)

        if self.controller.app_data["word_shuffle"].get():
            random.shuffle(question_list)
        entries = self.controller.app_data["entries"]
        for idx, text in enumerate(dict):
            label = tk.Label(self.frm_scroll.scrollable_frame, text=question_list[idx])
            entry = tk.Entry(self.frm_scroll.scrollable_frame, width=50)
            label.grid(row=idx, column=0)
            entry.grid(row=idx, column=1)
            entries.append(entry)

            

app = SampleApp()
app.mainloop()