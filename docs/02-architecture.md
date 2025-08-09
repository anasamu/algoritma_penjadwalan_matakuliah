# Architecture Documentation

## Arsitektur Sistem

Sistem Perbandingan Algoritma Penjadwalan Mata Kuliah menggunakan arsitektur modular yang memisahkan concern dengan jelas. Setiap komponen memiliki tanggung jawab spesifik dan dapat dikembangkan secara independen.

## Overview Arsitektur

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                      │
├─────────────────────────────────────────────────────────────┤
│  HTML Reports  │  Charts/Graphs  │  Performance Metrics    │
└─────────────────────────────────────────────────────────────┘
                                ▲
                                │
┌─────────────────────────────────────────────────────────────┐
│                     APPLICATION LAYER                       │
├─────────────────────────────────────────────────────────────┤
│         main.py (Orchestrator)                             │
│    ┌─────────────┬─────────────┬─────────────┐              │
│    │   Greedy    │ Backtracking│     ILP     │              │
│    │ Scheduler   │  Scheduler  │  Scheduler  │              │
│    └─────────────┴─────────────┴─────────────┘              │
└─────────────────────────────────────────────────────────────┘
                                ▲
                                │
┌─────────────────────────────────────────────────────────────┐
│                      SERVICE LAYER                          │
├─────────────────────────────────────────────────────────────┤
│  utils.py (Utility Functions & Report Generation)          │
│  • Data Loading        • Time Conversion                   │
│  • Conflict Detection  • Report Generation                 │
│  • Statistics          • Visualization                     │
└─────────────────────────────────────────────────────────────┘
                                ▲
                                │
┌─────────────────────────────────────────────────────────────┐
│                       DATA LAYER                            │
├─────────────────────────────────────────────────────────────┤
│  JSON Dataset    │   HTML Template   │   Generated Reports │
│  • Dosen         │   • Structure     │   • Statistics      │
│  • Mata Kuliah   │   • Styling       │   • Charts          │
│  • Ruangan       │   • Placeholders  │   • Schedules       │
│  • Slot Waktu    │                   │                     │
└─────────────────────────────────────────────────────────────┘
```

## Komponen Sistem

### 1. Main Application (main.py)

**Fungsi**: Orchestrator utama yang mengkoordinasikan seluruh proses
**Tanggung Jawab**:
- Memuat dataset dari file JSON
- Menginisialisasi dan menjalankan semua scheduler
- Mengumpulkan hasil dari setiap algoritma
- Memicu pembuatan laporan komprehensif

```python
# Flow eksekusi utama
Dataset Loading → Algorithm Execution → Result Collection → Report Generation
```

### 2. Algorithm Layer

#### 2.1 Greedy Scheduler (`algoritma/greedy.py`)
**Strategi**: First-fit heuristic dengan prioritas mata kuliah
**Karakteristik**:
- Kompleksitas waktu: O(n²) 
- Memory usage: Rendah
- Solusi: Cepat tapi tidak optimal

**Core Methods**:
- `solve()`: Menjalankan algoritma greedy
- `is_conflict()`: Deteksi konflik ruangan/dosen
- `mark_used()`: Menandai slot yang telah digunakan
- `calculate_stats()`: Menghitung statistik performa

#### 2.2 Backtracking Scheduler (`algoritma/backtrack.py`)
**Strategi**: Systematic search dengan backtracking
**Karakteristik**:
- Kompleksitas waktu: Exponential (worst case)
- Memory usage: Sedang
- Solusi: Lebih baik dari greedy

**Core Methods**:
- `solve()`: Implementasi backtracking
- `backtrack()`: Recursive backtracking function
- `is_valid_assignment()`: Validasi penempatan
- `undo_assignment()`: Membatalkan penempatan

#### 2.3 ILP Scheduler (`algoritma/ilp.py`)
**Strategi**: Mathematical optimization using PuLP
**Karakteristik**:
- Kompleksitas waktu: Polynomial (rata-rata)
- Memory usage: Tinggi
- Solusi: Optimal atau near-optimal

**Core Methods**:
- `solve()`: Setup dan solve ILP model
- `_generate_possible_time_slots()`: Generate time variables
- `_create_variables()`: Membuat decision variables
- `_add_constraints()`: Menambahkan constraint

### 3. Utility Layer (utils.py)

**Fungsi**: Menyediakan fungsi-fungsi bantuan dan report generation
**Komponen Utama**:

#### 3.1 Data Processing
```python
def load_dataset(filename)          # Memuat data JSON
def sks_to_minutes(sks)            # Konversi SKS ke menit
def time_to_minutes(time_str)      # Konversi waktu ke menit
def minutes_to_time(total_minutes) # Konversi menit ke waktu
```

#### 3.2 Analysis Functions
```python
def get_usage_counts(schedule, key) # Hitung penggunaan resource
def get_dosen_name(dosen_id, list)  # Ambil nama dosen
def calculate_conflicts(schedule)    # Deteksi konflik
```

#### 3.3 Report Generation
```python
def generate_full_report_html()     # Generate laporan lengkap
def create_performance_chart()      # Buat grafik performa
def create_usage_analysis()         # Analisis penggunaan resource
```

### 4. Data Layer

#### 4.1 Dataset Structure (dataset.json)
```json
{
  "dosen": [
    {
      "id": number,
      "nama": string,
      "bidang_keahlian": string,
      "email": string
    }
  ],
  "matakuliah": [
    {
      "id": number,
      "nama": string,
      "semester": number,
      "sks": number,
      "dosen_id": number,
      "jumlah_mahasiswa": number
    }
  ],
  "ruangan": [
    {
      "id": number,
      "nama": string,
      "kapasitas": number
    }
  ],
  "slot_waktu": [
    {
      "hari": string,
      "jam_mulai": string,
      "jam_selesai": string
    }
  ]
}
```

#### 4.2 Report Template (report_template.html)
- Template HTML untuk laporan
- Placeholder untuk data dinamis
- Styling dan layout responsif

## Design Patterns

### 1. Strategy Pattern
Setiap algoritma penjadwalan mengimplementasikan interface yang sama:
```python
class SchedulerInterface:
    def solve(self) -> dict
    def calculate_stats(self) -> dict
