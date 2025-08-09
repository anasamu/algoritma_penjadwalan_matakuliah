# Configuration Guide

## Overview Konfigurasi

Panduan lengkap untuk mengkonfigurasi dan menyesuaikan sistem penjadwalan mata kuliah sesuai dengan kebutuhan spesifik institusi atau penelitian.

---

## Konfigurasi Dataset

### 1. Parameter Waktu

#### SKS ke Durasi Mapping
```python
# File: utils.py
def sks_to_minutes(sks):
    """Konfigurasi durasi kuliah berdasarkan SKS"""
    mapping = {
        1: 60,   # 1 SKS = 60 menit
        2: 90,   # 2 SKS = 90 menit (default)
        3: 135,  # 3 SKS = 135 menit (default)
        4: 180   # 4 SKS = 180 menit
    }
    return mapping.get(sks, 0)
```

#### Interval Waktu Scheduling
```python
# File: algoritma/ilp.py
def _generate_possible_time_slots(self):
    """Konfigurasi interval scheduling"""
    interval_minutes = 15  # Ubah ke 30 untuk interval lebih besar
    
    for start_time_candidate in range(start_minutes_slot, end_minutes_slot, interval_minutes):
        # Generate time slots
```

#### Format Waktu Custom
```python
# File: utils.py
TIME_FORMAT = "%H:%M"  # Default format
# Alternatif: "%I:%M %p" untuk format 12-jam dengan AM/PM

def parse_time(time_str):
    """Parse waktu dengan format custom"""
    from datetime import datetime
    return datetime.strptime(time_str, TIME_FORMAT)
```

### 2. Hari Kerja Configuration

```python
# File: utils.py
HARI_ORDER = {
    "Senin": 1, "Selasa": 2, "Rabu": 3, 
    "Kamis": 4, "Jumat": 5, "Sabtu": 6
    # "Minggu": 7  # Uncomment jika Minggu digunakan
}

# Working days untuk filtering
WORKING_DAYS = ["Senin", "Selasa", "Rabu", "Kamis", "Jumat", "Sabtu"]

def is_working_day(hari):
    return hari in WORKING_DAYS
```

### 3. Constraint Configuration

#### Kapasitas Buffer
```python
# Tambahkan buffer untuk kapasitas ruangan
def check_capacity_constraint(course, room, buffer_percent=10):
    """Check kapasitas dengan buffer"""
    effective_capacity = room['kapasitas'] * (1 - buffer_percent/100)
    return course['jumlah_mahasiswa'] <= effective_capacity
```

#### Break Time antar Sesi
```python
# Minimum break time antar sesi untuk dosen yang sama
MINIMUM_BREAK_MINUTES = 15

def has_sufficient_break(existing_sessions, new_session, dosen_id):
    """Check minimum break time"""
    for session in existing_sessions:
        if session['dosen_id'] == dosen_id:
            time_gap = abs(session['jam_selesai_menit'] - new_session['jam_mulai_menit'])
            if time_gap < MINIMUM_BREAK_MINUTES:
                return False
    return True
```

#### Preferensi Hari per Semester
```python
# File: configuration.py
SEMESTER_DAY_PREFERENCES = {
    1: ["Senin", "Rabu", "Jumat"],      # Semester 1 preferensi hari ganjil
    2: ["Senin", "Rabu", "Jumat"],      # Semester 2 preferensi hari ganjil  
    3: ["Selasa", "Kamis", "Sabtu"],    # Semester 3 preferensi hari genap
    4: ["Selasa", "Kamis", "Sabtu"],    # dst...
    # Tambahkan preferensi untuk semester lainnya
}

def get_preferred_days(semester):
    return SEMESTER_DAY_PREFERENCES.get(semester, WORKING_DAYS)
```

---

## Konfigurasi Algoritma

### 1. Greedy Algorithm Configuration

