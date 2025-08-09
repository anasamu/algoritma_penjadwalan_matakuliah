# Backtracking Algorithm Flowchart

## Backtracking Scheduling Process

```
┌─────────────────┐
│ BACKTRACK START │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Sort Mata Kuliah│
│ by Complexity:  │
│ - Most students │
│ - Most constrained
│ - Hardest first │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Initialize:     │
│ - course_index=0│
│ - schedule = [] │
│ - used_rooms{}  │
│ - used_dosen{}  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ RECURSIVE CALL: │
│ backtrack(      │
│   course_index, │
│   current_state)│
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ BASE CASE:      │
│ course_index >= │
│ total_courses?  │
└─────────┬───────┘
          │ Yes
    ┌─────v─────┐
    │ SUCCESS!  │
    │ Return    │
    │ True      │
    └───────────┘
          │ No
          v
┌─────────────────┐
│ Get Current     │
│ Course to       │
│ Schedule        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Generate All    │
│ Required        │
│ Sessions for    │
│ Current Course  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ FOR each        │
│ possible        │
│ assignment      │
│ (time + room)   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check if        │
│ Assignment      │
│ is Valid:       │
│ - Capacity OK   │
│ - No conflicts  │
│ - Time fits     │
└─────────┬───────┘
          │
      ┌───v───┐
      │Valid? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Try Next  │
    │ Assignment│
    └─────┬─────┘
          │
          │ Yes
          v
┌─────────────────┐
│ MAKE            │
│ ASSIGNMENT:     │
│ - Add to        │
│   schedule      │
│ - Mark resources│
│   as used       │
│ - Update state  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ RECURSIVE CALL: │
│ backtrack(      │
│   course_index+1,
│   new_state)    │
└─────────┬───────┘
          │
      ┌───v───┐
      │Success?│
      └───┬───┘
          │ Yes
    ┌─────v─────┐
    │ Propagate │
    │ SUCCESS   │
    │ Return    │
    │ True      │
    └───────────┘
          │ No
          v
┌─────────────────┐
│ BACKTRACK:      │
│ - Remove from   │
│   schedule      │
│ - Free resources│
│ - Restore state │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Try Next        │
│ Assignment      │
│ (continue loop) │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ All assignments │
│ tried for       │
│ current course? │
└─────────┬───────┘
          │ No
          │ (back to assignment loop)
          │
          │ Yes
          v
┌─────────────────┐
│ FAILURE:        │
│ No valid        │
│ assignment      │
│ found           │
│ Return False    │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ BACKTRACK END   │
│ (with result)   │
└─────────────────┘
```

## Detailed Assignment Validation

```
┌─────────────────┐
│ is_valid_       │
│ assignment()    │
│ Parameters:     │
│ - course        │
│ - time_slot     │
│ - room          │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Check Capacity  │
│ Constraint:     │
│ course.students │
│ ≤ room.capacity │
└─────────┬───────┘
          │
      ┌───v───┐
      │ OK?   │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Return    │
    │ False     │
    └───────────┘
          │ Yes
          v
┌─────────────────┐
│ Check Duration  │
│ Constraint:     │
│ session_duration│
│ fits in slot    │
└─────────┬───────┘
          │
      ┌───v───┐
      │ Fits? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Return    │
    │ False     │
    └───────────┘
          │ Yes
          v
┌─────────────────┐
│ Check Room      │
│ Availability:   │
│ No overlapping  │
│ sessions        │
└─────────┬───────┘
          │
      ┌───v───┐
      │Available?│
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Return    │
    │ False     │
    └───────────┘
          │ Yes
          v
┌─────────────────┐
│ Check Lecturer  │
│ Availability:   │
│ No overlapping  │
│ teaching duties │
└─────────┬───────┘
          │
      ┌───v───┐
      │Available?│
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ Return    │
    │ False     │
    └───────────┘
          │ Yes
          v
┌─────────────────┐
│ All Constraints │
│ Satisfied       │
│ Return True     │
└─────────────────┘
```

## State Management

