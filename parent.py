import pandas as pd
import os
import subprocess

# Excel dosyasından isimleri okuma
def read_names_from_excel(file_name, first_column_name, second_column_name, third_column_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    file_path = os.path.join(dir_path, file_name)
    
    df = pd.read_excel(file_path, engine='openpyxl')
    
    if all(col in df.columns for col in [first_column_name, second_column_name, third_column_name]):
        first_column_names = df[first_column_name].dropna().tolist()
        second_column_names = df[second_column_name].dropna().tolist()
        third_column_names = df[third_column_name].dropna().tolist()
    else:
        raise ValueError("Belirtilen sütunlardan biri veya ikisi Excel dosyasında bulunamadı.")
    
    return first_column_names, second_column_names, third_column_names

# Branch ismini formatlamak
def format_branch_name(name):
    return name.replace(' ', '_').replace('/', '_').replace('\\', '_')

# Git komutları ile branch oluşturma ve push yapma
def create_and_push_branches(repo_path, first_column_names, second_column_names, third_column_names, remote_name='origin'):
    git_path = r'C:\Program Files\Git\bin\git.exe'
    
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Git repo dizini bulunamadı: {repo_path}")
    
    os.chdir(repo_path)
    
    # Mevcut branch'leri al
    result = subprocess.run([git_path, 'branch', '--format=%(refname:short)'], capture_output=True, text=True, check=True)
    existing_branches = result.stdout.splitlines()
    existing_branches = [branch.strip() for branch in existing_branches]

    print(f"Mevcut Branch'ler: {existing_branches}")

    # Ana branch'ten yeni branch oluşturma
    for first_name in first_column_names:
        branch_name = format_branch_name(first_name)
        if branch_name not in existing_branches:
            subprocess.run([git_path, 'checkout', 'main'], check=True)
            result = subprocess.run([git_path, 'checkout', '-b', branch_name], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Branch '{branch_name}' oluşturuldu ve bu branch'e geçiş yapıldı.")
                result = subprocess.run([git_path, 'push', remote_name, branch_name], capture_output=True, text=True)
                if result.returncode == 0:
                    print(f"Branch '{branch_name}' uzak repoya gönderildi.")
                else:
                    print(f"Branch uzak repoya gönderilirken hata oluştu: {result.stderr}")
            else:
                print(f"Branch oluşturulurken hata oluştu: {result.stderr}")
        else:
            print(f"Branch '{branch_name}' zaten mevcut.")
    
    # İkinci sütundaki branch'leri oluşturma
    for first_name in first_column_names:
        for second_name in second_column_names:
            parent_branch = format_branch_name(first_name)
            branch_name = format_branch_name(f"{first_name}_{second_name}")
            if branch_name not in existing_branches:
                result = subprocess.run([git_path, 'checkout', parent_branch], check=True)
                if result.returncode == 0:
                    result = subprocess.run([git_path, 'checkout', '-b', branch_name], capture_output=True, text=True)
                    if result.returncode == 0:
                        print(f"Branch '{branch_name}' oluşturuldu ve bu branch'e geçiş yapıldı.")
                        result = subprocess.run([git_path, 'push', remote_name, branch_name], capture_output=True, text=True)
                        if result.returncode == 0:
                            print(f"Branch '{branch_name}' uzak repoya gönderildi.")
                        else:
                            print(f"Branch uzak repoya gönderilirken hata oluştu: {result.stderr}")
                    else:
                        print(f"Branch oluşturulurken hata oluştu: {result.stderr}")
                else:
                    print(f"Branch '{parent_branch}' üzerine geçiş yapılamadı: {result.stderr}")

    # Üçüncü sütundaki branch'leri oluşturma
    for first_name in first_column_names:
        for second_name in second_column_names:
            parent_branch = format_branch_name(f"{first_name}_{second_name}")
            for third_name in third_column_names:
                branch_name = format_branch_name(f"{first_name}_{second_name}_{third_name}")
                if branch_name not in existing_branches:
                    result = subprocess.run([git_path, 'checkout', parent_branch], check=True)
                    if result.returncode == 0:
                        result = subprocess.run([git_path, 'checkout', '-b', branch_name], capture_output=True, text=True)
                        if result.returncode == 0:
                            print(f"Branch '{branch_name}' oluşturuldu ve bu branch'e geçiş yapıldı.")
                            result = subprocess.run([git_path, 'push', remote_name, branch_name], capture_output=True, text=True)
                            if result.returncode == 0:
                                print(f"Branch '{branch_name}' uzak repoya gönderildi.")
                            else:
                                print(f"Branch uzak repoya gönderilirken hata oluştu: {result.stderr}")
                        else:
                            print(f"Branch oluşturulurken hata oluştu: {result.stderr}")
                    else:
                        print(f"Branch '{parent_branch}' üzerine geçiş yapılamadı: {result.stderr}")

# Ana işlev
def main():
    excel_file_name = 'deneme.xlsx'
    first_column_name = 'kompresor'
    second_column_name = 'bm_no'
    third_column_name = 'drop_freq'
    repo_path = r'C:\Users\sefad\OneDrive\Masaüstü\b'
    
    first_column_names, second_column_names, third_column_names = read_names_from_excel(excel_file_name, first_column_name, second_column_name, third_column_name)
    
    create_and_push_branches(repo_path, first_column_names, second_column_names, third_column_names)

if __name__ == "__main__":
    main()
