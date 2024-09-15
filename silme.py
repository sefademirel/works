import os
import subprocess

def delete_all_branches(repo_path, remote_name='origin'):
    # Git'in tam yolunu belirtin (Windows için örnek yol, güncellemeyi unutmayın)
    git_path = r'C:\Program Files\Git\bin\git.exe'
    
    # Git repo dizinine geçiş yap
    if not os.path.isdir(repo_path):
        raise FileNotFoundError(f"Git repo dizini bulunamadı: {repo_path}")
    os.chdir(repo_path)
    
    # Mevcut yerel branch'leri al
    result = subprocess.run([git_path, 'branch', '--format=%(refname:short)'], capture_output=True, text=True, check=True)
    local_branches = result.stdout.splitlines()
    
    # Uzak branch'leri al
    result = subprocess.run([git_path, 'branch', '-r'], capture_output=True, text=True, check=True)
    remote_branches = result.stdout.splitlines()
    remote_branches = [branch.strip().split('/')[-1] for branch in remote_branches if f'{remote_name}/' in branch]
    
    # Pushlanmamış branch'leri belirle
    unpushed_branches = [branch for branch in local_branches if branch not in remote_branches]
    
    # Tüm yerel branch'leri sil
    for branch in local_branches:
        if branch in unpushed_branches:
            # Pushlanmamış branch'leri sil
            result = subprocess.run([git_path, 'branch', '-d', branch], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Pushlanmamış branch '{branch}' silindi.")
            else:
                print(f"Pushlanmamış branch '{branch}' silinirken hata oluştu: {result.stderr}")
        else:
            # Pushlanmış branch'leri sil
            result = subprocess.run([git_path, 'branch', '-d', branch], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"Pushlanmış branch '{branch}' silindi.")
            else:
                print(f"Pushlanmış branch '{branch}' silinirken hata oluştu: {result.stderr}")

# Ana işlev
def main():
    repo_path = r'C:\Users\sefad\OneDrive\Masaüstü\c'  # Git repo dizininizin tam yolu
    
    # Tüm branch'leri sil
    delete_all_branches(repo_path)

if __name__ == "__main__":
    main()
