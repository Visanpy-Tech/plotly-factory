import plotly as pl
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from collections import OrderedDict, defaultdict
from datetime import datetime
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
from scipy import stats


def axis_layout(title=None, title_size=16, title_color="#666666", grid_color="#F0F0F0", show_grid=False,
                tick_angle=0, tick_family="Times New Roman", tick_size=14, tick_color="#4d4d4d", ticks="",
                show_exponent=None, exponent_format=None, range_=None, dtick=None, showticklabels=True, 
                type_=None, fixedrange=True):
    axis_dict = dict(
        title=dict(
            text=title,
            font=dict(
                size=title_size,
                color=title_color
            )
        ),
        showgrid=show_grid,
        gridcolor=grid_color,
        dtick=dtick,
        tickfont=dict(
            family=tick_family,
            size=tick_size,
            color=tick_color
        ),
        tickangle=tick_angle,
        range=range_,
        ticks=ticks,
        showticklabels=showticklabels,
        type=type_,
        fixedrange=fixedrange,
        showexponent = show_exponent,
        exponentformat = exponent_format
    )
    return axis_dict


def title_layout(title, title_size=21, x_position=0.5, y_position=0.9, color="#A8A8A8", family="Times New Roman"):
    title_ = dict(
        text=title,
        x=x_position,
        y=y_position,
        font=dict(
            size=title_size,
            color=color,
            family=family
        )
    )
    return title_


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



def plot_box(df, y, x_main, main_categories, x_sub=None,  sub_categories=None, orientation="v", 
             notched=True, legend="default", mean=True, points="outliers", transparent=True):
    
    fig = go.Figure()
    colors = ["#191970", "#64b5f6", "#ef6c00", "#ffd54f"]

    legend_font = {}
    if legend == "default":
        legend_font.update(
            dict(bgcolor="rgba(0,0,0,0)",
                 font=dict(size=18, family="Times New Roman")
                )
        )
        
    if x_sub is None:
        x_ = df.loc[df[x_main].isin(main_categories)][x_main]
        y_ = df.loc[df[x_main].isin(main_categories)][y]
        trace = go.Box(
            x=x_,
            y=y_,
            marker=dict(
                size=5,
                opacity=0.6,
                color=colors[1]
            ),
        boxmean=mean,
        boxpoints=points,
        orientation=orientation,
        opacity=0.9,
        notched=notched,
        
            )
        fig.add_trace(trace)
    else:
        for k, sub in enumerate(sub_categories):
            x_ = df.loc[df[x_main].isin(main_categories) & (df[x_sub] == sub)][x_main]
            y_ = df.loc[df[x_main].isin(main_categories) & (df[x_sub] == sub)][y]
            trace = go.Box(
                x=x_,
                y=y_,
                name=sub,
                marker=dict(
                    size=5,
                    opacity=0.6,
                    color=colors[k]
                ),
                boxmean=mean,
                boxpoints=points,
                orientation=orientation,
                opacity=0.9,
                notched=notched,
            )
            fig.add_trace(trace)


        
    fig.update_layout(
        {"boxmode":"group",
         "legend":legend_font
        }
    )
    if transparent:
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    return fig


