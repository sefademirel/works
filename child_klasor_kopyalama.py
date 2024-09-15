import os
import shutil

def copy_deepest_folders(src, dest):
    # Kök klasörler için bir kuyruk oluşturun
    stack = [src]
    
    # En alt düzey klasörleri saklayacak bir liste
    deepest_folders = []

    # Klasörleri gez
    while stack:
        current_dir = stack.pop()
        
        # Klasördeki tüm alt klasörleri alın
        try:
            entries = os.listdir(current_dir)
        except PermissionError:
            continue

        subdirs = [os.path.join(current_dir, entry) for entry in entries if os.path.isdir(os.path.join(current_dir, entry))]
        
        if subdirs:
            stack.extend(subdirs)
        else:
            deepest_folders.append(current_dir)
    
    # En alt düzey klasörleri hedef klasöre kopyala
    for folder in deepest_folders:
        # Hedef klasör yolunu oluştur
        target_folder = os.path.join(dest, os.path.basename(folder))
        if not os.path.exists(target_folder):
            os.makedirs(target_folder)
        
        # Klasör içeriğini kopyala
        for item in os.listdir(folder):
            s = os.path.join(folder, item)
            d = os.path.join(target_folder, item)
            if os.path.isdir(s):
                shutil.copytree(s, d, False, None)
            else:
                shutil.copy2(s, d)
    
    print("En alt düzey klasörler başarıyla kopyalandı.")

# Kaynak ve hedef klasörleri belirtin
source_dir = r'C:\Users\sefad\OneDrive\Masaüstü\cc'
destination_dir = r'C:\Users\sefad\OneDrive\Masaüstü\last'

copy_deepest_folders(source_dir, destination_dir)
