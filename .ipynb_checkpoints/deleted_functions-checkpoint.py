
def plot_hue(df, main_bars, sub_bars, transparent=True):
    d_dict = defaultdict(list)

    grp = df.groupby(by=[sub_bars, main_bars]).count()
    for (main, sub), val in zip(grp.index, grp.values):
        d_dict[main].append({sub: val[0]})

    fig = go.Figure()
    subbars_count = df.groupby(by=sub_bars).count()
    subbars = subbars_count.sort_values(by=df.columns[-1]).index

    for sub in list(subbars)[::-1]:
        values = [list(i.items())[0] for i in d_dict[sub]]
        values = sorted(values, key=lambda x: x[1], reverse=True)
        x = [i[0] for i in values]
        y = [i[1] for i in values]
        trace = go.Bar(
            x=x,
            y=y,
            name=sub,
            text=sub
        )
        fig.add_trace(trace)
    if transparent:
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


def count_by(df, main_category, sub_category, n_main, n_sub, add_percentage=False,):
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
                    total_counts.update(
                        {main: [sub + f"<br>{percent:.1f} %</br>"]})
                else:
                    total_counts.update({main: [sub]})
            else:
                if add_percentage:
                    total_counts[main].append(
                        sub + f"<br>{percent:.1f} %</br>")
                else:
                    total_counts[main].append(sub)
    return pd.DataFrame(total_counts)