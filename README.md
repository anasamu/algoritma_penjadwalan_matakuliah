# Perbandingan 3 algoritma penjadwalan mata kuliah greedy, backtracking, dan ILP

## Deskripsi

Proyek ini membandingkan tiga algoritma penjadwalan mata kuliah: Greedy, Backtracking, dan Integer Linear Programming (ILP). Tujuan dari proyek ini adalah untuk mengevaluasi kinerja masing-masing algoritma dalam hal waktu eksekusi, jumlah sesi terjadwal, dan penggunaan sumber daya seperti
ruangan dan slot waktu.

## Struktur Proyek

``` is_directory
jadwal_matakuliah/
├── data/
│   └── dataset.json
├── algortma/
│   ├── greedy.py
│   ├── backtracking.py
│   └── ilp.py
├── report/
│   ├── automated generate folder report
│       └── report_files.html
│       └── images.png
├── main.py
├── requirements.txt
├── utils.py
└── README.md
```

## Instalasi dependensi

```bash
pip install -r requirements.txt
```

## Menjalankan program

```bash
python main.py
```

## Hasil Contoh program

Hasil program akan menghasilkan laporan penjadwalan mata kuliah dalam format HTML yang berisi:

- Perbandingan waktu eksekusi algoritma

![Contoh Gambar Laporan](report/20250725_165510/performance_comparison.png)

- Perbandingan jumlah sesi terjadwal per hari

![Contoh Gambar Laporan](report/20250725_165510/schedule_comparison.png)

- Perbandingan penggunaan mata kuliah

![Contoh Gambar Laporan](report/20250725_165510/matakuliah_usage_comparison.png)

- Perbandingan penggunaan ruangan

![Contoh Gambar Laporan](report/20250725_165510/ruangan_usage_comparison.png)

- Perbandingan penggunaan slot waktu

![Contoh Gambar Laporan](report/20250725_165510/slot_waktu_usage_comparison.png)

[Lihat laporan penjadwalan lengkap (HTML)](report/20250725_165510/dataset_laporan_penjadwalan_lengkap.html)
