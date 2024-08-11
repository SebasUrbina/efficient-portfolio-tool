# Efficient Portfolio Tool

Efficient Portfolio Tool is a [Streamlit ](https://streamlit.io/) application designed to help users create efficient investment portfolios using [Markowitz's Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory). This tool provides a user-friendly interface to construct and visualize the efficient frontier, enabling you to optimize asset allocation for maximum return and minimum risk.

## Overview

This application was inspired by the [Medium post on constructing Markowitz's efficient frontier](https://medium.com/@guilherme.ziegler/constructing-markowitzs-efficient-frontier-with-python-and-streamlit-f99a495fb74d) by Guilherme Ziegler and another [related article](https://medium.com/datadriveninvestor/coding-markowitzs-efficient-frontier-with-python-and-streamlit-97014e8cb06d). While inspired by these resources, the code and functionalities of this tool were independently developed to provide a unique and tailored experience.

## Features

- ✅ **Multi-Currency Data Extraction**: Seamlessly extract and process data from multiple currencies, enabling comprehensive portfolio analysis.
- 🔄 **Efficient Frontier Construction**: Build and visualize the efficient frontier based on selected assets.
- 🔄 **Portfolio Optimization**: Identify the optimal portfolio allocation for maximum return with minimum risk.
- 🔄 **Interactive Visualizations**: Use Plotly to create dynamic, interactive charts that help you understand the portfolio's risk-return trade-off.
- 🔄**User-Friendly Interface**: Leverage the power of Streamlit to make sophisticated portfolio management accessible to users of all experience levels.

## Getting Started

To use this tool, simply follow the instructions below to set up and run the application.

### Prerequisites

```
streamlit==1.37.1
yfinance==0.2.41
plotly==5.23.0
pyportfolioopt==1.5.5
```

### Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/yourusername/efficient-portfolio-tool.git
cd efficient-portfolio-tool
pip install -r requirements.txt
```

### Usage
```bash
streamlit run app.py
```

Open the provided URL in your web browser to start using the Efficient Portfolio Tool.

### Inspiration and Acknowledgements

This project draws inspiration from [Guilherme Ziegler's Medium article]((https://medium.com/@guilherme.ziegler/constructing-markowitzs-efficient-frontier-with-python-and-streamlit-f99a495fb74d)) and other related works. Although the app is similar, all code has been independently developed to ensure a unique implementation.