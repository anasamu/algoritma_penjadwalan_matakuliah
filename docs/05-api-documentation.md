# API Documentation

## Overview

Dokumentasi lengkap untuk semua kelas, fungsi, dan API yang tersedia dalam sistem penjadwalan mata kuliah. Sistem menggunakan pola Object-Oriented Programming dengan interface yang konsisten antar komponen.

---

## Main Application

### main.py

#### Functions

##### `main()`
**Deskripsi**: Entry point utama aplikasi yang mengorkestrasi seluruh proses penjadwalan

**Flow Eksekusi**:
1. Load dataset dari JSON
2. Inisialisasi semua scheduler
3. Eksekusi algoritma secara berurutan
4. Generate laporan komprehensif

```python
# Usage Example
if __name__ == "__main__":
    # Dataset loading
    dataset_name = 'dataset'
    files_dataset = 'data/' + dataset_name + '.json' 
    files = utils.load_dataset(files_dataset)
    
    # Scheduler initialization
    schedulers = {
        "Backtracking": BacktrackingScheduler(files),
        "Greedy": GreedyScheduler(files),
        "ILP": ILPScheduler(files),
    }
    
    # Execute and collect results
    algorithm_results = {}
    for algo_name, scheduler_instance in schedulers.items():
        results = scheduler_instance.solve()
        algorithm_results[algo_name] = results
    
    # Generate report
    utils.generate_full_report_html(files, algorithm_results, report_filename)
```

---

## Algorithm Classes

### Base Scheduler Interface

Semua scheduler mengimplementasikan interface yang konsisten:

```python
class SchedulerInterface:
    def __init__(self, data: dict)
    def solve(self) -> dict
    def calculate_stats(self) -> dict
    def is_conflict(self, hari: str, jam_mulai: int, jam_selesai: int, 
                   ruangan_id: int, dosen_id: int) -> str|None
```

### 1. GreedyScheduler

**File**: `algoritma/greedy.py`
**Deskripsi**: Implementasi algoritma greedy dengan strategi first-fit

#### Constructor

```python
def __init__(self, data: dict)
```
**Parameters**:
- `data`: Dictionary berisi dataset (dosen, matakuliah, ruangan, slot_waktu)

**Attributes**:
- `matakuliah`: List mata kuliah
- `dosen`: List dosen
- `slot_waktu`: List slot waktu tersedia
- `ruangan`: List ruangan tersedia
- `jadwal`: List hasil penjadwalan
- `used_rooms`: Dict tracking penggunaan ruangan
- `used_dosen`: Dict tracking penggunaan dosen
- `failed_sessions`: List sesi yang gagal dijadwalkan

#### Methods

##### `solve() -> dict`
**Deskripsi**: Menjalankan algoritma greedy untuk penjadwalan

**Returns**:
```python
{
    'schedule': [
        {
            'matakuliah_id': int,
            'matakuliah': str,
            'dosen': str,
            'ruangan': str,
            'hari': str,
            'jam_mulai': str,
            'jam_selesai': str,
            'sesi': int,
            'jumlah_mahasiswa': int
        },
        ...
    ],
    'stats': {
        'execution_time': float,
        'total_slots_attempted': int,
        'scheduled_slots': int,
        'conflicts': int,
        'failed_details': list
    }
}
```

**Algorithm Flow**:
1. Sort mata kuliah berdasarkan jumlah mahasiswa (descending)
2. Untuk setiap mata kuliah, generate sesi sesuai SKS
3. Cari slot waktu dan ruangan pertama yang available
4. Assign jika tidak ada konflik, skip jika ada konflik

##### `is_conflict(hari: str, jam_mulai_menit: int, jam_selesai_menit: int, ruangan_id: int, dosen_id: int) -> str|None`
**Deskripsi**: Deteksi konflik ruangan atau dosen

**Parameters**:
- `hari`: Nama hari
- `jam_mulai_menit`: Waktu mulai dalam menit
- `jam_selesai_menit`: Waktu selesai dalam menit
- `ruangan_id`: ID ruangan
- `dosen_id`: ID dosen

