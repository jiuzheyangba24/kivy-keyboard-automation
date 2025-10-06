from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from kivy.uix.progressbar import ProgressBar
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import platform
import threading
import time

# 在移动端，键盘模拟功能受限，这里提供模拟实现
class MobileKeyboardController:
    def __init__(self):
        self.output_callback = None
    
    def set_output_callback(self, callback):
        """设置输出回调函数"""
        self.output_callback = callback
    
    def type_text(self, text):
        """模拟输入文本（在移动端输出到界面）"""
        if self.output_callback:
            self.output_callback(text)
    
    def press_enter(self):
        """模拟回车"""
        if self.output_callback:
            self.output_callback('\n')

class KeyboardSimulatorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard_controller = MobileKeyboardController()
        self.stop_event = threading.Event()
        self.simulation_thread = None
        self.execution_count = 0
        self.records = []
        
    def build(self):
        # 设置窗口背景色
        Window.clearcolor = (0.95, 0.97, 0.98, 1)  # 浅灰蓝背景
        
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
        
        # 标题
        title_label = Label(
            text='ikun牌键盘自动化工具',
            font_size='24sp',
            size_hint_y=None,
            height='60dp',
            color=(0.2, 0.6, 0.86, 1)  # 科技蓝
        )
        main_layout.add_widget(title_label)
        
        # 输入区域
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.4, spacing=10)
        
        input_label = Label(
            text='输入内容:',
            font_size='16sp',
            size_hint_y=None,
            height='30dp',
            halign='left'
        )
        input_label.bind(size=input_label.setter('text_size'))
        input_layout.add_widget(input_label)
        
        # 文本输入框（使用ScrollView包装以支持滚动）
        scroll = ScrollView()
        self.text_input = TextInput(
            multiline=True,
            font_size='14sp',
            background_color=(1, 1, 1, 1),
            foreground_color=(0.17, 0.24, 0.31, 1),
            cursor_color=(0.2, 0.6, 0.86, 1),
            size_hint_y=None
        )
        self.text_input.bind(minimum_height=self.text_input.setter('height'))
        scroll.add_widget(self.text_input)
        input_layout.add_widget(scroll)
        
        # 文本统计
        self.stats_label = Label(
            text='字符数: 0 | 行数: 1',
            font_size='12sp',
            size_hint_y=None,
            height='25dp',
            halign='left',
            color=(0.5, 0.55, 0.6, 1)
        )
        self.stats_label.bind(size=self.stats_label.setter('text_size'))
        self.text_input.bind(text=self.update_text_stats)
        input_layout.add_widget(self.stats_label)
        
        main_layout.add_widget(input_layout)
        
        # 参数控制区域
        params_layout = GridLayout(cols=2, size_hint_y=None, height='200dp', spacing=10)
        
        # 开始延迟
        params_layout.add_widget(Label(text='开始延迟:', font_size='14sp', halign='left'))
        delay_layout = BoxLayout(orientation='horizontal', spacing=5)
        self.delay_slider = Slider(min=0, max=20, value=3, step=0.1)
        self.delay_label = Label(text='3.0秒', font_size='12sp', size_hint_x=None, width='60dp')
        self.delay_slider.bind(value=self.update_delay_label)
        delay_layout.add_widget(self.delay_slider)
        delay_layout.add_widget(self.delay_label)
        params_layout.add_widget(delay_layout)
        
        # 字符间隔
        params_layout.add_widget(Label(text='字符间隔:', font_size='14sp', halign='left'))
        interval_layout = BoxLayout(orientation='horizontal', spacing=5)
        self.interval_slider = Slider(min=0.01, max=1, value=0.08, step=0.01)
        self.interval_label = Label(text='0.08秒', font_size='12sp', size_hint_x=None, width='60dp')
        self.interval_slider.bind(value=self.update_interval_label)
        interval_layout.add_widget(self.interval_slider)
        interval_layout.add_widget(self.interval_label)
        params_layout.add_widget(interval_layout)
        
        # 重复次数
        params_layout.add_widget(Label(text='重复次数:', font_size='14sp', halign='left'))
        self.repetition_input = TextInput(
            text='1',
            font_size='14sp',
            multiline=False,
            input_filter='int',
            size_hint_x=0.3
        )
        params_layout.add_widget(self.repetition_input)
        
        # 换行方式
        params_layout.add_widget(Label(text='换行方式:', font_size='14sp', halign='left'))
        self.newline_spinner = Spinner(
            text='Enter',
            values=['Enter', 'Shift+Enter', '双击空格', '制表符'],
            font_size='14sp'
        )
        params_layout.add_widget(self.newline_spinner)
        
        main_layout.add_widget(params_layout)
        
        # 选项区域
        options_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='40dp', spacing=20)
        
        clear_layout = BoxLayout(orientation='horizontal', size_hint_x=None, width='200dp')
        self.clear_checkbox = CheckBox(size_hint_x=None, width='30dp')
        clear_layout.add_widget(self.clear_checkbox)
        clear_layout.add_widget(Label(text='执行后清除文本', font_size='12sp'))
        options_layout.add_widget(clear_layout)
        
        main_layout.add_widget(options_layout)
        
        # 按钮区域
        button_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height='50dp', spacing=10)
        
        self.start_button = Button(
            text='开始输入',
            font_size='16sp',
            background_color=(0.2, 0.6, 0.86, 1),
            color=(1, 1, 1, 1)
        )
        self.start_button.bind(on_press=self.start_simulation)
        
        self.stop_button = Button(
            text='停止',
            font_size='16sp',
            background_color=(0.9, 0.3, 0.24, 1),
            color=(1, 1, 1, 1),
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_simulation)
        
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        
        main_layout.add_widget(button_layout)
        
        # 进度条
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height='20dp'
        )
        main_layout.add_widget(self.progress_bar)
        
        # 输出记录区域
        records_layout = BoxLayout(orientation='vertical', size_hint_y=0.3, spacing=5)
        
        records_label = Label(
            text='执行记录:',
            font_size='14sp',
            size_hint_y=None,
            height='25dp',
            halign='left'
        )
        records_label.bind(size=records_label.setter('text_size'))
        records_layout.add_widget(records_label)
        
        # 记录显示区域
        records_scroll = ScrollView()
        self.records_display = Label(
            text='等待执行...',
            font_size='12sp',
            text_size=(None, None),
            halign='left',
            valign='top',
            color=(0.3, 0.3, 0.3, 1)
        )
        records_scroll.add_widget(self.records_display)
        records_layout.add_widget(records_scroll)
        
        main_layout.add_widget(records_layout)
        
        # 设置键盘控制器的输出回调
        self.keyboard_controller.set_output_callback(self.on_simulated_output)
        
        return main_layout
    
    def update_text_stats(self, instance, text):
        """更新文本统计"""
        char_count = len(text)
        line_count = text.count('\n') + 1 if text else 1
        self.stats_label.text = f'字符数: {char_count} | 行数: {line_count}'
    
    def update_delay_label(self, instance, value):
        """更新延迟标签"""
        self.delay_label.text = f'{value:.1f}秒'
    
    def update_interval_label(self, instance, value):
        """更新间隔标签"""
        self.interval_label.text = f'{value:.2f}秒'
    
    def start_simulation(self, instance):
        """开始模拟"""
        text_content = self.text_input.text.strip()
        if not text_content:
            self.add_record('错误: 请输入要模拟的内容')
            return
        
        try:
            repetitions = int(self.repetition_input.text)
            if repetitions < 1:
                raise ValueError
        except ValueError:
            self.add_record('错误: 重复次数必须是正整数')
            return
        
        # 更新UI状态
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.stop_event.clear()
        
        # 计算总进度
        total_chars = repetitions * len(text_content)
        self.progress_bar.max = total_chars
        self.progress_bar.value = 0
        
        # 启动模拟线程
        self.simulation_thread = threading.Thread(
            target=self.simulation_worker,
            args=(text_content, repetitions),
            daemon=True
        )
        self.simulation_thread.start()
    
    def simulation_worker(self, text_content, repetitions):
        """模拟工作线程"""
        delay = self.delay_slider.value
        interval = self.interval_slider.value
        newline_mode = self.newline_spinner.text
        
        try:
            # 开始延迟
            for i in range(int(delay), 0, -1):
                if self.stop_event.is_set():
                    return
                Clock.schedule_once(lambda dt: self.add_record(f'倒计时: {i}秒'), 0)
                time.sleep(1)
            
            if self.stop_event.is_set():
                return
            
            Clock.schedule_once(lambda dt: self.add_record('开始执行模拟输入...'), 0)
            
            # 开始输入
            for rep in range(repetitions):
                if self.stop_event.is_set():
                    break
                
                for char in text_content:
                    if self.stop_event.is_set():
                        break
                    
                    if char == '\n':
                        self.handle_newline(newline_mode)
                    else:
                        self.keyboard_controller.type_text(char)
                    
                    # 更新进度
                    Clock.schedule_once(lambda dt: self.update_progress(), 0)
                    time.sleep(interval)
                
                if self.stop_event.is_set():
                    break
                
                # 记录执行结果
                self.execution_count += 1
                timestamp = time.strftime('%H:%M:%S')
                record = f'[{timestamp}] 第{self.execution_count}次执行完成'
                Clock.schedule_once(lambda dt, r=record: self.add_record(r), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_record(f'错误: {str(e)}'), 0)
        finally:
            # 清理工作
            if self.clear_checkbox.active:
                Clock.schedule_once(lambda dt: setattr(self.text_input, 'text', ''), 0)
            
            Clock.schedule_once(lambda dt: self.reset_ui_state(), 0)
    
    def handle_newline(self, mode):
        """处理换行"""
        if mode == 'Enter':
            self.keyboard_controller.press_enter()
        elif mode == 'Shift+Enter':
            self.keyboard_controller.type_text('\n')
        elif mode == '双击空格':
            self.keyboard_controller.type_text('  ')
        elif mode == '制表符':
            self.keyboard_controller.type_text('\t')
    
    def update_progress(self):
        """更新进度条"""
        self.progress_bar.value += 1
    
    def stop_simulation(self, instance):
        """停止模拟"""
        self.stop_event.set()
        self.reset_ui_state()
        self.add_record('模拟已停止')
    
    def reset_ui_state(self):
        """重置UI状态"""
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.progress_bar.value = 0
    
    def add_record(self, record):
        """添加记录"""
        self.records.append(record)
        # 只显示最近的10条记录
        recent_records = self.records[-10:]
        self.records_display.text = '\n'.join(recent_records)
        self.records_display.text_size = (self.records_display.parent.width, None)
    
    def on_simulated_output(self, text):
        """处理模拟输出（在移动端显示在记录区域）"""
        if text == '\n':
            self.add_record('执行: [回车]')
        else:
            self.add_record(f'输入: {text}')

if __name__ == '__main__':
    KeyboardSimulatorApp().run()