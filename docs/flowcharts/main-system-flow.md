# System Flowchart

## Main System Flow

```
┌─────────────────┐
│   START SYSTEM  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│   Load Dataset  │
│   (dataset.json)│
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Validate Dataset│
│ - Structure     │
│ - Data Types    │
│ - Constraints   │
└─────────┬───────┘
          │
      ┌───v───┐
      │Valid? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │Show Errors│
    │   EXIT    │
    └───────────┘
          │ Yes
          v
┌─────────────────┐
│ Initialize      │
│ Schedulers:     │
│ - Greedy        │
│ - Backtracking  │
│ - ILP           │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Execute         │
│ Algorithms      │
│ (Parallel/      │
│  Sequential)    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Collect Results │
│ - Schedules     │
│ - Statistics    │
│ - Performance   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Generate        │
│ Visualizations  │
│ - Performance   │
│ - Usage Charts  │
│ - Comparisons   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Create HTML     │
│ Report          │
│ - Combine Data  │
│ - Format Output │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Save Report     │
│ to Timestamped  │
│ Directory       │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│    END SYSTEM   │
│   (Success)     │
└─────────────────┘
```

## Algorithm Execution Flow

```
┌─────────────────┐
│ For Each        │
│ Algorithm       │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Start Timer     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Initialize      │
│ Data Structures │
│ - Schedule []   │
│ - Used Resources│
│ - Failed List   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Execute Core    │
│ Algorithm Logic │
│ (See individual │
│  flowcharts)    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Stop Timer      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Calculate       │
│ Statistics      │
│ - Success Rate  │
│ - Conflicts     │
│ - Resource Usage│
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Return Results  │
│ {schedule,stats}│
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Next Algorithm  │
│ or Complete     │
└─────────────────┘
```

---

[→ Greedy Algorithm Flowchart](greedy-flowchart.md)
[→ Backtracking Algorithm Flowchart](backtracking-flowchart.md)  
[→ ILP Algorithm Flowchart](ilp-flowchart.md)
[→ Data Flow Diagram](data-flow-diagram.md)