**Returns**:
- `"Konflik Ruangan"`: Jika ruangan sudah terpakai
- `"Konflik Dosen"`: Jika dosen sudah mengajar
- `None`: Jika tidak ada konflik

##### `mark_used(hari: str, jam_mulai_menit: int, jam_selesai_menit: int, ruangan_id: int, dosen_id: int)`
**Deskripsi**: Menandai ruangan dan dosen sebagai terpakai pada slot waktu tertentu

##### `calculate_stats() -> dict`
**Deskripsi**: Menghitung statistik performa algoritma

**Returns**:
```python
{
    'total_slots_attempted': int,
    'scheduled_slots': int,
    'conflicts': int,
    'failed_details': list
}
```

### 2. BacktrackingScheduler

**File**: `algoritma/backtrack.py`
**Deskripsi**: Implementasi algoritma backtracking dengan pencarian sistematis

#### Constructor & Attributes
Sama dengan GreedyScheduler

#### Methods

##### `solve() -> dict`
**Deskripsi**: Menjalankan algoritma backtracking

**Algorithm Flow**:
1. Sort mata kuliah berdasarkan kompleksitas
2. Gunakan recursive backtracking
3. Coba setiap kemungkinan slot untuk mata kuliah
4. Backtrack jika mengarah ke dead-end
5. Return solusi terbaik yang ditemukan

##### `backtrack_schedule(course_index: int, sorted_courses: list) -> bool`
**Deskripsi**: Fungsi rekursif utama untuk backtracking

**Parameters**:
- `course_index`: Index mata kuliah saat ini
- `sorted_courses`: List mata kuliah yang sudah diurutkan

**Returns**:
- `True`: Jika solusi ditemukan
- `False`: Jika tidak ada solusi

##### `undo_assignment(assignment: dict)`
**Deskripsi**: Membatalkan assignment sebelumnya (backtrack)

### 3. ILPScheduler

**File**: `algoritma/ilp.py`  
**Deskripsi**: Implementasi Integer Linear Programming menggunakan PuLP

#### Constructor

```python
def __init__(self, data: dict)
```
**Additional Attributes**:
- `mk_dict`: Dictionary lookup mata kuliah
- `dosen_dict`: Dictionary lookup dosen
- `ruangan_dict`: Dictionary lookup ruangan
- `urutan_hari`: Mapping hari ke nomor urut
- `all_possible_time_slots`: List semua slot waktu yang mungkin

#### Methods

##### `solve() -> dict`
**Deskripsi**: Setup dan solve ILP model

**Algorithm Flow**:
1. Generate decision variables untuk setiap kombinasi yang feasible
2. Setup objective function (maximize scheduled sessions)
3. Add constraints (capacity, conflicts, time limits)
4. Solve menggunakan CBC solver
5. Extract solution dari variables

##### `_generate_possible_time_slots() -> list`
**Deskripsi**: Generate semua kemungkinan slot waktu dengan interval 15 menit

**Returns**: List dictionary dengan format:
```python
[
    {
        'hari': str,
        'jam_mulai_menit': int,
        'jam_selesai_slot_menit': int
    },
    ...
]
```

##### `_create_variables(courses: list, rooms: list, time_slots: list) -> dict`
**Deskripsi**: Membuat binary decision variables untuk ILP

**Returns**: Dictionary variables dengan key format `"x_{course_id}_{room_id}_{time_id}"`

##### `_add_constraints(prob: LpProblem, variables: dict)`
**Deskripsi**: Menambahkan constraint ke ILP model

**Constraint Types**:
- **Capacity Constraint**: Jumlah mahasiswa ≤ kapasitas ruangan
- **Room Conflict**: Satu ruangan per time slot
- **Lecturer Conflict**: Satu dosen per time slot
- **Session Limit**: Maksimal sesi per mata kuliah

---

## Utility Functions

### utils.py

#### Data Loading & Conversion

##### `load_dataset(filename: str) -> dict`
**Deskripsi**: Memuat dataset dari file JSON

**Parameters**:
- `filename`: Path ke file JSON

**Returns**: Dictionary dengan structure:
```python
{
    'dosen': list,
    'matakuliah': list,
    'ruangan': list,
    'slot_waktu': list
}
```