def plot_horizontal_count_bars(df, column, first_n="all", colorscale="algae", show_percentage=False, show_text=False, 
                    text_font="default", text_position="inside", text_percentage_space="  ", round_percentage_decimals=1,
                              transparent=True):
    # font for text and percentage
    if text_font=="default":
        text_font= dict(
            family="Time New Roman", 
            size=16, 
            color="#000080"
        )
    
    # count and sort entries in a given column
    total_counts = df[column].value_counts().sort_values(ascending=False)
    if first_n == "all":
        # we use [::-1] in order to have descending values frm top to bottom 
        counts = total_counts[::-1]
    else:
        counts = total_counts[:first_n][::-1]
        
    y = counts.index # entries
    x = counts.values # number of entries in a given column
    
    # make bar chart
    trace = go.Bar(
        x=x,
        y=y,
        marker=dict(
            color=counts,
            colorscale=colorscale,
            opacity=0.7
        ),
        orientation="h",
        hoverinfo="x + y"
    )
    
    # calculate percentages
    if show_text:
        if show_percentage:
            counts_normalized = x / sum(total_counts)
            percentage = np.round(100 * counts_normalized, round_percentage_decimals)
            text = ["<b>" + entry + text_percentage_space +
                    str(percent) + " %" + "</b>" for entry, percent in zip(y, percentage)]     
        else:
            text = ["<b>" + y_ + "</b>" for y_ in y]
            
    elif show_percentage:
        counts_normalized = x / sum(total_counts)
        percentage = np.round(100 * counts_normalized, round_percentage_decimals)
        text = ["<b>" + entry + text_percentage_space +
                str(percent) + " %" + "</b>" for entry, percent in zip(y, percentage)]   
    else:
        text = ["" for y_ in y]
    
    # update trace with text
    trace.update(dict(
        text=text,
        textposition=text_position,
        textfont=text_font)
    )
    
    fig = go.Figure(data=[trace])
    if transparent:
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    
    return fig


def plot_subplots(df, main_category, sub_category, layout, n_rows, n_cols, n_bars,
                  colorscale="mint", vertical_spacing=0.2, share_x=False, share_y=False):

    main_counts = df[main_category].value_counts()
    sub_counts = df[sub_category].value_counts()
    counts_dict = OrderedDict()

    for main in main_counts.index:
        counts = df.loc[df[main_category] == main][sub_category].value_counts()
        subs = counts.index
        subs_freq = counts.values
        for sub, freq in zip(subs, subs_freq):
            if main not in counts_dict.keys():
                counts_dict.update({main: [[sub, freq]]})
            else:
                counts_dict[main].append([sub, freq])

    fig = pl.subplots.make_subplots(
        rows=n_rows,
        cols=n_cols,
        subplot_titles=list(main_counts.keys())[:n_cols * n_rows],
        shared_yaxes=share_y,
        shared_xaxes=share_x,
        vertical_spacing=vertical_spacing)

    for i, main in enumerate(list(counts_dict.keys())[:n_rows * n_cols]):
        x = np.array(counts_dict[main])[:n_bars, 0]
        y = np.array(counts_dict[main])[:n_bars, 1]
        trace = go.Bar(
            x=x,
            y=y,
            marker=dict(
                color=sub_counts,
                colorscale=colorscale),
            hoverinfo="x + y",
        )
        fig.add_trace(trace, row=i // 2 + 1, col=i % 2 + 1)
        if i > n_cols * n_rows - 2:
            break
    fig.update_layout(layout)
    return fig


def plot_histograms(df, main_column, main_categories, sub_column=None, sub_categories=None, show_box=False,
                    x_legend=0.84, y_legend=0.7, legend="default", percentage=False, points = False,notched=True, mean=True, percentage_relative_to="sub_category", sort_values="initial_sort", transparent=True):
    legend_font = {"x": x_legend, "y":y_legend}
    
    if legend == "default":
        legend_font.update(
           {
                "bgcolor":"rgba(0,0,0,0)",
                "font":dict(size=18, family="Times New Roman")
           }
        )

    colors = ["#191970", "#64b5f6", "#ef6c00", "#ffd54f"]
    
    
    # a trick to generate bar charts only for main category
    if sub_column is None:
        df["trick_column"] = len(df)*["trick"]
        sub_categories = ["trick"]
        sub_column="trick_column"
        showlegend=False
        domain_1 =[0.90, 1]
        domain_2 =[0, 0.90]
    else:
        showlegend=True
        domain_1 =[0.80, 1]
        domain_2 =[0, 0.80]
    
    # iterate over all subcategories
    for k, sub in enumerate(sub_categories):
        # count entries of each subcategory that belongs to provided main category
        counts = df.loc[(df[main_column].isin(main_categories)) & (
            df[sub_column] == sub)][main_column].value_counts().sort_index()

        for main in main_categories:
            if main not in counts.index:
                print(f"Column {main} not found")
                counts.at[main] = 0

        x_ = counts.index

        ## percentage options ##
        if percentage == True:
            if percentage_relative_to == "sub_category":
                y_ = 100 * counts.values / len(df.loc[df[sub_column] == sub])
            elif percentage_relative_to == "total":
                y_ = 100 * counts.values / len(df)
            elif percentage_relative_to == "main_category":
                denominator = df.loc[df[main_column].isin(
                    main_categories)][main_column].value_counts().sort_index()
                for main in main_categories:
                    if main not in denominator.index:
                        denominator.at[main] = 0
                y_ = 100 * counts.values / denominator.values

            text = [str(count) + ", " + str(round(y, 2)) + " %" for count, y in zip(counts, y_)]
        else:
            y_ = counts.values
            text = [str(x) + str(y) for x, y in zip(x_, y_)]

        # sorting options
        if sort_values == "counts":
            x_y_ = list(zip(x_, y_))
            x_y_sorted = sorted(x_y_, key=lambda item: item[1], reverse=True)
            x_ = [item[0] for item in x_y_sorted]
            y_ = [item[1] for item in x_y_sorted]
        elif sort_values == "initial_sort":
            values_dict = OrderedDict(zip(x_, y_))
            y_ = np.array([values_dict.get(key) for key in main_categories])
            x_ = main_categories

        # for every subcategory make a bar chart
        bar = go.Bar(
            y=np.round(y_, 2),
            x=x_,
            marker=dict(color=colors[k], opacity=0.7),
            name=sub,
            text=text,
            hoverinfo="x +  text",
            showlegend=showlegend
                    )

        if show_box:
            # if show_box is True, make a subplots 2x1
            if k == 0:
                fig = make_subplots(rows=2, cols=1)
            box = go.Box(x=df.loc[df[sub_column] == sub][main_column],
                         marker=dict(color=colors[k]),
                         boxpoints=points,
                         notched=notched,
                         boxmean=mean,
                         showlegend=False,

                         )
            # add box and bar plots to the subplots
            fig.add_trace(box, row=1, col=1)
            fig.add_trace(bar, row=2, col=1)

            fig.layout["xaxis"].update(
                axis_layout(showticklabels=False,
                            range_=[main_categories[0], 
                                    main_categories[-1]],
                           )
            )

            # set box-bar ratio to 0.8 : 0.2
            fig.layout["yaxis"].update(
                axis_layout(showticklabels=False),
                                       domain=domain_1)

            fig.layout["yaxis2"].update(domain=domain_2)

        else:
            # if show_box is False, make a single Figure and add bar chart
            if k == 0:
                fig = go.Figure()
            fig.add_trace(bar)
    
    fig.update_layout(legend=legend_font)
    
    if transparent:
        fig.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)")
    
    if "trick_column" in df.columns:
        df.drop(columns=["trick_column"], inplace=True)
        
    return fig




