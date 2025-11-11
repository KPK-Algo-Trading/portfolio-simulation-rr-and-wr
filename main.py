import pandas as pd
import matplotlib.pyplot as plt
import random
import numpy as np

def simulateOne(days, winrate, rr, starting_capital, risk_amount, sim_results, sim):
    results_over_time = []
    result = starting_capital
    for i in range(days):
        results_over_time.append(result)
        random_number = random.randrange(1, 100)
        if(random_number <= winrate):
            result *= (1 + ((risk_amount*rr)/100))
        else:
            result *= (1 - (risk_amount/100))
    sim_results.append(pd.Series(results_over_time))

    return sim_results

def display(df):
    fig, ax = plt.subplots(figsize=(8, 5))
    # Plot each numeric column as a line
    for col in df.columns:
        ax.plot(df.index, df[col], label=f'Column {col}')

    ax.set_title('Line Chart')
    ax.set_xlabel('Day')
    ax.set_ylabel('Account size')
    #ax.legend(title='Columns')
    ax.grid(True)

    return fig,ax

def monteCarloPlot(df):
    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(df, alpha=0.2, color='gray')  # faint lines for each simulation
    ax.plot(df.mean(axis=1), color='blue', linewidth=2, label='Average Portfolio')

    ax.set_title('Monte Carlo Portfolio Simulations')
    ax.set_xlabel('Days')
    ax.set_ylabel('Account size')
    ax.grid(True)

    return fig,ax

def monteCarloPlotSecond(df, bins):
    final_values = df.iloc[-1]
    counts, bin_edges = np.histogram(final_values, bins=bins)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    window_size = 3  # number of bins to smooth over
    moving_avg = pd.Series(counts).rolling(window=window_size, center=True).mean()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.bar(bin_centers, counts, width=bin_edges[1]-bin_edges[0], edgecolor='black', alpha=0.7, label='Simulation density')
    ax.plot(bin_centers, moving_avg, color='red', linewidth=2, label='Moving average')
    ax.axvline(final_values.mean(), color='blue', linestyle='dashed', linewidth=2, label=f'Mean')
    
    ax.set_title('Monte Carlo Simulation – Final Portfolio Value Distribution')
    ax.set_xlabel('Final Portfolio Value ($)')
    ax.set_ylabel('Number of Simulations')
    ax.grid(axis='y', alpha=0.3)

    return fig,ax



def main():
    sim_results = []
    winrate = int(input("Pass your winrate in %: "))
    rr = int(input("Pass in your Risk to Reward ratio 1:"))
    starting_capital = int(input("Input your starting capital in usd$: "))
    risk_amount = int(input("Input your risk amount in % of your account: "))
    days_to_simulate = int(input("How many days would you like to simulate?: "))
    num_of_simulations = int(input("how many times would you like to simulate?: "))
    bins = int(input("How many bins on the barchart?: "))

    dataframe = pd.DataFrame(index=range(days_to_simulate))

    for i in range(num_of_simulations):
        sim_results = simulateOne(days_to_simulate, winrate, rr, starting_capital, risk_amount, sim_results, i)
    
    dataframe = pd.concat(sim_results, axis=1)
    dataframe.columns = range(num_of_simulations)
    
    fig1, ax1 = display(dataframe)
    fig2, ax2 = monteCarloPlot(dataframe)
    fig3, ax3 = monteCarloPlotSecond(dataframe, bins)

    plt.show()

    final_values = dataframe.iloc[-1]
    highest = final_values.max()
    lowest = final_values.min()
    mean_final = final_values.mean()

    print(f"Highest final portfolio: ${highest:,.2f}")
    print(f"Lowest final portfolio:  ${lowest:,.2f}")
    print(f"Average final portfolio: ${mean_final:,.2f}")


if __name__ == "__main__":
    main()
