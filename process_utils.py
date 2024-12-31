# process_utils.py
import psutil

def find_process_using_file(file_path):
    """
    查找使用特定文件的进程。
    """
    for proc in psutil.process_iter(['pid', 'name', 'open_files']):
        try:
            for file in proc.open_files():
                if file.path == file_path:
                    return proc.info
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return None

def is_system_process(pid):
    """
    检查进程是否为系统进程。
    """
    try:
        process = psutil.Process(pid)
        return process.exe().startswith('/System') or process.exe().startswith('/usr')
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return False

def get_process_info(pid):
    """
    获取进程信息。
    """
    try:
        process = psutil.Process(pid)
        return {
            'pid': process.pid,
            'name': process.name(),
            'exe': process.exe(),
            'username': process.username()
        }
    except (psutil.NoSuchProcess, psutil.AccessDenied):
        return None

def kill_process(pid):
    """
    关闭进程。
    """
    process_info = get_process_info(pid)
    if process_info:
        if is_system_process(pid):
            print(f"进程 {pid} 是系统进程，不允许关闭。")
            return False

        confirm_message = (
            f"您即将关闭进程：\n"
            f"PID: {process_info['pid']}\n"
            f"名称: {process_info['name']}\n"
            f"路径: {process_info['exe']}\n"
            f"用户: {process_info['username']}\n"
            f"这可能会导致系统不稳定或数据丢失。\n"
            f"您确定要继续吗？"
        )
        if input(confirm_message) == "yes":
            try:
                process = psutil.Process(pid)
                process.terminate()
                return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                print(f"无法访问进程 {pid} 的信息或没有权限。")
                return False
            except Exception as e:
                print(f"关闭进程 {pid} 时发生错误：{e}")
                return False
        else:
            print("关闭进程操作已取消。")
            return False
    else:
        print("无效的进程ID。")
        return False
