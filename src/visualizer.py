import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def plot_results(df, game_name):
    fig, ax1 = plt.subplots(figsize=(12, 6))
    
    # Steam followers (line)
    ax1.plot(
        df['Date'], 
        df['Steam_Followers'], 
        'b-', 
        label='Steam Followers'
    )
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Followers', color='b')
    ax1.tick_params('y', colors='b')
    
    # Mentions (scatter)
    ax2 = ax1.twinx()
    ax2.scatter(
        df['Date'], 
        df['Social_Mentions'], 
        color='r', 
        label='Reddit Mentions'
    )
    ax2.set_ylabel('Mentions', color='r')
    ax2.tick_params('y', colors='r')
    
    # Formatting
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    fig.autofmt_xdate()
    plt.title(f'{game_name} - Followers vs Mentions')
    fig.tight_layout()
    import config
    plt.savefig(config.PLOT_FILENAME, dpi=300)