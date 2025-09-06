# Crossover Trading Bot (Alpaca API + Python)
#### Video Demo: [Watch Here](https://youtu.be/vVf5KyeJTx8)

## Description

This is a real-time automated trading bot built using the [Alpaca API](https://alpaca.markets/) and Python. It trades **AMZN stock** using a short-term **Moving Average Crossover Strategy** on 1-minute candlestick data. The bot runs continuously and places **bracket orders** with predefined **Take Profit (TP)** and **Stop Loss (SL)** levels.

---

## Features

-  Fetches 1-minute historical data from Alpaca
-  Calculates 1-hour and 6-hour moving averages
-  Generates buy/sell signals using crossover detection
-  Executes paper trades using bracket orders
-  Automatically manages TP and SL
-  Loops every 60 seconds for updates
-  API keys securely stored in `config.py`

---

## Strategy Overview

The bot uses a **Moving Average Crossover Strategy**, a classic trend-following technique used in algorithmic trading.

It compares two Simple Moving Averages (SMA) calculated from recent 1-minute price data:

- **MA1**: 1-hour SMA → `rolling(60)`
- **MA6**: 6-hour SMA → `rolling(360)`
- **pre_MA1**: Previous MA1 to detect actual crossover

### 🔼 Buy Signal (Bullish Crossover)
A buy is triggered when:
- Current **MA1 ≥ MA6**
- Previous **MA1 < MA6**

This implies the shorter-term average has just crossed above the longer-term, signaling **upward momentum**.

### 🔽 Sell Signal (Bearish Crossover)
A sell is triggered when:
- Current **MA1 ≤ MA6**
- Previous **MA1 > MA6**

This indicates a downward momentum shift, prompting a **short** position.

### No Signal
If neither crossover occurs, the bot **waits** for the next opportunity without placing any trades.

---

## Why Moving Averages?

- Helps filter market noise
- Identifies potential trend reversals
- Simple and effective for automated trading

---

## Risk Management

The bot follows a **2:1 Reward-to-Risk** ratio using bracket orders:

- **Buy SL**: Lowest low from last 100 candles
- **Buy TP**: Entry + 2 × (Entry − SL)
- **Sell SL**: Highest high from last 100 candles
- **Sell TP**: Entry − 2 × (SL − Entry)

Bracket orders automatically place TP and SL with each trade.

---

## Setup Instructions

### 1. Clone the Repo

```bash
git clone https://github.com/amit1527/crossover-trading-bot.git
cd crossover-trading-bot
