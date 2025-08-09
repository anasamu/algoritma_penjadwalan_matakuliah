# Integer Linear Programming (ILP) Flowchart

## ILP Mathematical Optimization Process

```
┌─────────────────┐
│ ILP START       │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Generate All    │
│ Possible Time   │
│ Slots (15-min   │
│ intervals)      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Create Decision │
│ Variables:      │
│ x[i,j,k,t] =    │
│ binary variable │
│ for each valid  │
│ combination     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Filter Feasible │
│ Combinations:   │
│ - Capacity OK   │
│ - Duration fits │
│ - Valid time    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Setup LP        │
│ Problem:        │
│ - Objective     │
│ - Constraints   │
│ - Variable      │
│   bounds        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Define          │
│ Objective       │
│ Function:       │
│ Maximize        │
│ Σ x[i,j,k,t]    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Add Constraint  │
│ Types:          │
│ 1. Session Limit│
│ 2. Room Conflict│
│ 3. Lecturer     │
│    Conflict     │
│ 4. Capacity     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Configure       │
│ Solver:         │
│ - CBC (default) │
│ - Time limit    │
│ - MIP gap       │
│ - Threads       │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ SOLVE LP        │
│ PROBLEM         │
│ (Call CBC       │
│  solver)        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Solver    │
│ Status:         │
│ - Optimal       │
│ - Infeasible    │
│ - Time limit    │
│ - Error         │
└─────────┬───────┘
          │
      ┌───v───┐
      │Optimal?│
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Handle    │
    │ Non-optimal│
    │ Result    │
    └─────┬─────┘
          │
          │ Yes
          v
┌─────────────────┐
│ Extract         │
│ Solution:       │
│ Find variables  │
│ with value = 1  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Convert         │
│ Variables to    │
│ Schedule        │
│ Entries         │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Calculate       │
│ Statistics:     │
│ - Scheduled     │
│ - Conflicts     │
│ - Optimality    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Return Results: │
│ {schedule,      │
│  stats}         │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ ILP END         │
└─────────────────┘
```

## Variable Generation Process

```
┌─────────────────┐
│ Generate        │
│ Decision        │
│ Variables       │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ course i in     │
│ matakuliah      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ room j in       │
│ ruangan         │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Capacity  │
│ Feasibility:    │
│ students[i] ≤   │
│ capacity[j]     │
└─────────┬───────┘
          │
      ┌───v───┐
      │ OK?   │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Skip this │
    │ room for  │
    │ this course│
    └─────┬─────┘
          │
          │ Yes
          v
┌─────────────────┐
│ FOR each        │
│ time slot t     │
│ (15-min         │
│ intervals)      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Duration  │
│ Feasibility:    │
│ course_duration │
│ fits in         │
│ remaining slot  │
└─────────┬───────┘
          │
      ┌───v───┐
      │ Fits? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Skip this │
    │ time slot │
    └─────┬─────┘
          │
          │ Yes
          v
┌─────────────────┐
│ Create Binary   │
│ Variable:       │
│ x[i,j,t] =      │
│ {0, 1}          │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Add to Variable │
│ Dictionary with │
│ Unique Name     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Continue to     │
│ Next            │
│ Combination     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ All Variables   │
│ Generated       │
└─────────────────┘
```

## Constraint Generation

### 1. Session Limit Constraints
```
┌─────────────────┐
│ FOR each        │
│ course i        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Calculate       │
│ Required        │
│ Sessions:       │
│ sessions[i]     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Add Constraint: │
│ Σ(j,t) x[i,j,t] │
│ ≤ sessions[i]   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Next Course     │
└─────────────────┘
```

### 2. Room Conflict Constraints
```
┌─────────────────┐
│ FOR each        │
│ room j          │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ time slot t     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Add Constraint: │
│ Σ(i) x[i,j,t]   │
│ ≤ 1             │
│ (max 1 course   │
│  per room/time) │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Next Time/Room  │
└─────────────────┘
```

### 3. Lecturer Conflict Constraints
```
┌─────────────────┐
│ FOR each        │
│ lecturer k      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ time slot t     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Find all        │
│ courses taught  │
│ by lecturer k   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Add Constraint: │
│ Σ(i,j) x[i,j,t] │
│ ≤ 1             │
│ for courses     │
│ where           │
│ lecturer[i] = k │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Next Time/      │
│ Lecturer        │
└─────────────────┘
```

