# Usage Guide

## Panduan Instalasi dan Penggunaan

Panduan lengkap untuk menginstal, mengkonfigurasi, dan menjalankan sistem perbandingan algoritma penjadwalan mata kuliah.

---

## Persyaratan Sistem

### Hardware Requirements
- **RAM**: Minimum 4GB, Recommended 8GB atau lebih
- **Storage**: Minimum 1GB free space
- **CPU**: Multi-core processor recommended untuk performa optimal

### Software Requirements
- **Python**: Versi 3.8 atau lebih baru
- **Operating System**: Windows, macOS, atau Linux
- **Internet Connection**: Untuk instalasi dependencies

---

## Instalasi

### 1. Clone Repository

```bash
# Clone repository
git clone https://github.com/anasamu/algoritma_penjadwalan_matakuliah.git

# Masuk ke direktori project
cd algoritma_penjadwalan_matakuliah
```

### 2. Setup Virtual Environment (Recommended)

```bash
# Buat virtual environment
python -m venv venv

# Aktifkan virtual environment
# Untuk Linux/Mac:
source venv/bin/activate

# Untuk Windows:
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
# Install semua dependencies yang diperlukan
pip install -r requirements.txt
```

#### Dependencies yang Diinstall:
- **matplotlib**: Untuk visualisasi dan pembuatan grafik
- **pulp**: Untuk optimisasi Integer Linear Programming

### 4. Verifikasi Instalasi

```bash
# Test run untuk memastikan instalasi berhasil
python main.py
```

Jika berhasil, Anda akan melihat output seperti:
```
Running Backtracking Scheduler...
Backtracking Scheduler finished.
Running Greedy Scheduler...
Greedy Scheduler finished.
Running ILP Scheduler...
Welcome to the CBC MILP Solver...
ILP Scheduler finished.

Laporan lengkap berhasil dibuat: report/YYYYMMDD_HHMMSS/dataset_laporan_penjadwalan_lengkap.html
```

---

## Menjalankan Program

### Basic Usage

```bash
# Jalankan dengan dataset default
python main.py
```

### Struktur Output

Program akan menghasilkan:
1. **Folder report** dengan timestamp
2. **HTML report** lengkap dengan analisis
3. **Grafik PNG** untuk visualisasi performa
4. **Console output** dengan progress info

### Sample Output Structure
```
report/
└── 20250809_112827/
    ├── dataset_laporan_penjadwalan_lengkap.html
    ├── performance_comparison.png
    ├── schedule_comparison.png
    ├── matakuliah_usage_comparison.png
    ├── ruangan_usage_comparison.png
    └── slot_waktu_usage_comparison.png
```

---

## Konfigurasi Dataset

### Format Dataset

Dataset menggunakan format JSON dengan struktur berikut:

```json
{
  "dosen": [...],
  "matakuliah": [...],
  "ruangan": [...],
  "slot_waktu": [...]
}
```

### Menggunakan Dataset Custom

1. **Buat file JSON baru** di folder `data/`
2. **Update main.py** untuk menggunakan dataset baru:

```python
# Ganti nama dataset
dataset_name = 'dataset_custom'  # tanpa ekstensi .json
files_dataset = 'data/' + dataset_name + '.json'
```

### Contoh Dataset Minimal

```json
{
  "dosen": [
    {
      "id": 1,
      "nama": "Dr. Ahmad",
      "bidang_keahlian": "Pemrograman",
      "email": "ahmad@univ.edu"
    }
  ],
  "matakuliah": [
    {
      "id": 1,
      "nama": "Algoritma Dasar",
      "semester": 2,
      "sks": 3,
      "dosen_id": 1,
      "jumlah_mahasiswa": 30
    }
  ],
  "ruangan": [
    {
      "id": 1,
      "nama": "Lab Komputer",
      "kapasitas": 35
    }
  ],
  "slot_waktu": [
    {
      "hari": "Senin",
      "jam_mulai": "08:00",
      "jam_selesai": "12:00"
    }
  ]
}
```

---

## Customization Options

### 1. Memilih Algoritma Tertentu

```python
# Jalankan hanya algoritma tertentu
schedulers = {
    "Greedy": GreedyScheduler(files),
    # "Backtracking": BacktrackingScheduler(files),  # Commented out
    # "ILP": ILPScheduler(files),  # Commented out
}
```

### 2. Mengubah Parameter Waktu

```python
# Dalam utils.py, modify fungsi sks_to_minutes
def sks_to_minutes(sks):
    if sks == 2:
        return 100  # Ubah dari 90 menit ke 100 menit
    elif sks == 3:
        return 150  # Ubah dari 135 menit ke 150 menit
    return 0
```

### 3. Custom Report Filename