#### Priority Sorting Strategy
```python
# File: algoritma/greedy.py
class GreedyScheduler:
    def __init__(self, data, config=None):
        self.config = config or self.get_default_config()
        
    def get_default_config(self):
        return {
            'priority_strategy': 'student_count',  # 'student_count', 'sks', 'semester'
            'sort_order': 'desc',                 # 'desc', 'asc'
            'tie_breaker': 'sks'                  # Field untuk tie breaking
        }
    
    def sort_courses(self):
        """Sort mata kuliah berdasarkan konfigurasi priority"""
        strategy = self.config['priority_strategy']
        reverse = self.config['sort_order'] == 'desc'
        
        if strategy == 'student_count':
            return sorted(self.matakuliah, 
                         key=lambda x: (x['jumlah_mahasiswa'], x.get(self.config['tie_breaker'], 0)), 
                         reverse=reverse)
        elif strategy == 'sks':
            return sorted(self.matakuliah, 
                         key=lambda x: (x['sks'], x.get(self.config['tie_breaker'], 0)), 
                         reverse=reverse)
        elif strategy == 'semester':
            return sorted(self.matakuliah, 
                         key=lambda x: (x['semester'], x.get(self.config['tie_breaker'], 0)), 
                         reverse=reverse)
```

#### Room Selection Strategy
```python
def get_room_selection_strategy(self):
    """Konfigurasi strategi pemilihan ruangan"""
    return {
        'strategy': 'best_fit',  # 'first_fit', 'best_fit', 'worst_fit'
        'prefer_labs': True,     # Preferensi lab untuk mata kuliah praktikum
        'capacity_threshold': 0.8 # Minimal 80% kapasitas terpakai
    }

def select_room(self, course, available_rooms):
    """Pilih ruangan berdasarkan strategi"""
    config = self.get_room_selection_strategy()
    
    if config['strategy'] == 'best_fit':
        # Pilih ruangan dengan kapasitas paling pas
        suitable_rooms = [r for r in available_rooms 
                         if r['kapasitas'] >= course['jumlah_mahasiswa']]
        if suitable_rooms:
            return min(suitable_rooms, key=lambda r: r['kapasitas'])
    
    elif config['strategy'] == 'first_fit':
        # Pilih ruangan pertama yang cocok
        for room in available_rooms:
            if room['kapasitas'] >= course['jumlah_mahasiswa']:
                return room
    
    return None
```

### 2. Backtracking Algorithm Configuration

#### Search Strategy
```python
# File: algoritma/backtrack.py
class BacktrackingScheduler:
    def __init__(self, data, config=None):
        self.config = config or self.get_default_config()
    
    def get_default_config(self):
        return {
            'max_depth': 1000,              # Maksimal kedalaman rekursi
            'timeout_seconds': 300,         # Timeout 5 menit
            'early_termination': True,      # Hentikan jika solusi cukup baik
            'solution_threshold': 0.9,      # 90% mata kuliah terjadwal = cukup baik
            'variable_ordering': 'most_constrained_first'  # Urutan variabel
        }
    
    def should_terminate_early(self, current_schedule):
        """Check apakah harus terminate early"""
        if not self.config['early_termination']:
            return False
            
        total_courses = len(self.matakuliah)
        scheduled_courses = len(set(item['matakuliah_id'] for item in current_schedule))
        completion_rate = scheduled_courses / total_courses
        
        return completion_rate >= self.config['solution_threshold']
```

#### Heuristic Configuration
```python
def get_variable_ordering(self):
    """Konfigurasi urutan variabel untuk backtracking"""
    strategy = self.config['variable_ordering']
    
    if strategy == 'most_constrained_first':
        # Mata kuliah dengan constraint paling banyak dulu
        return sorted(self.matakuliah, 
                     key=lambda x: self.count_constraints(x), 
                     reverse=True)
    elif strategy == 'least_constraining_value':
        # Mata kuliah yang paling fleksibel dulu
        return sorted(self.matakuliah, 
                     key=lambda x: self.count_available_slots(x), 
                     reverse=True)
    
    return self.matakuliah

def count_constraints(self, course):
    """Hitung jumlah constraint untuk mata kuliah"""
    constraints = 0
    
    # Constraint kapasitas ruangan
    suitable_rooms = [r for r in self.ruangan 
                     if r['kapasitas'] >= course['jumlah_mahasiswa']]
    constraints += (len(self.ruangan) - len(suitable_rooms))
    
    # Constraint dosen (jika dosen sudah banyak mengajar)
    dosen_courses = [mk for mk in self.matakuliah if mk['dosen_id'] == course['dosen_id']]
    constraints += len(dosen_courses)
    
    return constraints
```

