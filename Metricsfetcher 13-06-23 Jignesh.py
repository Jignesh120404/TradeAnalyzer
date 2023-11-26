import csv
import statistics
from collections import defaultdict
import math

trades_by_address = defaultdict(lambda: {'total': 0, 'winning': 0, 'returns': [], 'volumes': [], 'pnl': []})


with open("level finance top trades.csv", "r") as file:
    
    reader = csv.reader(file)

  
    for row in reader:
     
        address = row[1]


        try:
            pnl = float(row[4])
            volume = float(row[2])
        except (ValueError, IndexError):
            print("Invalid or non-numeric value for pnl or volume")
            continue  
    
        trades_by_address[address]['total'] += 1

       
        if pnl > 0:
            trades_by_address[address]['winning'] += 1

        
        if volume != 0:
            returns = pnl / volume * 100.0

            trades_by_address[address]['returns'].append(returns)
            trades_by_address[address]['volumes'].append(volume)
            trades_by_address[address]['pnl'].append(pnl)


with open("trade_analysis.csv", "w", newline="") as file:
    writer = csv.writer(file)

  
    writer.writerow(["Address", "ROI", "Win Rate", "Upside Capture", "Downside Capture", "Frequency", "Sharpe Ratio", "Median Volume", "Median PnL"])

    
    for address, trades in trades_by_address.items():
        total_trades = trades['total']
        winning_trades = trades['winning']
        returns = trades['returns']
        volumes = trades['volumes']
        pnl = trades['pnl']

        if total_trades > 0:
            win_rate = (winning_trades / total_trades) * 100
            upside_capture = len([r for r in returns if r > 0]) / len(returns) * 100
            downside_capture = len([r for r in returns if r < 0]) / len(returns) * 100
            if returns:
                median_returns = statistics.median(returns)
            if volumes:
                median_volume = statistics.median(volumes)
            if pnl:
                median_pnl = statistics.median(pnl)

            
            risk_free_rate = 0  
            avg_returns = statistics.mean(returns)
            std_dev = statistics.stdev(returns) if len(returns) >= 2 else math.nan
            sharpe_ratio = (avg_returns - risk_free_rate) / std_dev if std_dev != 0 else math.nan

            
            writer.writerow([address, median_returns, win_rate, upside_capture, downside_capture, total_trades, sharpe_ratio, median_volume, median_pnl])
        else:
            
            writer.writerow([address, "No trades found", "", "", "", "", "", "", ""])

print("Trade analysis results have been written to trade_analysis.csv.")
