# Troubleshooting Guide

## Overview

Panduan lengkap untuk mendiagnosis dan menyelesaikan masalah umum yang mungkin terjadi saat menggunakan sistem penjadwalan mata kuliah.

---

## Masalah Instalasi

### 1. Dependency Installation Issues

#### Problem: ModuleNotFoundError
```
ModuleNotFoundError: No module named 'matplotlib'
ModuleNotFoundError: No module named 'pulp'
```

**Diagnosis**:
```bash
# Check Python version
python --version

# Check pip version
pip --version

# List installed packages
pip list
```

**Solutions**:
```bash
# Solusi 1: Install ulang dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Solusi 2: Install manual
pip install matplotlib pulp

# Solusi 3: Force reinstall
pip install --force-reinstall matplotlib pulp

# Solusi 4: Install dengan user flag (jika permission error)
pip install --user matplotlib pulp
```

#### Problem: Permission Denied saat Install
```
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied
```

**Solutions**:
```bash
# Solusi 1: Install sebagai user
pip install --user -r requirements.txt

# Solusi 2: Gunakan virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Solusi 3: Install dengan sudo (Linux/Mac only)
sudo pip install -r requirements.txt
```

#### Problem: Package Version Conflicts
```
ERROR: pip's dependency resolver does not currently consider all the packages
```

**Solutions**:
```bash
# Solusi 1: Upgrade pip
pip install --upgrade pip

# Solusi 2: Install dengan no-deps flag
pip install --no-deps matplotlib pulp

# Solusi 3: Create clean virtual environment
python -m venv fresh_env
source fresh_env/bin/activate
pip install -r requirements.txt
```

### 2. Python Version Issues

#### Problem: Syntax Error atau Incompatibility
```
SyntaxError: invalid syntax
AttributeError: module has no attribute 'xxx'
```

**Diagnosis**:
```bash
# Check Python version
python --version
# Pastikan >= 3.8

# Check available Python versions
python3 --version
python3.8 --version
python3.9 --version
```

**Solutions**:
```bash
# Gunakan Python version yang sesuai
python3.8 -m venv venv
python3.9 main.py

# Update Python (Ubuntu/Debian)
sudo apt update
sudo apt install python3.9

# Update Python (macOS with Homebrew)
brew install python@3.9
```

---

## Masalah Runtime

### 1. Dataset Loading Issues

#### Problem: FileNotFoundError
```
FileNotFoundError: [Errno 2] No such file or directory: 'data/dataset.json'
```

**Diagnosis**:
```bash
# Check file existence
ls -la data/
ls -la data/dataset.json

# Check current directory
pwd
```

**Solutions**:
```bash
# Solusi 1: Pastikan berada di direktori yang benar
cd /path/to/algoritma_penjadwalan_matakuliah

# Solusi 2: Check dan buat folder data jika tidak ada
mkdir -p data

# Solusi 3: Copy dataset jika ada
cp dataset.json data/

# Solusi 4: Download dataset dari repository
# (jika dataset tidak ada dalam clone)
```

#### Problem: JSON Decode Error
```
json.decoder.JSONDecodeError: Expecting ',' delimiter: line 5 column 2 (char 123)
```

**Diagnosis**:
```bash
# Validate JSON syntax
python -c "import json; json.load(open('data/dataset.json'))"

# Check file encoding
file data/dataset.json
```

**Solutions**:
```bash
# Solusi 1: Validate JSON dengan online tools
# Copy content ke https://jsonlint.com/

# Solusi 2: Fix common JSON issues
# - Remove trailing commas
# - Check quote marks (harus double quotes)
# - Check bracket balancing

# Solusi 3: Regenerate JSON safely
python -c "
import json
# Recreate JSON with proper formatting
data = {...}  # Your data here
with open('data/dataset.json', 'w') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
"
```

#### Problem: Invalid Data Structure
```
KeyError: 'dosen'
KeyError: 'matakuliah'
```

