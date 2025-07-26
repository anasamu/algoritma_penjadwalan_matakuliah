import utils

# Import schedulers from their respective modules
from algoritma.backtrack import BacktrackingScheduler
from algoritma.greedy import GreedyScheduler
from algoritma.ilp import ILPScheduler
# from algoritma.dynamic_programing import DPScheduler

# Load dataset
dataset_name = 'dataset'
files_dataset = 'data/' + dataset_name + '.json' 
files = utils.load_dataset(files_dataset)

# Initialize Algorithm Schedulers
# It's good practice to store schedulers in a dictionary if you plan to iterate or manage them dynamically
schedulers = {
    "Backtracking": BacktrackingScheduler(files),
    "Greedy": GreedyScheduler(files),
    "ILP": ILPScheduler(files),
    # "Dynamic Programming": DPScheduler(files),
}

# Dictionary to store results from each algorithm
algorithm_results = {}

# Run each algorithm scheduler and store its results
for algo_name, scheduler_instance in schedulers.items():
    print(f"Running {algo_name} Scheduler...")
    # The .solve() method is expected to return a dictionary with 'schedule' and 'stats' keys
    # as per the generate_full_report_html function's expectation in utils.py
    results = scheduler_instance.solve()
    algorithm_results[algo_name] = results
    print(f"{algo_name} Scheduler finished.")

# Generate the comprehensive report
report_filename = dataset_name + "_laporan_penjadwalan_lengkap.html"

# Now, pass the consolidated algorithm_results dictionary to the report generator
utils.generate_full_report_html(
    files, # The original dataset is still needed for general info tables
    algorithm_results, # This now contains all schedules and stats
    report_filename
)

print(f"\nLaporan penjadwalan lengkap telah dibuat: {report_filename}")
