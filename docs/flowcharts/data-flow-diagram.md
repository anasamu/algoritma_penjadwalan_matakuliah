# Data Flow Diagram

## System Data Flow Overview

```
┌──────────────────┐    JSON     ┌──────────────────┐
│                  │  Dataset    │                  │
│   Dataset File   │─────────────│   Data Loader    │
│  (dataset.json)  │             │    (utils.py)    │
│                  │             │                  │
└──────────────────┘             └─────────┬────────┘
                                           │ Parsed
                                           │ Data
                                           v
                                 ┌──────────────────┐
                                 │                  │
                                 │ Data Validation  │
                                 │  & Processing    │
                                 │                  │
                                 └─────────┬────────┘
                                           │ Validated
                                           │ Dataset
                                           v
┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│                  │             │                  │             │                  │
│ Greedy Scheduler │◄────────────│  Main Control    │────────────►│Backtrack Scheduler│
│                  │  Dataset    │   (main.py)      │  Dataset    │                  │
└─────────┬────────┘             │                  │             └─────────┬────────┘
          │ Results              └─────────┬────────┘                       │ Results
          │                                │ Dataset                        │
          v                                v                                v
┌──────────────────┐             ┌──────────────────┐             ┌──────────────────┐
│ Greedy Results   │             │  ILP Scheduler   │             │Backtrack Results │
│ - Schedule       │             │                  │             │ - Schedule       │
│ - Statistics     │             └─────────┬────────┘             │ - Statistics     │
│ - Performance    │                       │ Results              │ - Performance    │
└─────────┬────────┘                       │                      └─────────┬────────┘
          │                                v                                │
          │                      ┌──────────────────┐                      │
          │                      │  ILP Results     │                      │
          │                      │ - Schedule       │                      │
          │                      │ - Statistics     │                      │
          │                      │ - Performance    │                      │
          │                      └─────────┬────────┘                      │
          │                                │                                │
          └────────────────────────────────┼────────────────────────────────┘
                                           │ All Results
                                           v
                                 ┌──────────────────┐
                                 │                  │
                                 │ Results Aggreg.  │
                                 │ & Analysis       │
                                 │   (utils.py)     │
                                 └─────────┬────────┘
                                           │ Processed
                                           │ Results
                                           v
                                 ┌──────────────────┐
                                 │                  │
                                 │ Visualization    │
                                 │ Generation       │
                                 │ (matplotlib)     │
                                 └─────────┬────────┘
                                           │ Charts
                                           │ (PNG)
                                           v
┌──────────────────┐             ┌──────────────────┐
│                  │             │                  │
│  HTML Template   │────────────►│ Report Generator │
│ (report_template │   Template  │    (utils.py)    │
│     .html)       │             │                  │
└──────────────────┘             └─────────┬────────┘
                                           │ Final
                                           │ Report
                                           v
                                 ┌──────────────────┐
                                 │                  │
                                 │  Output Files    │
                                 │ - HTML Report    │
                                 │ - PNG Charts     │
                                 │ - Timestamped    │
                                 │   Directory      │
                                 └──────────────────┘
```

## Detailed Data Transformation

### 1. Input Data Processing

```
Raw JSON Dataset
       │
       │ utils.load_dataset()
       v
┌─────────────────────────────┐
│ Python Dictionary:          │
│ {                          │
│   "dosen": [...],          │
│   "matakuliah": [...],     │
│   "ruangan": [...],        │
│   "slot_waktu": [...]      │
│ }                          │
└─────────────┬───────────────┘
              │
              │ Validation & Processing
              v
┌─────────────────────────────┐
│ Processed Data Structures:  │
│ - ID mappings               │
│ - Time conversions          │
│ - Capacity checks           │
│ - Constraint validation     │
└─────────────┬───────────────┘
              │
              │ Distribution to Algorithms
              v
    ┌─────────┼─────────┐
    │         │         │
    v         v         v
 Greedy  Backtrack    ILP
```

### 2. Algorithm Processing

