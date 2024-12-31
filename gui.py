# gui.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from file_utils import validate_extensions, perform_file_rename, perform_text_deletion
from process_utils import kill_process
from constants import file_extensions
from styles import setup_styles



def show_message_async(message, title, msg_type):
    def show_message():

        messagebox.showmessage(title, message)

    root.after(0, show_message)

def browse_folder():
    global root_folder
    root_folder = filedialog.askdirectory()
    if root_folder:
        folder_label.config(text=f"选择的文件夹: {root_folder}")
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, root_folder)

def rename_files():
    if not root_folder:
        show_message_async("请先选择一个文件夹。", "错误", "error")
        return
    
    old_exts = [ext.strip() for ext in old_ext_entry.get().split(',') if ext.strip()]
    new_ext = new_ext_entry.get().strip()
    
    if not old_exts or not new_ext:
        show_message_async("请输入原始文件扩展名和新的文件扩展名。", "错误", "error")
        return
    
    try:
        validate_extensions(old_exts, new_ext)
    except ValueError as e:
        show_message_async(str(e), "错误", "error")
        return
    
    changed_files = perform_file_rename(root_folder, old_exts, new_ext)
    if changed_files:
        show_message_async(f"成功更名为 {changed_files} 个文件。", "信息", "info")
    else:
        show_message_async("未找到与指定扩展名匹配的文件。", "信息", "info")

def delete_files_text():
    if not root_folder:
        show_message_async("请先选择一个文件夹。", "错误", "error")
        return
    
    delete_text = delete_text_entry.get().strip()
    if not delete_text:
        show_message_async("请输入要删除的文字。", "错误", "error")
        return
    
    changed_files = perform_text_deletion(root_folder, delete_text)
    if changed_files:
        show_message_async(f"成功删除 {changed_files} 个文件名中的文字。", "信息", "info")
    else:
        show_message_async("未找到包含指定文字的文件名。", "信息", "info")

def close_target_process():
    pid = pid_entry.get()
    if pid:
        if kill_process(int(pid)):
            show_message_async(f"进程 {pid} 已被关闭。", "信息", "info")
        else:
            show_message_async(f"无法关闭进程 {pid}。", "错误", "error")
    else:
        show_message_async("请输入有效的PID。", "错误", "error")

def select_extensions(category):
    extensions = file_extensions.get(category, [])
    old_ext_entry.delete(0, tk.END)
    for ext in extensions:
        old_ext_entry.insert(tk.END, ext + ',')
    old_ext_entry.delete(len(old_ext_entry.get()) - 1, tk.END)


setup_styles()
root = tk.Tk()
root.title("File extension changer")
root.geometry('900x600')  # 调整窗口大小以适应所有组件
root.minsize(900, 650)

folder_label = ttk.Label(root, text="选择的文件夹: 无", style='TLabel')
folder_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

folder_entry = ttk.Entry(root, width=50, style='TEntry')
folder_entry.grid(row=1, column=0, columnspan=3, padx=5, pady=5, sticky='ew')

for i, (category, _) in enumerate(file_extensions.items()):
    button = ttk.Button(root, text=f"选择{category}文件后缀", command=lambda c=category: select_extensions(c), style='TButton')
    button.grid(row=7 + i, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

# 创建关闭进程的标签和输入框
pid_label = ttk.Label(root, text="输入要关闭的进程PID：", style='TLabel')
pid_label.grid(row=0 + len(file_extensions), column=4, padx=5, pady=5, sticky='w')

pid_entry = ttk.Entry(root, width=50, style='TEntry')
pid_entry.grid(row=1 + len(file_extensions), column=4, columnspan=1, padx=5, pady=5, sticky='ew')

close_process_button = ttk.Button(root, text="关闭目标进程", command=close_target_process, style='TButton')
close_process_button.grid(row=2 + len(file_extensions), column=4, padx=5, pady=20)

# 创建删除文件名中文字的标签和输入框
delete_text_label = ttk.Label(root, text="请输入文件名中要删除的文字：", style='TLabel')
delete_text_label.grid(row=3 + len(file_extensions), column=4, padx=5, pady=5, sticky='w')

delete_text_entry = ttk.Entry(root, width=50, style='TEntry')
delete_text_entry.grid(row=4 + len(file_extensions), column=4, columnspan=1, padx=5, pady=5, sticky='ew')

delete_button = ttk.Button(root, text="删除文件名中的文字", command=delete_files_text, style='TButton')
delete_button.grid(row=5 + len(file_extensions), column=4, padx=5, pady=20)

browse_button = ttk.Button(root, text="浏览", command=browse_folder, style='TButton')
browse_button.grid(row=1, column=2, padx=5, pady=5)

old_ext_label = ttk.Label(root, text="原始文件扩展名（例如：mp3, wav）：", style='TLabel')
old_ext_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

old_ext_entry = ttk.Entry(root, width=50, style='TEntry')
old_ext_entry.grid(row=3, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

new_ext_label = ttk.Label(root, text="新的文件扩展名（例如：m4a）：", style='TLabel')
new_ext_label.grid(row=4, column=0, padx=5, pady=5, sticky='w')

new_ext_entry = ttk.Entry(root, width=50, style='TEntry')
new_ext_entry.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

rename_button = ttk.Button(root, text="重命名文件", command=rename_files, style='TButton')
rename_button.grid(row=6, column=0, columnspan=2, padx=5, pady=20) 

if __name__ == "__main__":
    root.mainloop()
