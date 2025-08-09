# System Architecture Diagram

## High-Level System Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                            PRESENTATION LAYER                                 ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌─────────────────┐  ┌─────────────────┐  ┌─────────────────┐              ║
║  │   HTML Report   │  │  Charts & Graphs │  │ Performance     │              ║
║  │                 │  │                 │  │ Metrics         │              ║
║  │ • Bootstrap UI  │  │ • Matplotlib    │  │                 │              ║
║  │ • Responsive    │  │ • PNG Export    │  │ • Time Analysis │              ║
║  │ • Interactive   │  │ • Comparison    │  │ • Success Rates │              ║
║  │   Elements      │  │   Visualizations│  │ • Resource Usage│              ║
║  └─────────────────┘  └─────────────────┘  └─────────────────┘              ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                            APPLICATION LAYER                                  ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌───────────────────────────────────────────────────────────────────────┐   ║
║  │                        MAIN ORCHESTRATOR                              │   ║
║  │                           (main.py)                                   │   ║
║  │                                                                       │   ║
║  │  • Dataset Loading & Validation                                       │   ║
║  │  • Algorithm Coordination                                             │   ║
║  │  • Result Aggregation                                                 │   ║
║  │  • Report Generation Control                                          │   ║
║  └───────────────────────────┬───────────────────────────────────────────┘   ║
║                              │                                               ║
║  ┌───────────────────────────┼───────────────────────────────────────────┐   ║
║  │              ALGORITHM EXECUTION LAYER                               │   ║
║  │                              │                                       │   ║
║  │ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐     │   ║
║  │ │   GREEDY    │ │ BACKTRACKING│ │     ILP     │ │ EXTENSIBLE  │     │   ║
║  │ │  SCHEDULER  │ │  SCHEDULER  │ │  SCHEDULER  │ │   PLUGINS   │     │   ║
║  │ │             │ │             │ │             │ │             │     │   ║
║  │ │ • First-fit │ │ • Recursive │ │ • PuLP Lib  │ │ • Dynamic   │     │   ║
║  │ │ • Fast O(n²)│ │ • Backtrack │ │ • CBC Solver│ │ • Load      │     │   ║
║  │ │ • Heuristic │ │ • Systematic│ │ • Optimal   │ │ • Custom    │     │   ║
║  │ │ • Local Opt │ │ • Complete  │ │ • Math Prog │ │ • Algorithms│     │   ║
║  │ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘     │   ║
║  └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                              SERVICE LAYER                                    ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ┌───────────────────────────────────────────────────────────────────────┐   ║
║  │                        UTILITY SERVICES                              │   ║
║  │                           (utils.py)                                 │   ║
║  │                                                                       │   ║
║  │ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐         │   ║
║  │ │ DATA PROCESSING │ │ CONFLICT ENGINE │ │ REPORT GENERATOR│         │   ║
║  │ │                 │ │                 │ │                 │         │   ║
║  │ │ • JSON Loading  │ │ • Room Conflicts│ │ • HTML Template │         │   ║
║  │ │ • Time Convert  │ │ • Lecturer      │ │ • Chart Creation│         │   ║
║  │ │ • Data Validate │ │   Conflicts     │ │ • Data Binding  │         │   ║
║  │ │ • Structure     │ │ • Overlap       │ │ • File Export   │         │   ║
║  │ │   Enhancement   │ │   Detection     │ │ • Timestamping  │         │   ║
║  │ └─────────────────┘ └─────────────────┘ └─────────────────┘         │   ║
║  │                                                                       │   ║
║  │ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐         │   ║
║  │ │ VISUALIZATION   │ │ STATISTICS      │ │ FILE MANAGEMENT │         │   ║
║  │ │                 │ │                 │ │                 │         │   ║
║  │ │ • Performance   │ │ • Success Rates │ │ • Directory     │         │   ║
║  │ │   Charts        │ │ • Resource      │ │   Creation      │         │   ║
║  │ │ • Usage Graphs  │ │   Utilization   │ │ • Path Handling │         │   ║
║  │ │ • Comparison    │ │ • Execution     │ │ • Permission    │         │   ║
║  │ │   Plots         │ │   Metrics       │ │   Management    │         │   ║
║  │ └─────────────────┘ └─────────────────┘ └─────────────────┘         │   ║
║  └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                               ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                               DATA LAYER                                      ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────┐ ║
║ │   INPUT DATA    │ │    TEMPLATES    │ │  CONFIGURATION  │ │   OUTPUT    │ ║
║ │                 │ │                 │ │                 │ │             │ ║
║ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────────┐ │ │ ┌─────────┐ │ ║
║ │ │dataset.json │ │ │ │report_      │ │ │ │Algorithm    │ │ │ │Reports  │ │ ║
║ │ │             │ │ │ │template.html│ │ │ │Config       │ │ │ │(HTML)   │ │ ║
║ │ │• Dosen      │ │ │ │             │ │ │ │             │ │ │ │         │ │ ║
║ │ │• MataKuliah │ │ │ │• Bootstrap  │ │ │ │• Parameters │ │ │ │• Charts │ │ ║
║ │ │• Ruangan    │ │ │ │• Responsive │ │ │ │• Timeouts   │ │ │ │ (PNG)   │ │ ║
║ │ │• SlotWaktu  │ │ │ │• Placehldrs │ │ │ │• Priorities │ │ │ │         │ │ ║
║ │ └─────────────┘ │ │ └─────────────┘ │ │ └─────────────┘ │ │ └─────────┘ │ ║
║ └─────────────────┘ └─────────────────┘ └─────────────────┘ └─────────────┘ ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## Component Interaction Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                             EXECUTION FLOW                                 │
└─────────────────────────────────────────────────────────────────────────────┘

     User Execution
          │
          ▼
