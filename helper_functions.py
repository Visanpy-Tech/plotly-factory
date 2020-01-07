import pandas as pd
from collections import OrderedDict

def make_counts_df(df, main_category, sub_category, n_main, n_sub, add_percentage=False, bold=False):

    main_counts = df[main_category].value_counts()
    total_counts = OrderedDict()
    for main in main_counts.index[:n_main]:
        sub_counts = df.loc[df[main_category] ==
                            main][sub_category].value_counts()
        subs = sub_counts.index[:n_sub]
        percentage = 100 * sub_counts.values[:n_sub] / sum(sub_counts.values)
        for sub, percent in zip(subs, percentage):
            if main not in total_counts.keys():
                if add_percentage:
                    if bold:
                        perc = sub + f" <br>{percent:.1f} %</br>"
                    else:
                        perc = sub + f" {percent:.1f} %"
                        
                    total_counts.update(
                        {main: [perc]})
                else:
                    total_counts.update({main: [sub]})
            else:
                if add_percentage:
                    if bold:
                        perc = f" <br>{percent:.1f} %</br>"
                    else:
                        perc = f" {percent:.1f} %"
                    total_counts[main].append(
                        sub + perc)
                else:
                    total_counts[main].append(sub)

    return pd.DataFrame(total_counts)