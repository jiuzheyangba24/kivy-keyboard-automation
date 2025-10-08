# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.clock import Clock
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
import threading
import time
import traceback
import sys

# 移动端键盘模拟器（简化版）
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
        try:
            super().__init__(**kwargs)
            self.keyboard_controller = MobileKeyboardController()
            self.keyboard_controller.set_output_callback(self.on_simulated_output)
            self.is_running = False
            self.simulation_thread = None
            self.log_messages = []
        except Exception as e:
            print(f"应用初始化错误: {e}")
            print(traceback.format_exc())
        
    def build(self):
        try:
            # 设置窗口背景色
            Window.clearcolor = get_color_from_hex('#f8f9fa')
            
            # 主容器
            main_layout = BoxLayout(orientation='vertical', padding=20, spacing=15)
            
            self.safe_log("应用界面初始化开始")
        
        # 标题
        title = Label(
            text='ikun牌键盘自动化工具',
            font_size='24sp',
            color=get_color_from_hex('#2c3e50'),
            size_hint_y=None,
            height=60
        )
        main_layout.add_widget(title)
        
        # 文本输入区域
        input_layout = BoxLayout(orientation='vertical', spacing=10)
        
        input_label = Label(
            text='输入要自动输入的文本:',
            font_size='16sp',
            color=get_color_from_hex('#34495e'),
            size_hint_y=None,
            height=30,
            halign='left'
        )
        input_label.bind(size=input_label.setter('text_size'))
        input_layout.add_widget(input_label)
        
        self.text_input = TextInput(
            multiline=True,
            hint_text='请输入要自动输入的文本...',
            font_size='14sp',
            size_hint_y=None,
            height=150
        )
        input_layout.add_widget(self.text_input)
        
        main_layout.add_widget(input_layout)
        
        # 重复次数设置
        repeat_layout = BoxLayout(orientation='horizontal', spacing=10, size_hint_y=None, height=50)
        
        repeat_label = Label(
            text='重复次数:',
            font_size='16sp',
            color=get_color_from_hex('#34495e'),
            size_hint_x=None,
            width=100
        )
        repeat_layout.add_widget(repeat_label)
        
        self.repeat_slider = Slider(
            min=1,
            max=100,
            value=1,
            step=1
        )
        repeat_layout.add_widget(self.repeat_slider)
        
        self.repeat_value_label = Label(
            text='1',
            font_size='16sp',
            color=get_color_from_hex('#3498db'),
            size_hint_x=None,
            width=50
        )
        self.repeat_slider.bind(value=self.update_repeat_label)
        repeat_layout.add_widget(self.repeat_value_label)
        
        main_layout.add_widget(repeat_layout)
        
        # 控制按钮
        button_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=None, height=60)
        
        self.start_button = Button(
            text='开始模拟',
            font_size='18sp',
            background_color=get_color_from_hex('#27ae60'),
            color=(1, 1, 1, 1)
        )
        self.start_button.bind(on_press=self.start_simulation)
        button_layout.add_widget(self.start_button)
        
        self.stop_button = Button(
            text='停止模拟',
            font_size='18sp',
            background_color=get_color_from_hex('#e74c3c'),
            color=(1, 1, 1, 1),
            disabled=True
        )
        self.stop_button.bind(on_press=self.stop_simulation)
        button_layout.add_widget(self.stop_button)
        
        main_layout.add_widget(button_layout)
        
        # 状态显示
        self.status_label = Label(
            text='状态: 就绪',
            font_size='14sp',
            color=get_color_from_hex('#7f8c8d'),
            size_hint_y=None,
            height=40
        )
        main_layout.add_widget(self.status_label)
        
        # 输出日志
        log_label = Label(
            text='输出日志:',
            font_size='16sp',
            color=get_color_from_hex('#34495e'),
            size_hint_y=None,
            height=30,
            halign='left'
        )
        log_label.bind(size=log_label.setter('text_size'))
        main_layout.add_widget(log_label)
        
        self.log_output = TextInput(
            multiline=True,
            readonly=True,
            font_size='12sp',
            size_hint_y=None,
            height=150
        )
        main_layout.add_widget(self.log_output)
        
            self.safe_log("应用界面初始化完成")
            return main_layout
        except Exception as e:
            self.safe_log(f"界面构建错误: {e}")
            print(f"界面构建错误: {e}")
            print(traceback.format_exc())
            # 返回一个简单的错误界面
            error_layout = BoxLayout(orientation='vertical')
            error_label = Label(text=f'应用启动失败: {str(e)}')
            error_layout.add_widget(error_label)
            return error_layout
    
    def update_repeat_label(self, instance, value):
        self.repeat_value_label.text = str(int(value))
    
    def start_simulation(self, instance):
        try:
            text_content = self.text_input.text.strip()
            if not text_content:
                self.safe_update_status('状态: 请输入要模拟的文本')
                return
            
            repetitions = int(self.repeat_slider.value)
            
            self.is_running = True
            self.start_button.disabled = True
            self.stop_button.disabled = False
            self.safe_update_status(f'状态: 正在模拟 (共{repetitions}次)')
            
            # 清空日志
            self.safe_clear_log()
            self.safe_log(f"开始模拟输入，文本长度: {len(text_content)}, 重复次数: {repetitions}")
            
            # 启动模拟线程
            self.simulation_thread = threading.Thread(
                target=self.simulation_worker,
                args=(text_content, repetitions)
            )
            self.simulation_thread.daemon = True
            self.simulation_thread.start()
        except Exception as e:
            self.safe_log(f"启动模拟失败: {e}")
            self.safe_update_status(f'状态: 启动失败 - {str(e)}')
            self.reset_ui_state()
    
    def simulation_worker(self, text_content, repetitions):
        try:
            self.safe_log("模拟工作线程启动")
            
            for i in range(repetitions):
                if not self.is_running:
                    self.safe_log("模拟被用户停止")
                    break
                
                try:
                    Clock.schedule_once(
                        lambda dt, msg=f'第{i+1}次模拟开始': self.safe_update_status(f'状态: {msg}')
                    )
                    
                    # 模拟输入文本
                    self.keyboard_controller.type_text(text_content)
                    
                    # 模拟按回车
                    self.keyboard_controller.press_enter()
                    
                    # 等待间隔
                    time.sleep(1)
                    
                    self.safe_log(f"完成第{i+1}次模拟")
                    
                except Exception as e:
                    self.safe_log(f"第{i+1}次模拟出错: {e}")
                    continue
            
            if self.is_running:
                Clock.schedule_once(
                    lambda dt: self.safe_update_status('状态: 模拟完成')
                )
                self.safe_log("所有模拟任务完成")
            
        except Exception as e:
            error_msg = f'模拟过程发生严重错误: {str(e)}'
            self.safe_log(error_msg)
            print(f"模拟工作线程错误: {e}")
            print(traceback.format_exc())
            Clock.schedule_once(
                lambda dt: self.safe_update_status(f'状态: 发生错误 - {str(e)}')
            )
        finally:
            Clock.schedule_once(lambda dt: self.reset_ui_state())
            self.safe_log("模拟工作线程结束")
    
    def safe_update_status(self, message):
        try:
            if hasattr(self, 'status_label') and self.status_label:
                self.status_label.text = message
        except Exception as e:
            print(f"更新状态失败: {e}")
    
    def stop_simulation(self, instance):
        try:
            self.is_running = False
            self.safe_update_status('状态: 正在停止...')
            self.safe_log("用户请求停止模拟")
        except Exception as e:
            self.safe_log(f"停止模拟时出错: {e}")
    
    def reset_ui_state(self):
        try:
            self.is_running = False
            if hasattr(self, 'start_button') and self.start_button:
                self.start_button.disabled = False
            if hasattr(self, 'stop_button') and self.stop_button:
                self.stop_button.disabled = True
            if hasattr(self, 'status_label') and self.status_label:
                if self.status_label.text.startswith('状态: 正在'):
                    self.status_label.text = '状态: 已停止'
        except Exception as e:
            print(f"重置UI状态失败: {e}")
    
    def on_simulated_output(self, text):
        try:
            Clock.schedule_once(
                lambda dt: self.safe_add_log(text)
            )
        except Exception as e:
            print(f"处理模拟输出失败: {e}")
    
    def safe_add_log(self, message):
        try:
            current_time = time.strftime('%H:%M:%S')
            log_entry = f'[{current_time}] {message}\n'
            
            if hasattr(self, 'log_output') and self.log_output:
                self.log_output.text += log_entry
                # 自动滚动到底部
                self.log_output.cursor = (len(self.log_output.text), 0)
            
            # 同时保存到内存日志
            self.log_messages.append(log_entry)
            # 限制日志条数，避免内存溢出
            if len(self.log_messages) > 1000:
                self.log_messages = self.log_messages[-500:]
                
        except Exception as e:
            print(f"添加日志失败: {e}")
    
    def safe_log(self, message):
        try:
            self.safe_add_log(message)
        except Exception as e:
            print(f"安全日志记录失败: {e}")
    
    def safe_clear_log(self):
        try:
            if hasattr(self, 'log_output') and self.log_output:
                self.log_output.text = ''
            self.log_messages = []
        except Exception as e:
            print(f"清空日志失败: {e}")

if __name__ == '__main__':
    KeyboardSimulatorApp().run()