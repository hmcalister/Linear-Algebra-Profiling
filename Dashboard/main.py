from enum import Enum
import pandas as pd
import numpy as np

from dash import Dash, html, dcc, dash_table
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px

df = pd.read_csv("AggregatedRandomClean.csv", index_col="Unnamed: 0")
# ------------------------------------------------------------------------------------------------------------------------------------------
best_by_impl = {
    "numpy": df.loc[(df["implementation"]=="numpy") & (df["threads"]==8)],
    "golang": df.loc[(df["implementation"]=="golang") & (df["threads"]==8)],
    "tensorflow_cpu": df.loc[(df["implementation"]=="tensorflow_cpu") & (df["batchsize"]==256)],
    "tensorflow_gpu": df.loc[(df["implementation"]=="tensorflow_gpu") & (df["batchsize"]==256)],
    "dynamic_rust": df.loc[(df["implementation"]=="dynamic_rust") & (df["threads"]==8)],
    "static_rust": df.loc[(df["implementation"]=="static_rust") & (df["threads"]==8)],
}

best_df = pd.DataFrame()
for impl in best_by_impl.values():
    best_df = pd.concat([best_df, impl], ignore_index=True)

best_fig = px.scatter(best_df, x="effective_multiplications", y="time", color="implementation", trendline="ols", title="Best Performance by Implementation", height=800)
trendlines = px.get_trendline_results(best_fig)
trendline_data = pd.DataFrame()
for trendline_index in range(len(trendlines)):
    fit_results = trendlines.iloc[trendline_index].px_fit_results
    curr_df = pd.DataFrame([[trendlines.iloc[trendline_index].implementation,fit_results.params[1],fit_results.params[0],fit_results.rsquared]], 
        columns=["Implementation", "Slope", "Intercept", "R^2"])
    trendline_data = pd.concat([trendline_data, curr_df], ignore_index=True)

scientific_notation_format = dash_table.Format.Format(precision=3, scheme=dash_table.Format.Scheme.exponent)
fixed_decimal_format = dash_table.Format.Format(precision=4, scheme=dash_table.Format.Scheme.fixed)
columns = [
    dict(id="Implementation", name="Implementation"),
    dict(id="Slope", name="Slope", type="numeric", format=scientific_notation_format),
    dict(id="Intercept", name="Intercept", type="numeric", format=fixed_decimal_format),
    dict(id="R^2", name="R^2", type="numeric", format=fixed_decimal_format)
]
trendline_datatable = dash_table.DataTable(trendline_data.to_dict("records"), columns,
    sort_action="native", sort_mode="single", sort_by=[{"column_id":"Slope","direction": "asc"}],
    style_cell={'textAlign': 'center', "padding":"10px 30px"})

best_plot_div = html.Div(children=[dcc.Graph(id="bestPlot", figure=best_fig), trendline_datatable])

# ------------------------------------------------------------------------------------------------------------------------------------------

class SCALE_COL(Enum):
    THREADS = 0,
    BATCHSIZE = 1,
implementations = {
    "numpy": SCALE_COL.THREADS,
    "golang": SCALE_COL.THREADS,
    "tensorflow_cpu": SCALE_COL.BATCHSIZE,
    "tensorflow_gpu": SCALE_COL.BATCHSIZE,
    "dynamic_rust": SCALE_COL.THREADS,
    "static_rust": SCALE_COL.THREADS,
}
threaded_impls = []
batched_impls = []

app=Dash("Linear Algebra Profiling")

NUM_ROWS = 3
NUM_COLS = 2
fig_layout = go.Layout(height=1000, title="All Implementations")
scatter_fig = go.Figure(layout=fig_layout)
scatter_fig = make_subplots(rows=NUM_ROWS, cols=NUM_COLS, shared_xaxes="all", shared_yaxes="all",
    vertical_spacing=0.05,
    subplot_titles=list(implementations.keys()), figure=scatter_fig)
scatter_fig.update_layout(legend_title_text="Implementation", legend=dict(groupclick="toggleitem"))

threads = list(df["threads"].unique())
threads.sort()
batchsizes = list(df["batchsize"].unique())
batchsizes.sort()

curr_index = 0
for implementation, scale_col in implementations.items():
    row = 1+curr_index//NUM_COLS
    col = 1+curr_index%NUM_COLS
    if scale_col == SCALE_COL.THREADS:
        for thread in threads:
            target_data = df.loc[(df["implementation"]==implementation) & (df["threads"]==thread)]
            scatter_fig.add_trace(go.Scatter(x=target_data["effective_multiplications"], y=target_data["time"],
                mode="markers", legendgroup=f"{implementation}", name=f"Threads: {thread}", legendgrouptitle_text=f"{implementation}"
            ), row=row, col=col)
    elif scale_col == SCALE_COL.BATCHSIZE:
        for batchsize in batchsizes:
            target_data = df.loc[(df["implementation"]==implementation) & (df["batchsize"] == batchsize)]
            scatter_fig.add_trace(go.Scatter(x=target_data["effective_multiplications"], y=target_data["time"],
                mode="markers", legendgroup=f"{implementation}", name=f"Batch Size: {batchsize}", legendgrouptitle_text=f"{implementation}"
            ), row=row, col=col)
    curr_index+=1

scatter_plot_div = html.Div(children=[dcc.Graph(id="scatterPlot", figure=scatter_fig)])

# ------------------------------------------------------------------------------------------------------------------------------------------

# Layout and creation
app.layout = html.Div(children=[
    html.H1(children="Linear Algebra Profiling"),
    best_plot_div,
    html.Hr(),
    scatter_plot_div,
], style={"text-align":"justify", "margin":"0 10%"})

if __name__ == '__main__':
    app.run(debug=False)