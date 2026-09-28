import os
import re
import time
import json
from google import genai

# 1. Konfigurasi Client Gemini
API_KEY = "MASUKKAN_GEMINI_API_KEY_ANDA"
client = genai.Client(api_key=API_KEY)

# 2. Path File & Direktori
OUTPUT_DIR = os.path.join("src", "pages", "blog")
JSON_PATH = os.path.join("src", "data", "articles.json")

# 3. Daftar Artikel Target
daftar_artikel = [
    {
        "judul": "Jasa Pasang CCTV Karangasem: Panduan Biaya & Pemilihan Titik Kamera Rumah",
        "kategori": "CCTV & Keamanan",
        "kategoriId": "cctv",
        "link_layanan": "/cctv/",
        "nama_layanan": "jasa pasang CCTV Karangasem"
    },
    {
        "judul": "Tips Memilih Kamera CCTV Outdoor Tahan Cuaca Hujan untuk Vila di Bali",
        "kategori": "CCTV & Keamanan",
        "kategoriId": "cctv",
        "link_layanan": "/cctv/",
        "nama_layanan": "paket pemasangan CCTV vila Bali"
    },
    {
        "judul": "Cara Setting Pantau CCTV Lewat HP Android & iPhone Jarak Jauh Tanpa Ribet",
        "kategori": "CCTV & Keamanan",
        "kategoriId": "cctv",
        "link_layanan": "/cctv/",
        "nama_layanan": "layanan instalasi CCTV Bali"
    },
    {
        "judul": "Perbedaan Kamera CCTV Analog HD vs IP Camera PoE: Mana yang Lebih Bagus?",
        "kategori": "CCTV & Keamanan",
        "kategoriId": "cctv",
        "link_layanan": "/cctv/",
        "nama_layanan": "teknisi CCTV profesional Bali"
    },
    {
        "judul": "Pasang CCTV Toko dan UMKM di Amlapura: Cegah Kehilangan & Pantau Kasir",
        "kategori": "CCTV & Keamanan",
        "kategoriId": "cctv",
        "link_layanan": "/cctv/",
        "nama_layanan": "jasa pasang CCTV tempat usaha"
    },
    {
        "judul": "Jasa Pembuatan Website Karangasem: Solusi UMKM & Bisnis Go Digital",
        "kategori": "Web Development",
        "kategoriId": "website",
        "link_layanan": "/website/",
        "nama_layanan": "jasa pembuatan website Karangasem"
    },
    {
        "judul": "Keuntungan Website Direct Booking untuk Vila & Homestay di Candidasa dan Amed",
        "kategori": "Web Development",
        "kategoriId": "website",
        "link_layanan": "/website/",
        "nama_layanan": "pembuatan website vila Bali"
    },
    {
        "judul": "Cara Agar Usaha dan Toko Muncul di Google Maps & Halaman 1 Google Bali",
        "kategori": "Web Development",
        "kategoriId": "website",
        "link_layanan": "/website/",
        "nama_layanan": "jasa SEO lokal dan website Bali"
    },
    {
        "judul": "Kenapa Kecepatan Loading Website Sangat Penting untuk Promosi Pariwisata Bali",
        "kategori": "Web Development",
        "kategoriId": "website",
        "link_layanan": "/website/",
        "nama_layanan": "jasa web developer profesional Bali"
    },
    {
        "judul": "Berapa Biaya Pembuatan Website Company Profile & Toko Online di Bali?",
        "kategori": "Web Development",
        "kategoriId": "website",
        "link_layanan": "/website/",
        "nama_layanan": "paket pembuatan website Bali Nusa Media"
    }
]

def buat_slug(judul):
    slug = judul.lower()
    slug = re.sub(r'[^a-z0-9\s-]', '', slug)
    return re.sub(r'[\s-]+', '-', slug).strip('-')

def bersihkan_html(konten):
    konten = re.sub(r'^```html\s*', '', konten, flags=re.MULTILINE)
    konten = re.sub(r'^```\s*$', '', konten, flags=re.MULTILINE)
    return konten.strip()

def format_astro(judul, slug, kategori, deskripsi, tanggal, konten, gambar):
    return f"""---
// src/pages/blog/{slug}.astro
import BlogLayout from "../../layouts/BlogLayout.astro";
---

<BlogLayout category="{kategori}" date="{tanggal}" dateIso="2026-09-22" description="{deskripsi}" image="{gambar}" readTime="5 menit" slug="{slug}" title="{judul}">
{konten}
</BlogLayout>
"""