**Example**:
```python
data = utils.load_dataset('data/dataset.json')
```

##### `sks_to_minutes(sks: int) -> int`
**Deskripsi**: Konversi SKS ke durasi dalam menit

**Parameters**:
- `sks`: Jumlah SKS (2 atau 3)

**Returns**:
- `90`: untuk 2 SKS
- `135`: untuk 3 SKS
- `0`: untuk input invalid

##### `time_to_minutes(time_str: str) -> int`
**Deskripsi**: Konversi string waktu ke menit sejak 00:00

**Parameters**:
- `time_str`: Format "HH:MM"

**Returns**: Total menit sebagai integer

**Example**:
```python
minutes = time_to_minutes("08:30")  # Returns 510
```

##### `minutes_to_time(total_minutes: int) -> str`
**Deskripsi**: Konversi menit ke format waktu

**Parameters**:
- `total_minutes`: Total menit sejak 00:00

**Returns**: String format "HH:MM"

**Example**:
```python
time_str = minutes_to_time(510)  # Returns "08:30"
```

#### Data Analysis

##### `get_dosen_name(dosen_id: int, dosen_list: list) -> str`
**Deskripsi**: Ambil nama dosen berdasarkan ID

**Parameters**:
- `dosen_id`: ID dosen
- `dosen_list`: List data dosen

**Returns**: Nama dosen atau "Unknown Dosen"

##### `get_usage_counts(schedule: list, key_name_or_func: str|callable) -> dict`
**Deskripsi**: Hitung frekuensi penggunaan berdasarkan key tertentu

**Parameters**:
- `schedule`: List jadwal
- `key_name_or_func`: Nama key atau function untuk extract value

**Returns**: Dictionary dengan count untuk setiap unique value

**Example**:
```python
room_usage = get_usage_counts(schedule, 'ruangan')
# Returns: {'Lab A': 5, 'Ruang B': 3, ...}

day_usage = get_usage_counts(schedule, lambda x: x['hari'])
# Returns: {'Senin': 8, 'Selasa': 6, ...}
```

##### `check_conflicts(schedule: list) -> list`
**Deskripsi**: Deteksi semua konflik dalam jadwal

**Parameters**:
- `schedule`: List jadwal untuk dicek

**Returns**: List string deskripsi konflik

**Conflict Types**:
- Konflik ruangan: Dua mata kuliah di ruangan sama pada waktu overlap
- Konflik dosen: Satu dosen mengajar di waktu overlap

#### Visualization Functions

##### `performance_comparison(algorithm_results: dict, report_dir: str, filename: str = "performance_comparison.png")`
**Deskripsi**: Generate grafik perbandingan waktu eksekusi

**Parameters**:
- `algorithm_results`: Dictionary hasil dari setiap algoritma
- `report_dir`: Directory untuk menyimpan gambar
- `filename`: Nama file output

**Generated**: Bar chart dengan waktu eksekusi setiap algoritma

##### `schedule_comparison(algorithm_results: dict, report_dir: str, filename: str = "schedule_comparison.png")`
**Deskripsi**: Generate grafik perbandingan jumlah sesi per hari

**Parameters**: Sama dengan performance_comparison

**Generated**: Grouped bar chart sesi per hari untuk setiap algoritma

##### `compare_usage(algorithm_results: dict, key_name_or_func: str|callable, title: str, ylabel: str, report_dir: str, filename: str)`
**Deskripsi**: Generate grafik perbandingan penggunaan resource

**Parameters**:
- `key_name_or_func`: Key untuk extract data usage
- `title`: Judul grafik
- `ylabel`: Label sumbu Y

**Usage Examples**:
```python
# Compare room usage
compare_usage(results, 'ruangan', 'Penggunaan Ruangan', 'Frequency', dir, 'room_usage.png')

# Compare time slot usage
compare_usage(results, lambda x: f"{x['hari']} {x['jam_mulai']}", 
              'Penggunaan Slot Waktu', 'Frequency', dir, 'time_usage.png')
```

#### HTML Generation

##### `create_html_table(data_list: list, headers_map: dict) -> str`
**Deskripsi**: Generate tabel HTML dengan Bootstrap styling

