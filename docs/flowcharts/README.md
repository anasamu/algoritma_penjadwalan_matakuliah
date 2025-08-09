# Flowcharts

Koleksi diagram alur (flowcharts) untuk menjelaskan proses dan alur kerja sistem penjadwalan mata kuliah.

## Daftar Flowcharts

### 🔄 [Main System Flow](main-system-flow.md)
Diagram alur utama sistem mulai dari input dataset hingga output laporan.

### 🎯 [Greedy Algorithm Flowchart](greedy-flowchart.md)
Diagram alur detail untuk algoritma Greedy dengan strategi first-fit heuristic.

### 🔄 [Backtracking Algorithm Flowchart](backtracking-flowchart.md)
Diagram alur untuk algoritma Backtracking dengan pencarian sistematis dan backtrack.

### 🧮 [ILP Algorithm Flowchart](ilp-flowchart.md)
Diagram alur untuk algoritma Integer Linear Programming dengan optimisasi matematis.

### 📊 [Data Flow Diagram](data-flow-diagram.md)
Diagram aliran data mendetail mulai dari input, processing, hingga output sistem.

## Cara Membaca Flowcharts

### Simbol yang Digunakan

```
┌─────────────────┐     Proses/Operasi
│     Process     │
└─────────────────┘

    ┌───────┐           Keputusan/Kondisi
    │ Yes/No│
    └───┬───┘

        │               Aliran Data/Kontrol
        ▼

╔═══════════════════╗   Layer/Boundary
║     Layer         ║
╚═══════════════════╝
```

### Konvensi Penamaan

- **Boxes**: Menunjukkan operasi atau proses
- **Diamonds**: Menunjukkan decision points
- **Arrows**: Menunjukkan aliran eksekusi
- **Colors/Styles**: Membedakan kategori operasi

## Navigation

- [← Kembali ke Documentation](../README.md)
- [→ Lihat Diagrams](../diagrams/)

---

**Note**: Semua flowcharts menggunakan format text ASCII untuk kompatibilitas maksimal dan kemudahan edit.