```
┌─────────────────┐
│ Algorithm Input │
│ (Processed Data)│
└─────────┬───────┘
          │
          │ Algorithm-specific processing
          v
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│ Greedy Process  │         │Backtrack Process│         │  ILP Process    │
│                 │         │                 │         │                 │
│ 1. Sort courses │         │ 1. Sort courses │         │ 1. Generate     │
│ 2. First-fit    │         │ 2. Recursive    │         │    variables    │
│    assignment   │         │    search       │         │ 2. Set up       │
│ 3. No backtrack │         │ 3. Backtrack on │         │    constraints  │
│                 │         │    conflicts    │         │ 3. Solve LP     │
└─────────┬───────┘         └─────────┬───────┘         └─────────┬───────┘
          │                           │                           │
          │ Schedule + Stats          │ Schedule + Stats          │ Schedule + Stats
          v                           v                           v
┌─────────────────┐         ┌─────────────────┐         ┌─────────────────┐
│ Greedy Output:  │         │Backtrack Output:│         │ ILP Output:     │
│ {               │         │ {               │         │ {               │
│   "schedule": [],         │   "schedule": [],         │   "schedule": [],
│   "stats": {    │         │   "stats": {    │         │   "stats": {    │
│     "time": x,  │         │     "time": y,  │         │     "time": z,  │
│     "conflicts":│         │     "conflicts":│         │     "conflicts":│
│     ...         │         │     ...         │         │     ...         │
│   }             │         │   }             │         │   }             │
│ }               │         │ }               │         │ }               │
└─────────┬───────┘         └─────────┬───────┘         └─────────┬───────┘
          │                           │                           │
          └─────────────┬─────────────┴─────────────┬─────────────┘
                        │                           │
                        v                           v
              ┌─────────────────────────────────────┐
              │        Combined Results:            │
              │ {                                   │
              │   "Greedy": {schedule, stats},      │
              │   "Backtracking": {schedule, stats},│
              │   "ILP": {schedule, stats}          │
              │ }                                   │
              └─────────────┬───────────────────────┘
                            │
                            v
                  ┌─────────────────┐
                  │ Report Generation│
                  └─────────────────┘
```

### 3. Output Generation Pipeline

```
Combined Algorithm Results
           │
           │ Analysis & Aggregation
           v
┌─────────────────────────────┐
│ Statistical Analysis:       │
│ - Performance comparison    │
│ - Resource usage analysis   │
│ - Conflict detection        │
│ - Success rate calculation  │
└─────────────┬───────────────┘
              │
              │ Parallel Processing
              ├─────────────────────┬─────────────────────┐
              │                     │                     │
              v                     v                     v
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ Chart Generation    │   │ Table Generation    │   │ HTML Composition    │
│                     │   │                     │   │                     │
│ 1. Performance      │   │ 1. Dataset tables   │   │ 1. Load template    │
│    comparison       │   │ 2. Schedule tables  │   │ 2. Insert data      │
│ 2. Usage analysis   │   │ 3. Statistics       │   │ 3. Insert charts    │
│ 3. Schedule dist.   │   │    tables           │   │ 4. Insert tables    │
│                     │   │                     │   │                     │
└─────────┬───────────┘   └─────────┬───────────┘   └─────────┬───────────┘
          │                         │                         │
          │ PNG Files               │ HTML Fragments          │ Complete HTML
          v                         v                         v
┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
│ Image Files:        │   │ Data Tables:        │   │ Final Report:       │
│ - performance_      │   │ - Formatted HTML    │   │ - Complete HTML     │
│   comparison.png    │   │ - Bootstrap styling │   │ - Embedded charts   │
│ - schedule_         │   │ - Interactive       │   │ - Professional      │
│   comparison.png    │   │   elements          │   │   layout            │
│ - usage_*.png       │   │                     │   │                     │
└─────────┬───────────┘   └─────────┬───────────┘   └─────────┬───────────┘
          │                         │                         │
          └─────────────────────────┼─────────────────────────┘
                                    │
                                    v
                          ┌─────────────────────┐
                          │ File System Output: │
                          │ report/             │
                          │ ├── YYYYMMDD_HHMMSS/│
                          │ │   ├── report.html  │
                          │ │   ├── *.png        │
                          │ │   └── metadata     │
                          └─────────────────────┘
```