```
┌─────────────────┐
│ MAKE            │
│ ASSIGNMENT      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Create Session  │
│ Object with:    │
│ - course_id     │
│ - room_id       │
│ - time_start    │
│ - time_end      │
│ - lecturer_id   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Add Session to  │
│ Current         │
│ Schedule        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Mark Room as    │
│ Used:           │
│ used_rooms      │
│ [day][room]     │
│ .append(time)   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Mark Lecturer   │
│ as Busy:        │
│ used_dosen      │
│ [day][lecturer] │
│ .append(time)   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Assignment      │
│ Complete        │
└─────────────────┘

┌─────────────────┐
│ UNDO            │
│ ASSIGNMENT      │
│ (Backtrack)     │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Remove Session  │
│ from Schedule   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Free Room:      │
│ Remove time     │
│ interval from   │
│ used_rooms      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Free Lecturer:  │
│ Remove time     │
│ interval from   │
│ used_dosen      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ State Restored  │
│ to Previous     │
│ Point           │
└─────────────────┘
```

## Optimization Strategies

### Variable Ordering Heuristics

```
┌─────────────────┐
│ Choose Next     │
│ Course to       │
│ Schedule        │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Strategy 1:     │
│ Most Constrained│
│ First (MRV)     │
│ - Fewest rooms  │
│ - Fewest times  │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Strategy 2:     │
│ Largest Course  │
│ First           │
│ - Most students │
│ - Hardest to    │
│   place later   │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Strategy 3:     │
│ Lecturer        │
│ Workload        │
│ - Balance       │
│   teaching load │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Select Best     │
│ Strategy based  │
│ on Problem      │
│ Characteristics │
└─────────────────┘
```

### Pruning Techniques

```
┌─────────────────┐
│ Before Making   │
│ Assignment      │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Forward         │
│ Checking:       │
│ Will this       │
│ assignment make │
│ future          │
│ assignments     │
│ impossible?     │
└─────────┬───────┘
          │
      ┌───v───┐
      │ Safe? │
      └───┬───┘
          │ No
    ┌─────v─────┐
    │ PRUNE:    │
    │ Skip this │
    │ assignment│
    └───────────┘
          │ Yes
          v
┌─────────────────┐
│ Constraint      │
│ Propagation:    │
│ Update domain   │
│ of remaining    │
│ variables       │
└─────────┬───────┘
          │
          v
┌─────────────────┐
│ Early           │
│ Termination:    │
│ Good enough     │
│ solution found? │
└─────────┬───────┘
          │ Yes
    ┌─────v─────┐
    │ Return    │
    │ Current   │
    │ Solution  │
    └───────────┘
          │ No
          v
┌─────────────────┐
│ Continue        │
│ Search          │
└─────────────────┘
```

## Backtracking Characteristics

### Time Complexity: O(b^d)
- **b** = branching factor (avg. choices per decision)
- **d** = depth (number of courses)
- **Exponential** in worst case

### Space Complexity: O(d)
- **Recursion stack**: Depth = number of courses
- **State storage**: Current assignments only

### Search Strategy: Depth-First
1. **Complete assignment** before trying alternatives
2. **Systematic exploration** of solution space
3. **Backtrack** when dead-end reached
4. **Optimality**: Finds optimal solution if time permits

### Optimizations:
- 🎯 **Variable ordering**: Choose hard variables first
- ✂️ **Pruning**: Skip impossible branches early
- 🔍 **Forward checking**: Prevent future conflicts
- ⏰ **Early termination**: Stop when good enough

### Pros:
- 🎯 **Better solutions** than greedy
- ✅ **Complete search** (finds solution if exists)
- 🔄 **Flexible** - can undo bad decisions
- 📈 **Optimal** given enough time

### Cons:
- ⏱️ **Exponential time** complexity
- 💾 **Memory overhead** for state management
- 🔢 **Unpredictable** execution time
- 📊 **May timeout** on large problems

---

[← Greedy Flowchart](greedy-flowchart.md) | [→ ILP Flowchart](ilp-flowchart.md)