**Diagnosis & Solutions**:
```python
# Diagnosis script
import json

def validate_dataset(filename):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
        
        required_keys = ['dosen', 'matakuliah', 'ruangan', 'slot_waktu']
        missing_keys = [key for key in required_keys if key not in data]
        
        if missing_keys:
            print(f"Missing keys: {missing_keys}")
            return False
        
        # Check data types
        for key in required_keys:
            if not isinstance(data[key], list):
                print(f"Key '{key}' should be a list, got {type(data[key])}")
                return False
        
        print("Dataset structure is valid")
        return True
        
    except Exception as e:
        print(f"Error validating dataset: {e}")
        return False

# Run validation
validate_dataset('data/dataset.json')
```

### 2. Memory Issues

#### Problem: MemoryError
```
MemoryError: Unable to allocate array
```

**Diagnosis**:
```bash
# Check available memory
free -h  # Linux
# OR
vm_stat  # macOS

# Check Python memory usage
python -c "
import psutil
import os
process = psutil.Process(os.getpid())
print(f'Memory usage: {process.memory_info().rss / 1024 / 1024:.2f} MB')
"
```

**Solutions**:

1. **Reduce Dataset Size**:
```python
# Temporary workaround - reduce dataset size
def reduce_dataset_size(data, max_courses=50):
    """Reduce dataset for testing"""
    data['matakuliah'] = data['matakuliah'][:max_courses]
    return data

# Usage
data = load_dataset('data/dataset.json')
data = reduce_dataset_size(data, 30)  # Test with 30 courses
```

2. **Use Only Fast Algorithms**:
```python
# Skip memory-intensive algorithms
schedulers = {
    "Greedy": GreedyScheduler(files),
    # "Backtracking": BacktrackingScheduler(files),  # Skip for large datasets
    # "ILP": ILPScheduler(files),  # Skip for large datasets
}
```

3. **Optimize Algorithm Configuration**:
```python
# For ILP - reduce variable space
class OptimizedILPScheduler(ILPScheduler):
    def _generate_possible_time_slots(self):
        # Use larger intervals to reduce variables
        slots = []
        for slot in self.slot_waktu:
            start = utils.time_to_minutes(slot["jam_mulai"])
            end = utils.time_to_minutes(slot["jam_selesai"])
            
            # Use 30-minute intervals instead of 15
            for start_time in range(start, end, 30):
                slots.append({
                    "hari": slot["hari"],
                    "jam_mulai_menit": start_time,
                    "jam_selesai_slot_menit": end
                })
        return slots
```

#### Problem: Algorithm Hangs/Takes Too Long
```
# Process appears to hang without output
```

**Diagnosis**:
```python
# Add timeout and progress monitoring
import signal
import time

class TimeoutError(Exception):
    pass

def timeout_handler(signum, frame):
    raise TimeoutError("Algorithm execution timed out")

# Usage with timeout
signal.signal(signal.SIGALRM, timeout_handler)
signal.alarm(300)  # 5 minute timeout

try:
    results = scheduler.solve()
    signal.alarm(0)  # Cancel alarm
except TimeoutError:
    print("Algorithm timed out - consider using smaller dataset")
```

**Solutions**:
```python
# Add progress monitoring
def solve_with_progress(self):
    start_time = time.time()
    last_progress_time = start_time
    
    # Your algorithm implementation with periodic progress checks
    for i, course in enumerate(self.matakuliah):
        current_time = time.time()
        
        # Print progress every 30 seconds
        if current_time - last_progress_time > 30:
            elapsed = current_time - start_time
            progress = (i + 1) / len(self.matakuliah) * 100
            print(f"Progress: {progress:.1f}% - Elapsed: {elapsed:.1f}s")
            last_progress_time = current_time
        
        # Process course...
```

### 3. Algorithm-Specific Issues

#### Problem: ILP Solver Not Found
```
PulpSolverError: PuLP: Error while executing the 'cbc' command
```

**Diagnosis**:
```bash
# Check if CBC solver is available
which cbc
cbc -?
```

