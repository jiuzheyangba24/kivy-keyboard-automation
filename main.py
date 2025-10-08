# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.anchorlayout import AnchorLayout
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
from kivy.graphics import Color, Rectangle, Line
from kivy.core.text import LabelBase
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import threading
import time
import os

# 注册中文字体
if os.name == 'nt':  # Windows系统
    try:
        # 尝试注册微软雅黑字体
        font_path = 'C:/Windows/Fonts/msyh.ttc'
        if os.path.exists(font_path):
            LabelBase.register(name='Microsoft YaHei', fn_regular=font_path)
        else:
            # 备用字体：宋体
            font_path = 'C:/Windows/Fonts/simsun.ttc'
            if os.path.exists(font_path):
                LabelBase.register(name='Microsoft YaHei', fn_regular=font_path)
    except Exception as e:
        print(f"字体注册失败: {e}")

class LabelFrame(BoxLayout):
    """自定义LabelFrame组件，模拟ttk.LabelFrame"""
    def __init__(self, title="", **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.title = title
        
        # 标题标签
        if title:
            title_label = Label(
                text=title,
                font_name='Microsoft YaHei',
                font_size='12sp',
                color=get_color_from_hex('#3498db'),  # 科技蓝
                size_hint_y=None,
                height=dp(30),
                halign='left',
                valign='bottom'
            )
            title_label.bind(size=title_label.setter('text_size'))
            self.add_widget(title_label)
        
        # 内容容器
        self.content_layout = BoxLayout(orientation='vertical', padding=dp(10))
        
        # 绘制边框
        with self.content_layout.canvas.before:
            Color(0.835, 0.859, 0.859, 1)  # #d5dbdb 边框灰
            self.border_line = Line(width=1)
        
        self.content_layout.bind(pos=self._update_border, size=self._update_border)
        self.add_widget(self.content_layout)
    
    def _update_border(self, instance, value):
        """更新边框"""
        self.border_line.rectangle = (instance.x, instance.y, instance.width, instance.height)
    
    def add_content_widget(self, widget):
        """添加内容组件"""
        self.content_layout.add_widget(widget)

class TechSlider(Slider):
    """自定义滑动条，模拟原版ttk.Scale样式"""
    def __init__(self, **kwargs):
        # 设置默认样式参数，模拟原版ttk.Scale
        kwargs.setdefault('cursor_size', (dp(12), dp(12)))  # 更小的滑块
        kwargs.setdefault('background_width', dp(4))  # 更粗的轨道
        kwargs.setdefault('value_track_width', dp(4))
        super().__init__(**kwargs)
        
        # 设置颜色，模拟原版灰色调
        self.background_color = get_color_from_hex('#d0d0d0')  # 灰色背景轨道
        self.value_track_color = get_color_from_hex('#a0a0a0')  # 稍深的灰色值轨道
        
        # 重新绘制滑块样式
        self.bind(pos=self._update_graphics, size=self._update_graphics)
    
    def _update_graphics(self, *args):
        """更新滑块图形"""
        # 这里可以添加自定义绘制逻辑
        pass

# 在移动端，键盘模拟功能受限，这里提供模拟实现
class MobileKeyboardController:
    def __init__(self):
        self.output_callback = None
        
    def set_output_callback(self, callback):
        self.output_callback = callback
        
    def type_text(self, text):
        if self.output_callback:
            self.output_callback(f"模拟输入: {text}")
            
    def press_enter(self):
        if self.output_callback:
            self.output_callback("模拟按下回车键")

class KeyboardSimulatorApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyboard_controller = MobileKeyboardController()
        self.stop_event = threading.Event()
        self.input_thread = None
        self.execution_count = 0
        
    def build(self):
        # 设置窗口大小和背景色
        Window.size = (900, 800)
        Window.minimum_width = 850
        Window.minimum_height = 750
        Window.clearcolor = (0.96, 0.97, 0.98, 1)  # #f5f7fa 浅灰蓝背景
        
        # 启动标题动画
        self.start_title_animation()
        
        # 主布局 - 使用垂直布局匹配原版
        main_layout = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(15))
        
        # 设置背景色
        with main_layout.canvas.before:
            Color(0.96, 0.97, 0.98, 1)  # #f5f7fa 浅灰蓝背景
            self.rect = Rectangle(size=main_layout.size, pos=main_layout.pos)
        main_layout.bind(size=self._update_rect, pos=self._update_rect)
        
        # === 标题区域 ===
        title_layout = BoxLayout(orientation='vertical', size_hint_y=None, height=80, spacing=5)
        
        # 主标题
        self.title_label = Label(
            text='哎哟你干嘛~',
            font_name='Microsoft YaHei',
            font_size='20sp',
            size_hint_y=None,
            height='40dp',
            color=(0.204, 0.596, 0.859, 1),  # #3498db 科技蓝
            bold=True
        )
        title_layout.add_widget(self.title_label)
        
        # 副标题
        subtitle_label = Label(
            text='高效键盘自动化工具',
            font_name='Microsoft YaHei',
            font_size='14sp',
            size_hint_y=None,
            height='25dp',
            color=(0.498, 0.549, 0.553, 1)  # #7f8c8d 中灰
        )
        title_layout.add_widget(subtitle_label)
        
        main_layout.add_widget(title_layout)
        
        # === 输入内容区域 ===
        input_frame = LabelFrame(title='输入内容', size_hint_y=0.4)
        
        # 文本输入框（使用ScrollView包装以支持滚动）
        scroll = ScrollView()
        self.text_input = TextInput(
            multiline=True,
            font_size='12sp',
            background_color=(1, 1, 1, 1),  # 纯白背景
            foreground_color=(0.172, 0.243, 0.314, 1),  # #2c3e50 深蓝灰文字
            cursor_color=(0.204, 0.596, 0.859, 1),  # #3498db 科技蓝光标
            size_hint_y=None,
            padding=[15, 15]
        )
        self.text_input.bind(minimum_height=self.text_input.setter('height'))
        scroll.add_widget(self.text_input)
        input_frame.add_content_widget(scroll)
        
        # 文本统计
        self.stats_label = Label(
            text='字符数: 0 | 行数: 1',
            font_name='Microsoft YaHei',
            font_size='11sp',
            size_hint_y=None,
            height='25dp',
            halign='left',
            color=(0.498, 0.549, 0.553, 1)  # #7f8c8d 中灰
        )
        self.stats_label.bind(size=self.stats_label.setter('text_size'))
        self.text_input.bind(text=self.update_text_stats)
        input_frame.add_content_widget(self.stats_label)
        
        main_layout.add_widget(input_frame)
        
        # === 参数控制区域 ===
        params_frame = LabelFrame(title='参数设置', size_hint_y=None, height=200)
        
        params_grid = GridLayout(cols=3, size_hint_y=None, height=160, spacing=[12, 8])
        
        # 开始延迟
        params_grid.add_widget(Label(
            text='开始延迟:', 
            font_name='Microsoft YaHei',
            font_size='12sp',
            halign='left',
            color=(0.172, 0.243, 0.314, 1)
        ))
        
        delay_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.delay_slider = TechSlider(
             min=0, max=20, value=3.0, step=0.1
         )
        self.delay_label = Label(
            text='3.00秒', 
            font_name='Microsoft YaHei',
            font_size='11sp', 
            size_hint_x=None, 
            width='60dp',
            color=(0.204, 0.596, 0.859, 1)  # #3498db 科技蓝
        )
        self.delay_slider.bind(value=self.update_delay_label)
        delay_layout.add_widget(self.delay_slider)
        delay_layout.add_widget(self.delay_label)
        params_grid.add_widget(delay_layout)
        params_grid.add_widget(Label())  # 占位符
        
        # 字符间隔
        params_grid.add_widget(Label(
            text='字符间隔:', 
            font_name='Microsoft YaHei',
            font_size='12sp',
            halign='left',
            color=(0.172, 0.243, 0.314, 1)
        ))
        
        interval_layout = BoxLayout(orientation='horizontal', spacing=10)
        self.interval_slider = TechSlider(
             min=0.01, max=1, value=0.08, step=0.01
         )
        self.interval_label = Label(
            text='0.08秒', 
            font_name='Microsoft YaHei',
            font_size='11sp', 
            size_hint_x=None, 
            width='60dp',
            color=(0.204, 0.596, 0.859, 1)  # #3498db 科技蓝
        )
        self.interval_slider.bind(value=self.update_interval_label)
        interval_layout.add_widget(self.interval_slider)
        interval_layout.add_widget(self.interval_label)
        params_grid.add_widget(interval_layout)
        params_grid.add_widget(Label())  # 占位符
        
        # 重复次数
        params_grid.add_widget(Label(
            text='重复次数:', 
            font_name='Microsoft YaHei',
            font_size='12sp',
            halign='left',
            color=(0.172, 0.243, 0.314, 1)
        ))
        
        self.repetition_input = TextInput(
            text='1',
            font_size='12sp',
            multiline=False,
            input_filter='int',
            size_hint_x=0.3,
            background_color=(1, 1, 1, 1),
            foreground_color=(0.172, 0.243, 0.314, 1)
        )
        params_grid.add_widget(self.repetition_input)
        params_grid.add_widget(Label())  # 占位符
        
        # 换行方式
        params_grid.add_widget(Label(
            text='换行方式:', 
            font_name='Microsoft YaHei',
            font_size='12sp',
            halign='left',
            color=(0.172, 0.243, 0.314, 1)
        ))
        
        self.newline_spinner = Spinner(
            text='Enter',
            values=['Enter', 'Shift+Enter', 'Shift+Tab x10', 'Home x2'],
            font_size='12sp',
            background_color=(1, 1, 1, 1),
            color=(0.172, 0.243, 0.314, 1)
        )
        params_grid.add_widget(self.newline_spinner)
        params_grid.add_widget(Label())  # 占位符
        
        params_frame.add_content_widget(params_grid)
        main_layout.add_widget(params_frame)
        
        # === 执行记录区域 ===
        records_frame = LabelFrame(title='执行记录', size_hint_y=0.3)
        
        # 记录显示区域
        records_scroll = ScrollView()
        self.records_display = Label(
            text='等待执行...',
            font_name='Microsoft YaHei',
            font_size='11sp',
            halign='left',
            valign='top',
            color=(0.172, 0.243, 0.314, 1),  # #2c3e50 深蓝灰
            markup=True
        )
        self.records_display.bind(size=self.records_display.setter('text_size'))
        records_scroll.add_widget(self.records_display)
        records_frame.add_content_widget(records_scroll)
        
        main_layout.add_widget(records_frame)
        
        # === 控制按钮和选项区域 ===
        control_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50, spacing=20)
        
        # 左侧选项
        options_layout = BoxLayout(orientation='horizontal', size_hint_x=0.6, spacing=20)
        
        topmost_layout = BoxLayout(orientation='horizontal', size_hint_x=None, width=120, spacing=5)
        self.topmost_checkbox = CheckBox(size_hint_x=None, width=30, active=False)
        topmost_layout.add_widget(self.topmost_checkbox)
        topmost_layout.add_widget(Label(
            text='窗口置顶', 
            font_name='Microsoft YaHei',
            font_size='11sp',
            color=(0.498, 0.549, 0.553, 1)  # #7f8c8d 中灰
        ))
        options_layout.add_widget(topmost_layout)
        
        clear_layout = BoxLayout(orientation='horizontal', size_hint_x=None, width=150, spacing=5)
        self.clear_checkbox = CheckBox(size_hint_x=None, width=30, active=False)
        clear_layout.add_widget(self.clear_checkbox)
        clear_layout.add_widget(Label(
            text='执行后清除文本', 
            font_name='Microsoft YaHei',
            font_size='11sp',
            color=(0.498, 0.549, 0.553, 1)  # #7f8c8d 中灰
        ))
        options_layout.add_widget(clear_layout)
        
        control_layout.add_widget(options_layout)
        
        # 右侧按钮组
        button_layout = BoxLayout(orientation='horizontal', size_hint_x=0.4, spacing=10)
        
        self.start_button = Button(
            text='开始输入 (F5)',
            font_name='Microsoft YaHei',
            font_size='14sp',
            background_color=(0.204, 0.596, 0.859, 1),  # #3498db 科技蓝
            color=(1, 1, 1, 1)
        )
        self.start_button.bind(on_press=self.start_simulation)
        
        self.stop_button = Button(
            text='停止 (F6)',
            font_name='Microsoft YaHei',
            font_size='14sp',
            background_color=(0.831, 0.835, 0.839, 1),  # #d5dbdb 边框灰（禁用状态）
            color=(0.498, 0.549, 0.553, 1),  # #7f8c8d 中灰
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_simulation)
        
        self.save_button = Button(
            text='保存记录',
            font_name='Microsoft YaHei',
            font_size='14sp',
            background_color=(0.172, 0.243, 0.314, 1),  # #2c3e50 深蓝灰
            color=(1, 1, 1, 1)
        )
        self.save_button.bind(on_press=self.save_records)
        
        button_layout.add_widget(self.start_button)
        button_layout.add_widget(self.stop_button)
        button_layout.add_widget(self.save_button)
        
        control_layout.add_widget(button_layout)
        main_layout.add_widget(control_layout)
        
        # === 进度条 ===
        self.progress_bar = ProgressBar(
            max=100,
            value=0,
            size_hint_y=None,
            height='20dp'
        )
        main_layout.add_widget(self.progress_bar)
        
        # 设置键盘控制器的输出回调
        self.keyboard_controller.set_output_callback(self.on_simulated_output)
        
        return main_layout
    
    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
    
    def update_text_stats(self, instance, text):
        char_count = len(text)
        line_count = text.count('\n') + 1 if text else 1
        self.stats_label.text = f'字符数: {char_count} | 行数: {line_count}'
    
    def update_delay_label(self, instance, value):
        self.delay_label.text = f'{value:.2f}秒'
    
    def update_interval_label(self, instance, value):
        self.interval_label.text = f'{value:.2f}秒'
    
    def start_simulation(self, instance):
        text_content = self.text_input.text.strip()
        if not text_content:
            self.add_record("[错误] 请输入要模拟的文本内容")
            return
        
        try:
            repetitions = int(self.repetition_input.text) if self.repetition_input.text else 1
            if repetitions <= 0:
                raise ValueError("重复次数必须大于0")
        except ValueError as e:
            self.add_record(f"[错误] 重复次数设置无效: {e}")
            return
        
        # 重置停止事件
        self.stop_event.clear()
        
        # 更新UI状态
        self.start_button.disabled = True
        self.stop_button.disabled = False
        self.stop_button.background_color = (0.906, 0.298, 0.235, 1)  # #e74c3c 错误红
        
        # 启动模拟线程
        self.input_thread = threading.Thread(
            target=self.simulation_worker,
            args=(text_content, repetitions)
        )
        self.input_thread.daemon = True
        self.input_thread.start()
        
        self.add_record(f"[开始] 准备输入 {len(text_content)} 个字符，重复 {repetitions} 次")
    
    def simulation_worker(self, text_content, repetitions):
        try:
            delay = self.delay_slider.value
            interval = self.interval_slider.value
            newline_mode = self.newline_spinner.text
            
            # 开始延迟
            if delay > 0:
                Clock.schedule_once(lambda dt: self.add_record(f"[延迟] 等待 {delay:.2f} 秒后开始..."), 0)
                for i in range(int(delay * 10)):
                    if self.stop_event.is_set():
                        return
                    time.sleep(0.1)
            
            total_chars = len(text_content) * repetitions
            processed_chars = 0
            
            for rep in range(repetitions):
                if self.stop_event.is_set():
                    break
                
                Clock.schedule_once(
                    lambda dt, r=rep+1: self.add_record(f"[执行] 第 {r} 次重复开始"), 0
                )
                
                for char in text_content:
                    if self.stop_event.is_set():
                        break
                    
                    if char == '\n':
                        self.handle_newline(newline_mode)
                    else:
                        self.keyboard_controller.type_text(char)
                    
                    processed_chars += 1
                    progress = (processed_chars / total_chars) * 100
                    Clock.schedule_once(lambda dt, p=progress: setattr(self.progress_bar, 'value', p), 0)
                    
                    if interval > 0:
                        time.sleep(interval)
                
                # 每次重复后的换行
                if rep < repetitions - 1:  # 不是最后一次重复
                    self.handle_newline(newline_mode)
            
            if not self.stop_event.is_set():
                Clock.schedule_once(lambda dt: self.add_record(f"[完成] 成功输入 {processed_chars} 个字符"), 0)
                
                # 如果选择了清除文本
                if self.clear_checkbox.active:
                    Clock.schedule_once(lambda dt: setattr(self.text_input, 'text', ''), 0)
                    Clock.schedule_once(lambda dt: self.add_record("[清理] 已清除输入文本"), 0)
            
        except Exception as e:
            Clock.schedule_once(lambda dt: self.add_record(f"[错误] 执行过程中出现异常: {e}"), 0)
        finally:
            Clock.schedule_once(lambda dt: self.reset_ui_state(), 0)
    
    def handle_newline(self, mode):
        if mode == "Enter":
            self.keyboard_controller.press_enter()
        elif mode == "Shift+Enter":
            self.keyboard_controller.type_text("\n")
        elif mode == "Shift+Tab x10":
            for _ in range(10):
                self.keyboard_controller.type_text("\t")
        elif mode == "Home x2":
            self.keyboard_controller.type_text("\n\n")
    
    def update_progress(self):
        # 进度更新逻辑
        pass
    
    def stop_simulation(self, instance):
        self.stop_event.set()
        self.add_record("[停止] 用户手动停止了模拟")
        self.reset_ui_state()
    
    def reset_ui_state(self):
        self.start_button.disabled = False
        self.stop_button.disabled = True
        self.stop_button.background_color = (0.831, 0.835, 0.839, 1)  # #d5dbdb 边框灰
        self.progress_bar.value = 0
    
    def add_record(self, record):
        current_time = time.strftime("%H:%M:%S")
        new_record = f"[{current_time}] {record}\n"
        self.records_display.text += new_record
    
    def save_records(self, instance):
        # 模拟保存记录功能
        self.add_record("[保存] 记录已保存到本地")
    
    def on_simulated_output(self, text):
        # 处理模拟输出
        pass
    
    def start_title_animation(self):
        """启动标题动画"""
        self.title_colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
        self.current_color_index = 0
        self.title_animation_event = Clock.schedule_interval(self.animate_title, 0.8)
    
    def animate_title(self, dt):
        """标题动画效果"""
        from kivy.utils import get_color_from_hex
        color = self.title_colors[self.current_color_index]
        self.title_label.color = get_color_from_hex(color)
        self.current_color_index = (self.current_color_index + 1) % len(self.title_colors)
        return True
    
    def stop_title_animation(self):
        """停止标题动画"""
        if hasattr(self, 'title_animation_event') and self.title_animation_event:
            self.title_animation_event.cancel()
            self.title_animation_event = None

if __name__ == '__main__':
    KeyboardSimulatorApp().run()