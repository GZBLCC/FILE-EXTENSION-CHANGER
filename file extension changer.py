import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter import ttk
import psutil
# 全局变量来存储选择的文件夹路径
root_folder = ""

# 常见的文件后缀列表，按类别分类
file_extensions = {
    '文本': ['txt', 'doc', 'docx', 'pdf', 'rtf', 'odt', 'epub'],
    '视频': ['mp4', 'avi', 'mov', 'wmv', 'mkv', 'flv', 'webm'],
    '音频': ['mp3', 'wav', 'ogg', 'flac', 'm4a', 'aac', 'wma'],
    '图像': ['jpg', 'jpeg', 'png', 'gif', 'bmp', 'tiff', 'svg'],
    '压缩包': ['zip', 'rar', '7z', 'tar', 'gz', 'bz2'],
    '表格': ['xls', 'xlsx', 'ods'],
    '演示文稿': ['ppt', 'pptx', 'odp'],
    '脚本': ['py', 'js', 'java', 'c', 'cpp', 'cs', 'php', 'html', 'css'],
    '数据库': ['db', 'sql', 'mdb']
}

# 设置样式
style = ttk.Style()
style.theme_use('clam')
style.configure('TLabel', font=('Helvetica', 10), foreground='#333333')
style.configure('TButton', font=('Helvetica', 10, 'bold'), padding=10)
style.configure('TEntry', font=('Helvetica', 10), padding=5)

def kill_process(pid):
    try:
        p = psutil.Process(pid)
        p.terminate()  # 或者使用 p.kill() 来强制结束进程
        return True
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def find_process_using_file(file_path):
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            for file in proc.open_files():
                if file.path == file_path:
                    return proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def find_process_using_file(file_path):
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
         try:
             for file in proc.open_files():
                 if file.path == file_path:
                      return proc.info
         except (psutil.NoSuchProcess, psutil.AccessDenied):
              pass
         return None
def kill_process(pid):
     try:
          p = psutil.Process(pid)
          p.terminate()  # 或者使用 p.kill() 来强制结束进程
          return True
     except (psutil.NoSuchProcess, psutil.AccessDenied):
          return False

def error_process1(root_folder, old_exts, new_ext):
    changed_files = 0
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if any(file.lower().endswith('.' + ext) for ext in old_exts):
                file_path = os.path.join(root, file)
                new_file_name = os.path.splitext(file)[0] + '.' + new_ext
                new_file_path = os.path.join(root, new_file_name)
                if os.path.exists(new_file_path):
                    os.remove(new_file_path)
                try:
                    os.rename(file_path, new_file_path)
                    changed_files += 1
                except PermissionError:
                    process = find_process_using_file(file_path)
                    if process:
                        process_name = process['name']
                        pid = process['pid']
                        messagebox.showerror("错误", f"无法重命名文件：{file_path} -> {new_file_path}。文件正在被进程 '{process_name}' (PID: {pid}) 使用。")
                        close_process = messagebox.askyesno("关闭进程", f"是否尝试关闭进程 '{process_name}' (PID: {pid}) 以释放文件？")
                        if close_process:
                            if kill_process(pid):
                                messagebox.showinfo("信息", f"进程 '{process_name}' (PID: {pid}) 已被关闭。")
                                os.rename(file_path, new_file_path)
                                changed_files += 1
                            else:
                                messagebox.showerror("错误", f"无法关闭进程 '{process_name}' (PID: {pid})。")
                    else:
                        messagebox.showerror("错误", f"无法重命名文件：{file_path} -> {new_file_path}。文件可能正在被使用，但找不到使用它的进程。")
                except Exception as e:
                    messagebox.showerror("错误", f"重命名文件时出错：{file_path} -> {new_file_path}。错误信息：{e}")
    return changed_files

def rename_files():
    if not root_folder:
        messagebox.showerror("错误", "请先选择一个文件夹。")
        return
    old_exts = [ext.strip() for ext in old_ext_entry.get().split(',') if ext.strip()]
    new_ext = new_ext_entry.get().strip()
    if not old_exts or not new_ext:
        messagebox.showerror("错误", "请输入原始文件扩展名和新的文件扩展名。")
        return
    if any(ext.startswith('.') for ext in old_exts) or new_ext.startswith('.'):
        messagebox.showerror("错误", "文件扩展名不需要以点（.）开头。")
        return
    # 检查原始扩展名和新扩展名是否相同，并清除相同的扩展名
    if new_ext in old_exts:
        old_exts.remove(new_ext)
        old_ext_entry.delete(0, tk.END)
        for ext in old_exts:
            old_ext_entry.insert(tk.END, ext + ',')
        old_ext_entry.delete(len(old_ext_entry.get()) - 1, tk.END)
    changed_files = error_process1(root_folder, old_exts, new_ext)
    if changed_files:
        messagebox.showinfo("信息", f"成功更名为 {changed_files} 个文件。")
    else:
        messagebox.showinfo("信息", "未找到与指定扩展名匹配的文件。")

def browse_folder():
    global root_folder
    root_folder = filedialog.askdirectory()
    if root_folder:
        folder_label.config(text=f"选择的文件夹: {root_folder}")
        folder_entry.delete(0, tk.END)
        folder_entry.insert(0, root_folder)

def select_extensions(category):
    extensions = file_extensions[category]
    old_ext_entry.delete(0, tk.END)
    for ext in extensions:
        old_ext_entry.insert(tk.END, ext + ',')
    old_ext_entry.delete(len(old_ext_entry.get()) - 1, tk.END)

def close_target_process():
    pid = pid_entry.get()
    if pid:
        if kill_process(int(pid)):
            messagebox.showinfo("信息", f"进程 {pid} 已被关闭。")
        else:
            messagebox.showerror("错误", f"无法关闭进程 {pid}。")
    else:
        messagebox.showerror("错误", "请输入有效的PID。")

# 创建主窗口
root = tk.Tk()
root.title("File extension changer")
root.geometry('460x800')
root.minsize(450, 800)

folder_label = ttk.Label(root, text="选择的文件夹: 无", style='TLabel')
folder_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')

folder_entry = ttk.Entry(root, width=50, style='TEntry')
folder_entry.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

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

for i, (category, _) in enumerate(file_extensions.items()):
    button = ttk.Button(root, text=f"选择{category}文件后缀", command=lambda c=category: select_extensions(c), style='TButton')
    button.grid(row=7 + i, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

pid_label = ttk.Label(root, text="输入要关闭的进程PID：", style='TLabel')
pid_label.grid(row=9+i, column=0, padx=5, pady=5, sticky='w')
pid_entry = ttk.Entry(root, width=50, style='TEntry')
pid_entry.grid(row=10+i, column=0, columnspan=2, padx=5, pady=5, sticky='ew')

# 创建一个按钮用于关闭目标进程
close_process_button = ttk.Button(root, text="关闭目标进程", command=close_target_process, style='TButton')
close_process_button.grid(row=11+i, column=0, columnspan=2, padx=5, pady=20)

root.mainloop()