
import os
import numpy as np
import pandas as pd
import plotly.graph_objs as go
from collections import OrderedDict
from plotly_functions import *
from plotly.io import write_html


df_germany = pd.read_csv("df_germany_englang.csv").sample(n=59000)

df_serbia = pd.read_csv("df_serbia_englang.csv").sample(n=59000)

df = pd.concat([df_serbia, df_germany], sort=False)

manufacturers_germany = plot_horizontal_count_bars(
    df_germany, "manufacturer",
    first_n=12, show_percentage=True, show_text=True, text_position="auto",
    colorscale="mint",
)

manufacturers_germany.update_layout(
    title=title_layout(
        "<b>German</b> market", title_size=20, color="#52527a"),
    yaxis=axis_layout(
        "Car brand", showticklabels=False),
    xaxis=axis_layout(
        "Number of Cars", tick_size=16, dtick=2000, range_=[0, 12000], show_exponent="last", show_grid=True),
    width=850, 
    height=500
)


manufacturers_serbia = plot_horizontal_count_bars(
    df_serbia, "manufacturer",
    first_n=12, show_percentage=True, show_text=True, text_position="auto",
    colorscale="mint",
)

manufacturers_serbia.update_layout(
    title=title_layout(
        "<b>Serbian</b> market", title_size=20, color="#52527a"),
    yaxis=axis_layout(
        "Car brand", showticklabels=False),
    xaxis=axis_layout(
        "Number of Cars", tick_size=16, dtick=2000, range_=[0, 12000], show_exponent="last", show_grid=True),
    width=850, 
    height=500
)

df_mod_per_manuf_serbia = count_by(
    df_serbia, "manufacturer", "model", 6, 5, add_percentage=True)
df_mod_per_manuf_germany = count_by(
    df_germany, "manufacturer", "model", 6, 5, add_percentage=True)


mod_per_manuf_serbia = plot_table(df_mod_per_manuf_serbia,
                                  add_table_height=33, cell_align="left", header_align="left", width=540, cell_height=48,
                                  title=title_layout("Most popular models on <b>Serbian</b>...",
                                                     title_size=20,
                                                     y_position=0.98,
                                                     color="grey",)
                                  )

mod_per_manuf_germany = plot_table(df_mod_per_manuf_germany,
                                   add_table_height=33, cell_align="left", header_align="left", width=540, cell_height=48,
                                   title=title_layout("...and <b>German</b> used cars market",
                                                      title_size=20,
                                                      y_position=0.98,
                                                      color="grey",)
                                   )
top_body_styles = plot_horizontal_count_bars(
    df_serbia,
    "body_style",
    show_percentage=True,
    text_position="auto",
    colorscale="mint",
    first_n=6)

top_body_styles.update_layout(
    title=title_layout(
        "Body Type", 
        title_size=20,
        color="#52527a", 
        y_position=0.85
    ),
    yaxis=axis_layout(showticklabels=False),
    xaxis=axis_layout(showticklabels=False),
    width=500,
    height=350
)


top_transmissions = plot_horizontal_count_bars(
    df_serbia,
    "transmission",
    show_percentage=True,
    text_position="auto",
    colorscale="mint",
    first_n=2)

top_transmissions.update_layout(
    title=title_layout(
        "Transmission", 
        title_size=20,
        color="#52527a", 
        y_position=0.85),
    yaxis=axis_layout(showticklabels=False),
    xaxis=axis_layout(showticklabels=False),
    width=500,
    height=350
)


top_fuel_types = plot_horizontal_count_bars(
    df_serbia,
    "fuel_type",
    show_percentage=True,
    text_position="auto",
    colorscale="mint",
    first_n=3)

top_fuel_types.update_layout(
    title=title_layout(
        "Fuel", 
        title_size=20,
        color="#52527a", 
        y_position=0.85
    ),
    yaxis=axis_layout(showticklabels=False),
    xaxis=axis_layout(showticklabels=False),
    width=500,
    height=350
)