┌─────────────────┐
│     main.py     │──┐
│   Entry Point   │  │
└─────────────────┘  │
          │          │
          ▼          │ 1. Load Dataset
┌─────────────────┐  │
│   utils.py      │◄─┘
│ load_dataset()  │
└─────────────────┘
          │
          ▼ Validated Data
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ GreedyScheduler │     │BacktrackScheduler│     │  ILPScheduler   │
│                 │     │                 │     │                 │
│ ┌─────────────┐ │     │ ┌─────────────┐ │     │ ┌─────────────┐ │
│ │   solve()   │ │     │ │   solve()   │ │     │ │   solve()   │ │
│ └─────────────┘ │     │ └─────────────┘ │     │ └─────────────┘ │
│         │       │     │         │       │     │         │       │
│         ▼       │     │         ▼       │     │         ▼       │
│ ┌─────────────┐ │     │ ┌─────────────┐ │     │ ┌─────────────┐ │
│ │is_conflict()│ │     │ │backtrack()  │ │     │ │setup_model()│ │
│ │mark_used()  │ │     │ │validate()   │ │     │ │solve_ilp()  │ │
│ └─────────────┘ │     │ └─────────────┘ │     │ └─────────────┘ │
└─────────────────┘     └─────────────────┘     └─────────────────┘
          │                       │                       │
          ▼ Results               ▼ Results               ▼ Results
┌─────────────────────────────────────────────────────────────────┐
│                     Results Aggregation                        │
│                        (main.py)                               │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼ Combined Results
┌─────────────────────────────────────────────────────────────────┐
│                     Report Generation                          │
│                        (utils.py)                              │
│                                                                 │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐   │
│ │Chart Generation │ │Table Generation │ │HTML Composition │   │
│ │                 │ │                 │ │                 │   │
│ │• matplotlib     │ │• Bootstrap      │ │• Template       │   │
│ │• PNG export     │ │• Responsive     │ │• Data binding   │   │
│ │• Comparisons    │ │• Formatting     │ │• File output    │   │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘   │
└─────────────────────────────┬───────────────────────────────────┘
                              │
                              ▼ Report Files