### 3. ILP Algorithm Configuration

#### Solver Configuration
```python
# File: algoritma/ilp.py
class ILPScheduler:
    def get_solver_config(self):
        return {
            'solver': 'CBC',              # 'CBC', 'GUROBI', 'CPLEX'
            'time_limit': 600,            # 10 menit timeout
            'mip_gap': 0.01,             # 1% optimality gap
            'threads': 4,                 # Jumlah thread
            'presolve': True,            # Enable preprocessing
            'cuts': True,                # Enable cutting planes
            'heuristics': True           # Enable heuristics
        }
    
    def configure_solver(self, prob):
        """Konfigurasi solver berdasarkan setting"""
        config = self.get_solver_config()
        
        if config['solver'] == 'CBC':
            # CBC specific settings
            solver = pulp.COIN_CMD(
                timeLimit=config['time_limit'],
                fracGap=config['mip_gap'],
                threads=config['threads']
            )
        elif config['solver'] == 'GUROBI':
            # Gurobi specific settings (jika tersedia)
            solver = pulp.GUROBI_CMD(
                timeLimit=config['time_limit'],
                MIPGap=config['mip_gap']
            )
        
        return solver
```

#### Objective Function Weighting
```python
def create_objective_function(self, variables):
    """Objective function dengan multiple weights"""
    weights = {
        'schedule_weight': 10,      # Weight untuk scheduled sessions
        'preference_weight': 5,     # Weight untuk preferred time slots
        'balance_weight': 2,        # Weight untuk balanced workload
        'compactness_weight': 1     # Weight untuk compactness
    }
    
    objective = 0
    
    # Basic scheduling objective
    objective += weights['schedule_weight'] * lpSum(variables.values())
    
    # Add preference-based terms
    for var_name, var in variables.items():
        course_id, room_id, time_slot = self.parse_variable_name(var_name)
        
        # Preference untuk waktu tertentu
        if self.is_preferred_time(time_slot):
            objective += weights['preference_weight'] * var
        
        # Penalty untuk workload imbalance
        objective -= weights['balance_weight'] * self.get_workload_penalty(course_id, time_slot)
    
    return objective
```

---

## Konfigurasi Output & Reporting

### 1. HTML Report Configuration

#### Template Customization
```python
# File: report_config.py
REPORT_CONFIG = {
    'title': 'Laporan Penjadwalan Mata Kuliah',
    'subtitle': 'Perbandingan Algoritma Optimisasi',
    'institution': 'Universitas ABC',
    'department': 'Fakultas Teknik Informatika',
    'theme': 'bootstrap',      # 'bootstrap', 'material', 'custom'
    'color_scheme': 'blue',    # 'blue', 'green', 'red', 'purple'
    'logo_path': 'assets/logo.png',
    'include_raw_data': True,
    'include_charts': True,
    'chart_style': 'modern'    # 'classic', 'modern', 'minimal'
}

def get_html_template():
    """Load template berdasarkan konfigurasi"""
    theme = REPORT_CONFIG['theme']
    template_file = f"data/templates/report_template_{theme}.html"
    
    with open(template_file, 'r', encoding='utf-8') as f:
        return f.read()
```

#### Chart Configuration
```python
# File: visualization_config.py
CHART_CONFIG = {
    'performance_chart': {
        'figure_size': (12, 6),
        'colors': ['#3498db', '#e74c3c', '#2ecc71', '#f39c12'],
        'style': 'seaborn',
        'grid': True,
        'show_values': True,
        'title_size': 16,
        'label_size': 12
    },
    'schedule_chart': {
        'figure_size': (15, 7),
        'bar_width': 0.8,
        'alpha': 0.8,
        'rotation': 45,
        'legend_position': 'upper right'
    }
}

def apply_chart_style():
    """Apply global chart styling"""
    plt.style.use(CHART_CONFIG['performance_chart']['style'])
    plt.rcParams['figure.figsize'] = CHART_CONFIG['performance_chart']['figure_size']
    plt.rcParams['font.size'] = CHART_CONFIG['performance_chart']['label_size']
```

