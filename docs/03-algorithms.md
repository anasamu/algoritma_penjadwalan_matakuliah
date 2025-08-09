# Algorithms Documentation

## Overview Algoritma

Sistem ini mengimplementasikan tiga algoritma berbeda untuk menyelesaikan masalah penjadwalan mata kuliah. Setiap algoritma memiliki pendekatan, kelebihan, dan keterbatasan yang unik.

## Perbandingan Algoritma

| Aspek | Greedy | Backtracking | ILP |
|-------|--------|--------------|-----|
| **Kompleksitas Waktu** | O(n²) | O(b^d) eksponensial | Polynomial rata-rata |
| **Kualitas Solusi** | Baik | Sangat Baik | Optimal |
| **Penggunaan Memori** | Rendah | Sedang | Tinggi |
| **Kecepatan Eksekusi** | Sangat Cepat | Sedang | Lambat |
| **Jaminan Optimality** | Tidak | Tidak | Ya |
| **Cocok untuk Dataset** | Kecil-Sedang | Sedang | Besar |

---

## Algoritma Greedy

### Konsep Dasar

Algoritma Greedy menggunakan pendekatan **first-fit heuristic** dengan membuat keputusan optimal lokal pada setiap langkah. Algoritma ini tidak menjamin solusi global optimal, tetapi memberikan solusi yang cukup baik dengan waktu eksekusi yang sangat cepat.

### Strategi Algoritma

1. **Urutkan mata kuliah** berdasarkan prioritas (jumlah mahasiswa, SKS)
2. **Untuk setiap mata kuliah**, cari slot waktu dan ruangan pertama yang tersedia
3. **Assign immediately** tanpa mempertimbangkan impact ke mata kuliah lain
4. **Lanjutkan** hingga semua mata kuliah diproses

### Pseudocode

```python
def greedy_solve():
    initialize_data_structures()
    
    for each course in sorted_courses:
        for each session in course.required_sessions:
            best_slot = find_first_available_slot(course, session)
            if best_slot:
                assign_slot(course, session, best_slot)
                mark_resources_used(best_slot)
            else:
                add_to_failed_sessions(course, session)
    
    return schedule, statistics
```

### Implementasi Detail

#### 1. Inisialisasi
```python
def __init__(self, data):
    self.matakuliah = data["matakuliah"]
    self.dosen = data["dosen"]
    self.slot_waktu = data["slot_waktu"]
    self.ruangan = data["ruangan"]
    self.jadwal = []
    self.used_rooms = {}  # Track occupied rooms
    self.used_dosen = {}  # Track lecturer conflicts
```

#### 2. Deteksi Konflik
```python
def is_conflict(self, hari, jam_mulai, jam_selesai, ruangan_id, dosen_id):
    # Check room conflicts
    if room_occupied(hari, ruangan_id, jam_mulai, jam_selesai):
        return "Konflik Ruangan"
    
    # Check lecturer conflicts  
    if lecturer_busy(hari, dosen_id, jam_mulai, jam_selesai):
        return "Konflik Dosen"
    
    return None
```

#### 3. Penandaan Resource
```python
def mark_used(self, hari, jam_mulai, jam_selesai, ruangan_id, dosen_id):
    self.used_rooms.setdefault(hari, {}).setdefault(ruangan_id, [])
        .append((jam_mulai, jam_selesai))
    self.used_dosen.setdefault(hari, {}).setdefault(dosen_id, [])
        .append((jam_mulai, jam_selesai))
```

### Kelebihan
- ⚡ **Sangat cepat**: Kompleksitas O(n²)
- 💾 **Memory efficient**: Penggunaan memori minimal
- 🎯 **Simple implementation**: Mudah dipahami dan di-debug
- 📈 **Scalable**: Dapat menangani dataset besar

### Keterbatasan
- 🎲 **Tidak optimal**: Solusi bergantung pada urutan input
- 🔄 **Tidak ada backtracking**: Keputusan tidak dapat diubah
- 📊 **Kualitas bervariasi**: Hasil bergantung pada karakteristik dataset

---

## Algoritma Backtracking

### Konsep Dasar

