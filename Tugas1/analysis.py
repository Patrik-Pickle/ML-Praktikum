# analysis.py
# Tugas Praktikum Data Mining - Tahap 2 & 3
# Import dataset, pemahaman dataset, statistik deskriptif, cek data hilang & outlier

import pandas as pd

df = pd.read_csv("raw_github_repos.csv")

print("===== 2. IMPORT & PEMAHAMAN DATASET =====")
print(df.head())
print()
print("Ukuran data (baris, kolom):", df.shape)
print()
print(df.info())
print()
print(df.dtypes)

# ubah kolom created_at jadi tipe tanggal, terus ambil tahunnya saja
df["created_at"] = pd.to_datetime(df["created_at"])
df["created_year"] = df["created_at"].dt.year

# --- Klasifikasi tipe atribut (masih menurut pemahaman saya sejauh ini) ---
# nominal      : name, owner_login, owner_type, language, license_name
# nominal biner: has_wiki, is_fork, archived (isinya True/False)
# numerik diskrit : stargazers_count, forks_count, open_issues_count, created_year
# numerik kontinu : size_kb

print()
print("===== 3. STATISTIK DESKRIPTIF =====")

kolom_numerik = ["stargazers_count", "forks_count", "open_issues_count", "size_kb"]

print("\nRata-rata, median, dst untuk kolom numerik:")
print(df[kolom_numerik].describe())

print("\nModus (nilai paling sering muncul):")
print(df[kolom_numerik].mode().iloc[0])

print("\nFrekuensi kolom kategorikal:")
print(df["language"].value_counts())
print()
print(df["owner_type"].value_counts())
print()
print(df["license_name"].value_counts().head(10))

# --- cek data yang hilang (missing value) ---
print("\n===== CEK MISSING VALUE =====")
print(df.isnull().sum())
# ternyata cuma kolom license_name yang ada nilai kosong.
# itu wajar, artinya repo tersebut memang tidak pasang lisensi apapun.
# jadi saya isi saja dengan "No License" daripada dihapus baris-nya.
df["license_name"] = df["license_name"].fillna("No License")

# --- cek outlier pakai metode IQR (yang diajarkan di kelas) ---
print("\n===== CEK OUTLIER (metode IQR) =====")
for kolom in ["stargazers_count", "forks_count", "size_kb"]:
    Q1 = df[kolom].quantile(0.25)
    Q3 = df[kolom].quantile(0.75)
    IQR = Q3 - Q1
    batas_bawah = Q1 - 1.5 * IQR
    batas_atas = Q3 + 1.5 * IQR
    jumlah_outlier = ((df[kolom] < batas_bawah) | (df[kolom] > batas_atas)).sum()
    print(f"{kolom}: ada {jumlah_outlier} outlier dari {len(df)} baris "
          f"(batas atas = {batas_atas:.0f})")

# Outlier di sini saya biarkan saja (tidak dihapus), soalnya kalau dilihat lagi
# repo dengan stars/forks sangat tinggi itu memang repo yang populer beneran,
# bukan salah input data. Jadi bukan error, cuma sebaran datanya memang lebar.

df.to_csv("cleaned_github_repos.csv", index=False)
print("\nData sudah dibersihkan (missing value diisi), disimpan ke cleaned_github_repos.csv")
