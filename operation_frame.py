#!/usr/bin/python3
# operation_frame.py
# Author: Claudio <3261958605@qq.com>
# Created: 2017-07-27 16:41:43
# Code:
'''
操作界面组件
'''


import operation
import restore
import tkinter as tk
import tkinter.filedialog as filedialog
import tkinter.messagebox as messeagebox
import validate
from public import FONT


class Frame(tk.Frame):
    def __init__(self, master, settings_frame):
        super(Frame, self).__init__(master)
        self.master = master

        self.settings_frame = settings_frame

        self.font = (FONT['family'], FONT['size'] + 1, 'normal')

        self.folder_icon = tk.PhotoImage(file='folder.png')
        self.excel_icon = tk.PhotoImage(file='excel.png')

        self.src_folder = tk.StringVar()
        self.dst_folder = tk.StringVar()
        self.excel_file = tk.StringVar()
        self.progress_str = tk.StringVar()

        # 测试用
        # self.src_folder.set(
        #     '/home/claudio/Desktop/Python/pics-handler/data_test/pics')
        # self.dst_folder.set(
        #     '/home/claudio/Desktop/Python/pics-handler/data_test/pics_new')
        # self.excel_file.set(
        #     '/home/claudio/Desktop/Python/pics-handler/data_test/2017年1月-2017年12月.xlsx')

        self.src_folder_widget = None
        self.src_folder_button_widget = None
        self.dst_folder_widget = None
        self.dst_folder_button_widget = None
        self.excel_file_widget = None
        self.excel_file_button_widget = None
        self.submit_button_widget = None

        self.add_src_dir()
        self.add_dst_dir()
        self.add_excel_file()
        self.add_commit_button()
        self.add_progress()

        self.interactive_widgets = [
            self.src_folder_widget,
            self.src_folder_button_widget,
            self.dst_folder_widget,
            self.dst_folder_button_widget,
            self.excel_file_widget,
            self.excel_file_button_widget,
            self.submit_button_widget,
        ]

        # 加载上次配置
        restore.load(self.settings_frame.default_lane,
                     self.src_folder, self.dst_folder,
                     self.excel_file)

    #
    # 添加组件
    #

    def add_src_dir(self):
        tk.Label(self,
                 text='待处理图片所在文件夹：',
                 font=self.font,
                 ).grid(row=0, column=0, sticky='w', pady=(10, 0))

        self.src_folder_widget = tk.Entry(self,
                                          textvariable=self.src_folder,
                                          width=33,
                                          font=self.font,
                                          )
        self.src_folder_widget.grid(row=1, column=0, sticky='w')

        self.src_folder_button_widget = tk.Button(self,
                                                  image=self.folder_icon,
                                                  command=self.ask_src_folder,
                                                  )
        self.src_folder_button_widget.grid(
            row=1, column=1, sticky='e', padx=(0, 0))

    def add_dst_dir(self):
        tk.Label(self,
                 text='照片处理后放置文件夹：',
                 font=self.font,
                 ).grid(row=2, column=0, sticky='w', pady=(10, 0))

        self.dst_folder_widget = tk.Entry(self,
                                          textvariable=self.dst_folder,
                                          width=33,
                                          font=self.font,
                                          )
        self.dst_folder_widget.grid(row=3, column=0, sticky='w')

        self.dst_folder_button_widget = tk.Button(self,
                                                  image=self.folder_icon,
                                                  command=self.ask_dst_folder,
                                                  )

        self.dst_folder_button_widget.grid(
            row=3, column=1, sticky='e', padx=(5, 0))

    def add_excel_file(self):
        tk.Label(self,
                 text='需操作的Excel文件：',
                 font=self.font,
                 ).grid(row=4, column=0, sticky='w', pady=(10, 0))

        self.excel_file_widget = tk.Entry(self,
                                          textvariable=self.excel_file,
                                          width=33,
                                          font=self.font,
                                          )
        self.excel_file_widget.grid(row=5, column=0, sticky='w')

        self.excel_file_button_widget = tk.Button(self,
                                                  image=self.excel_icon,
                                                  command=self.ask_excel_file,
                                                  )

        self.excel_file_button_widget.grid(
            row=5, column=1, sticky='e', padx=(5, 0))

    def add_progress(self):
        tk.Label(self,
                 textvariable=self.progress_str,
                 font=(FONT['family'], FONT['size'], 'italic'),
                 ).grid(row=6, column=0, columnspan=2, pady=(10, 20))

    def add_commit_button(self):
        self.submit_button_widget = tk.Button(self,
                                              text='开始',
                                              font=(
                                                  FONT['family'], FONT['size'] + 2, 'bold'),
                                              command=self.run,
                                              )
        self.submit_button_widget.grid(
            row=7, column=0, columnspan=2, pady=(0, 30))

    #
    # UI 交互
    #

    def disable_interactive(self):
        self.settings_frame.disable_interactive()

        for widget in self.interactive_widgets:
            widget.configure(state='disabled')

    def enable_interactive(self):
        self.settings_frame.enable_interactive()

        for widget in self.interactive_widgets:
            widget.configure(state='normal')

    def ask_src_folder(self):
        dirname = filedialog.askdirectory(title='请选择待处理照片所在文件夹',
                                          )
        self.src_folder.set(dirname)

        if not self.dst_folder.get():
            self.dst_folder.set(dirname)

    def ask_dst_folder(self):
        dirname = filedialog.askdirectory(title='请选择照片处理后放置的文件夹',
                                          )
        self.dst_folder.set(dirname)

    def ask_excel_file(self):
        name = filedialog.askopenfilename(title='请选择需操作的excel文件',
                                          filetypes=(
                                              ('xlsx文件', '.xlsx'),
                                              ('all files', '*.*')),
                                          )
        self.excel_file.set(name)

    # def update_progress(self, message):
    #     self.progress_str.set(message)
    #     self.master.update_idletasks()

    #
    # 事件处理
    #

    def validate(self):
        '验证所有交互获得数据'
        # edited = validate.edited(
        #     self.settings_frame.edited,
        #     self.settings_frame.edited_widget)
        # if False is edited:
        #     return False

        default_lane = validate.default_lane(
            self.settings_frame.default_lane,
            self.settings_frame.default_lane_widget)
        if False is default_lane:
            return False

        image_files = validate.src_folder(
            self.src_folder,
            self.src_folder_widget)
        if False is image_files:
            return False

        src_folder = self.src_folder.get().strip()
        dst_folder = validate.dst_folder(
            self.dst_folder,
            src_folder,
            self.dst_folder_widget)
        if False is dst_folder:
            return False

        excel_file = validate.excel_file(
            self.excel_file,
            self.excel_file_widget)
        if False is excel_file:
            return False

        # print('edited: ', edited)
        # print('default_lane', default_lane)
        # print('src_folder中的图片数量为：', src_folder)
        # print('dst_folder路径为：', dst_folder)
        # print('excel文件路径为：', excel_file)
        return {
            # 'edited': edited,
            'default_lane': default_lane,
            'image_files': image_files,
            'src_folder': src_folder,
            'dst_folder': dst_folder,
            'excel_file': excel_file, }

    def run(self):
        infos = self.validate()
        if not infos:
            # validate.show_error('验证失败，执行结束')
            return

        # print(infos)
        #
        # 获取交互配置
        #

        # edited = infos.get('edited')
        default_lane = infos.get('default_lane')
        image_files = infos.get('image_files')
        src_folder = infos.get('src_folder')
        dst_folder = infos.get('dst_folder')
        excel_file = infos.get('excel_file')

        #
        # 为退出程序添加事件，存储配置
        #
        def on_closing():
            restore.dump(default_lane, src_folder,
                         dst_folder, excel_file)
            self.master.destroy()

        self.master.protocol('WM_DELETE_WINDOW', on_closing)

        #
        # 执行操作
        #
        self.disable_interactive()

        result = operation.main(default_lane=default_lane,
                                image_files=image_files,
                                src_folder=src_folder,
                                dst_folder=dst_folder,
                                excel_file=excel_file,
                                progress_str=self.progress_str,
                                root=self.master)

        if isinstance(result, str):
            validate.show_error(result)
            self.enable_interactive()
            return

        self.enable_interactive()

        messeagebox.showinfo(title='成功', message='操作成功')