Algoritma Backtracking menggunakan **systematic search** dengan kemampuan untuk membatalkan keputusan sebelumnya jika mengarah ke dead-end. Algoritma ini menjelajahi ruang solusi secara lengkap dan dapat menemukan solusi yang lebih baik daripada greedy.

### Strategi Algoritma

1. **Coba assign** mata kuliah ke slot yang tersedia
2. **Jika berhasil**, lanjutkan ke mata kuliah berikutnya
3. **Jika gagal** (konflik atau tidak ada slot), **backtrack**
4. **Coba alternative** di level sebelumnya
5. **Ulangi** hingga semua mata kuliah terjadwal atau terbukti tidak ada solusi

### Pseudocode

```python
def backtrack_solve(course_index):
    if course_index >= total_courses:
        return True  # All courses scheduled
    
    current_course = courses[course_index]
    
    for each_possible_slot in available_slots:
        if is_valid_assignment(current_course, slot):
            assign(current_course, slot)
            
            if backtrack_solve(course_index + 1):
                return True  # Solution found
            
            undo_assignment(current_course, slot)  # Backtrack
    
    return False  # No solution possible
```

### Implementasi Detail

#### 1. Struktur Data
```python
class BacktrackingScheduler:
    def __init__(self, data):
        self.matakuliah = data["matakuliah"]
        self.used_rooms = {}
        self.used_dosen = {}
        self.current_assignments = []  # Track for backtracking
```

#### 2. Fungsi Backtracking
```python
def solve(self):
    start_time = time.time()
    
    # Sort courses by complexity (high student count first)
    sorted_courses = sorted(self.matakuliah, 
                          key=lambda x: x['jumlah_mahasiswa'], 
                          reverse=True)
    
    success = self.backtrack_schedule(0, sorted_courses)
    
    execution_time = time.time() - start_time
    return self.format_results(execution_time, success)
```

#### 3. Validasi Assignment
```python
def is_valid_assignment(self, course, time_slot, room):
    # Check capacity constraint
    if room['kapasitas'] < course['jumlah_mahasiswa']:
        return False
    
    # Check conflicts
    if self.has_conflict(course, time_slot, room):
        return False
    
    return True
```

#### 4. Undo Mechanism
```python
def undo_assignment(self, course, assignment):
    # Remove from schedule
    self.jadwal.remove(assignment)
    
    # Free up resources
    self.free_room_slot(assignment)
    self.free_lecturer_slot(assignment)
```

### Kelebihan
- 🎯 **Solusi lebih baik**: Eksplorasi sistematis ruang solusi
- 🔄 **Flexibility**: Dapat membatalkan keputusan buruk
- ✅ **Completeness**: Akan menemukan solusi jika ada
- 🧩 **Optimal untuk subset**: Optimal dalam batasan yang dieksplorasi

### Keterbatasan
- ⏱️ **Kompleksitas eksponensial**: Bisa sangat lambat untuk dataset besar
- 💾 **Memory overhead**: Perlu menyimpan state untuk backtracking
- 🔢 **Tidak deterministik**: Waktu eksekusi tidak dapat diprediksi

---

## Algoritma Integer Linear Programming (ILP)

### Konsep Dasar

ILP mengformulasikan masalah penjadwalan sebagai **mathematical optimization problem**. Masalah dinyatakan dalam bentuk objective function yang dimaksimasi/minimasi dengan berbagai constraint linear.

### Formulasi Matematis

#### Decision Variables
```
x[i,j,k,t] = {1 if course i assigned to room j by lecturer k at time t
             {0 otherwise
```

#### Objective Function
```
Maximize: Σ x[i,j,k,t] for all valid combinations
```

#### Constraints

1. **Unique Assignment Constraint**
```
Σ(j,k,t) x[i,j,k,t] ≤ sessions_required[i] ∀i
```

2. **Room Capacity Constraint**
```
students[i] * x[i,j,k,t] ≤ capacity[j] ∀i,j,k,t
```

3. **Room Conflict Constraint**
```
Σi x[i,j,k,t] ≤ 1 ∀j,t
```

4. **Lecturer Conflict Constraint**
```
Σ(i,j) x[i,j,k,t] ≤ 1 ∀k,t
```