┌─────────────────────────────────────────────────────────────────┐
│                      File System Output                        │
│                                                                 │
│ report/YYYYMMDD_HHMMSS/                                        │
│ ├── dataset_laporan_penjadwalan_lengkap.html                   │
│ ├── performance_comparison.png                                 │
│ ├── schedule_comparison.png                                    │
│ ├── matakuliah_usage_comparison.png                           │
│ ├── ruangan_usage_comparison.png                              │
│ └── slot_waktu_usage_comparison.png                           │
└─────────────────────────────────────────────────────────────────┘
```

## Technology Stack Architecture

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                           TECHNOLOGY STACK                                   ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║ ┌───────────────────────────────────────────────────────────────────────┐   ║
║ │                         FRONTEND/OUTPUT LAYER                        │   ║
║ │                                                                       │   ║
║ │  HTML5 + CSS3 + JavaScript          Bootstrap 5.x                    │   ║
║ │  ┌─────────────────┐                 ┌─────────────────┐             │   ║
║ │  │ • Responsive    │                 │ • Grid System   │             │   ║
║ │  │ • Interactive   │                 │ • Components    │             │   ║
║ │  │ • Semantic      │                 │ • Accordion     │             │   ║
║ │  │ • Modern        │                 │ • Tables        │             │   ║
║ │  └─────────────────┘                 └─────────────────┘             │   ║
║ └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                               ║
║ ┌───────────────────────────────────────────────────────────────────────┐   ║
║ │                        BACKEND/LOGIC LAYER                           │   ║
║ │                                                                       │   ║
║ │  Python 3.8+                         Core Libraries                  │   ║
║ │  ┌─────────────────┐                 ┌─────────────────┐             │   ║
║ │  │ • Object Orient │                 │ • JSON (built-in)│             │   ║
║ │  │ • Modular Design│                 │ • datetime      │             │   ║
║ │  │ • Error Handling│                 │ • collections   │             │   ║
║ │  │ • Documentation │                 │ • os, sys       │             │   ║
║ │  └─────────────────┘                 └─────────────────┘             │   ║
║ └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                               ║
║ ┌───────────────────────────────────────────────────────────────────────┐   ║
║ │                    SPECIALIZED LIBRARIES LAYER                       │   ║
║ │                                                                       │   ║
║ │  Optimization                        Visualization                    │   ║
║ │  ┌─────────────────┐                 ┌─────────────────┐             │   ║
║ │  │ PuLP            │                 │ Matplotlib      │             │   ║
║ │  │ • Linear Prog   │                 │ • Chart Gen     │             │   ║
║ │  │ • CBC Solver    │                 │ • PNG Export    │             │   ║
║ │  │ • Optimization  │                 │ • Customizable  │             │   ║
║ │  │ • Constraints   │                 │ • Professional  │             │   ║
║ │  └─────────────────┘                 └─────────────────┘             │   ║
║ └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                               ║
║ ┌───────────────────────────────────────────────────────────────────────┐   ║
║ │                         DATA LAYER                                   │   ║
║ │                                                                       │   ║
║ │  File System                         Data Formats                    │   ║
║ │  ┌─────────────────┐                 ┌─────────────────┐             │   ║
║ │  │ • JSON Files    │                 │ • UTF-8 Encoding│             │   ║
║ │  │ • HTML Reports  │                 │ • Structured    │             │   ║
║ │  │ • PNG Images    │                 │ • Normalized    │             │   ║
║ │  │ • Temp Files    │                 │ • Validated     │             │   ║
║ │  └─────────────────┘                 └─────────────────┘             │   ║
║ └───────────────────────────────────────────────────────────────────────┘   ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

## Module Dependency Diagram

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            MODULE DEPENDENCIES                             │
└─────────────────────────────────────────────────────────────────────────────┘

                                main.py
                                   │
                                   │ imports
                                   ▼
                ┌─────────────────────────────────────┐
                │              utils.py               │
                │                                     │
                │ • load_dataset()                    │
                │ • time conversion functions         │
                │ • conflict detection               │
                │ • visualization functions          │
                │ • report generation                │
                └─────────────────┬───────────────────┘
                                  │
                    ┌─────────────┼─────────────┐
                    │             │             │
                    ▼             ▼             ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │algoritma/       │ │algoritma/       │ │algoritma/       │
        │greedy.py        │ │backtrack.py     │ │ilp.py           │
        │                 │ │                 │ │                 │
        │ class           │ │ class           │ │ class           │
        │ GreedyScheduler │ │BacktrackScheduler│ │ ILPScheduler    │
        └─────────────────┘ └─────────────────┘ └─────────┬───────┘
                │                       │                 │
                │ imports utils         │ imports utils   │ imports
                │                       │                 │
                ▼                       ▼                 ▼
        ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
        │ Standard        │ │ Standard        │ │      PuLP       │
        │ Libraries       │ │ Libraries       │ │                 │
        │                 │ │                 │ │ • LpProblem     │
        │ • time          │ │ • time          │ │ • LpVariable    │
        │ • collections   │ │ • collections   │ │ • LpMaximize    │
        │                 │ │ • sys (recursion)│ │ • COIN_CMD      │
        └─────────────────┘ └─────────────────┘ └─────────────────┘

External Dependencies:
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   matplotlib    │    │      PuLP       │    │   CBC Solver    │
│                 │    │                 │    │                 │
│ • pyplot        │    │ • Linear Prog   │    │ • External      │
│ • charts        │    │ • Optimization  │    │ • Binary        │
│ • PNG export    │    │ • Modeling      │    │ • COIN-OR       │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

## Design Patterns Implementation

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                            DESIGN PATTERNS                                 │
└─────────────────────────────────────────────────────────────────────────────┘

1. STRATEGY PATTERN
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                    SchedulerInterface (Implicit)                           │
│                            │                                               │
│          ┌─────────────────┼─────────────────┐                             │
│          │                 │                 │                             │
│          ▼                 ▼                 ▼                             │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐               │
│ │GreedyScheduler  │ │BacktrackScheduler│ │ ILPScheduler    │               │
│ │                 │ │                 │ │                 │               │
│ │ + solve()       │ │ + solve()       │ │ + solve()       │               │
│ │ + calculate_    │ │ + calculate_    │ │ + calculate_    │               │
│ │   stats()       │ │   stats()       │ │   stats()       │               │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘               │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

2. TEMPLATE METHOD PATTERN
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                    Abstract Solve Template:                                │
│                                                                             │
│    def solve(self):                                                         │
│        start_time = time.time()                                             │
│        self.initialize_data_structures()    # Common                        │
│        result = self.execute_algorithm()    # Algorithm-specific            │
│        execution_time = time.time() - start_time                            │
│        stats = self.calculate_stats()       # Common interface              │
│        return {'schedule': result, 'stats': stats}                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

3. FACTORY PATTERN
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        Scheduler Factory (main.py):                        │
│                                                                             │
│    schedulers = {                                                           │
│        "Backtracking": BacktrackingScheduler(files),                       │
│        "Greedy": GreedyScheduler(files),                                    │
│        "ILP": ILPScheduler(files),                                         │
│    }                                                                        │
│                                                                             │
│    # Dynamic instantiation and execution                                    │
│    for algo_name, scheduler_instance in schedulers.items():                │
│        results = scheduler_instance.solve()                                │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

4. BUILDER PATTERN
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│                        Report Builder (utils.py):                          │
│                                                                             │
│    def generate_full_report_html():                                         │
│        report = ReportBuilder()                                             │
│            .add_dataset_info(data)                                          │
│            .add_algorithm_results(results)                                  │
│            .add_performance_charts(charts)                                  │
│            .add_statistics_tables(stats)                                    │
│            .build()                                                         │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Scalability Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          SCALABILITY CONSIDERATIONS                        │
└─────────────────────────────────────────────────────────────────────────────┘

HORIZONTAL SCALING (Multiple Algorithms):
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Algorithm 1   │    │   Algorithm 2   │    │   Algorithm N   │
│   (Process 1)   │    │   (Process 2)   │    │   (Process N)   │
└─────────┬───────┘    └─────────┬───────┘    └─────────┬───────┘
          │                      │                      │
          └──────────────────────┼──────────────────────┘
                                 │
                                 ▼
                        ┌─────────────────┐
                        │ Result Aggregator│
                        │    (main.py)    │
                        └─────────────────┘

VERTICAL SCALING (Dataset Partitioning):
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  Large Dataset                                                              │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   │
│  │  Semester 1 │     │  Semester 3 │     │  Semester 5 │                   │
│  │   Courses   │────▶│   Courses   │────▶│   Courses   │                   │
│  └─────────────┘     └─────────────┘     └─────────────┘                   │
│         │                    │                    │                        │
│         ▼                    ▼                    ▼                        │
│  ┌─────────────┐     ┌─────────────┐     ┌─────────────┐                   │
│  │  Schedule   │     │  Schedule   │     │  Schedule   │                   │
│  │  Subset 1   │     │  Subset 2   │     │  Subset 3   │                   │
│  └─────────────┘     └─────────────┘     └─────────────┘                   │
│         │                    │                    │                        │
│         └────────────────────┼────────────────────┘                        │
│                              │                                             │
│                              ▼                                             │
│                     ┌─────────────────┐                                    │
│                     │ Schedule Merger │                                    │
│                     │ & Validator     │                                    │
│                     └─────────────────┘                                    │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘

MEMORY OPTIMIZATION:
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│  Streaming Processing:                                                      │
│  ┌─────────────┐ process ┌─────────────┐ process ┌─────────────┐           │
│  │   Chunk 1   │────────▶│   Chunk 2   │────────▶│   Chunk N   │           │
│  └─────────────┘         └─────────────┘         └─────────────┘           │
│                                                                             │
│  Lazy Loading:                                                              │
│  ┌─────────────┐ on-demand ┌─────────────┐                                 │
│  │ Data Source │──────────▶│ Memory Cache│                                 │
│  └─────────────┘           └─────────────┘                                 │
│                                                                             │
│  Garbage Collection:                                                        │
│  ┌─────────────┐ cleanup  ┌─────────────┐                                  │
│  │ Algorithm   │─────────▶│ Memory Free │                                  │
│  │ Complete    │          │ Resources   │                                  │
│  └─────────────┘          └─────────────┘                                  │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

[← Data Flow Diagram](../flowcharts/data-flow-diagram.md) | [Kembali ke README ←](../README.md)