
# 🚀 Quick Guide to Python Jupyter Usage

## 🛠️ Before You Begin: Set Up a Virtual Environment (venv)
It's best practice to use a virtual environment to keep dependencies isolated.

```bash
pip install virtualenv

# Create a virtual environment
python -m venv myenv

# Activate it (Windows)
myenv\Scripts\activate

# Activate it (macOS/Linux)
source myenv/bin/activate
```

## 🧰 1. What is Jupyter Notebook?
Jupyter Notebooks let you write and run Python code in an interactive, cell-based format—great for data science, experimentation, and learning.

## 📦 2. How to Launch
- Install Jupyter via Anaconda (recommended) or `pip install notebook`
- Run:

```bash
jupyter notebook
```
This will open it in your browser.

## 🔹 3. Notebook Interface Basics
- **Code Cells**: Write Python code here
- **Markdown Cells**: Write formatted text using Markdown
- **Run Cell**: `Shift + Enter`
- **Add Cell**: `+` icon or `B` (below), `A` (above)

## 🐍 4. Basic Python in Jupyter

```python
# Simple output
print("Hello, Jupyter!")

# Math
x = 10
y = 5
x + y

# Loop
for i in range(3):
    print(i)
```

## 📊 5. Plotting (example with matplotlib)

```python
import matplotlib.pyplot as plt

x = [1, 2, 3]
y = [2, 4, 1]
plt.plot(x, y)
plt.title("Simple Plot")
plt.show()
```

## 🧪 6. Data Handling (with pandas)

```python
import pandas as pd

# Create DataFrame
df = pd.DataFrame({
    'Name': ['Alice', 'Bob'],
    'Age': [25, 30]
})
print(df)

# Read CSV
# df = pd.read_csv('your_file.csv')
```

## 🔍 7. Magic Commands

```python
%timeit x = sum(range(1000))  # Timing code
%matplotlib inline  # Plots inline
```

## 💾 8. Save & Export
- Save: `Ctrl + S` or File > Save
- Export: File > Download as (HTML, PDF, Python script)