### 2. Export Configuration

#### Multiple Format Export
```python
# File: export_config.py
EXPORT_CONFIG = {
    'formats': ['html', 'pdf', 'csv', 'json', 'xlsx'],
    'compression': True,
    'include_metadata': True,
    'separate_files_per_algorithm': False,
    'filename_template': '{dataset}_{algorithm}_{timestamp}',
    'output_directory': 'output'
}

def export_results(algorithm_results, dataset_name):
    """Export dengan multiple format"""
    config = EXPORT_CONFIG
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for format_type in config['formats']:
        if format_type == 'csv':
            export_to_csv(algorithm_results, dataset_name, timestamp)
        elif format_type == 'json':
            export_to_json(algorithm_results, dataset_name, timestamp)
        elif format_type == 'xlsx':
            export_to_excel(algorithm_results, dataset_name, timestamp)
```

---

## Environment Configuration

### 1. Development vs Production

#### Configuration Files
```python
# File: config/development.py
DEBUG = True
ENABLE_PROFILING = True
LOG_LEVEL = 'DEBUG'
MAX_DATASET_SIZE = 50
ENABLE_ALL_ALGORITHMS = True
TIMEOUT_SECONDS = 60

# File: config/production.py  
DEBUG = False
ENABLE_PROFILING = False
LOG_LEVEL = 'INFO'
MAX_DATASET_SIZE = 500
ENABLE_ALL_ALGORITHMS = False  # Hanya algoritma cepat
TIMEOUT_SECONDS = 300
```

#### Environment Variable Configuration
```python
import os

def get_config():
    """Load configuration based on environment"""
    env = os.getenv('APP_ENV', 'development')
    
    if env == 'production':
        from config.production import *
    else:
        from config.development import *
    
    return {
        'debug': DEBUG,
        'log_level': LOG_LEVEL,
        'max_dataset_size': MAX_DATASET_SIZE,
        'timeout': TIMEOUT_SECONDS
    }
```

### 2. Logging Configuration

```python
# File: logging_config.py
import logging
from datetime import datetime

def setup_logging(level='INFO'):
    """Setup comprehensive logging"""
    
    # Create logs directory
    os.makedirs('logs', exist_ok=True)
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # File handler
    file_handler = logging.FileHandler(
        f'logs/scheduling_{datetime.now().strftime("%Y%m%d")}.log'
    )
    file_handler.setFormatter(logging.Formatter(log_format))
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(log_format))
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, level),
        handlers=[file_handler, console_handler]
    )
    
    return logging.getLogger(__name__)
```

### 3. Performance Configuration

#### Memory Management
```python
# File: performance_config.py
PERFORMANCE_CONFIG = {
    'memory_limit_gb': 8,           # Batas memori maksimal
    'gc_threshold': 0.8,            # Trigger garbage collection
    'chunk_size': 100,              # Process data in chunks
    'parallel_processing': True,     # Enable multiprocessing
    'max_workers': 4                # Maksimal worker threads
}

def check_memory_usage():
    """Monitor penggunaan memori"""
    import psutil
    memory_percent = psutil.virtual_memory().percent
    
    if memory_percent > PERFORMANCE_CONFIG['gc_threshold'] * 100:
        import gc
        gc.collect()
        logging.warning(f"Memory usage high: {memory_percent}%. Triggered GC.")
```

---

## Custom Extensions

### 1. Plugin Architecture

