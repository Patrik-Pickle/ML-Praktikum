# visualize.py
# Tugas Praktikum Data Mining - Tahap 4: Visualisasi Data

import pandas as pd
import matplotlib.pyplot as plt
import os

df = pd.read_csv("cleaned_github_repos.csv")

os.makedirs("charts", exist_ok=True)

# ------------------------------------------------------------
# 1. Histogram - distribusi jumlah stars (numerik)
# ------------------------------------------------------------
# datanya sangat lebar (dari ribuan sampai ratusan ribu), jadi kalau
# langsung di-plot semua, grafiknya jadi susah dibaca (numpuk di kiri).
# makanya saya batasi cuma yang di bawah 100.000 stars saja biar kelihatan
# bentuk distribusinya. Sisanya (yang di atas itu) sudah ketahuan sebagai
# outlier di analysis.py tadi.
plt.figure(figsize=(7, 4.5))
plt.hist(df[df["stargazers_count"] < 100000]["stargazers_count"], bins=25,
         color="steelblue", edgecolor="black")
plt.title("Distribusi Jumlah Stars Repository (<100.000)")
plt.xlabel("Jumlah stars")
plt.ylabel("Jumlah repository")
plt.tight_layout()
plt.savefig("charts/1_histogram_stars.png")
plt.close()

# ------------------------------------------------------------
# 2. Bar chart - jumlah repo per bahasa pemrograman (kategorikal)
# ------------------------------------------------------------
plt.figure(figsize=(8, 4.5))
df["language"].value_counts().plot(kind="bar", color="seagreen")
plt.title("Jumlah Repository per Bahasa Pemrograman")
plt.xlabel("Bahasa")
plt.ylabel("Jumlah repository")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("charts/2_barchart_language.png")
plt.close()

# ------------------------------------------------------------
# 3. Scatter plot - hubungan stars dan forks
# ------------------------------------------------------------
plt.figure(figsize=(6.5, 5.5))
plt.scatter(df["stargazers_count"], df["forks_count"], alpha=0.4, s=15, color="darkorange")
plt.title("Hubungan Jumlah Stars dan Forks")
plt.xlabel("Jumlah stars")
plt.ylabel("Jumlah forks")
plt.tight_layout()
plt.savefig("charts/3_scatter_stars_forks.png")
plt.close()

# ------------------------------------------------------------
# 4. Correlation heatmap - antar kolom numerik
# ------------------------------------------------------------
kolom_numerik = ["stargazers_count", "forks_count", "open_issues_count", "size_kb"]
corr = df[kolom_numerik].corr()

plt.figure(figsize=(5.5, 4.5))
plt.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
plt.colorbar(label="Korelasi")
plt.xticks(range(len(kolom_numerik)), kolom_numerik, rotation=45, ha="right")
plt.yticks(range(len(kolom_numerik)), kolom_numerik)
# tulis angkanya di tiap kotak biar gampang dibaca
for i in range(len(kolom_numerik)):
    for j in range(len(kolom_numerik)):
        plt.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
plt.title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("charts/4_correlation_heatmap.png")
plt.close()

# ------------------------------------------------------------
# 5. Boxplot - jumlah stars per bahasa (dibatasi <100.000 juga)
# ------------------------------------------------------------
plt.figure(figsize=(9, 5))
data_boxplot = df[df["stargazers_count"] < 100000]
data_boxplot.boxplot(column="stargazers_count", by="language", rot=45)
plt.title("Sebaran Jumlah Stars per Bahasa Pemrograman")
plt.suptitle("")  # hilangkan judul otomatis dari pandas
plt.xlabel("Bahasa")
plt.ylabel("Jumlah stars")
plt.tight_layout()
plt.savefig("charts/5_boxplot_stars_language.png")
plt.close()

print("Grafik selesai dibuat, tersimpan di folder charts/")