def plot_heatmap(df_corr, show_annotations=True, colorscale="brwnyl", plot_triangle = False,
                 showscale=True, text_color = "#000000", text_size = 14, xgap=1, ygap=1):
    
    trace=go.Heatmap(
        colorscale=colorscale,
        hoverinfo="text",
        xgap=xgap,
        ygap=ygap,
        showscale=showscale
    )
    
    if plot_triangle:
        corr_triangle = np.array([[None for k in range(df_corr.shape[1]-1)] for j in range(df_corr.shape[0]-1)])
        for k, vals in enumerate(df_corr[1:].values):
            corr_triangle[k][:k+1] = np.round(vals[:k+1], 2)

        trace.update(z = corr_triangle[::-1], x = df_corr.index[:-1], 
                     y = df_corr.index[1:][::-1], text = corr_triangle[::-1])
        fig = go.Figure(data=[trace])
        if show_annotations:
            annotations = []
            for k, y in enumerate(df_corr.index):
                for x in df_corr.index[:k]:
                    anot = go.layout.Annotation(
                        x=x,
                        y=y,
                        xref="x",
                        yref="y",
                        text= "<b>" + str(round(df_corr[x][y], 2)) + "</b>",
                        showarrow=False,
                        font = {
                            "color": text_color,
                            "size": text_size,
                            "family": "Times New Roman"
                        }
                    )
                    annotations.append(anot)


    
        
    else:
        trace.update(z = df_corr.values[::-1], x = df_corr.index, 
                     y = df_corr.index[::-1], text= np.round(df_corr.values[::-1], 2))
        fig = go.Figure(data=[trace])
        
        if show_annotations:
            annotations = []
            for k, y in enumerate(df_corr.index):
                for x in df_corr.index:
                    anot = go.layout.Annotation(
                        x=x,
                        y=y,
                        xref="x",
                        yref="y",
                        text= "<b>" + str(round(df_corr[x][y], 2)) + "</b>",
                        showarrow=False,
                        font = {
                            "color": text_color,
                            "size": text_size,
                            "family": "Times New Roman"
                        }
                    )
                    annotations.append(anot)
    
    
    fig.update_layout(
        showlegend=False,
        annotations=annotations
    )    


    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)"
        )
    return fig