top_styles_count = df_serbia["body_style"].value_counts().index[:6]
top_fuel_types_count = df_serbia["fuel_type"].value_counts().index[:3]

fuel_distribution = plot_histograms(
    df_serbia, 
    "body_style", 
    top_styles_count,
    "fuel_type", 
    top_fuel_types_count, 
    False,
    y_legend=1, 
    percentage=True, 
    percentage_relative_to="main_category"
)

fuel_distribution.update_layout(dict(
    height=400,
    title=title_layout("Fuel by body type", title_size=20, color="#52527a")),
    yaxis=axis_layout(
        title="Fuel share (%)",
        tick_size=16),
    xaxis=axis_layout(tick_size=18),
    width=850, 
    height=500
)

top_transmissions_count = df_serbia["transmission"].value_counts().index[:2]

body_transmission_distribution = plot_histograms(
    df_serbia, 
    "body_style",
    top_styles_count, 
    "transmission", 
    top_transmissions_count,
    False, 
    y_legend=1.2, 
    percentage=True, 
    percentage_relative_to="main_category"
)

body_transmission_distribution.update_layout(dict(
    title=title_layout(
        "Transmission by body type", 
        title_size=20, 
        color="#52527a"
    ),
    yaxis=axis_layout(
        title="Body Type (%)",
        tick_size=16
    ),
    xaxis=axis_layout(tick_size=18),
    width=850,
    height=500
)
)

body_per_year = plot_histograms(
    df_serbia, 
    "year", 
    np.arange(2009, 2020),
    "body_style", 
    ["SUV", "Caravan"], 
    percentage=True, 
    sort_values="initial",
    percentage_relative_to="main_category", 
    y_legend=1, 
    x_legend=0.02
)

body_per_year.update_layout(
    dict(
        title=title_layout(
            title="Increasing trend in SUV offer",
            title_size=20, 
            color="#52527a"
        ),
    xaxis=axis_layout(tick_size=16, dtick=1),
    yaxis=axis_layout(title="share by year (%)", tick_size=16, show_grid=True),
    ),
    width=850, 
    height=500
)

transmission_per_year = plot_histograms(
    df_serbia, 
    "year", 
    np.arange(2009, 2019),
    "transmission", 
    ["Automatic", "Manual"], 
    percentage=True,
    percentage_relative_to="main_category", 
    sort_values="initial", 
    y_legend=1, 
    x_legend=0.80
)

transmission_per_year.update_layout(
    dict(
        title=title_layout(title="Increasing trend for transmission type", title_size=20, color="#52527a"),
        xaxis=axis_layout("Year", tick_size=16, dtick=1),
        yaxis=axis_layout("Share per year (%)", tick_size=16),
    ),
    width=850, 
    height=500
)


fuel_per_year = plot_histograms(
    df_serbia, 
    "year", 
    np.arange(2009, 2019),
    "fuel_type", 
    ["Diesel", "Gasoline"], 
    percentage=True,
    percentage_relative_to="main_category", 
    sort_values="initial", 
    y_legend=1, 
    x_legend=0.80
)

fuel_per_year.update_layout(
    dict(
        title=title_layout("Fuel Type by year", title_size=20, color="#52527a"),
        xaxis=axis_layout("", tick_size=16, dtick=1),
        yaxis=axis_layout("Share per year (%)", tick_size=16),
        width=850, 
        height=500
    )
)


top_body_styles_ger = plot_horizontal_count_bars(
    df_germany,
    "body_style",
    show_percentage=True,
    text_position="auto",
    colorscale="mint",
    first_n=6)

top_body_styles_ger.update_layout(
    title=title_layout("Body type", title_size=20,
                       color="#52527a", y_position=0.85),
    yaxis=axis_layout(showticklabels=False),
    xaxis=axis_layout(showticklabels=False),
    width=500,
    height=350
)


top_transmissions_ger = plot_horizontal_count_bars(
    df_germany,
    "transmission",
    show_percentage=True,
    text_position="auto",
    colorscale="mint",
    first_n=2)