```python
# Ubah nama laporan
import datetime
timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
report_filename = f"custom_report_{timestamp}.html"
```

### 4. Menambahkan Algoritma Baru

1. **Buat file baru** di folder `algoritma/`
2. **Implement interface** yang sama:

```python
class CustomScheduler:
    def __init__(self, data):
        # Initialize data
        pass
    
    def solve(self):
        # Implement algorithm
        return {
            'schedule': [...],
            'stats': {...}
        }
    
    def calculate_stats(self):
        # Calculate performance stats
        pass
```

3. **Tambahkan ke main.py**:

```python
from algoritma.custom import CustomScheduler

schedulers = {
    "Custom": CustomScheduler(files),
    # ... other schedulers
}
```

---

## Advanced Usage

### 1. Batch Processing Multiple Datasets

```python
import os
import glob

# Process semua dataset di folder data/
dataset_files = glob.glob('data/*.json')

for dataset_file in dataset_files:
    print(f"Processing {dataset_file}...")
    
    # Load dataset
    files = utils.load_dataset(dataset_file)
    
    # Run algorithms
    algorithm_results = {}
    for algo_name, scheduler_class in scheduler_classes.items():
        scheduler = scheduler_class(files)
        results = scheduler.solve()
        algorithm_results[algo_name] = results
    
    # Generate report
    dataset_name = os.path.basename(dataset_file).replace('.json', '')
    report_filename = f"{dataset_name}_comparison_report.html"
    utils.generate_full_report_html(files, algorithm_results, report_filename)
```

### 2. Performance Benchmarking

```python
import time
import statistics

def benchmark_algorithm(scheduler_class, data, runs=5):
    """Run algorithm multiple times and get average performance"""
    times = []
    
    for i in range(runs):
        scheduler = scheduler_class(data)
        start_time = time.time()
        results = scheduler.solve()
        execution_time = time.time() - start_time
        times.append(execution_time)
    
    return {
        'mean_time': statistics.mean(times),
        'median_time': statistics.median(times),
        'std_dev': statistics.stdev(times) if len(times) > 1 else 0,
        'min_time': min(times),
        'max_time': max(times)
    }

# Usage
benchmark_results = {}
for algo_name, scheduler_class in scheduler_classes.items():
    benchmark_results[algo_name] = benchmark_algorithm(scheduler_class, files)
    print(f"{algo_name}: {benchmark_results[algo_name]}")
```

### 3. Memory Usage Monitoring

```python
import psutil
import os

def monitor_memory_usage():
    """Monitor memory usage during execution"""
    process = psutil.Process(os.getpid())
    memory_info = process.memory_info()
    return {
        'rss': memory_info.rss / 1024 / 1024,  # MB
        'vms': memory_info.vms / 1024 / 1024   # MB
    }

# Monitor during execution
print("Memory before:", monitor_memory_usage())
results = scheduler.solve()
print("Memory after:", monitor_memory_usage())
```

### 4. Export Results to Different Formats

```python
import json
import csv
import pandas as pd

def export_schedule_to_csv(schedule, filename):
    """Export schedule to CSV format"""
    if schedule:
        df = pd.DataFrame(schedule)
        df.to_csv(filename, index=False)
        print(f"Schedule exported to {filename}")

def export_results_to_json(algorithm_results, filename):
    """Export all results to JSON"""
    with open(filename, 'w') as f:
        json.dump(algorithm_results, f, indent=2, ensure_ascii=False)
    print(f"Results exported to {filename}")

# Usage
for algo_name, results in algorithm_results.items():
    export_schedule_to_csv(results['schedule'], f"{algo_name}_schedule.csv")

export_results_to_json(algorithm_results, "all_results.json")
```

---

## Troubleshooting

### Common Issues dan Solutions

#### 1. ModuleNotFoundError
```
ModuleNotFoundError: No module named 'matplotlib'
```
**Solution**:
```bash
pip install matplotlib pulp
```

#### 2. Permission Error saat Generate Report
```
PermissionError: [Errno 13] Permission denied: 'report/'
```
**Solution**:
```bash
# Buat folder report secara manual
mkdir report
chmod 755 report
```

#### 3. Memory Error pada Dataset Besar
```
MemoryError: Unable to allocate array
```
**Solutions**:
- Kurangi ukuran dataset
- Gunakan algoritma Greedy saja untuk dataset besar
- Tambah RAM atau gunakan virtual memory

#### 4. ILP Solver Error
```
PulpSolverError: PuLP: Error while executing the 'cbc' command
```
**Solutions**:
```bash
# Install CBC solver secara manual
sudo apt-get install coinor-cbc  # Ubuntu/Debian
brew install coin-or-tools/tap/cbc  # macOS
```