**Solutions**:
```bash
# Install CBC solver
# Ubuntu/Debian:
sudo apt-get update
sudo apt-get install coinor-cbc

# macOS with Homebrew:
brew install coin-or-tools/tap/cbc

# Windows: Download from COIN-OR website
# Or use alternative solver:
```

```python
# Alternative: Use different solver
from pulp import GLPK_CMD, COIN_CMD

def solve_with_alternative_solver(self):
    try:
        # Try CBC first
        prob.solve(COIN_CMD())
    except:
        try:
            # Try GLPK as fallback
            prob.solve(GLPK_CMD())
        except:
            # Try default solver
            prob.solve()
```

#### Problem: Backtracking Stack Overflow
```
RecursionError: maximum recursion depth exceeded
```

**Solutions**:
```python
import sys

# Increase recursion limit (careful!)
sys.setrecursionlimit(5000)

# Or implement iterative version
def iterative_backtrack(self):
    """Iterative version to avoid stack overflow"""
    stack = [(0, [])]  # (course_index, current_schedule)
    
    while stack:
        course_index, current_schedule = stack.pop()
        
        if course_index >= len(self.matakuliah):
            return current_schedule  # Solution found
        
        current_course = self.matakuliah[course_index]
        
        for slot in self.get_available_slots():
            if self.is_valid_assignment(current_course, slot):
                new_schedule = current_schedule + [self.create_assignment(current_course, slot)]
                stack.append((course_index + 1, new_schedule))
    
    return []  # No solution found
```

#### Problem: Greedy Algorithm Returns Empty Schedule
```
Warning: Greedy algorithm scheduled 0 out of X courses
```

**Diagnosis**:
```python
def diagnose_greedy_issues(self):
    """Diagnose why greedy algorithm fails"""
    issues = []
    
    # Check capacity constraints
    for course in self.matakuliah:
        suitable_rooms = [r for r in self.ruangan 
                         if r['kapasitas'] >= course['jumlah_mahasiswa']]
        if not suitable_rooms:
            issues.append(f"No suitable room for {course['nama']} ({course['jumlah_mahasiswa']} students)")
    
    # Check time availability
    total_duration_needed = sum(utils.sks_to_minutes(c['sks']) for c in self.matakuliah)
    total_time_available = self.calculate_total_available_time()
    
    if total_duration_needed > total_time_available:
        issues.append(f"Insufficient time: need {total_duration_needed} min, have {total_time_available} min")
    
    # Check lecturer conflicts
    lecturer_courses = {}
    for course in self.matakuliah:
        lecturer_id = course['dosen_id']
        lecturer_courses.setdefault(lecturer_id, []).append(course)
    
    for lecturer_id, courses in lecturer_courses.items():
        total_lecturer_time = sum(utils.sks_to_minutes(c['sks']) for c in courses)
        if total_lecturer_time > total_time_available:
            issues.append(f"Lecturer {lecturer_id} overloaded: {total_lecturer_time} min needed")
    
    return issues

# Usage
issues = scheduler.diagnose_greedy_issues()
for issue in issues:
    print(f"ISSUE: {issue}")
```

---

## Masalah Output

### 1. Report Generation Issues

#### Problem: HTML Report Not Generated
```
FileNotFoundError: [Errno 2] No such file or directory: 'report/'
```

**Solutions**:
```bash
# Create report directory
mkdir -p report

# Check permissions
chmod 755 report

# For Windows:
mkdir report
```

#### Problem: Charts Not Appearing in Report
```
# HTML generated but charts are missing or broken
```

**Diagnosis & Solutions**:
```python
# Check if matplotlib backend is available
import matplotlib
print(f"Matplotlib backend: {matplotlib.get_backend()}")

# For headless systems, use Agg backend
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Verify chart files are created
import os
def check_chart_files(report_dir):
    chart_files = [
        'performance_comparison.png',
        'schedule_comparison.png',
        'matakuliah_usage_comparison.png',
        'ruangan_usage_comparison.png',
        'slot_waktu_usage_comparison.png'
    ]
    
    for chart_file in chart_files:
        file_path = os.path.join(report_dir, chart_file)
        if os.path.exists(file_path):
            print(f"✓ {chart_file} exists ({os.path.getsize(file_path)} bytes)")
        else:
            print(f"✗ {chart_file} missing")
```