top_transmissions_ger.update_layout(
    title=title_layout("Transmission type", title_size=20,
                       color="#52527a", y_position=0.85),
    yaxis=axis_layout(showticklabels=False),
    xaxis=axis_layout(showticklabels=False),
    width=500,
    height=350
)


top_fuel_types_ger = plot_horizontal_count_bars(
    df_germany,
    "fuel_type",
    show_percentage=True,
    text_position="auto",
    colorscale="mint",
    first_n=3)

top_fuel_types_ger.update_layout(
    title=title_layout("Fuel", title_size=20,
                       color="#52527a", y_position=0.85),
    yaxis=axis_layout(showticklabels=False),
    xaxis=axis_layout(showticklabels=False),
    width=500,
    height=350
)


top_styles_count_ger = df_germany["body_style"].value_counts().index[:6]
top_transmissions_count_ger = df_germany["transmission"].value_counts().index[:2]
top_fuel_types_count_ger = df_germany["fuel_type"].value_counts().index[:2]

fuel_distribution_ger = plot_histograms(
    df_germany, 
    "body_style", 
    top_styles_count_ger, 
    "fuel_type",  
    top_fuel_types_count_ger, 
    False,
    y_legend=1, 
    x_legend=0.4, 
    percentage=True, 
    percentage_relative_to="main_category")

fuel_distribution_ger.update_layout(dict(
    height=400,
    title=title_layout("Fuel by body type", title_size=20, color="#52527a")),
    yaxis=axis_layout(title="Body type share (%)", tick_size=16, ticks=""),
    xaxis=axis_layout(tick_size=16),
    width=850, 
    height=500
)


body_per_year_ger = plot_histograms(
    df_germany, 
    "year", 
    np.arange(2009, 2019),
    "body_style", 
    ["SUV", "Caravan"], 
    percentage=True, 
    sort_values="initial",
    percentage_relative_to="main_category", 
    y_legend=1, 
    x_legend=0.02
)

body_per_year_ger.update_layout(
    dict(
        title=title_layout("Increasing trend in SUV offer", title_size=20, color="#52527a"),
        xaxis=axis_layout(tick_size=16,dtick=1),
        yaxis=axis_layout(title="share by year (%)", tick_size=16),
    ),
    width=850, 
    height=500
)

transmission_per_year_ger = plot_histograms(
    df_germany, 
    "year", 
    np.arange(2009, 2019),
    "transmission", 
    ["Automatic", "Manual", ], 
    percentage=True,
    percentage_relative_to="main_category", 
    sort_values="initial", 
    y_legend=1, 
    x_legend=0.80
)

transmission_per_year_ger.update_layout(
    dict(
        title=title_layout("Increasing trend for transmission type", title_size=20, color="#52527a"),
        xaxis=axis_layout("Year", tick_size=16, dtick=1),
        yaxis=axis_layout("Share per Year (%)", tick_size=16, show_grid=True),
    ),
    width=850, 
    height=500
)


fuel_per_year_ger = plot_histograms(
    df_germany, 
    "year",
    np.arange(2009, 2019),
    "fuel_type", 
    ["Diesel", "Gasoline"], 
    percentage=True,
    percentage_relative_to="main_category", 
    sort_values="initial", 
    y_legend=1, 
    x_legend=0.75
)

fuel_per_year_ger.update_layout(
    dict(
        title=title_layout("Fuel type by year", title_size=20, color="#52527a"),
        xaxis=axis_layout("Year", tick_size=16, dtick=1),
        yaxis=axis_layout("Share per year (%)", tick_size=16),
    ),
    width=850, 
    height=500
)

year_distribution = plot_histograms(
    df, 
    "year", 
    np.arange(2000, 2020), 
    "country", 
    ["Serbia", "Germany"],
    show_box=True, 
    x_legend=0.05, 
    y_legend=0.75, 
    percentage=True, 
    mean=False
)


