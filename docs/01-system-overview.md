# System Overview

## Tentang Sistem

Sistem Perbandingan Algoritma Penjadwalan Mata Kuliah adalah aplikasi penelitian yang dirancang untuk membandingkan efektivitas dan efisiensi tiga algoritma berbeda dalam menyelesaikan masalah penjadwalan mata kuliah di perguruan tinggi.

## Tujuan Sistem

### Tujuan Utama
- **Membandingkan Performa**: Menganalisis waktu eksekusi, tingkat keberhasilan, dan kualitas solusi dari tiga algoritma penjadwalan
- **Evaluasi Efisiensi**: Mengukur penggunaan sumber daya (ruangan, waktu, dosen) oleh masing-masing algoritma
- **Penelitian Akademik**: Menyediakan basis untuk penelitian lebih lanjut dalam optimisasi penjadwalan

### Tujuan Spesifik
- Mengidentifikasi algoritma terbaik untuk dataset tertentu
- Menganalisis kompleksitas waktu dan ruang setiap algoritma
- Memberikan visualisasi yang jelas tentang hasil penjadwalan
- Menghasilkan laporan komprehensif untuk analisis lebih lanjut

## Fitur Utama

### 🔍 **Perbandingan Multi-Algoritma**
- **Greedy Algorithm**: Pendekatan heuristik dengan pemilihan optimal lokal
- **Backtracking Algorithm**: Pencarian sistematis dengan backtrack
- **Integer Linear Programming (ILP)**: Optimisasi matematis dengan constraint

### 📊 **Analisis Performa Komprehensif**
- Pengukuran waktu eksekusi real-time
- Perhitungan tingkat keberhasilan penjadwalan
- Analisis penggunaan sumber daya
- Deteksi dan pelaporan konflik

### 📈 **Visualisasi dan Pelaporan**
- Grafik perbandingan performa algoritma
- Tabel distribusi sesi per hari
- Analisis penggunaan ruangan dan slot waktu
- Laporan HTML interaktif dengan gambar

### ⚙️ **Fleksibilitas Dataset**
- Format JSON yang mudah diedit
- Dukungan untuk berbagai ukuran dataset
- Konfigurasi slot waktu yang fleksibel
- Pengelolaan constraint kapasitas ruangan

## Studi Kasus

Sistem ini dirancang untuk menyelesaikan permasalahan penjadwalan mata kuliah dengan karakteristik:

### Data Input
- **Dosen**: ID, nama, bidang keahlian, email
- **Mata Kuliah**: ID, nama, semester, SKS, dosen pengampu, jumlah mahasiswa
- **Ruangan**: ID, nama, kapasitas
- **Slot Waktu**: Hari, jam mulai, jam selesai

### Constraint yang Ditangani
- **Konflik Dosen**: Satu dosen tidak boleh mengajar di waktu yang sama
- **Konflik Ruangan**: Satu ruangan tidak boleh digunakan bersamaan
- **Kapasitas**: Jumlah mahasiswa tidak boleh melebihi kapasitas ruangan
- **Durasi**: Durasi kuliah disesuaikan dengan jumlah SKS

### Output yang Dihasilkan
- Jadwal lengkap untuk semua mata kuliah
- Statistik performa setiap algoritma
- Analisis konflik dan solusi
- Laporan visual dan terstruktur

## Keunggulan Sistem

### 🚀 **Performa Tinggi**
- Implementasi algoritma yang dioptimasi
- Penanganan dataset besar secara efisien
- Waktu eksekusi yang dapat diukur dan dibandingkan

### 📋 **Dokumentasi Lengkap**
- Dokumentasi API yang detail
- Panduan penggunaan yang mudah diikuti
- Contoh dataset dan konfigurasi

### 🔧 **Mudah Dikustomisasi**
- Struktur kode yang modular
- Parameter yang dapat disesuaikan
- Ekstensibilitas untuk algoritma baru

### 📊 **Analisis Mendalam**
- Metrik performa yang komprehensif
- Visualisasi yang informatif
- Laporan yang dapat digunakan untuk publikasi

## Penggunaan Sistem

Sistem ini cocok untuk:

### 🎓 **Institusi Pendidikan**
- Perguruan tinggi yang membutuhkan sistem penjadwalan otomatis
- Optimisasi penggunaan sumber daya akademik
- Peningkatan efisiensi operasional

### 🔬 **Penelitian Akademik**
- Studi perbandingan algoritma optimisasi
- Penelitian dalam bidang Operations Research
- Pengembangan metode penjadwalan baru

### 💼 **Pengembangan Sistem**
- Template untuk pengembangan sistem penjadwalan
- Referensi implementasi algoritma klasik
- Basis untuk sistem enterprise yang lebih besar

## Teknologi yang Digunakan

### 🐍 **Python 3.x**
- Bahasa pemrograman utama
- Ekosistem library yang kaya
- Mudah untuk dikembangkan dan dipelihara

### 📦 **Dependencies**
- **PuLP**: Untuk optimisasi Integer Linear Programming
- **Matplotlib**: Untuk visualisasi dan pembuatan grafik
- **JSON**: Untuk format data yang standar

### 📄 **Output Format**
- **HTML**: Laporan interaktif yang dapat dibuka di browser
- **PNG**: Gambar grafik untuk dokumentasi
- **JSON**: Data terstruktur untuk analisis lanjutan

---

[← Kembali ke README](README.md) | [Lanjut ke Architecture →](02-architecture.md)