#### Problem: Encoding Issues in HTML Report
```
UnicodeDecodeError: 'ascii' codec can't decode byte
```

**Solutions**:
```python
# Ensure UTF-8 encoding throughout
def generate_html_report_safe(data, results, filename):
    try:
        # Force UTF-8 encoding
        with open(filename, 'w', encoding='utf-8') as f:
            html_content = create_html_content(data, results)
            f.write(html_content)
    except UnicodeEncodeError as e:
        print(f"Encoding error: {e}")
        # Fallback: remove problematic characters
        html_content = html_content.encode('ascii', 'ignore').decode('ascii')
        with open(filename, 'w', encoding='ascii') as f:
            f.write(html_content)
```

### 2. Data Export Issues

#### Problem: CSV Export Fails
```
PermissionError: [Errno 13] Permission denied: 'output.csv'
```

**Solutions**:
```python
import os
import tempfile

def safe_csv_export(data, filename):
    """Safe CSV export with error handling"""
    try:
        # Try direct export
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        
    except PermissionError:
        # Use temporary file and move
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as tmp:
            df.to_csv(tmp.name, index=False, encoding='utf-8')
            tmp_name = tmp.name
        
        # Move to final location
        import shutil
        shutil.move(tmp_name, filename)
        
    except Exception as e:
        print(f"Export failed: {e}")
        # Try alternative format
        with open(filename.replace('.csv', '.txt'), 'w') as f:
            for item in data:
                f.write(str(item) + '\n')
```

---

## Performance Issues

### 1. Slow Performance

#### Problem: Algorithm Takes Too Long
**Diagnosis**:
```python
import cProfile
import pstats

def profile_algorithm(scheduler):
    """Profile algorithm performance"""
    pr = cProfile.Profile()
    pr.enable()
    
    results = scheduler.solve()
    
    pr.disable()
    stats = pstats.Stats(pr)
    stats.sort_stats('tottime')
    stats.print_stats(20)  # Top 20 time-consuming functions
    
    return results
```

**Solutions**:
1. **Optimize Data Structures**:
```python
# Use sets for faster membership testing
used_rooms_set = set()
used_lecturers_set = set()

def is_conflict_optimized(self, hari, jam, ruangan_id, dosen_id):
    # Use set lookup instead of list iteration
    slot_key = (hari, jam, ruangan_id)
    lecturer_key = (hari, jam, dosen_id)
    
    return slot_key in used_rooms_set or lecturer_key in used_lecturers_set
```

2. **Limit Search Space**:
```python
# Limit backtracking depth
def backtrack_with_limits(self, course_index, depth_limit=100):
    if course_index >= len(self.matakuliah) or depth_limit <= 0:
        return self.current_schedule
    
    # Continue with limited depth...
```

3. **Use Early Termination**:
```python
def should_continue(self, current_schedule, target_percentage=0.8):
    """Stop if we achieve good enough solution"""
    scheduled_courses = len(set(item['matakuliah_id'] for item in current_schedule))
    total_courses = len(self.matakuliah)
    
    return (scheduled_courses / total_courses) < target_percentage
```

#### Problem: Memory Usage Grows Over Time
**Diagnosis**:
```python
import gc
import psutil

def monitor_memory():
    """Monitor memory usage"""
    process = psutil.Process()
    memory_info = process.memory_info()
    
    print(f"RSS: {memory_info.rss / 1024 / 1024:.2f} MB")
    print(f"VMS: {memory_info.vms / 1024 / 1024:.2f} MB")
    print(f"Objects in memory: {len(gc.get_objects())}")

# Call periodically during execution
monitor_memory()
```

