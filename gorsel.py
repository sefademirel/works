import subprocess
import os
import networkx as nx
import matplotlib.pyplot as plt

def run_git_command(command, repo_path):
    """Git komutunu çalıştırır ve çıktıyı döndürür."""
    git_cmd = r"C:\Program Files\Git\bin\git.exe"  # Git yürütülebilir dosyasının tam yolu
    result = subprocess.run(
        [git_cmd] + command.split(),
        cwd=repo_path,
        text=True,
        capture_output=True
    )
    return result.stdout.strip()

def get_commit_parents(commit_hash, repo_path):
    """Bir commit'in parent'larını döndürür."""
    command = f"rev-list --parents -n 1 {commit_hash}"
    output = run_git_command(command, repo_path)
    parts = output.split()
    return parts[1:]  # İlk parça commit hash'idir, geri kalanlar parent'lerdir

def get_branch_commits(branch, repo_path):
    """Bir branch'teki tüm commit'leri döndürür."""
    command = f"log --pretty=format:%H {branch}"
    output = run_git_command(command, repo_path)
    return output.splitlines()

# Git repo yolunu belirtin
repo_path = "C:/Users/sefad/OneDrive/Masaüstü/b"  # Buraya Git repo yolunuzu girin

# Dizin yolunun geçerliliğini kontrol edin
if not os.path.isdir(repo_path):
    raise NotADirectoryError(f"Geçersiz dizin yolu: {repo_path}")

# Boş bir NetworkX grafiği oluştur
G = nx.DiGraph()

# Branch'leri al
branches = run_git_command("branch --format '%(refname:short)'", repo_path).splitlines()

# Branch'lerin commit'lerini ve parent-child ilişkilerini belirle
for branch in branches:
    commits = get_branch_commits(branch, repo_path)
    for commit in commits:
        parents = get_commit_parents(commit, repo_path)
        for parent in parents:
            G.add_edge(parent, commit)

# Ağaçları daha okunabilir hale getirmek için düğümlerin adlarını branch isimleriyle etiketle
labels = {}
for branch in branches:
    commits = get_branch_commits(branch, repo_path)
    for commit in commits:
        labels[commit] = branch

# Grafiği çiz
pos = nx.spring_layout(G, seed=42)  # Seed ile aynı düzeni korur
nx.draw(G, pos, with_labels=False, node_size=50, node_color='blue', edge_color='gray', alpha=0.5)
nx.draw_networkx_labels(G, pos, labels=labels, font_size=8, font_color='white')
plt.title('Git Branch Parent-Child Relationships')
plt.show()