**Parameters**:
- `data_list`: List of dictionaries dengan data
- `headers_map`: Mapping display name ke data key

**Returns**: String HTML table

**Example**:
```python
headers = {
    "ID": "id",
    "Nama": "nama", 
    "Email": "email"
}
html = create_html_table(dosen_list, headers)
```

##### `generate_html_schedule_content(schedule: list, ordered_days: list = ["Senin", "Selasa", ...]) -> str`
**Deskripsi**: Generate konten HTML untuk jadwal dengan accordion Bootstrap

**Parameters**:
- `schedule`: List jadwal
- `ordered_days`: Urutan hari untuk ditampilkan

**Returns**: String HTML dengan accordion per hari

##### `generate_html_failed_sessions_content(failed_sessions: list) -> str`
**Deskripsi**: Generate konten HTML untuk sesi yang gagal dijadwalkan

**Parameters**:
- `failed_sessions`: List sesi yang gagal

**Returns**: String HTML table atau pesan jika tidak ada yang gagal

##### `generate_full_report_html(data: dict, algorithm_results: dict, filename: str)`
**Deskripsi**: Generate laporan HTML lengkap dengan semua visualisasi

**Parameters**:
- `data`: Dataset original
- `algorithm_results`: Dictionary hasil semua algoritma
- `filename`: Nama file output

**Generated Files**:
- HTML report lengkap
- PNG grafik perbandingan performa
- PNG grafik perbandingan jadwal per hari
- PNG grafik penggunaan ruangan
- PNG grafik penggunaan slot waktu

**Report Structure**:
1. **Dataset Summary**: Tabel data dosen, mata kuliah, ruangan
2. **Algorithm Results**: Jadwal per algoritma dengan accordion
3. **Performance Analysis**: Grafik waktu eksekusi
4. **Schedule Analysis**: Grafik distribusi per hari
5. **Resource Usage**: Grafik penggunaan ruangan dan slot waktu
6. **Conflict Analysis**: Daftar konflik yang terdeteksi

---

## Constants & Globals

### `HARI_ORDER`
**Type**: Dictionary
**Deskripsi**: Mapping nama hari ke nomor urut untuk sorting

```python
HARI_ORDER = {
    "Senin": 1, "Selasa": 2, "Rabu": 3, 
    "Kamis": 4, "Jumat": 5, "Sabtu": 6, "Minggu": 7
}
```

---

## Error Handling

### Common Exceptions

#### `FileNotFoundError`
**When**: Dataset file tidak ditemukan
**Solution**: Pastikan path file benar dan file exists

#### `json.JSONDecodeError`
**When**: Format JSON invalid
**Solution**: Validasi format JSON dataset

#### `KeyError`
**When**: Missing required fields dalam dataset
**Solution**: Pastikan semua field required ada dalam data

#### `ValueError`
**When**: Invalid data values (e.g., negative SKS)
**Solution**: Validasi data sebelum processing

### Error Handling Pattern

```python
try:
    data = utils.load_dataset('data/dataset.json')
    scheduler = GreedyScheduler(data)
    results = scheduler.solve()
except FileNotFoundError:
    print("Dataset file not found")
except json.JSONDecodeError:
    print("Invalid JSON format")
except KeyError as e:
    print(f"Missing required field: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

---

## Performance Considerations

### Memory Usage
- **Greedy**: O(n) - minimal memory footprint
- **Backtracking**: O(d) - proportional to recursion depth
- **ILP**: O(n³) - extensive variable storage

### Time Complexity
- **Greedy**: O(n²) - predictable and fast
- **Backtracking**: O(b^d) - exponential worst case
- **ILP**: Polynomial average - depends on solver

### Optimization Tips

1. **Dataset Size**: Limit mata kuliah < 100 untuk performa optimal
2. **Time Slots**: Gunakan interval yang reasonable (15-30 menit)
3. **Memory**: Monitor memory usage untuk dataset besar
4. **Parallel Processing**: Algoritma dapat dijalankan parallel

---

[← Data Model](04-data-model.md) | [Lanjut ke Usage Guide →](06-usage-guide.md)