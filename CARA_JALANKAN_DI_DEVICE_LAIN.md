# 📱 Panduan Menjalankan OtotKu di HP & Perangkat Lain

Aplikasi **OtotKu** sudah terhubung dengan **GitHub Pages** dan **Database Cloud Terintegrasi (Zero-Config)** sehingga bisa langsung diakses dari HP Anda kapan saja tanpa perlu menyalakan laptop!

---

## 🌐 CARA 1: Akses Langsung via Link GitHub Pages (Paling Mudah — Dari Mana Saja)
*Bisa dibuka menggunakan paket data HP (4G/5G) maupun Wi-Fi tanpa perlu laptop menyala.*

1. Buka browser di HP Anda (Chrome di Android atau Safari di iPhone).
2. Kunjungi alamat resmi aplikasi Anda:
   👉 **https://rifatgh12.github.io/ototku/**
3. Atau klik tombol **📱 (Ikon HP)** di bagian atas aplikasi pada laptop, lalu **Scan QR Code** menggunakan kamera HP Anda.
4. **Database Sudah Terintegrasi Otomatis!**
   - Anda **tidak perlu** mengatur API Key atau membuat database secara manual.
   - Status di pojok kanan atas akan langsung bertuliskan **🟢 Cloud Aktif / Tersinkron** dengan kunci bawaan `rifatgh12`.
   - Setiap kali Anda mencatat makan, menyelesaikan set gym, atau mencatat berat badan di HP, datanya **otomatis tersimpan ke Cloud** dan langsung muncul di laptop Anda secara real-time!

---

## 📲 CARA 2: Pasang ke Layar Utama HP (Install PWA)
*Jadikan OtotKu seperti aplikasi native di HP dengan ikon tersendiri dan tampilan layar penuh tanpa bilah browser.*

Setelah membuka **https://rifatgh12.github.io/ototku/** di browser HP Anda:

### 🤖 Untuk Android (Google Chrome / Edge):
1. Ketuk ikon **titik tiga (⋮)** di pojok kanan atas browser.
2. Pilih menu **"Instal aplikasi"** atau **"Tambahkan ke Layar Utama" (Add to Home screen)**.
3. Ketuk **Instal**.
4. Ikon **OtotKu** sekarang sudah ada di home screen HP Anda!

### 🍎 Untuk iPhone / iPad (Safari):
1. Buka link di browser **Safari**.
2. Ketuk tombol **Bagikan (Share)** di bilah bawah layar (ikon kotak dengan panah ke atas).
3. Gulir ke bawah dan ketuk **"Tambah ke Layar Utama" (Add to Home Screen)**.
4. Ketuk **Tambah (Add)** di pojok kanan atas.

---

## ⚡ CARA 3: Jaringan Wi-Fi Lokal (Opsional / Offline LAN)
*Jika sedang tidak ada internet sama sekali dan ingin menjalankan dari laptop ke HP lewat Wi-Fi lokal:*

1. Di komputer/laptop Anda, klik dua kali file `jalankan_server.bat`.
2. Scan QR Code yang muncul di layar terminal menggunakan kamera HP Anda.

---

## ☁️ Tentang Database Cloud Terintegrasi
- **Provider Default:** `Cloud Terintegrasi (Otomatis)` — langsung aktif tanpa konfigurasi.
- **Kunci Sinkronisasi Default:** `rifatgh12` (otomatis sama di laptop dan HP).
- **Sinkronisasi Real-Time:** Menggunakan kombinasi Cloud REST JSON Storage + Server-Sent Events (SSE) real-time serta penyimpanan lokal (`localStorage`) untuk mode offline.
- **Dukungan Custom Database:** Jika suatu saat Anda ingin menggunakan database pribadi, menu **Pengaturan → Sinkronisasi Cloud** juga mendukung **Supabase** dan **Firebase**.
