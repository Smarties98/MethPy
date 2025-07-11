# MethPy

![logo](logo.png)
![Copyright](https://img.shields.io/badge/copyright-2025-blue?style=for-the-badge)]
![Version](https://img.shields.io/badge/V_1.0-yellow)

MethPy is a Python toolkit for the analysis and visualization of DNA methylation data, with features for quality control, table and graph generation, and management of reference datasets.

## 🧪 Main Features

- Loading and validation of methylation data
- Analysis and quality control (`check.py`)
- Visualization of results (`plot.py`)
- Management of biological references (`ref.py`)
- Table generation (`table.py`)
- Guided execution (`start.py`, `tutorial.py`)

## 🚀 Installation

Must have: Python ≥ 3.8 installed.

```bash
git clone https://github.com/Smarties98/MethPy.git
cd MethPy
pip install .
```

Using  `pip` directly:

```bash
pip install git+https://github.com/Smarties98/MethPy.git
```

## 🧭 Usage

Start the main interface from the terminal with:

```bash
python -m methpy.start
```

Refer to the `tutorial.py` module for practical and demonstration examples, as different OS

## 📁 Project Structure

```
methpy/
├── check.py        # Data quality control
├── plot.py         # Graphical visualization
├── ref.py          # Reference management
├── start.py        # Main entry point
├── table.py        # Table generation
└── tutorial.py     # Examples and guide
```

## 📄 License

This project is distributed under the [MIT](./LICENSE) license.

## 👨‍💻 Author

Developer: Martina Roiati
Corresponding Author: Andrea Fuso, PhD