```python
# File: plugins/base.py
class SchedulerPlugin:
    """Base class untuk scheduler plugins"""
    
    def __init__(self, config):
        self.config = config
    
    def pre_process(self, data):
        """Hook sebelum processing"""
        return data
    
    def post_process(self, results):
        """Hook setelah processing"""
        return results
    
    def validate_schedule(self, schedule):
        """Custom validation"""
        return True

# File: plugins/semester_plugin.py
class SemesterGroupingPlugin(SchedulerPlugin):
    """Plugin untuk grouping berdasarkan semester"""
    
    def pre_process(self, data):
        # Group mata kuliah by semester
        grouped_courses = defaultdict(list)
        for course in data['matakuliah']:
            grouped_courses[course['semester']].append(course)
        
        data['_semester_groups'] = dict(grouped_courses)
        return data
```

### 2. Custom Constraints

```python
# File: constraints/custom.py
class CustomConstraints:
    """Custom constraint definitions"""
    
    @staticmethod
    def no_friday_afternoon(schedule_item):
        """Constraint: Tidak boleh ada kuliah Jumat sore"""
        if schedule_item['hari'] == 'Jumat':
            jam_mulai = time_to_minutes(schedule_item['jam_mulai'])
            return jam_mulai < 13 * 60  # Sebelum jam 13:00
        return True
    
    @staticmethod  
    def max_sessions_per_day(schedule, max_sessions=4):
        """Constraint: Maksimal sesi per hari"""
        day_counts = defaultdict(int)
        for item in schedule:
            day_counts[item['hari']] += 1
        
        return all(count <= max_sessions for count in day_counts.values())
    
    @staticmethod
    def lecturer_workload_balance(schedule, dosen_list):
        """Constraint: Balance workload antar dosen"""
        lecturer_loads = defaultdict(int)
        for item in schedule:
            lecturer_loads[item['dosen_id']] += 1
        
        if not lecturer_loads:
            return True
            
        max_load = max(lecturer_loads.values())
        min_load = min(lecturer_loads.values())
        
        return (max_load - min_load) <= 2  # Maksimal selisih 2 sesi
```

---

## Configuration File Examples

### 1. Main Configuration File

```python
# File: config.py
import os
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SchedulingConfig:
    """Main configuration class"""
    
    # Dataset configuration
    dataset_path: str = 'data/dataset.json'
    output_path: str = 'report'
    
    # Algorithm configuration
    enabled_algorithms: List[str] = None
    algorithm_timeout: int = 300
    parallel_execution: bool = True
    
    # Report configuration
    generate_html: bool = True
    generate_charts: bool = True
    include_raw_data: bool = True
    
    # Performance configuration
    memory_limit_gb: int = 8
    max_dataset_size: int = 500
    
    def __post_init__(self):
        if self.enabled_algorithms is None:
            self.enabled_algorithms = ['Greedy', 'Backtracking', 'ILP']
    
    @classmethod
    def from_file(cls, config_file: str):
        """Load configuration from file"""
        import json
        with open(config_file, 'r') as f:
            config_data = json.load(f)
        return cls(**config_data)
    
    def save_to_file(self, config_file: str):
        """Save configuration to file"""
        import json
        with open(config_file, 'w') as f:
            json.dump(self.__dict__, f, indent=2)

# Usage
config = SchedulingConfig(
    dataset_path='data/custom_dataset.json',
    enabled_algorithms=['Greedy', 'ILP'],
    algorithm_timeout=600
)
```

### 2. Algorithm-Specific Configuration

```json
{
  "greedy": {
    "priority_strategy": "student_count",
    "sort_order": "desc",
    "room_selection": "best_fit",
    "enable_preferences": true
  },
  "backtracking": {
    "max_depth": 1000,
    "timeout_seconds": 300,
    "early_termination": true,
    "solution_threshold": 0.9,
    "variable_ordering": "most_constrained_first"
  },
  "ilp": {
    "solver": "CBC",
    "time_limit": 600,
    "mip_gap": 0.01,
    "threads": 4,
    "objective_weights": {
      "schedule_weight": 10,
      "preference_weight": 5,
      "balance_weight": 2
    }
  }
}
```

---

[← Usage Guide](06-usage-guide.md) | [Lanjut ke Troubleshooting →](08-troubleshooting.md)