year_distribution.update_layout(
    dict(
        yaxis2=axis_layout("Market share (%)", tick_size=16),
        xaxis2=axis_layout(title="Year", dtick=1, tick_size=16, tick_angle=-20),
    ),
    width=900, 
    height=600
)


mileage_per_year = plot_box(
    df, 
    "mileage", 
    "year", 
    np.arange(2005, 2016),
    "country",  
    ["Serbia", "Germany"])

mileage_per_year.update_layout(
    dict(
        xaxis=axis_layout("Year", tick_size=16, dtick=1, tick_angle=-20),
        yaxis=axis_layout( "Mileage", tick_size=16, range_=[30000, 300000]),
    ),
    width=1100, 
    height=500,
)

price_per_year = plot_box(
    df, 
    "price", 
    "year", 
    np.arange(2005, 2016), 
    "country", 
    ["Serbia", "Germany"]
)

price_per_year.update_layout(
    dict(
        xaxis=axis_layout("Year", tick_size=16, dtick=1, tick_angle=-20),
        yaxis=axis_layout("Price (€)", tick_size=16, range_=[800, 22000]),
    ),
    width=1100, 
    height=500,
)



price_distplot_serb = plot_distplot(df_serbia, "price", kde_resolution=1024, gauss=False, n_bins=256, show_legend=False, bargap=0.2)
price_distplot_serb.update_layout(
    xaxis1 = axis_layout(range_=[0, 50000], showticklabels=False),
    xaxis2 = axis_layout("Price [€]", range_=[0, 50000], show_exponent="last", dtick=2000),
    yaxis2 = axis_layout("PDF", showticklabels=False),
    width=1100, 
    height=500,
)

price_distplot_ger = plot_distplot(df_germany, "price", kde_resolution=1024, gauss=False, n_bins=256, bargap=0.2)
price_distplot_ger.update_layout(
    title = title_layout("Price distribution on German and Serbian used cars market", color="#000066", title_size=20),
    xaxis1 = axis_layout(range_=[0, 50000], showticklabels=False),
    xaxis2 = axis_layout(range_=[0, 50000], showticklabels=False),
    yaxis2 = axis_layout("PDF", showticklabels=False),
    width=1100, 
    height=500,
)



per_year_ger = []
for year in np.arange(2005, 2016):
    per_year_ger.append(df_germany.loc[df_germany.year==year].sample(n=700))

per_year_serb = []
for year in np.arange(2005, 2016):
    per_year_serb.append(df_serbia.loc[df_serbia.year==year].sample(n=700))

df_germany0814 = pd.concat(per_year_ger)
df_serbia0814 = pd.concat(per_year_serb)


corr_germany_dizel = df_germany0814[["year", "price", "mileage"]].loc[df_germany0814.fuel_type=="Diesel"].corr("spearman")
corr_serbia_dizel = df_serbia0814[["year", "price", "mileage"]].loc[df_serbia0814.fuel_type=="Diesel"].corr("spearman")

corr_germany_benzin = df_germany0814[["year", "price", "mileage"]].loc[df_germany0814.fuel_type=="Gasoline"].corr("spearman")
corr_serbia_benzin = df_serbia0814[["year", "price", "mileage"]].loc[df_serbia0814.fuel_type=="Gasoline"].corr("spearman")



germany_dizel = plot_heatmap(corr_germany_dizel)
serbia_dizel = plot_heatmap(corr_serbia_dizel)
germany_benzin = plot_heatmap(corr_germany_benzin)
serbia_benzin = plot_heatmap(corr_serbia_benzin)


germany_dizel.update_layout(
    title=title_layout("Diesel", title_size =20, color='#A8A8A8'), 
    xaxis=axis_layout(title_size=20, tick_size=17, ticks=None),
    yaxis=axis_layout("Germany", title_size=18, tick_size=17, tick_angle=-90, ticks="outside"),
    width=550, 
    height=500
)

serbia_dizel.update_layout(
    xaxis=axis_layout(tick_size=17, ticks=None),
    yaxis=axis_layout("Serbia", title_size=18, tick_size=17, tick_angle=-90, ticks="outside"),
    width=550, 
    height=500
)


