import pandas as pd
import os

# Excel dosyasını yükle
excel_file = 'deneme.xlsx'  # Excel dosyanızın yolunu buraya yazın
df = pd.read_excel(excel_file)

# Kök klasör yolu
root_folder = 'cc'  # Klasörlerin oluşturulacağı ana yol
os.makedirs(root_folder, exist_ok=True)

# Birinci sütundaki tüm ana klasörleri toplamak
first_level_folders = df.iloc[:, 0].dropna().astype(str).str.strip()

# İkinci sütundaki tüm ikinci seviye klasörleri toplamak
second_level_folders = df.iloc[:, 1].dropna().astype(str).str.strip()

# Üçüncü sütundaki tüm üçüncü seviye klasörleri toplamak
third_level_folders = df.iloc[:, 2].dropna().astype(str).str.strip()

# Ana klasörleri oluştur
for first_level in first_level_folders:
    # Ana klasörlerin oluşturulması
    first_level_path = os.path.join(root_folder, first_level)
    os.makedirs(first_level_path, exist_ok=True)
    
    # İkinci seviye klasörlerin oluşturulması
    for second_level in second_level_folders:
        second_level_path = os.path.join(first_level_path, f"{first_level}_{second_level}")
        os.makedirs(second_level_path, exist_ok=True)
        
        # Üçüncü seviye klasörlerin oluşturulması
        for third_level in third_level_folders:
            third_level_path = os.path.join(second_level_path, f"{first_level}_{second_level}_{third_level}")
            os.makedirs(third_level_path, exist_ok=True)
            
            # Her üçüncü seviye klasörün içine bir metin dosyası oluştur
            text_file_path = os.path.join(third_level_path, 'info.txt')
            with open(text_file_path, 'w') as f:
                f.write(f"Ana Klasör: {first_level}\nİkinci Seviye Klasör: {second_level}\nÜçüncü Seviye Klasör: {third_level}")

print("Klasörler ve dosyalar başarıyla oluşturuldu!")