## Data Structure Evolution

### Raw Dataset → Processed Data

```
JSON Input:                    Processed Internal:
{                             {
  "dosen": [                    "_dosen_lookup": {
    {                             1: "Dr. Andi",
      "id": 1,                    2: "Dr. Siti",
      "nama": "Dr. Andi",         ...
      ...                       },
    }                           "_mk_by_dosen": {
  ],                              1: [mk1, mk3],
  "matakuliah": [                 2: [mk2, mk4],
    {                             ...
      "id": 1,                  },
      "nama": "PTI",            "_time_slots_minutes": [
      "dosen_id": 1,              {480, 495, 510, ...}, // Monday
      ...                         {480, 495, 510, ...}, // Tuesday
    }                             ...
  ],                            ],
  ...                           ...
}                             }
```

### Algorithm Output → Report Data

```
Algorithm Results:                Report Data:
{                                {
  "Greedy": {                      "algorithms": ["Greedy", "Backtrack", "ILP"],
    "schedule": [...],             "performance_data": {
    "stats": {                       "times": [0.1, 2.5, 15.8],
      "execution_time": 0.1,         "scheduled": [45, 50, 52],
      "scheduled_slots": 45,         "conflicts": [5, 2, 0]
      "conflicts": 5                },
    }                              "schedule_data": {
  },                                 "Greedy": formatted_schedule,
  "Backtracking": {                  "Backtracking": formatted_schedule,
    "schedule": [...],               "ILP": formatted_schedule
    "stats": {                     },
      "execution_time": 2.5,       "charts": {
      "scheduled_slots": 50,         "performance": "performance.png",
      "conflicts": 2                 "schedule": "schedule.png",
    }                                "usage": ["room_usage.png", ...]
  },                               },
  "ILP": {                         "metadata": {
    "schedule": [...],               "timestamp": "2024-01-01 12:00",
    "stats": {                       "dataset": "dataset.json",
      "execution_time": 15.8,        "total_courses": 32
      "scheduled_slots": 52,       }
      "conflicts": 0               }
    }
  }
}
```

## Data Validation Flow

```
┌─────────────────┐
│ Input JSON      │
└─────────┬───────┘
          │
          │ JSON.parse()
          v
┌─────────────────┐
│ Basic Structure │
│ Validation      │
│ - Required keys │
│ - Data types    │
└─────────┬───────┘
          │
      ┌───v───┐
      │Valid? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Throw     │
    │ JSON Error│
    └───────────┘
          │ Yes
          v
┌─────────────────┐
│ Business Rules  │
│ Validation      │
│ - ID uniqueness │
│ - Foreign keys  │
│ - Constraints   │
└─────────┬───────┘
          │
      ┌───v───┐
      │Valid? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Show      │
    │ Warnings  │
    └─────┬─────┘
          │
          │ Yes/Continue
          v
┌─────────────────┐
│ Data Enhancement│
│ - Lookup tables │
│ - Computed fields│
│ - Optimization  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Ready for       │
│ Algorithm       │
│ Processing      │
└─────────────────┘
```

## Error Propagation

```
Error Source → Detection → Handling → User Feedback

Dataset Issues:
JSON Parse Error → load_dataset() → Exception → "Invalid JSON format"
Missing Fields → validation → Warning → "Missing optional field X"
Invalid Values → business_rules → Error → "Course Y has invalid capacity"

Algorithm Issues:
Memory Error → solve() → Exception → "Dataset too large, try smaller set"
Timeout → solve() → Warning → "Algorithm timed out, partial results"
No Solution → solve() → Info → "No feasible solution found"

Output Issues:
File Permission → report_gen() → Exception → "Cannot write to report directory"
Chart Generation → matplotlib → Warning → "Charts unavailable, text report only"
Template Missing → html_gen() → Exception → "Report template not found"
```

---

[← ILP Flowchart](ilp-flowchart.md) | [→ System Architecture](../diagrams/system-architecture.md)