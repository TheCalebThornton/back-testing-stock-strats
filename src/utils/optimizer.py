#TODO - Update this function to accept strats with params and stockDataFrames
def optimize_stochastic_smac_hybrid_results (stockDataFrames):
    lengths = [1,2,3]
    smoothKs = [1,2,3,4,5,6]
    smoothDs = [1,2,3,4,5,6]
    upperBounds = [65, 80]
    lowerBounds = [45, 20]

    def get_avg_on_column (iterable, property):
        sum = 0.0
        for item in iterable:
            sum = sum + item[property]
        return sum / len(iterable)

    allPossibleCombos = np.array(np.meshgrid(lengths,smoothKs,smoothDs,upperBounds,lowerBounds)).T.reshape(-1,5)
    runningResults = []

    for optionSet in allPossibleCombos:
        runningOptionResults = []
        options_parsed = {
            'length': optionSet[0],
            'smoothK': optionSet[1],
            'smoothD': optionSet[2],
            'upperBound': optionSet[3],
            'lowerBound': optionSet[4]
        }
        for stockData in stockDataFrames:
            temp_res = stochastic_smac_hybrid(stockData, stratOptions=options_parsed).iloc[0]
            temp_res['stoch_hybrid_print'] = True
            temp_res['custom_opts'] = options_parsed
            runningOptionResults.append(temp_res)
        resultSetForStockFrames = pd.DataFrame(data={
            'configuration': f'{options_parsed}',
            # 'results': runningOptionResults,
            'average_gain': get_avg_on_column(runningOptionResults, 'pnl'),
            'average_win_rate': get_avg_on_column(runningOptionResults, 'win_rate'),
            'average_total_trades': get_avg_on_column(runningOptionResults, 'total')
        }, index=[0])
        runningResults.append(resultSetForStockFrames)

    for res in runningResults:
        file_path = 'src/testing_results/optimizerResults.csv'
        if not os.path.isfile(file_path):
           res.to_csv(file_path)
        else: # else it exists so append without writing the header
           res.to_csv(file_path, mode='a', header=False)

    return runningResults