#### 5. JSON Decode Error
```
json.decoder.JSONDecodeError: Invalid JSON format
```
**Solution**:
- Validasi format JSON menggunakan online validator
- Pastikan tidak ada trailing comma
- Check encoding file (harus UTF-8)

#### 6. Empty Schedule Results
```
Warning: No schedule generated by algorithm X
```
**Possible Causes**:
- Dataset constraints terlalu ketat
- Tidak ada ruangan dengan kapasitas yang cukup
- Slot waktu tidak mencukupi

**Solutions**:
- Review kapasitas ruangan vs jumlah mahasiswa
- Tambah slot waktu atau ruangan
- Kurangi jumlah mata kuliah untuk testing

---

## Performance Tips

### 1. Optimisasi untuk Dataset Besar

```python
# Skip algoritma yang lambat untuk dataset > 50 mata kuliah
total_courses = len(files['matakuliah'])

schedulers = {}
if total_courses <= 30:
    schedulers.update({
        "Backtracking": BacktrackingScheduler(files),
        "ILP": ILPScheduler(files),
    })

# Greedy selalu dijalankan karena cepat
schedulers["Greedy"] = GreedyScheduler(files)
```

### 2. Parallel Processing

```python
import multiprocessing
from concurrent.futures import ProcessPoolExecutor

def run_algorithm(args):
    """Helper function untuk parallel processing"""
    algo_name, scheduler_class, data = args
    scheduler = scheduler_class(data)
    return algo_name, scheduler.solve()

# Run algorithms in parallel
with ProcessPoolExecutor(max_workers=3) as executor:
    tasks = [
        ("Greedy", GreedyScheduler, files),
        ("Backtracking", BacktrackingScheduler, files),
        ("ILP", ILPScheduler, files)
    ]
    
    results = executor.map(run_algorithm, tasks)
    algorithm_results = dict(results)
```

### 3. Progress Monitoring

```python
import sys

def print_progress(message):
    """Print progress dengan timestamp"""
    from datetime import datetime
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")
    sys.stdout.flush()

# Usage dalam loop
for algo_name, scheduler_instance in schedulers.items():
    print_progress(f"Starting {algo_name} algorithm...")
    results = scheduler_instance.solve()
    print_progress(f"Completed {algo_name} in {results['stats']['execution_time']:.2f}s")
```

---

## Integration dengan Sistem Lain

### 1. REST API Wrapper

```python
from flask import Flask, request, jsonify
import tempfile
import os

app = Flask(__name__)

@app.route('/schedule', methods=['POST'])
def generate_schedule():
    try:
        # Get dataset from request
        data = request.json
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            json.dump(data, f)
            temp_file = f.name
        
        # Process
        files = utils.load_dataset(temp_file)
        scheduler = GreedyScheduler(files)
        results = scheduler.solve()
        
        # Cleanup
        os.unlink(temp_file)
        
        return jsonify({
            'success': True,
            'schedule': results['schedule'],
            'stats': results['stats']
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
```

### 2. Database Integration

```python
import sqlite3
import json

def save_results_to_database(algorithm_results, dataset_name):
    """Save results to SQLite database"""
    conn = sqlite3.connect('scheduling_results.db')
    cursor = conn.cursor()
    
    # Create table if not exists
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dataset_name TEXT,
            algorithm TEXT,
            execution_time REAL,
            scheduled_slots INTEGER,
            conflicts INTEGER,
            schedule_json TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Insert results
    for algo_name, results in algorithm_results.items():
        cursor.execute('''
            INSERT INTO results 
            (dataset_name, algorithm, execution_time, scheduled_slots, conflicts, schedule_json)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (
            dataset_name,
            algo_name,
            results['stats']['execution_time'],
            results['stats']['scheduled_slots'],
            results['stats']['conflicts'],
            json.dumps(results['schedule'])
        ))
    
    conn.commit()
    conn.close()
```

---

## Best Practices

### 1. Dataset Design
- **Konsistensi**: Pastikan ID unik dan tidak ada duplikasi
- **Realisme**: Gunakan data yang realistis untuk testing
- **Skalabilitas**: Test dengan berbagai ukuran dataset

### 2. Development Workflow
- **Version Control**: Commit setiap perubahan significant
- **Testing**: Test dengan dataset kecil sebelum dataset besar
- **Documentation**: Update dokumentasi saat menambah fitur

### 3. Production Deployment
- **Environment**: Gunakan virtual environment
- **Monitoring**: Monitor memory dan CPU usage
- **Backup**: Backup dataset dan results penting
- **Logging**: Implement comprehensive logging

---

[← API Documentation](05-api-documentation.md) | [Lanjut ke Configuration →](07-configuration.md)