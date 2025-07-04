# Cafe Employee Scheduling System

A Python-based employee scheduling system that uses a recursive divide-and-conquer algorithm to optimize shift assignments based on business demand patterns and employee experience levels.

## Build/Run Instructions

### Prerequisites
- Python 3.x

### Running the Application
```bash
python3 cafe_scheduler.py
```

This will execute the scheduling algorithm with test data and display a weekly schedule for 9 employees across 7 days.

### Testing
The main function includes built-in test scenarios that demonstrate the algorithm's behavior across different business patterns and employee availability constraints.

## Algorithm Overview

The system implements a recursive divide-and-conquer approach:
1. Splits time periods at the midpoint
2. Calculates business levels for each half
3. Assigns experienced workers to busier periods
4. Assigns less experienced workers to quieter periods
5. Recurses until minimum shift duration (2 hours) is reached

## Project Structure

- `cafe_scheduler.py` - Main application containing all classes and scheduling logic
- `README.md` - This file

## Tag Reference

Final submission tagged as: `v1.2-final`
