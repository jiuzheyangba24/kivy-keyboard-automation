import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog, ttk
from pynput.keyboard import Controller, Key
import time
import threading
import sys
import os

class TechKeyboardSimulator:
    def __init__(self, window):
        self.window = window
        self.window.title('ikun牌高效键盘自动化工具')
        self.window.geometry('900x800')
        self.window.minsize(850, 750)
        
        # 简约科技感色彩系统
        self.colors = {
            "primary_bg": "#f5f7fa",        # 浅灰蓝背景
            "secondary_bg": "#ffffff",      # 纯白
            "accent_primary": "#3498db",    # 科技蓝
            "accent_secondary": "#2c3e50",  # 深蓝灰
            "text_primary": "#2c3e50",      # 深灰蓝
            "text_secondary": "#7f8c8d",    # 中灰
            "success": "#27ae60",           # 成功绿
            "warning": "#f39c12",           # 警告橙
            "error": "#e74c3c",             # 错误红
            "border": "#d5dbdb"             # 边框灰
        }
        
        # 简约字体系统
        self.fonts = {
            "title": ("微软雅黑", 16, "bold"),
            "subtitle": ("微软雅黑", 12),
            "body": ("微软雅黑", 10),
            "caption": ("微软雅黑", 9),
            "monospace": ("Consolas", 10)
        }
        
        self.window.configure(bg=self.colors["primary_bg"])
        self.window.option_add('*TCombobox*Listbox.background', self.colors["secondary_bg"])
        self.window.option_add('*TCombobox*Listbox.foreground', self.colors["text_primary"])
        self.window.option_add('*TCombobox*Listbox.font', self.fonts["body"])
        
        # 初始化变量
        self.records = []
        self.stop_event = threading.Event()
        self.input_thread = None
        self.execution_count = 0
        self.title_blink_id = None
        
        # 构建UI
        self._setup_tech_styles()
        self._create_tech_interface()
        self._setup_keyboard_shortcuts()
        self._setup_title_animation()
        
    def _setup_tech_styles(self):
        """配置简约科技风格的ttk样式"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # 基础框架样式
        style.configure('TFrame', background=self.colors["primary_bg"])
        style.configure('TLabel', 
                       background=self.colors["primary_bg"],
                       foreground=self.colors["text_primary"],
                       font=self.fonts["body"])
        
        # 简约风格的标签框架
        style.configure('Tech.TLabelframe',
                       background=self.colors["primary_bg"],
                       borderwidth=1,
                       relief="solid",
                       bordercolor=self.colors["border"])
        style.configure('Tech.TLabelframe.Label',
                       background=self.colors["primary_bg"],
                       foreground=self.colors["accent_primary"],
                       font=self.fonts["subtitle"],
                       padding=(10, 5))
        
        # 简约按钮样式
        style.configure('Tech.TButton',
                       background=self.colors["secondary_bg"],
                       foreground=self.colors["accent_primary"],
                       borderwidth=1,
                       relief="flat",
                       font=self.fonts["body"],
                       padding=(10, 5))
        style.map('Tech.TButton',
                 background=[('active', self.colors["accent_primary"]),
                           ('pressed', '#2980b9')],
                 foreground=[('active', self.colors["secondary_bg"])])
        
        # 主要操作按钮样式
        style.configure('Primary.TButton',
                       background=self.colors["accent_primary"],
                       foreground=self.colors["secondary_bg"],
                       borderwidth=0,
                       font=self.fonts["body"],
                       padding=(12, 6))
        style.map('Primary.TButton',
                 background=[('active', '#2980b9'),
                           ('pressed', '#1c638e')])
        
        # 进度条样式
        style.configure('Tech.Horizontal.TProgressbar',
                       troughcolor=self.colors["secondary_bg"],
                       background=self.colors["accent_primary"],
                       borderwidth=0)
        
    def _create_tech_interface(self):
        """创建简约科技风格的界面"""
        # 主容器
        main_container = ttk.Frame(self.window, padding=(0, 0))
        main_container.pack(expand=True, fill=tk.BOTH, padx=20, pady=15)
        
        # 配置网格权重
        main_container.columnconfigure(0, weight=1)
        main_container.rowconfigure(1, weight=3)  # 输入区
        main_container.rowconfigure(3, weight=2)  # 记录区
        
        # === 标题区域 ===
        self.title_frame = ttk.Frame(main_container)
        self.title_frame.grid(row=0, column=0, sticky="ew", pady=(0, 15))
        
        # 主标题
        self.title_label = tk.Label(self.title_frame,
                              text="哎哟你干嘛~",
                              font=self.fonts["title"],
                              fg=self.colors["accent_primary"],
                              bg=self.colors["primary_bg"])
        self.title_label.pack()
        
        # 副标题
        subtitle_label = tk.Label(self.title_frame,
                                 text="高效键盘自动化工具",
                                 font=self.fonts["subtitle"],
                                 fg=self.colors["text_secondary"],
                                 bg=self.colors["primary_bg"])
        subtitle_label.pack()
        
        # === 输入内容区域 ===
        input_frame = ttk.LabelFrame(main_container, text="输入内容", style="Tech.TLabelframe")
        input_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 15))
        input_frame.columnconfigure(0, weight=1)
        input_frame.rowconfigure(0, weight=1)
        
        # 创建简约风格的文本区域
        self.text_area = scrolledtext.ScrolledText(
            input_frame,
            wrap=tk.WORD,
            font=self.fonts["monospace"],
            bg=self.colors["secondary_bg"],
            fg=self.colors["text_primary"],
            insertbackground=self.colors["accent_primary"],
            selectbackground=self.colors["accent_secondary"],
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=15
        )
        self.text_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # 文本统计
        self.text_stats = tk.Label(input_frame,
                                  text="字符数: 0 | 行数: 1",
                                  font=self.fonts["caption"],
                                  fg=self.colors["text_secondary"],
                                  bg=self.colors["secondary_bg"])
        self.text_stats.grid(row=1, column=0, sticky="w", padx=20, pady=(0, 10))
        self.text_area.bind('<KeyRelease>', self._update_text_stats)
        
        # === 参数控制区域 ===
        control_frame = ttk.LabelFrame(main_container, text="参数设置", style="Tech.TLabelframe")
        control_frame.grid(row=2, column=0, sticky="ew", pady=10)
        control_frame.columnconfigure(1, weight=3)
        
        # 使用网格布局参数控件
        label_grid_config = {'padx': 12, 'pady': 8, 'sticky': 'w'}
        control_grid_config = {'padx': 12, 'pady': 8, 'sticky': 'ew'}
        
        # 第一行：延迟设置
        ttk.Label(control_frame, text="开始延迟:", font=self.fonts["body"]).grid(
            row=0, column=0, **label_grid_config)
        
        self.delay_var = tk.DoubleVar(value=3.0)
        self.delay_scale = ttk.Scale(control_frame, from_=0, to=20, 
                                   orient=tk.HORIZONTAL, variable=self.delay_var,
                                   command=self._update_parameter_display)
        self.delay_scale.grid(row=0, column=1, **control_grid_config)
        
        self.delay_label = tk.Label(control_frame, text="3.00秒", 
                                   font=self.fonts["caption"],
                                   fg=self.colors["accent_primary"],
                                   bg=self.colors["primary_bg"])
        self.delay_label.grid(row=0, column=2, sticky="w", padx=(0, 12))
        
        # 第二行：间隔设置
        ttk.Label(control_frame, text="字符间隔:", font=self.fonts["body"]).grid(
            row=1, column=0, **label_grid_config)
        
        self.interval_var = tk.DoubleVar(value=0.08)
        self.interval_scale = ttk.Scale(control_frame, from_=0.01, to=1, 
                                      orient=tk.HORIZONTAL, variable=self.interval_var,
                                      command=self._update_parameter_display)
        self.interval_scale.grid(row=1, column=1, **control_grid_config)
        
        self.interval_label = tk.Label(control_frame, text="0.08秒", 
                                      font=self.fonts["caption"],
                                      fg=self.colors["accent_primary"],
                                      bg=self.colors["primary_bg"])
        self.interval_label.grid(row=1, column=2, sticky="w", padx=(0, 12))
        
        # 第三行：重复次数
        ttk.Label(control_frame, text="重复次数:", font=self.fonts["body"]).grid(
            row=2, column=0, **label_grid_config)
        
        self.repetition_var = tk.StringVar(value="1")
        self.repetition_entry = ttk.Entry(control_frame, 
                                         textvariable=self.repetition_var,
                                         font=self.fonts["body"],
                                         validate="key")
        self.repetition_entry.configure(validatecommand=(
            self.window.register(self._validate_integer), '%P'))
        self.repetition_entry.grid(row=2, column=1, sticky="w", padx=12, pady=8)
        
        # 第四行：换行方式
        ttk.Label(control_frame, text="换行方式:", font=self.fonts["body"]).grid(
            row=3, column=0, **label_grid_config)
        
        self.newline_var = tk.StringVar(value="Enter")
        newline_options = ["Enter", "Shift+Enter", "Shift+Tab x10", "Home x2"]
        self.newline_combo = ttk.Combobox(control_frame, 
                                         textvariable=self.newline_var,
                                         values=newline_options,
                                         state="readonly",
                                         font=self.fonts["body"])
        self.newline_combo.grid(row=3, column=1, sticky="ew", padx=12, pady=8)
        
        # === 输出记录区域 ===
        records_frame = ttk.LabelFrame(main_container, text="执行记录", style="Tech.TLabelframe")
        records_frame.grid(row=3, column=0, sticky="nsew", pady=(10, 0))
        records_frame.columnconfigure(0, weight=1)
        records_frame.rowconfigure(0, weight=1)
        
        self.records_area = scrolledtext.ScrolledText(
            records_frame,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=self.fonts["monospace"],
            bg=self.colors["secondary_bg"],
            fg=self.colors["text_primary"],
            relief="solid",
            borderwidth=1,
            padx=15,
            pady=15
        )
        self.records_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        
        # === 控制按钮区域 ===
        button_frame = ttk.Frame(main_container)
        button_frame.grid(row=4, column=0, sticky="ew", pady=(15, 0))
        
        # 左侧选项
        options_frame = ttk.Frame(button_frame)
        options_frame.pack(side=tk.LEFT, fill=tk.X)
        
        self.topmost_var = tk.BooleanVar()
        topmost_check = tk.Checkbutton(options_frame,
                                      text='窗口置顶',
                                      variable=self.topmost_var,
                                      command=self._toggle_topmost,
                                      font=self.fonts["caption"],
                                      fg=self.colors["text_secondary"],
                                      bg=self.colors["primary_bg"],
                                      selectcolor=self.colors["secondary_bg"],
                                      activebackground=self.colors["primary_bg"],
                                      activeforeground=self.colors["text_primary"])
        topmost_check.pack(side=tk.LEFT, padx=(0, 15))
        
        self.clear_text_var = tk.BooleanVar()
        clear_check = tk.Checkbutton(options_frame,
                                    text='执行后清除文本',
                                    variable=self.clear_text_var,
                                    font=self.fonts["caption"],
                                    fg=self.colors["text_secondary"],
                                    bg=self.colors["primary_bg"],
                                    selectcolor=self.colors["secondary_bg"],
                                    activebackground=self.colors["primary_bg"],
                                    activeforeground=self.colors["text_primary"])
        clear_check.pack(side=tk.LEFT)
        
        # 右侧按钮组
        action_frame = ttk.Frame(button_frame)
        action_frame.pack(side=tk.RIGHT)
        
        self.start_btn = ttk.Button(action_frame,
                                   text='开始输入 (F5)',
                                   command=self.start_simulation,
                                   style="Primary.TButton")
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = ttk.Button(action_frame,
                                  text='停止 (F6)',
                                  command=self.stop_simulation,
                                  style="Tech.TButton",
                                  state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.save_btn = ttk.Button(action_frame,
                                  text='保存记录',
                                  command=self.save_records,
                                  style="Tech.TButton")
        self.save_btn.pack(side=tk.LEFT, padx=5)
        
        # === 进度条区域 ===
        self.progress = ttk.Progressbar(main_container,
                                       orient=tk.HORIZONTAL,
                                       mode='determinate',
                                       style="Tech.Horizontal.TProgressbar")
        self.progress.grid(row=5, column=0, sticky="ew", pady=(15, 0))
        
        # 初始化参数显示
        self._update_parameter_display()
        
    def _setup_keyboard_shortcuts(self):
        """设置键盘快捷键"""
        self.window.bind('<F5>', lambda e: self.start_simulation())
        self.window.bind('<F6>', lambda e: self.stop_simulation())
        self.window.bind('<Control-s>', lambda e: self.save_records())
        
    def _setup_title_animation(self):
        """设置标题动态闪烁效果"""
        self.title_colors = [self.colors["accent_primary"], "#e74c3c", "#f39c12", "#27ae60"]
        self.current_color_index = 0
        self._animate_title()
        
    def _animate_title(self):
        """标题闪烁动画"""
        if self.title_label.winfo_exists():
            # 更新标题颜色
            new_color = self.title_colors[self.current_color_index]
            self.title_label.config(fg=new_color)
            
            # 更新索引
            self.current_color_index = (self.current_color_index + 1) % len(self.title_colors)
            
            # 设置下一次动画
            self.title_blink_id = self.window.after(800, self._animate_title)
    
    def _stop_title_animation(self):
        """停止标题动画"""
        if self.title_blink_id:
            self.window.after_cancel(self.title_blink_id)
            self.title_blink_id = None
    
    def _validate_integer(self, value):
        """验证输入是否为有效整数"""
        if value == "" or (value.isdigit() and int(value) > 0):
            return True
        return False
    
    def _update_text_stats(self, event=None):
        """更新文本统计信息"""
        content = self.text_area.get('1.0', 'end-1c')
        char_count = len(content)
        line_count = content.count('\n') + 1
        self.text_stats.config(text=f"字符数: {char_count} | 行数: {line_count}")
    
    def _update_parameter_display(self, event=None):
        """更新参数显示"""
        delay = self.delay_var.get()
        interval = self.interval_var.get()
        self.delay_label.config(text=f"{delay:.2f}秒")
        self.interval_label.config(text=f"{interval:.2f}秒")
    
    def _toggle_topmost(self):
        """切换窗口置顶状态"""
        self.window.attributes("-topmost", self.topmost_var.get())
    
    def start_simulation(self):
        """开始模拟输入"""
        try:
            repetitions = int(self.repetition_var.get())
            if repetitions < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("输入错误", "重复次数必须是一个正整数。")
            return
        
        text_content = self.text_area.get('1.0', 'end-1c').strip()
        if not text_content:
            messagebox.showwarning("输入警告", "请输入要模拟的内容。")
            return
        
        self.stop_event.clear()
        self._set_ui_state(True)
        
        # 计算总进度
        total_chars = repetitions * len(text_content)
        self.progress['maximum'] = total_chars
        self.progress['value'] = 0
        
        # 启动模拟线程
        self.input_thread = threading.Thread(
            target=self._simulation_worker,
            args=(text_content, repetitions),
            daemon=True
        )
        self.input_thread.start()
    
    def _simulation_worker(self, text_content, repetitions):
        """模拟输入工作线程"""
        keyboard = Controller()
        delay = self.delay_var.get()
        interval = self.interval_var.get()
        newline_mode = self.newline_var.get()
        
        def handle_newline():
            """处理不同的换行方式"""
            if newline_mode == "Enter":
                keyboard.tap(Key.enter)
            elif newline_mode == "Shift+Enter":
                with keyboard.pressed(Key.shift):
                    keyboard.tap(Key.enter)
            elif newline_mode == "Shift+Tab x10":
                keyboard.tap(Key.enter)
                time.sleep(interval)
                for _ in range(10):
                    if self.stop_event.is_set():
                        break
                    with keyboard.pressed(Key.shift):
                        keyboard.tap(Key.tab)
                    time.sleep(interval)
            elif newline_mode == "Home x2":
                keyboard.tap(Key.enter)
                time.sleep(interval)
                for _ in range(2):
                    if self.stop_event.is_set():
                        break
                    keyboard.tap(Key.home)
                    time.sleep(interval)
        
        try:
            # 开始延迟倒计时
            for i in range(int(delay), 0, -1):
                if self.stop_event.is_set():
                    break
                time.sleep(1)
            
            if self.stop_event.is_set():
                return
            
            # 开始输入
            for rep in range(repetitions):
                if self.stop_event.is_set():
                    break
                
                for char in text_content:
                    if self.stop_event.is_set():
                        break
                    
                    if char == '\n':
                        handle_newline()
                    else:
                        keyboard.type(char)
                    
                    # 更新进度
                    self.window.after(0, lambda: self.progress.step(1))
                    time.sleep(interval)
                
                if self.stop_event.is_set():
                    break
                
                # 记录执行结果
                self.execution_count += 1
                timestamp = time.strftime('%H:%M:%S')
                record = f"[{timestamp}] 第{self.execution_count}次执行完成"
                self.records.append(record)
                self.window.after(0, self._add_record, record)
                
        except Exception as e:
            self.window.after(0, lambda: messagebox.showerror("错误", f"执行过程中发生错误: {str(e)}"))
        finally:
            # 清理工作
            if self.clear_text_var.get():
                self.window.after(0, lambda: self.text_area.delete('1.0', 'end'))
            
            self.window.after(0, self._set_ui_state, False)
    
    def stop_simulation(self):
        """停止模拟"""
        self.stop_event.set()
        self._set_ui_state(False)
        messagebox.showinfo("已停止", "模拟输入任务已终止。")
    
    def _set_ui_state(self, running):
        """设置UI状态"""
        state = tk.DISABLED if running else tk.NORMAL
        self.start_btn.config(state=state)
        self.stop_btn.config(state=tk.NORMAL if running else tk.DISABLED)
        
        if not running:
            self.progress['value'] = 0
    
    def _add_record(self, record):
        """添加记录到记录区域"""
        self.records_area.config(state=tk.NORMAL)
        self.records_area.insert('end', record + '\n')
        self.records_area.see('end')
        self.records_area.config(state=tk.DISABLED)
    
    def save_records(self):
        """保存记录到文件"""
        if not self.records:
            messagebox.showwarning("无记录", "当前没有可保存的记录。")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension='.txt',
            filetypes=[('文本文件', '*.txt'), ('所有文件', '*.*')],
            title='保存执行记录'
        )
        
        if file_path:
            try:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write('\n'.join(self.records))
                messagebox.showinfo("保存成功", f"记录已保存到:\n{file_path}")
            except Exception as e:
                messagebox.showerror("保存失败", f"保存文件时出错:\n{str(e)}")
    
    def __del__(self):
        """析构函数，确保动画停止"""
        self._stop_title_animation()

def main():
    """主函数"""
    window = tk.Tk()
    app = TechKeyboardSimulator(window)
    
    # 窗口居中显示
    window.update_idletasks()
    width = window.winfo_width()
    height = window.winfo_height()
    x = (window.winfo_screenwidth() // 2) - (width // 2)
    y = (window.winfo_screenheight() // 2) - (height // 2)
    window.geometry(f'+{x}+{y}')
    
    try:
        window.mainloop()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    finally:
        # 确保动画停止
        app._stop_title_animation()

if __name__ == "__main__":
    main()
