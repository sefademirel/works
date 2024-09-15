import pandas as pd
import os
import subprocess

# Excel dosyasından isimleri okuma
def read_names_from_excel(file_name, column_name):
    # Python dosyasının bulunduğu dizini al
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, file_name)
    
    # Excel dosyasını okuma
    df = pd.read_excel(file_path, engine='openpyxl')
    
    # Belirtilen sütundan isimleri al
    if column_name in df.columns:
        names = df[column_name].dropna().tolist()  # Boş hücreleri hariç tutar
    else:
        raise ValueError(f"Sütun '{column_name}' Excel dosyasında bulunamadı.")
    
    return names

# Git komutları ile branch oluşturma ve push yapma
def create_and_push_branches_from_existing(repo_path, base_branch, names, remote_name='origin'):
    # Git'in tam yolunu belirtin (Windows için örnek yol, güncellemeyi unutmayın)
    git_path = r'C:\Program Files\Git\bin\git.exe'
    
    # Git repo dizinine geçiş yap
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Git repo dizini bulunamadı: {repo_path}")
    os.chdir(repo_path)
    
    # Mevcut branch'ten geçiş yap
    subprocess.run([git_path, 'checkout', base_branch], check=True)
    
    # Mevcut branch'leri al
    result = subprocess.run([git_path, 'branch'], capture_output=True, text=True, check=True)
    existing_branches = result.stdout.splitlines()
    existing_branches = [branch.strip('*').strip() for branch in existing_branches]
    print(f"Mevcut Branch'ler: {existing_branches}")  # Debug: mevcut branch'leri yazdır
    
    for name in names:
        # Branch isimlerinde geçersiz karakterleri değiştirin
        branch_name = name.replace(' ', '_').replace('/', '_').replace('\\', '_')
        print(f"Deneme: {branch_name}")  # Debug: branch ismini yazdır
        
        try:
            if branch_name in existing_branches:
                print(f"Branch '{branch_name}' zaten mevcut.")
            else:
                # Yeni branch oluşturma ve bu branch'e geçiş yapma
                result = subprocess.run([git_path, 'checkout', '-b', branch_name], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Branch '{branch_name}' oluşturuldu ve bu branch'e geçiş yapıldı.")
                else:
                    print(f"Branch oluşturulurken hata oluştu: {result.stderr}")
                    continue

            # Uzak repoya push yapma
            result = subprocess.run([git_path, 'push', remote_name, branch_name], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Branch '{branch_name}' uzak repoya gönderildi.")
            else:
                print(f"Branch uzak repoya gönderilirken hata oluştu: {result.stderr}")
        
        except subprocess.CalledProcessError as e:
            print(f"Git komutu hata verdi: {e}")
        except Exception as e:
            print(f"Beklenmedik bir hata oluştu: {e}")  

# Ana işlev
def main():
    excel_file_name = 'deneme.xlsx'  # Excel dosyasının adı
    column_name = 'branch'  # Excel dosyasındaki sütun adı
    repo_path = r'C:\Users\sefad\OneDrive\Masaüstü\a'  # Git repo dizininizin tam yolu
    base_branch = 'main'  # Mevcut branch adı, örneğin 'main' veya 'master'
    
    # Excel dosyasından isimleri al
    names = read_names_from_excel(excel_file_name, column_name)
    
    # Git komutları ile branch'ler oluştur ve push yap
    create_and_push_branches_from_existing(repo_path, base_branch, names)

if __name__ == "__main__":
    main()