germany_benzin.update_layout(
    title=title_layout("Gasoline", title_size =20, color='#A8A8A8'), 
    xaxis=axis_layout(tick_size=17, ticks=None),
    yaxis=axis_layout(title_size=18, tick_size=17, tick_angle=-90, ticks="outside"),
    width=550, 
    height=500
)

serbia_benzin.update_layout(
    xaxis=axis_layout(tick_size=17),
    yaxis=axis_layout(title_size=18, tick_size=17, tick_angle=-90, ticks="outside"),
    width=550, 
    height=500
)


manufacturers_germany.write_image("D://DataScienceEnv//Cars project//images//manufacturers_germany.svg", width=800, height=500)
manufacturers_serbia.write_image("D://DataScienceEnv//Cars project//images//manufacturers_serbia.svg", width=800, height=500)
mod_per_manuf_germany.write_image("D://DataScienceEnv//Cars project//images//mod_per_manuf_germany.svg")
mod_per_manuf_serbia.write_image("D://DataScienceEnv//Cars project//images//mod_per_manuf_serbia.svg")


top_body_styles.write_image("D://DataScienceEnv//Cars project//images//top_body_styles.svg")
top_transmissions.write_image("D://DataScienceEnv//Cars project//images//top_transmissions.svg")
top_fuel_types.write_image("D://DataScienceEnv//Cars project//images//top_fuel_types.svg")


fuel_distribution.write_image("D://DataScienceEnv//Cars project//images//fuel_distribution.svg", width=800, height=500)
body_transmission_distribution.write_image("D://DataScienceEnv//Cars project//images//body_transmission_distribution.svg", width=800, height=500)
body_per_year.write_image("D://DataScienceEnv//Cars project//images//body_per_year.svg", width=800, height=500)
transmission_per_year.write_image("D://DataScienceEnv//Cars project//images//transmission_per_year.svg", width=800, height=500)
fuel_per_year.write_image("D://DataScienceEnv//Cars project//images//fuel_per_year.svg", width=800, height=500)

top_body_styles_ger.write_image("D://DataScienceEnv//Cars project//images//top_body_styles_ger.svg")
top_transmissions_ger.write_image("D://DataScienceEnv//Cars project//images//top_transmissions_ger.svg")
top_fuel_types_ger.write_image("D://DataScienceEnv//Cars project//images//top_fuel_types_ger.svg")

fuel_distribution_ger.write_image("D://DataScienceEnv//Cars project//images//fuel_distribution_ger.svg", width=800, height=500)
body_per_year_ger .write_image("D://DataScienceEnv//Cars project//images//body_per_year_ger.svg", width=800, height=500)
transmission_per_year_ger.write_image("D://DataScienceEnv//Cars project//images//transmission_per_year_ger.svg", width=800, height=500)
fuel_per_year_ger.write_image("D://DataScienceEnv//Cars project//images//fuel_per_year_ger.svg", width=800, height=500)


year_distribution.write_image("D://DataScienceEnv//Cars project//images//year_distribution.svg", width=1100, height=600)
mileage_per_year.write_image("D://DataScienceEnv//Cars project//images//mileage_per_year.png", width=1100, height=500)
price_per_year.write_image("D://DataScienceEnv//Cars project//images//price_per_year.png", width=1100, height=500)

price_distplot_serb.write_image("D://DataScienceEnv//Cars project//images//price_distplot_serb.svg", width=1100, height=500)
price_distplot_ger.write_image("D://DataScienceEnv//Cars project//images//price_distplot_ger.svg", width=1100, height=500)

price_distplot_serb.write_image("D://DataScienceEnv//Cars project//images//price_distplot_serb.png", width=1100, height=500)
price_distplot_ger.write_image("D://DataScienceEnv//Cars project//images//price_distplot_ger.png", width=1100, height=500)

