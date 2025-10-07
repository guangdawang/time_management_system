# [file name]: gui_main.py
import PySimpleGUI as sg
import sys
import os
from datetime import datetime
from auth.user_manager import UserManager
from core.task_manager import TaskManager
from core.models import Task

# 设置主题
sg.theme('LightBlue2')

class TimeManagementGUI:
    def __init__(self):
        self.user_manager = UserManager()
        self.current_user = None
        self.current_session = None
        self.task_manager = None
        
    def login_window(self):
        """登录窗口"""
        layout = [
            [sg.Text('时间管理系统', font=('Arial', 20), justification='center')],
            [sg.Text('用户名:'), sg.InputText(key='-USERNAME-', size=(20, 1))],
            [sg.Text('密码:'), sg.InputText(key='-PASSWORD-', password_char='*', size=(20, 1))],
            [sg.Button('登录'), sg.Button('注册'), sg.Button('退出')],
            [sg.Text('', key='-LOGIN-MSG-', text_color='red')]
        ]
        
        window = sg.Window('登录', layout, element_justification='c')
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '退出'):
                window.close()
                return False
                
            elif event == '登录':
                username = values['-USERNAME-'].strip()
                password = values['-PASSWORD-']
                
                if not username or not password:
                    window['-LOGIN-MSG-'].update('用户名和密码不能为空')
                    continue
                    
                result = self.user_manager.login(username, password)
                if result:
                    self.current_session = result["token"]
                    self.current_user = result["user"]
                    self.task_manager = TaskManager(self.current_user.user_id)
                    window.close()
                    return True
                else:
                    window['-LOGIN-MSG-'].update('登录失败！用户名或密码错误')
                    
            elif event == '注册':
                window.close()
                if self.register_window():
                    return self.login_window()
                    
        return False
    
    def register_window(self):
        """注册窗口"""
        layout = [
            [sg.Text('用户注册', font=('Arial', 16))],
            [sg.Text('用户名 (至少3字符):'), sg.InputText(key='-USERNAME-', size=(20, 1))],
            [sg.Text('密码 (至少6字符):'), sg.InputText(key='-PASSWORD-', password_char='*', size=(20, 1))],
            [sg.Text('确认密码:'), sg.InputText(key='-CONFIRM-', password_char='*', size=(20, 1))],
            [sg.Button('注册'), sg.Button('返回')],
            [sg.Text('', key='-REGISTER-MSG-', text_color='red')]
        ]
        
        window = sg.Window('注册', layout, element_justification='c')
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '返回'):
                window.close()
                return False
                
            elif event == '注册':
                username = values['-USERNAME-'].strip()
                password = values['-PASSWORD-']
                confirm = values['-CONFIRM-']
                
                if not username or not password:
                    window['-REGISTER-MSG-'].update('用户名和密码不能为空')
                    continue
                    
                if len(username) < 3:
                    window['-REGISTER-MSG-'].update('用户名至少3个字符')
                    continue
                    
                if len(password) < 6:
                    window['-REGISTER-MSG-'].update('密码至少6个字符')
                    continue
                    
                if password != confirm:
                    window['-REGISTER-MSG-'].update('两次输入的密码不一致')
                    continue
                    
                if self.user_manager.register(username, password):
                    window['-REGISTER-MSG-'].update('注册成功！请登录', text_color='green')
                    window.close()
                    return True
                else:
                    window['-REGISTER-MSG-'].update('注册失败！用户名已存在')
                    
        return False
    
    def main_window(self):
        """主窗口"""
        # 创建菜单
        menu_def = [
            ['任务', ['添加任务', '编辑任务', '删除任务', '标记状态']],
            ['查看', ['所有任务', '待办任务', '进行中', '已完成']],
            ['统计', ['任务统计']],
            ['帮助', ['关于']]
        ]
        
        # 任务列表列定义
        headers = ['选择', '标题', '状态', '优先级', '截止日期', '预估时间']
        
        layout = [
            [sg.Menu(menu_def)],
            [sg.Text(f'欢迎, {self.current_user.username}', font=('Arial', 14))],
            [sg.Table(values=[], headings=headers, 
                     auto_size_columns=False,
                     justification='left',
                     num_rows=15,
                     key='-TASK-TABLE-',
                     enable_events=True,
                     col_widths=[5, 25, 10, 10, 12, 10])],
            [sg.Button('刷新'), sg.Button('添加任务'), sg.Button('编辑任务'), 
             sg.Button('标记状态'), sg.Button('删除任务'), sg.Button('统计'), sg.Button('退出')]
        ]
        
        window = sg.Window('时间管理系统', layout, finalize=True)
        self.refresh_task_table(window)
        
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '退出'):
                break
                
            elif event == '刷新':
                self.refresh_task_table(window)
                
            elif event in ('添加任务', '任务::添加任务'):
                if self.add_task_window():
                    self.refresh_task_table(window)
                    
            elif event in ('编辑任务', '任务::编辑任务'):
                selected_tasks = values['-TASK-TABLE-']
                if selected_tasks:
                    task_index = selected_tasks[0]
                    tasks = self.task_manager.list_tasks()
                    if 0 <= task_index < len(tasks):
                        if self.edit_task_window(tasks[task_index]):
                            self.refresh_task_table(window)
                else:
                    sg.popup('请先选择一个任务')
                    
            elif event in ('标记状态', '任务::标记状态'):
                selected_tasks = values['-TASK-TABLE-']
                if selected_tasks:
                    task_index = selected_tasks[0]
                    tasks = self.task_manager.list_tasks()
                    if 0 <= task_index < len(tasks):
                        if self.mark_status_window(tasks[task_index]):
                            self.refresh_task_table(window)
                else:
                    sg.popup('请先选择一个任务')
                    
            elif event in ('删除任务', '任务::删除任务'):
                selected_tasks = values['-TASK-TABLE-']
                if selected_tasks:
                    task_index = selected_tasks[0]
                    tasks = self.task_manager.list_tasks()
                    if 0 <= task_index < len(tasks):
                        task = tasks[task_index]
                        if sg.popup_yes_no(f'确认删除任务 "{task.title}"?') == 'Yes':
                            if self.task_manager.delete_task(task.task_id):
                                sg.popup('任务已删除')
                                self.refresh_task_table(window)
                            else:
                                sg.popup('删除失败')
                else:
                    sg.popup('请先选择一个任务')
                    
            elif event in ('所有任务', '查看::所有任务'):
                self.refresh_task_table(window)
                
            elif event in ('待办任务', '查看::待办任务'):
                tasks = self.task_manager.list_tasks(status='todo')
                self.update_task_table(window, tasks)
                
            elif event in ('进行中', '查看::进行中'):
                tasks = self.task_manager.list_tasks(status='in_progress')
                self.update_task_table(window, tasks)
                
            elif event in ('已完成', '查看::已完成'):
                tasks = self.task_manager.list_tasks(status='done')
                self.update_task_table(window, tasks)
                
            elif event in ('统计', '统计::任务统计'):
                self.show_statistics_window()
                
            elif event == '关于':
                sg.popup('时间管理系统 v1.0\n\n一个功能完整的时间管理工具\n支持任务管理和时间追踪')
                
        window.close()
        self.user_manager.logout(self.current_session)
        
    def refresh_task_table(self, window):
        """刷新任务表格"""
        tasks = self.task_manager.list_tasks()
        self.update_task_table(window, tasks)
        
    def update_task_table(self, window, tasks):
        """更新任务表格数据"""
        table_data = []
        for i, task in enumerate(tasks):
            status_text = {
                'todo': '待办',
                'in_progress': '进行中', 
                'done': '已完成',
                'cancelled': '已取消'
            }.get(task.status, task.status)
            
            priority_text = {
                'low': '低',
                'medium': '中',
                'high': '高',
                'urgent': '紧急'
            }.get(task.priority, task.priority)
            
            table_data.append([
                str(i+1),
                task.title,
                status_text,
                priority_text,
                task.due_date or '无',
                f"{task.estimated_hours}h"
            ])
            
        window['-TASK-TABLE-'].update(values=table_data)
        
    def add_task_window(self):
        """添加任务窗口"""
        layout = [
            [sg.Text('添加新任务', font=('Arial', 16))],
            [sg.Text('标题*:'), sg.InputText(key='-TITLE-', size=(30, 1))],
            [sg.Text('描述:'), sg.Multiline(key='-DESCRIPTION-', size=(30, 3))],
            [sg.Text('优先级:'), 
             sg.Combo(['低', '中', '高', '紧急'], default_value='中', key='-PRIORITY-')],
            [sg.Text('截止日期:'), sg.InputText(key='-DUE_DATE-', size=(15, 1)),
             sg.CalendarButton('选择日期', target='-DUE_DATE-', format='%Y-%m-%d')],
            [sg.Text('预估小时:'), sg.InputText(key='-ESTIMATED-', size=(10, 1))],
            [sg.Text('标签 (逗号分隔):'), sg.InputText(key='-TAGS-', size=(30, 1))],
            [sg.Button('保存'), sg.Button('取消')],
            [sg.Text('', key='-MSG-', text_color='red')]
        ]
        
        window = sg.Window('添加任务', layout)
        
        result = False
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '取消'):
                break
                
            elif event == '保存':
                title = values['-TITLE-'].strip()
                if not title:
                    window['-MSG-'].update('标题不能为空')
                    continue
                    
                # 转换优先级
                priority_map = {'低': 'low', '中': 'medium', '高': 'high', '紧急': 'urgent'}
                priority = priority_map.get(values['-PRIORITY-'], 'medium')
                
                # 处理标签
                tags = [tag.strip() for tag in values['-TAGS-'].split(',')] if values['-TAGS-'] else []
                
                # 处理预估时间
                estimated_hours = 0.0
                if values['-ESTIMATED-']:
                    try:
                        estimated_hours = float(values['-ESTIMATED-'])
                    except ValueError:
                        pass
                
                task_data = {
                    'title': title,
                    'description': values['-DESCRIPTION-'],
                    'priority': priority,
                    'due_date': values['-DUE_DATE-'] or None,
                    'estimated_hours': estimated_hours,
                    'tags': tags
                }
                
                task = self.task_manager.create_task(**task_data)
                if task:
                    sg.popup(f'任务 "{task.title}" 创建成功!')
                    result = True
                    break
                else:
                    window['-MSG-'].update('创建任务失败')
                    
        window.close()
        return result
        
    def edit_task_window(self, task):
        """编辑任务窗口"""
        # 反向转换状态和优先级
        status_map = {'todo': '待办', 'in_progress': '进行中', 'done': '已完成', 'cancelled': '已取消'}
        priority_map = {'low': '低', 'medium': '中', 'high': '高', 'urgent': '紧急'}
        
        layout = [
            [sg.Text('编辑任务', font=('Arial', 16))],
            [sg.Text('标题*:'), sg.InputText(key='-TITLE-', size=(30, 1), default_text=task.title)],
            [sg.Text('描述:'), sg.Multiline(key='-DESCRIPTION-', size=(30, 3), default_text=task.description)],
            [sg.Text('状态:'), 
             sg.Combo(['待办', '进行中', '已完成', '已取消'], 
                     default_value=status_map.get(task.status, '待办'), key='-STATUS-')],
            [sg.Text('优先级:'), 
             sg.Combo(['低', '中', '高', '紧急'], 
                     default_value=priority_map.get(task.priority, '中'), key='-PRIORITY-')],
            [sg.Text('截止日期:'), sg.InputText(key='-DUE_DATE-', size=(15, 1), default_text=task.due_date or ''),
             sg.CalendarButton('选择日期', target='-DUE_DATE-', format='%Y-%m-%d')],
            [sg.Text('预估小时:'), sg.InputText(key='-ESTIMATED-', size=(10, 1), default_text=str(task.estimated_hours))],
            [sg.Text('标签:'), sg.InputText(key='-TAGS-', size=(30, 1), default_text=', '.join(task.tags))],
            [sg.Button('保存'), sg.Button('取消')],
            [sg.Text('', key='-MSG-', text_color='red')]
        ]
        
        window = sg.Window('编辑任务', layout)
        
        result = False
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '取消'):
                break
                
            elif event == '保存':
                title = values['-TITLE-'].strip()
                if not title:
                    window['-MSG-'].update('标题不能为空')
                    continue
                    
                # 转换状态和优先级
                status_map_rev = {'待办': 'todo', '进行中': 'in_progress', '已完成': 'done', '已取消': 'cancelled'}
                priority_map_rev = {'低': 'low', '中': 'medium', '高': 'high', '紧急': 'urgent'}
                
                status = status_map_rev.get(values['-STATUS-'], 'todo')
                priority = priority_map_rev.get(values['-PRIORITY-'], 'medium')
                
                # 处理标签
                tags = [tag.strip() for tag in values['-TAGS-'].split(',')] if values['-TAGS-'] else []
                
                # 处理预估时间
                estimated_hours = 0.0
                if values['-ESTIMATED-']:
                    try:
                        estimated_hours = float(values['-ESTIMATED-'])
                    except ValueError:
                        pass
                
                update_data = {
                    'title': title,
                    'description': values['-DESCRIPTION-'],
                    'status': status,
                    'priority': priority,
                    'due_date': values['-DUE_DATE-'] or None,
                    'estimated_hours': estimated_hours,
                    'tags': tags
                }
                
                if self.task_manager.update_task(task.task_id, **update_data):
                    sg.popup('任务更新成功!')
                    result = True
                    break
                else:
                    window['-MSG-'].update('更新任务失败')
                    
        window.close()
        return result
        
    def mark_status_window(self, task):
        """标记状态窗口"""
        layout = [
            [sg.Text(f'标记任务状态: {task.title}', font=('Arial', 14))],
            [sg.Radio('待办', 'STATUS', default=task.status=='todo', key='-TODO-')],
            [sg.Radio('进行中', 'STATUS', default=task.status=='in_progress', key='-INPROGRESS-')],
            [sg.Radio('已完成', 'STATUS', default=task.status=='done', key='-DONE-')],
            [sg.Radio('已取消', 'STATUS', default=task.status=='cancelled', key='-CANCELLED-')],
            [sg.Button('保存'), sg.Button('取消')]
        ]
        
        window = sg.Window('标记状态', layout)
        
        result = False
        while True:
            event, values = window.read()
            
            if event in (sg.WIN_CLOSED, '取消'):
                break
                
            elif event == '保存':
                if values['-TODO-']:
                    status = 'todo'
                elif values['-INPROGRESS-']:
                    status = 'in_progress'
                elif values['-DONE-']:
                    status = 'done'
                elif values['-CANCELLED-']:
                    status = 'cancelled'
                else:
                    status = task.status
                    
                if self.task_manager.update_task(task.task_id, status=status):
                    sg.popup('状态更新成功!')
                    result = True
                    break
                else:
                    sg.popup('更新失败')
                    
        window.close()
        return result
        
    def show_statistics_window(self):
        """显示统计窗口"""
        stats = self.task_manager.get_task_statistics()
        
        layout = [
            [sg.Text('任务统计', font=('Arial', 16))],
            [sg.Text(f'总任务数: {stats["total_tasks"]}')],
            [sg.Text(f'已完成: {stats["completed_tasks"]}')],
            [sg.Text(f'进行中: {stats["in_progress_tasks"]}')],
            [sg.Text(f'待办: {stats["todo_tasks"]}')],
            [sg.Text(f'完成率: {stats["completion_rate"]:.1%}')],
            [sg.Text(f'总预估时间: {stats["total_estimated_hours"]:.1f}h')],
            [sg.Text(f'总实际时间: {stats["total_actual_hours"]:.1f}h')],
            [sg.Button('关闭')]
        ]
        
        window = sg.Window('任务统计', layout)
        window.read()
        window.close()

def main():
    app = TimeManagementGUI()
    
    # 显示登录窗口
    if app.login_window():
        # 登录成功，显示主窗口
        app.main_window()

if __name__ == "__main__":
    main()