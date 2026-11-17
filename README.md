# DAA Lab 4 — Dynamic Programming

**Student:** Harshit Kumar  
**Roll Number:** 2401201057  
**Programme:** BCA (AI & Data Science)  
**Section:** B  
**Course Code:** ENCA351  
**Lab:** Lab 4 — Dynamic Programming

## Algorithms
1. Longest Common Subsequence (LCS)
2. 0/1 Knapsack
3. Matrix Chain Multiplication

## Setup (Windows PowerShell)
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Run individual algorithms
```powershell
python lcs.py
python knapsack_dp.py
python matrix_chain.py
```

## Interactive menu
```powershell
python app.py
```

## Generate measurements and visualizations
```powershell
python run_experiments.py
python make_plots.py
```

Benchmark CSV files and generated images are saved in `outputs/`.

## Complexity summary

| Algorithm | Time | Space |
|---|---:|---:|
| LCS | O(mn) | O(mn) |
| 0/1 Knapsack | O(nC) | O(nC), optimized O(C) |
| Matrix Chain Multiplication | O(n^3) | O(n^2) |

**Important:** Benchmark results depend on the computer, Python version and system load. Use the generated CSV files from your own run in the final report.