def plot_table(df, title=False, cell_height=45, add_table_height=0, width=700, header_font="default", cell_font="default",
               header_bg_color="#191970", header_align="center", cell_align="center",
               cell_bg_colors=["rgba(158, 223, 249, 0.20)", "white"], split_words_on= True, line_color="lightgrey", line_width=2):
    
    if header_font == "default":
        header_font = dict(family="Times New Roman", color="white", size=15)
        
    if cell_font == "default":
        cell_font = dict(family="Times New Roman", color="#002266", size=14)
    
    if split_words_on:
        header_values = [val.replace("-", "<br>") for val in df.columns]
        
    table = go.Table(
        header=dict(
            values=header_values,
            fill_color=header_bg_color,
            line_color=line_color,
            line_width=line_width,
            height=cell_height,
            font=header_font,
            align=header_align
        ),
        cells=dict(
            values=[df[column] for column in df.columns],
            font=cell_font,
            height=cell_height,
            align=cell_align,
            fill_color=[cell_bg_colors * len(df)],
            line_color=line_color,
            line_width=line_width,
        ),
    )
    layout = go.Layout(
        height=(len(df) + 1) * cell_height + len(df) + add_table_height,
        width=width,
        margin=dict(r=1, b=0, l=1, t=0),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
    )
    if title:
        layout.update(height=(len(df) + 1) * cell_height + len(df) + 30 + add_table_height,
                      title=title, margin=dict(r=1, b=0, l=1, t=35), width=width)
    fig = go.Figure(data=[table], layout=layout)

    return fig