## Solution Extraction

```
┌─────────────────┐
│ Solver Returns  │
│ Optimal         │
│ Solution        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ variable        │
│ x[i,j,t]        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Variable  │
│ Value:          │
│ var.value() == 1│
└─────────┬───────┘
          │
      ┌───v───┐
      │Selected?│
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Skip      │
    │ Variable  │
    └─────┬─────┘
          │
          │ Yes
          v
┌─────────────────┐
│ Parse Variable  │
│ Name to Extract:│
│ - course_id (i) │
│ - room_id (j)   │
│ - time_slot (t) │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Lookup Course   │
│ Details:        │
│ - name          │
│ - lecturer      │
│ - students      │
│ - SKS           │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Lookup Room     │
│ Details:        │
│ - name          │
│ - capacity      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Convert Time    │
│ Slot to:        │
│ - day name      │
│ - start time    │
│ - end time      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Create Schedule │
│ Entry:          │
│ {matakuliah,    │
│  dosen, ruangan,│
│  hari, jam, etc}│
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Add to Final    │
│ Schedule List   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Continue with   │
│ Next Variable   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Schedule        │
│ Complete        │
└─────────────────┘
```

## Mathematical Formulation

### Decision Variables
```
x[i,j,t] ∈ {0,1}

Where:
i = course index (1 to |matakuliah|)
j = room index (1 to |ruangan|)  
t = time slot index (1 to |time_slots|)

x[i,j,t] = 1 if course i is assigned to room j at time t
x[i,j,t] = 0 otherwise
```

### Objective Function
```
Maximize: Σ Σ Σ x[i,j,t]
          i j t

Goal: Maximize total number of scheduled sessions
```

### Constraints

#### 1. Session Limit
```
Σ Σ x[i,j,t] ≤ required_sessions[i]  ∀i
j t

Each course can have at most its required number of sessions
```

#### 2. Room Conflicts
```
Σ x[i,j,t] ≤ 1  ∀j,t
i

At most one course per room per time slot
```

#### 3. Lecturer Conflicts
```
Σ Σ x[i,j,t] ≤ 1  ∀k,t
i∈L[k] j

Where L[k] = set of courses taught by lecturer k
At most one course per lecturer per time slot
```

#### 4. Capacity Constraints
```
students[i] × x[i,j,t] ≤ capacity[j] × x[i,j,t]  ∀i,j,t

If course i is assigned to room j, 
then room j must have sufficient capacity
```

#### 5. Variable Bounds
```
x[i,j,t] ∈ {0,1}  ∀i,j,t

All variables are binary
```

## ILP Characteristics

### Complexity: NP-Hard
- **Problem Class**: Integer Programming is NP-hard
- **Solver**: Uses branch-and-bound with cutting planes
- **Typical Time**: Polynomial on average, exponential worst case

### Optimality Guarantee
- **Global Optimum**: Guaranteed if solver terminates with "Optimal"
- **Approximation**: Can set MIP gap for near-optimal solutions
- **Bounds**: Provides lower/upper bounds during solving

### Solver Configuration Options

```python
CBC_OPTIONS = {
    'timeLimit': 600,        # Maximum 10 minutes
    'fracGap': 0.01,        # 1% optimality gap
    'threads': 4,           # Use 4 CPU cores
    'presolve': 'on',       # Enable preprocessing
    'cuts': 'on',           # Enable cutting planes
    'heuristics': 'on'      # Enable heuristics
}
```

### Memory Requirements
- **Variables**: O(|courses| × |rooms| × |time_slots|)
- **Constraints**: O(|courses| + |rooms|×|time_slots| + |lecturers|×|time_slots|)
- **Matrix**: Sparse representation for efficiency

### Pros:
- 🎯 **Optimal solutions** (given enough time)
- 📊 **Mathematical rigor** and proven bounds
- 🔧 **Flexible** - easy to add new constraints
- ⚖️ **Multi-objective** optimization possible

### Cons:
- ⏱️ **Computationally expensive** for large problems
- 💾 **High memory usage** for variable storage
- 🔧 **Complex setup** and mathematical modeling
- 📦 **External dependency** on LP solver

---

[← Backtracking Flowchart](backtracking-flowchart.md) | [→ Data Flow Diagram](data-flow-diagram.md)