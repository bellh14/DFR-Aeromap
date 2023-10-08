import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class Visualizer:

    def __init__(self, data: pd.DataFrame):
        self.aero_df = data

    def scatter_plot(self) -> None:
        fig = px.scatter(self.aero_df, x="Front Rideheight",
                         y="Front Axle Downforce", trendline='ols')
        fig.show()

        fig2 = px.scatter(self.aero_df, x="Front Rideheight",
                          y="Rear Axle Downforce", trendline='ols')
        fig2.show()

    def plot_aeromap(self, target_column: str = "Raw Downforce Mean",
                     save_plot: bool = False,
                     output_file_name: str = None) -> None:

        fig2 = go.Figure(go.Histogram2dContour(
            x=self.aero_df.get("Front Rideheight"),
            y=self.aero_df.get("Rear Rideheight"),
            z=self.aero_df.get(target_column),
            histfunc='avg',
            contours=dict(
                labelfont=dict(color='white'), start=70, end=135, size=5)))

        fig2.update_traces(contours_coloring="fill", contours_showlabels=False,
                           colorscale="balance",
                           colorbar=dict(title=f"{target_column}",
                                         titlefont=dict(size=20),
                                         titleside='right'),)
        fig2.update_layout(title=dict(text=f"Ride Height vs {target_column}",
                           font=dict(size=24), xref='paper', x=0.5),
                           # xaxis=dict(tick0=4.0, dtick=0.4),
                           # yaxis=dict(tick0=4.0, dtick=0.4),
                           # height=720, width=1024
                           )

        fig2.update_xaxes(title_text="Front Ride Height (in)", )
        fig2.update_yaxes(title_text="Rear Ride Height (in)")
        fig2.show()

        if save_plot:
            fig2.write_image(output_file_name + ".png")
            fig2.write_html(output_file_name + ".html")