# FUNGSI OTOMATIS TAMBAH KE ARTICLES.JSON
def sync_ke_json(judul, slug, kategori_id, kategori_label, ringkasan, gambar):
    os.makedirs(os.path.dirname(JSON_PATH), exist_ok=True)
    
    data = []
    if os.path.exists(JSON_PATH):
        try:
            with open(JSON_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = []

    # Cek apakah artikel sudah terdaftar agar tidak duplikat
    if any(item.get("slug") == slug for item in data):
        return

    artikel_baru = {
        "title": judul,
        "slug": slug,
        "kategoriId": kategori_id,
        "kategoriLabel": kategori_label,
        "ringkasan": ringkasan,
        "tanggal": "22 September 2026",
        "waktuBaca": "5 menit",
        "gambar": gambar,
        "isFeatured": False
    }

    # Sisipkan di urutan pertama (paling baru)
    data.insert(0, artikel_baru)

    with open(JSON_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"   📋 Data otomatis ditambahkan ke '{JSON_PATH}'")

def generate_articles():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    jumlah = len(daftar_artikel)
    print(f"\n🚀 Memulai Auto-Generator Blog & JSON... Total: {jumlah} artikel.\n")

    for index, item in enumerate(daftar_artikel, start=1):
        judul = item["judul"]
        kategori = item["kategori"]
        kategori_id = item["kategoriId"]
        link = item["link_layanan"]
        layanan = item["nama_layanan"]
        
        slug = buat_slug(judul)
        path_file = os.path.join(OUTPUT_DIR, f"{slug}.astro")
        gambar = "/assets/img/cctv/cctv-hero.webp" if "cctv" in kategori_id else "/assets/img/hero.webp"
        deskripsi = f"Panduan lengkap mengenai {judul}. Temukan solusi instalasi dan pengerjaan terstandar di Bali bersama Bali Nusa Media."

        # Jika file sudah ada, pastikan tetap sinkron ke JSON lalu skip
        if os.path.exists(path_file):
            sync_ke_json(judul, slug, kategori_id, kategori, deskripsi, gambar)
            print(f"[{index}/{jumlah}] ⏭️ Dilewati (Sudah ada): {slug}.astro")
            continue

        print(f"[{index}/{jumlah}] ⏳ Menulis artikel: '{judul}'...")

        prompt = f"""Tulis artikel edukasi dan panduan bisnis profesional sepanjang 450 - 600 kata dalam bahasa Indonesia dengan judul: '{judul}'.
Target pembaca: Pemilik rumah, pengelola vila, manajer operasional, dan pemilik UMKM di Karangasem (Amlapura, Candidasa, Amed, Sidemen) dan wilayah Bali lainnya (Denpasar, Badung, Gianyar).
Brand penyedia layanan: Bali Nusa Media.

Ketentuan penulisan:
1. Gunakan tag HTML terstruktur: <h2> untuk subjudul, <p> untuk paragraf, <ul>/<li> untuk poin penting, dan <strong> untuk penekanan.
2. Sisipkan 1 kali tautan kontekstual alami ke halaman layanan kami menggunakan tag: <a href="{link}">{layanan}</a>.
3. Hindari bahasa kaku/terlalu teoritis; gunakan nada teknisi lapangan yang ramah, jujur, mengutamakan keselamatan, dan solutif.
4. JANGAN gunakan tag ```html atau pembungkus markdown codeblock.
5. JANGAN berikan tag <html>, <head>, atau <body>, cukup konten artikelnya saja."""

        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                response = client.models.generate_content(
                    model='gemini-3.6-flash',
                    contents=prompt,
                )
                konten_bersih = bersihkan_html(response.text)

                # 1. Simpan file .astro
                file_final = format_astro(judul, slug, kategori, deskripsi, "22 September 2026", konten_bersih, gambar)
                with open(path_file, "w", encoding="utf-8") as f:
                    f.write(file_final)

                # 2. Update data ke articles.json secara otomatis
                sync_ke_json(judul, slug, kategori_id, kategori, deskripsi, gambar)

                print(f"[{index}/{jumlah}] ✅ Selesai: {slug}.astro")
                break

            except Exception as e:
                err_msg = str(e)
                if "503" in err_msg or "UNAVAILABLE" in err_msg:
                    print(f"[{index}/{jumlah}] ⚠️ Server sibuk (503). Menunggu 15 detik sebelum coba lagi (Percobaan {attempt}/{max_retries})...")
                    time.sleep(15)
                else:
                    print(f"[{index}/{jumlah}] ❌ Error pada '{judul}': {e}")
                    break

        time.sleep(10)

if __name__ == "__main__":
    generate_articles()
    print("\n🎉 Selesai! Semua artikel telah dibuat dan otomatis terdaftar di katalog blog.")