**Solutions**:
```python
# Explicit garbage collection
import gc

def cleanup_memory():
    """Force garbage collection"""
    gc.collect()

# Clear large data structures when done
def solve_with_cleanup(self):
    try:
        results = self.solve_algorithm()
        return results
    finally:
        # Clean up
        self.used_rooms.clear()
        self.used_dosen.clear()
        self.temporary_data = None
        cleanup_memory()
```

---

## Debugging Tools

### 1. Logging Setup

```python
import logging
from datetime import datetime

def setup_debug_logging():
    """Setup comprehensive debugging"""
    
    # Create debug directory
    os.makedirs('debug', exist_ok=True)
    
    # Configure logging
    log_filename = f"debug/debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

# Usage in schedulers
logger = setup_debug_logging()

def solve_with_logging(self):
    logger.info("Starting algorithm execution")
    logger.debug(f"Dataset size: {len(self.matakuliah)} courses")
    
    for i, course in enumerate(self.matakuliah):
        logger.debug(f"Processing course {i+1}/{len(self.matakuliah)}: {course['nama']}")
        # Algorithm logic...
    
    logger.info("Algorithm execution completed")
```

### 2. Debug Output Generation

```python
def generate_debug_report(scheduler_instance, algorithm_name):
    """Generate detailed debug information"""
    
    debug_info = {
        'algorithm': algorithm_name,
        'timestamp': datetime.now().isoformat(),
        'dataset_stats': {
            'total_courses': len(scheduler_instance.matakuliah),
            'total_lecturers': len(scheduler_instance.dosen),
            'total_rooms': len(scheduler_instance.ruangan),
            'total_time_slots': len(scheduler_instance.slot_waktu)
        },
        'execution_trace': [],
        'conflicts_found': [],
        'resource_usage': {}
    }
    
    # Save debug info
    debug_filename = f"debug/{algorithm_name}_debug_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(debug_filename, 'w') as f:
        json.dump(debug_info, f, indent=2)
    
    print(f"Debug report saved: {debug_filename}")
```

### 3. Validation Tools

```python
def validate_final_schedule(schedule, original_data):
    """Comprehensive schedule validation"""
    errors = []
    warnings = []
    
    # Check for conflicts
    conflicts = check_conflicts(schedule)
    if conflicts:
        errors.extend(conflicts)
    
    # Check capacity constraints
    for item in schedule:
        course = next(c for c in original_data['matakuliah'] if c['id'] == item['matakuliah_id'])
        room = next(r for r in original_data['ruangan'] if r['id'] == item['ruangan_id'])
        
        if course['jumlah_mahasiswa'] > room['kapasitas']:
            errors.append(f"Capacity exceeded: {course['nama']} ({course['jumlah_mahasiswa']} students) in {room['nama']} (capacity {room['kapasitas']})")
    
    # Check time constraints
    for item in schedule:
        start_time = utils.time_to_minutes(item['jam_mulai'])
        end_time = utils.time_to_minutes(item['jam_selesai'])
        
        if end_time <= start_time:
            errors.append(f"Invalid time range: {item['jam_mulai']} - {item['jam_selesai']}")
    
    # Summary
    print(f"Validation completed:")
    print(f"  - {len(errors)} errors found")
    print(f"  - {len(warnings)} warnings found")
    
    if errors:
        print("ERRORS:")
        for error in errors:
            print(f"  ! {error}")
    
    return len(errors) == 0
```

---

## Emergency Procedures

### 1. Quick Recovery

```bash
#!/bin/bash
# emergency_recovery.sh

echo "Starting emergency recovery..."

# 1. Check Python environment
python --version || echo "ERROR: Python not found"

# 2. Check dependencies
pip list | grep -E "(matplotlib|pulp)" || pip install matplotlib pulp

# 3. Check dataset
if [ ! -f "data/dataset.json" ]; then
    echo "ERROR: Dataset not found"
    echo "Creating minimal dataset..."
    cat > data/dataset.json << 'EOF'
{
  "dosen": [{"id": 1, "nama": "Test Lecturer", "bidang_keahlian": "Test", "email": "test@test.com"}],
  "matakuliah": [{"id": 1, "nama": "Test Course", "semester": 1, "sks": 2, "dosen_id": 1, "jumlah_mahasiswa": 10}],
  "ruangan": [{"id": 1, "nama": "Test Room", "kapasitas": 20}],
  "slot_waktu": [{"hari": "Senin", "jam_mulai": "08:00", "jam_selesai": "12:00"}]
}
EOF
fi

# 4. Test run with minimal setup
python -c "
import utils
try:
    data = utils.load_dataset('data/dataset.json')
    print('SUCCESS: Dataset loaded successfully')
except Exception as e:
    print(f'ERROR: {e}')
"

echo "Recovery completed"
```

