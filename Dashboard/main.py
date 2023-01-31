import pandas as pd
import numpy as np

from dash import Dash, html, dcc, dash_table
import plotly.express as px

df = pd.read_csv("AggregatedRandom.csv", index_col="Unnamed: 0")
app=Dash("Linear Algebra Profiling")

# Total time for all simulations
scientific_notation_format = dash_table.Format.Format(precision=3, scheme=dash_table.Format.Scheme.exponent)
fixed_decimal_format = dash_table.Format.Format(precision=4, scheme=dash_table.Format.Scheme.fixed)
total_times = df.copy()
total_times["time"] /= total_times["effective_multiplications"]
total_times = total_times[["implementation", "time"]].groupby("implementation").agg(["mean", "std","min", "max"])
total_times = total_times.reset_index()
total_times.columns = [" ".join(col).strip().title() for col in total_times.columns.values]
columns = [
    dict(id='Implementation', name='Implementation'),
    dict(id='Time Mean', name='Time Mean', type="numeric", format=scientific_notation_format),
    dict(id='Time Std', name='Time Std', type="numeric", format=scientific_notation_format),
    dict(id='Time Min', name='Time Min', type="numeric", format=scientific_notation_format),
    dict(id='Time Max', name='Time Max', type="numeric", format=scientific_notation_format),
]
total_times_table = dash_table.DataTable(
    total_times.to_dict("records"), columns,
    sort_action="native", sort_mode="single", sort_by=[{"column_id":"Time Mean","direction": "desc"}],
    style_cell={'textAlign': 'center', "padding":"10px 30px"})
table_desc = html.P(children="""
Here are some summaries about the timings taken for each implementation of the linear algebra program. As we can see, each program has a fairly quick mean time for each multiplication.
Notice, however, that numpy and tensorflow are an order of magnitude slower on average than the compiled languages. This may not seem very significant (especially at such small values) but remember this is time per multiplication! Scale up that factor of 10 to 10,000,000 multiplications and we would notice the speed up.
We can also see that numpy has a significantly larger minimum, maximum, and standard deviation than the other programs. At a single glance we can predict which implementation may perform the worst!
""", style={"width":"75%"})
total_times_div = html.Div(children=[
    html.H2("Timing Information By Implementation, Normalized By Effective Multiplications"),
    html.Div(children=[total_times_table,table_desc],
        style={"display":"flex", "justify-content":"space-evenly", "gap":"5%", "align-items":"center"}
    )
])

# Scatter plot of all data
target_data=df.copy()
target_data["threads"] = target_data["threads"].astype("string")
all_data_fig = px.scatter(target_data, x="effective_multiplications", y="time", 
    facet_col="implementation", facet_col_wrap=2, color="threads", 
    color_continuous_scale=px.colors.qualitative.Plotly,
    category_orders={"threads":["1","2","4","8"]},
    title="Effective Multiplications Timing by Implementation", height=1000)
all_data_fig_desc = [html.P(children=["""
As expected - numpy performs poorly here. Data for the numpy implementation was limited to trials in the range 0-1000, multiplications in the range 0-1000, while all other implementations had both ranges set to 0-2500. This was done to save some time during experimentation - it is already obvious numpy is much slower than other implementations! Threading had no impact on the numpy implementation due to both Python's GIL and numpy already implementing threading in the lower level API calls.
"""]),
html.P(children=["""
Other implementations show significant grouping/banding. For the compiled implementations this is shown to be due to threading, and for Tensorflow this is due to batchsizes (see below). It is promising that this scalability exists for compiled implementations, as it allows for easy timing improvements with additional computing resources.
"""]),
html.P(children=["""
We cannot at this stage determine if there is a clear winner by implementation, so we shall discard numpy and carry on!
"""])
]
all_data_graph_div = html.Div(children=[dcc.Graph(figure=all_data_fig),*all_data_fig_desc])

#Tensorflow only data
target_data = df.copy()
target_data["batchsize"] = target_data["batchsize"].astype("string")
target_data = target_data.loc[(target_data["implementation"] == "tensorflow_cpu") | (target_data["implementation"] == "tensorflow_gpu")]

tensorflow_plot = px.scatter(target_data, x="effective_multiplications", y="time", title="Tensorflow Effective Multiplication Timings",
    facet_col="implementation", color="batchsize", 
    category_orders={"batchsize":["8","32","64","256"]}, trendline="ols")

tensorflow_trendlines = px.get_trendline_results(tensorflow_plot)
tensorflow_trendline_data = pd.DataFrame()
for trendline_index in range(len(tensorflow_trendlines)):
    fit_results = tensorflow_trendlines.iloc[trendline_index].px_fit_results
    curr_df = pd.DataFrame([[tensorflow_trendlines.iloc[trendline_index].batchsize,fit_results.params[1],fit_results.params[0],fit_results.rsquared]], 
        columns=["Batch Size", "Slope", "Intercept", "R^2"])
    tensorflow_trendline_data = pd.concat([tensorflow_trendline_data, curr_df], ignore_index=True)

columns = [
    dict(id="Batch Size", name="Batch Size"),
    dict(id="Slope", name="Slope", type="numeric", format=scientific_notation_format),
    dict(id="Intercept", name="Intercept", type="numeric", format=fixed_decimal_format),
    dict(id="R^2", name="R^2", type="numeric", format=fixed_decimal_format)
]
tensorflow_trendline_datatable = dash_table.DataTable(tensorflow_trendline_data.to_dict("records"), columns,
    sort_action="native",
    style_cell={'textAlign': 'center', "padding":"10px 30px"})

tensorflow_data_desc = html.P(children=["""
Looking now just at the Tensorflow data, coloring by batchsize we see the banding above explained. Increasing batchsizes allows for Tensorflow to push more data through in each multiplication.
"""])
tensorflow_data_div = html.Div(children=[dcc.Graph(figure=tensorflow_plot), tensorflow_data_desc, tensorflow_trendline_datatable])

# Layout and creation
app.layout = html.Div(children=[
    html.H1(children="Linear Algebra Profiling"),
    total_times_div,
    html.Hr(),
    all_data_graph_div,
    html.Hr(),
    tensorflow_data_div,
    html.Hr(),
], style={"text-align":"justify", "margin":"0 20%"})

if __name__ == '__main__':
    app.run_server(debug=True)