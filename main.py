import utils

from algoritma.backtrack import BacktrackingScheduler
from algoritma.greedy import GreedyScheduler
from algoritma.ilp import ILPScheduler

# Load dataset
dataset_name = 'dataset'
files_dataset = 'data/' + dataset_name + '.json' 
files = utils.load_dataset(files_dataset )

# 1. Inisialisasi Schedulers Algoritma
backtracking_scheduler = BacktrackingScheduler(files)
greedy_scheduler = GreedyScheduler(files)
ilp_scheduler = ILPScheduler(files)

# 2. Jalankan setiap algoritma scheduler
backtracking_results = backtracking_scheduler.solve()
greedy_results = greedy_scheduler.solve()
ilp_results = ilp_scheduler.solve()

# 3. Ambil jadwal dan statistik dari setiap algoritma
backtracking_schedule = backtracking_results
greedy_schedule = greedy_results
ilp_schedule = ilp_results

# 4. Generate laporan lengkap
report_filename = dataset_name + "_laporan_penjadwalan_lengkap.html"

utils.generate_full_report_html(
    files,
    backtracking_schedule,
    greedy_schedule,
    ilp_schedule,
    report_filename
)

print("Laporan penjadwalan lengkap telah dibuat:", report_filename)