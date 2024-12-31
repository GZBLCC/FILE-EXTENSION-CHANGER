import os
import re
from concurrent.futures import ThreadPoolExecutor

def validate_extensions(old_exts, new_ext):
    """
    验证用户输入的扩展名是否合法。
    """
    extension_pattern = re.compile(r'^[a-zA-Z0-9_]+$')
    
    if new_ext.startswith('.'):
        raise ValueError("新的文件扩展名不需要以点（.）开头。")
    
    for ext in old_exts:
        if not (ext.startswith('.') and extension_pattern.match(ext[1:])):
            raise ValueError(f"原始文件扩展名 '{ext}' 无效。扩展名只能包含字母、数字和下划线。")
    
    return True

def rename_file(file_path, new_ext):
    """
    重命名单个文件。
    """
    try:
        file_dir, file_name = os.path.split(file_path)
        base_name, ext = os.path.splitext(file_name)
        new_file_name = f"{base_name}.{new_ext}"
        new_file_path = os.path.join(file_dir, new_file_name)
        os.rename(file_path, new_file_path)
        return 1  # 文件重命名成功
    except Exception as e:
        print(f"Error renaming {file_path} to {new_file_path}: {e}")
        return 0  # 文件重命名失败

def collect_files_to_rename(directory, old_exts):
    """
    收集需要重命名的文件。
    """
    files_to_rename = []
    with os.scandir(directory) as entries:
        for entry in entries:
            if entry.is_dir(follow_symlinks=False):
                files_to_rename.extend(collect_files_to_rename(entry.path, old_exts))
            elif any(entry.name.lower().endswith(f".{ext}") for ext in old_exts):
                files_to_rename.append(entry.path)
    return files_to_rename

def perform_file_rename(root_folder, old_exts, new_ext):
    """
    执行文件重命名操作。
    """
    changed_files = 0
    files_to_rename = collect_files_to_rename(root_folder, old_exts)
    
    with ThreadPoolExecutor() as executor:
        results = executor.map(lambda path: rename_file(path, new_ext), files_to_rename)
        
        changed_files = sum(results)
    
    return changed_files

def delete_text_from_filename(file_path, text_to_delete):
    """
    从文件名中删除特定文字。
    """
    try:
        file_dir, file_name = os.path.split(file_path)
        new_file_name = file_name.replace(text_to_delete, '')
        new_file_path = os.path.join(file_dir, new_file_name)
        os.rename(file_path, new_file_path)
        return 1  # 文件名修改成功
    except Exception as e:
        print(f"Error modifying {file_path} to {new_file_path}: {e}")
        return 0  # 文件名修改失败

def perform_text_deletion(root_folder, delete_text):
    """
    执行删除文件名中的特定文字操作。
    """
    changed_files = 0
    for root, dirs, files in os.walk(root_folder):
        for file in files:
            if delete_text in file:
                file_path = os.path.join(root, file)
                changed_files += delete_text_from_filename(file_path, delete_text)
    return changed_files