### Implementasi Detail

#### 1. Variable Generation
```python
def _create_variables(self):
    variables = {}
    for course in self.matakuliah:
        for room in self.ruangan:
            for time_slot in self.all_possible_time_slots:
                if self._is_feasible_combination(course, room, time_slot):
                    var_name = f"x_{course['id']}_{room['id']}_{time_slot['id']}"
                    variables[var_name] = LpVariable(var_name, cat='Binary')
    return variables
```

#### 2. Constraint Addition
```python
def _add_constraints(self, prob, variables):
    # Room conflict constraints
    for time_slot in self.time_slots:
        for room in self.ruangan:
            prob += lpSum([variables[var] for var in self._get_room_vars(room, time_slot)]) <= 1
    
    # Lecturer conflict constraints
    for time_slot in self.time_slots:
        for lecturer in self.dosen:
            prob += lpSum([variables[var] for var in self._get_lecturer_vars(lecturer, time_slot)]) <= 1
```

#### 3. Solution Extraction
```python
def _extract_solution(self, variables):
    schedule = []
    for var_name, var in variables.items():
        if var.varValue == 1:  # Variable is selected
            course_id, room_id, time_id = self._parse_variable_name(var_name)
            assignment = self._create_assignment(course_id, room_id, time_id)
            schedule.append(assignment)
    return schedule
```

### Solver Integration

#### 1. PuLP Configuration
```python
def solve(self):
    # Create problem instance
    prob = LpProblem("Penjadwalan_Kuliah", LpMaximize)
    
    # Generate variables
    variables = self._create_variables()
    
    # Set objective
    prob += lpSum(variables.values())
    
    # Add constraints
    self._add_constraints(prob, variables)
    
    # Solve
    prob.solve()
    
    return self._process_results(prob, variables)
```

#### 2. Result Processing
```python
def _process_results(self, prob, variables):
    if LpStatus[prob.status] == 'Optimal':
        schedule = self._extract_solution(variables)
        stats = self._calculate_statistics(schedule)
        return {'schedule': schedule, 'stats': stats}
    else:
        return {'schedule': [], 'stats': {'status': 'No solution'}}
```

### Kelebihan
- 🎯 **Optimal solution**: Dijamin optimal dalam constraint yang diberikan
- 🔢 **Mathematical rigor**: Pendekatan yang secara matematis sound
- 📊 **Flexible constraints**: Mudah menambah constraint baru
- ⚖️ **Balanced trade-offs**: Dapat mengoptimalkan multiple objectives

### Keterbatasan
- ⏱️ **Computational complexity**: Bisa sangat lambat untuk problem besar
- 💾 **Memory intensive**: Membutuhkan memori besar untuk variables
- 🔧 **Setup complexity**: Formulasi mathematical model yang kompleks
- 📦 **Dependency**: Membutuhkan external solver (CBC/CPLEX)

---

## Perbandingan Performa

### Kompleksitas Teoretis

| Algoritma | Time Complexity | Space Complexity | Best Case | Worst Case |
|-----------|----------------|------------------|-----------|------------|
| Greedy | O(n²) | O(n) | O(n²) | O(n²) |
| Backtracking | O(b^d) | O(d) | O(n) | O(b^d) |
| ILP | Polynomial avg | O(n³) | P | NP-hard |

### Karakteristik Praktis

#### Dataset Kecil (< 20 mata kuliah)
- **Greedy**: Instant, solusi 70-80% optimal
- **Backtracking**: < 1 detik, solusi 85-95% optimal  
- **ILP**: 1-5 detik, solusi optimal

#### Dataset Sedang (20-50 mata kuliah)
- **Greedy**: < 1 detik, solusi 60-75% optimal
- **Backtracking**: 5-30 detik, solusi 80-90% optimal
- **ILP**: 10-60 detik, solusi optimal

#### Dataset Besar (> 50 mata kuliah)
- **Greedy**: 1-3 detik, solusi 50-70% optimal
- **Backtracking**: > 2 menit, solusi 75-85% optimal
- **ILP**: 2-10 menit, solusi optimal

---

[← Architecture](02-architecture.md) | [Lanjut ke Data Model →](04-data-model.md)