price_distplot_serb.write_image("D://DataScienceEnv//Cars project//images//price_distplot_serb.pdf", width=1100, height=500)
price_distplot_ger.write_image("D://DataScienceEnv//Cars project//images//price_distplot_ger.pdf", width=1100, height=500)


germany_dizel.write_image("D://DataScienceEnv//Cars project//images//germany_dizel.svg", width=550, height=500)
serbia_dizel.write_image("D://DataScienceEnv//Cars project//images//serbia_dizel.svg", width=550, height=500)
germany_benzin.write_image("D://DataScienceEnv//Cars project//images//germany_benzin.svg", width=550, height=500)
serbia_benzin.write_image("D://DataScienceEnv//Cars project//images//serbia_benzin.svg", width=550, height=500)




write_html(manufacturers_germany, "D://DataScienceEnv//Cars project//images//html_images//manufacturers_germany.html")
write_html(manufacturers_serbia, "D://DataScienceEnv//Cars project//images//html_images//manufacturers_serbia.html")
write_html(mod_per_manuf_germany, "D://DataScienceEnv//Cars project//images//html_images//mod_per_manuf_germany.html")
write_html(mod_per_manuf_serbia, "D://DataScienceEnv//Cars project//images//html_images//mod_per_manuf_serbia.html")


write_html(top_body_styles, "D://DataScienceEnv//Cars project//images//html_images//top_body_styles.html")
write_html(top_transmissions, "D://DataScienceEnv//Cars project//images//html_images//top_transmissions.html")
write_html(top_fuel_types, "D://DataScienceEnv//Cars project//images//html_images//top_fuel_types.html")


write_html(fuel_distribution, "D://DataScienceEnv//Cars project//images//html_images//fuel_distribution.html")
write_html(body_transmission_distribution, "D://DataScienceEnv//Cars project//images//html_images//body_transmission_distribution.html")
write_html(body_per_year, "D://DataScienceEnv//Cars project//images//html_images//body_per_year.html")
write_html(transmission_per_year, "D://DataScienceEnv//Cars project//images//html_images//transmission_per_year.html")
write_html(fuel_per_year, "D://DataScienceEnv//Cars project//images//html_images//fuel_per_year.html")

write_html(top_body_styles_ger, "D://DataScienceEnv//Cars project//images//html_images//top_body_styles_ger.html")
write_html(top_transmissions_ger, "D://DataScienceEnv//Cars project//images//html_images//top_transmissions_ger.html")
write_html(top_fuel_types_ger, "D://DataScienceEnv//Cars project//images//html_images//top_fuel_types_ger.html")

write_html(fuel_distribution_ger,"D://DataScienceEnv//Cars project//images//html_images//fuel_distribution_ger.html")
write_html(body_per_year_ger,"D://DataScienceEnv//Cars project//images//html_images//body_per_year_ger.html")
write_html(transmission_per_year_ger, "D://DataScienceEnv//Cars project//images//html_images//transmission_per_year_ger.html")
write_html(fuel_per_year_ger, "D://DataScienceEnv//Cars project//images//html_images//fuel_per_year_ger.html")


write_html(year_distribution, "D://DataScienceEnv//Cars project//images//html_images//year_distribution.html")
write_html(mileage_per_year, "D://DataScienceEnv//Cars project//images//html_images//mileage_per_year.html")
write_html(price_per_year, "D://DataScienceEnv//Cars project//images//html_images//price_per_year.html")


write_html(germany_dizel,"D://DataScienceEnv//Cars project//images//html_images//germany_dizel.html")
write_html(serbia_dizel, "D://DataScienceEnv//Cars project//images//html_images//serbia_dizel.html")
write_html(germany_benzin, "D://DataScienceEnv//Cars project//images//html_images//germany_benzin.html")
write_html(serbia_benzin, "D://DataScienceEnv//Cars project//images//html_images//serbia_benzin.html")


write_html(price_distplot_ger, "D://DataScienceEnv//Cars project//images//html_images//price_distplot_ger.html")
write_html(price_distplot_serb, "D://DataScienceEnv//Cars project//images//html_images//price_distplot_serb.html")