### 2. Safe Mode Execution

```python
def run_safe_mode():
    """Run system in safe mode with minimal functionality"""
    print("Running in SAFE MODE...")
    
    try:
        # Load dataset with validation
        data = utils.load_dataset('data/dataset.json')
        
        # Validate dataset
        if not validate_dataset_basic(data):
            print("ERROR: Dataset validation failed")
            return
        
        # Run only Greedy algorithm (fastest and most reliable)
        scheduler = GreedyScheduler(data)
        
        # Set conservative timeout
        import signal
        signal.alarm(60)  # 1 minute timeout
        
        try:
            results = scheduler.solve()
            signal.alarm(0)
            
            # Generate minimal report
            print(f"SUCCESS: Scheduled {len(results['schedule'])} sessions")
            
            # Save results safely
            with open('safe_mode_results.json', 'w') as f:
                json.dump(results, f, indent=2)
                
        except Exception as e:
            print(f"ALGORITHM ERROR: {e}")
            
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")
        print("Please check installation and dataset")

if __name__ == "__main__":
    run_safe_mode()
```

---

## Getting Help

### 1. Diagnostic Information Collection

```python
def collect_diagnostic_info():
    """Collect system information for bug reports"""
    
    import platform
    import sys
    import pkg_resources
    
    info = {
        'system': {
            'platform': platform.platform(),
            'python_version': sys.version,
            'architecture': platform.architecture(),
        },
        'packages': {},
        'dataset_info': {},
        'error_logs': []
    }
    
    # Collect package versions
    for package in ['matplotlib', 'pulp', 'numpy']:
        try:
            version = pkg_resources.get_distribution(package).version
            info['packages'][package] = version
        except:
            info['packages'][package] = 'NOT INSTALLED'
    
    # Collect dataset info
    try:
        data = utils.load_dataset('data/dataset.json')
        info['dataset_info'] = {
            'courses': len(data.get('matakuliah', [])),
            'lecturers': len(data.get('dosen', [])),
            'rooms': len(data.get('ruangan', [])),
            'time_slots': len(data.get('slot_waktu', []))
        }
    except Exception as e:
        info['dataset_info'] = {'error': str(e)}
    
    # Save diagnostic info
    with open('diagnostic_info.json', 'w') as f:
        json.dump(info, f, indent=2)
    
    print("Diagnostic information saved to diagnostic_info.json")
    print("Please include this file when reporting issues")
    
    return info
```

### 2. Support Contacts

- **GitHub Issues**: https://github.com/anasamu/algoritma_penjadwalan_matakuliah/issues
- **Documentation**: Lihat file dokumentasi dalam folder `docs/`
- **Email Support**: Hubungi maintainer melalui GitHub profile

### 3. Before Reporting Issues

1. **Jalankan diagnostic script**:
   ```bash
   python -c "from troubleshooting import collect_diagnostic_info; collect_diagnostic_info()"
   ```

2. **Check existing issues** di GitHub repository

3. **Provide minimal reproducible example**:
   ```python
   # Minimal failing example
   import utils
   from algoritma.greedy import GreedyScheduler
   
   data = utils.load_dataset('data/minimal_dataset.json')
   scheduler = GreedyScheduler(data)
   results = scheduler.solve()  # This fails
   ```

4. **Include relevant logs** dan error messages

---

[← Configuration](07-configuration.md) | [Kembali ke README ←](README.md)