def plot_distplot(df, column, hist=True, kde=True, gauss=True, show_box=True, points = False, 
                  notched=True, show_mean=True, kde_resolution=128, colors="default", range_="auto",
                  n_bins=None, x_legend=0.85, y_legend=0.8, show_legend=True, legend="default", bargap=0.03):
    
    # vrednosti koje fitujemo
    variable_values = df[column].values
    
    # generiši vrednosti za x osu
    x_values = np.linspace(min(variable_values), max(variable_values), kde_resolution)
    
    # srednja vrednost i medijana za vrednosti koje fitujemo
    mean, std = stats.norm.fit(variable_values)
    # gustina verovatniće
    gauss_prob_dens = stats.norm.pdf(sorted(df[column].values), loc= mean, scale=std)
    
    # Kernel Density Estimate gustina verovatnoće
    kde = stats.gaussian_kde(variable_values)
    kde_values = kde(x_values)
    
    if colors=="default":
        colors = ["#191970", "#64b5f6", "#ef6c00", "#03adfc"]
    
    

    traces = []
    if show_box:
        box = go.Box(
            x=variable_values,
            marker=dict(color=colors[3]),
            boxpoints=points,
            notched=notched,
            boxmean=show_mean,
            showlegend=False,
        )
    
    if hist:
        hist_trace = go.Histogram(x=variable_values, 
                                  histnorm='probability density',
                                  marker=dict(color=colors[0], opacity=0.7),
                                  nbinsx=n_bins,
                                  name="Histogram",
                                  showlegend = show_legend
                                 )
        traces.append(hist_trace)
        
    # KDE probability density
    if kde:
        kde_trace = go.Scatter(
            x=x_values,
            y=kde_values,
            name="KDE PDF",
            showlegend = show_legend
        )
        traces.append(kde_trace)
        
    
    # Gaussian probability density
    if gauss:
        gauss_trace = go.Scatter(
            x=sorted(variable_values), 
            y=gauss_prob_dens,
            name="Gauss PDF",
            line=dict(color="#FFA500"),
            showlegend = show_legend
        )
        traces.append(gauss_trace)
    
    if range_=="auto":
        range_= [min(variable_values), max(variable_values)]
    
    if show_box:
        fig = make_subplots(rows=2, cols=1)
        fig.add_trace(box, row=1, col=1)
        for trace in traces:
            fig.add_trace(trace, row=2, col=1)
        
        fig.layout["xaxis2"].update(
            axis_layout(
                show_grid=False, 
                range_=range_,
                ticks=""
            )
        )
        fig.layout["yaxis2"].update(
            axis_layout(ticks=""), 
            domain=[0, 0.75],
            showexponent = 'last',
            exponentformat = 'power'
        )
        
        fig.layout["xaxis"].update(
            axis_layout(
                title="", 
                ticks="", 
                showticklabels=False,
                range_=range_, 
                show_grid=False,
            )
        )
        fig.layout["yaxis"].update(axis_layout(title="", ticks="", showticklabels=False, show_grid=False),
                                   domain=[0.78, 1])
    else:
        fig = go.Figure()
        for trace in traces:
            fig.add_trace(trace)

        fig.layout["xaxis"].update(
            axis_layout(
                title="", 
                range_=range_, 
                show_grid=False
            ),
        )

        fig.layout["yaxis"].update(
            axis_layout(
                title="", 
                show_grid=True
            ),
            showexponent = 'last',
            exponentformat = 'power'
        )
    
    
    layout = go.Layout(bargap=0.02)
    legend_font = {}
    legend_font["x"] = x_legend
    legend_font["y"] = y_legend
    if legend == "default":
        legend_font.update(dict(bgcolor="rgba(0,0,0,0)",
                                font=dict(size=16, family="Times New Roman")))
    fig.update_layout(
        legend=legend_font,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        bargap=bargap
    )
    
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


def plot_predictions(y_true, y_predict, num_sample, title, figsize= (10,5)):
    
    sample_ind = np.random.randint(0, len(y_true), size = num_sample)
    sample_true = y_true[sample_ind]
    sample_predict = y_predict[sample_ind]
    
    plt.figure(figsize=figsize)
    plt.scatter(np.arange(num_sample), sample_true, 
                marker = 'o', s=30, edgecolors='b', facecolors='none', label = 'True values')
    plt.scatter(np.arange(num_sample), sample_predict, 
                marker = 'x', c='red', s=20, label = 'Predicted values')
    val = [i for i in range(num_sample) for j in range(2)]
    s = []
    for i in range(num_sample):
        s.append(sample_true[i])
        s.append(sample_predict[i])
    for i in range(num_sample):
        plt.plot(val[2*i:2*i+2], s[2*i:2*i+2], ':', c = 'green', alpha=0.5)
    plt.legend(loc = 'best', fontsize=8)
    plt.xticks(np.arange(0,num_sample))
    plt.grid(alpha = 0.4)
    plt.ylabel("Price", fontsize = 10)
    plt.title(title, fontsize=12)
    plt.show()
    
    r2_ = r2_score(y_true, y_predict)
    mse = mean_squared_error(y_true, y_predict)
    mae = mean_absolute_error(y_true, y_predict)
    print("Mean Root Squared Error: {0:.3f}.".format(mse**0.5))
    print("Mean Absolute Error: {0:.1f}.".format(mae))
    print("R Squared Metric: {0:.3f}.".format(r2_))


def removeBarButtons():
    return dict(
        displaylogo=False,
        modeBarButtonsToRemove=["pan2d", "lasso2d", "select2d", "toggleSpikelines", "autoScale2d",
                                "hoverClosestCartesian", "hoverCompareCartesian"]
    )


def to_year(year):
    dt_year = datetime.strptime(str(int(year)), '%Y')
    return dt_year


def update_dict(dictonary, update):
    dictonary.update(update)
    return dictonary
