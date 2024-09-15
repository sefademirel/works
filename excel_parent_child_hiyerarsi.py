import os
import pandas as pd

def list_files_and_folders(base_dir):
    data = []
    parent_dirs = set()  # Parent klasörleri bir kez eklemek için bir set

    for root, dirs, files in os.walk(base_dir):
        # Parent klasörler
        for dir_name in dirs:
            parent = os.path.basename(root)
            child = dir_name
            full_path = os.path.join(root, dir_name)
            if parent not in parent_dirs:
                data.append([parent, '', '', '', full_path])
                parent_dirs.add(parent)
            data.append(['', child, '', '', full_path])
        
        # Dosyalar
        for file_name in files:
            parent = os.path.basename(root)
            child = file_name
            full_path = os.path.join(root, file_name)
            extension = os.path.splitext(file_name)[1].lstrip('.')
            data.append(['', '', file_name, extension, full_path])

    return data

def save_to_excel(data, output_file):
    df = pd.DataFrame(data, columns=['Parent', 'Child', 'File Name', 'File Extension', 'Path'])
    
    # Excel dosyasına yazma
    df.to_excel(output_file, index=False)

if __name__ == "__main__":
    base_directory = r'C:\Users\sefad\OneDrive\Masaüstü\cc'  # Klasör yolunu buraya girin
    output_file = 'output.xlsx'  # Çıktı dosyasının adı

    data = list_files_and_folders(base_directory)
    save_to_excel(data, output_file)