```

### 2. Template Method Pattern
Semua scheduler mengikuti template eksekusi yang sama:
1. Initialize data structures
2. Execute algorithm logic
3. Calculate statistics
4. Return standardized result

### 3. Factory Pattern
Main.py bertindak sebagai factory untuk scheduler instances:
```python
schedulers = {
    "Backtracking": BacktrackingScheduler(files),
    "Greedy": GreedyScheduler(files),
    "ILP": ILPScheduler(files),
}
```

## Data Flow

### 1. Input Processing
```
JSON Dataset → Validation → Data Structures → Algorithm Input
```

### 2. Algorithm Execution
```
For each algorithm:
  Initialize → Execute → Collect Results → Calculate Stats
```

### 3. Output Generation
```
Algorithm Results → Data Aggregation → Visualization → HTML Report
```

## Scalability Considerations

### 1. Memory Management
- Lazy loading untuk dataset besar
- Garbage collection setelah setiap algoritma
- Efficient data structures

### 2. Performance Optimization
- Algoritma dapat dijalankan parallel
- Caching untuk operasi berulang
- Optimized conflict detection

### 3. Extensibility
- Plugin architecture untuk algoritma baru
- Configurable parameters
- Modular report components

## Security & Reliability

### 1. Data Validation
- JSON schema validation
- Input sanitization
- Error handling untuk data corrupt

### 2. Error Recovery
- Graceful degradation
- Comprehensive logging
- Rollback mechanisms

### 3. Testing Strategy
- Unit tests untuk setiap komponen
- Integration tests untuk workflow
- Performance benchmarking

---

[← System Overview](01-system-overview.md) | [Lanjut ke Algorithms →](03-algorithms.md)