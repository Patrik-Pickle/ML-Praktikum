# scrape_github.py
# Tugas Praktikum Data Mining - Tahap 1: Scraping Dataset
# Nama    : Patrik
# Sumber  : GitHub Search API (https://api.github.com/search/repositories)
#
# Kenapa pakai ini: saya awalnya mau scraping web biasa pakai BeautifulSoup,
# tapi ternyata situs yang mau saya coba datanya sedikit (kurang dari 1500 baris).
# Jadi saya pakai library requests untuk ambil data dari GitHub (API publik,
# gratis, tidak perlu login/API key) supaya jumlah barisnya cukup.

import requests
import pandas as pd
import time

# beberapa bahasa pemrograman yang mau diambil datanya
bahasa_list = ["Python", "JavaScript", "TypeScript", "Java", "Go",
                "Rust", "C++", "PHP", "C#", "Ruby"]

url = "https://api.github.com/search/repositories"
semua_data = []

for bahasa in bahasa_list:
    print("Mengambil data bahasa:", bahasa)
    # ambil 2 halaman x 100 data = 200 repo per bahasa
    for halaman in range(1, 3):
        params = {
            "q": f"language:{bahasa} stars:>50",
            "sort": "stars",
            "order": "desc",
            "per_page": 100,
            "page": halaman
        }
        response = requests.get(url, params=params)
        hasil = response.json()
        items = hasil.get("items", [])
        print("  halaman", halaman, "-> dapat", len(items), "repo")

        for repo in items:
            owner = repo.get("owner") or {}
            lisensi = repo.get("license") or {}
            semua_data.append({
                "name": repo.get("name"),
                "owner_login": owner.get("login"),
                "owner_type": owner.get("type"),
                "language": repo.get("language"),
                "stargazers_count": repo.get("stargazers_count"),
                "forks_count": repo.get("forks_count"),
                "open_issues_count": repo.get("open_issues_count"),
                "size_kb": repo.get("size"),
                "license_name": lisensi.get("spdx_id"),
                "has_wiki": repo.get("has_wiki"),
                "is_fork": repo.get("fork"),
                "archived": repo.get("archived"),
                "created_at": repo.get("created_at"),
            })

        time.sleep(7)  # kasih jeda biar tidak kena limit dari GitHub

# ubah jadi dataframe lalu simpan ke csv (data mentah, belum dibersihkan)
df = pd.DataFrame(semua_data)
df.to_csv("raw_github_repos.csv", index=False)
print("Selesai. Total baris:", len(df))
print("Disimpan sebagai raw_github_repos.csv")
