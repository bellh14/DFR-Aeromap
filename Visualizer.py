import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class Visualizer:

    def __init__(self, data: pd.DataFrame):
        self.aero_df = data

    def scatter_plot(self) -> None:
        fig = px.scatter(self.aero_df, x="CdA Mean",
                         y="ClA Mean", trendline='lowess', trendline_color_override='red', trendline_options=dict(frac=0.5))
        # fig.show()
        # fig.write_html("front_axle_vs_rear_axle.html")
        # fig2 = px.scatter(self.aero_df, x="Front Rideheight",
        #                   y="Rear Axle Downforce Mean", trendline='ols')
        # fig2.show()
        self.aero_df["Chassis Angle"] = self.aero_df["Chassis Angle"].astype(
            str)
        fig2 = px.scatter(self.aero_df, x="Rideheight", y="Raw Downforce Mean", color="Chassis Angle",
                          size="Raw Downforce Mean", color_discrete_sequence=px.colors.qualitative.D3)
        fig2.update_layout(
            title="Ride Height vs Downforce",
            xaxis_title="Ride Height (in)",
            yaxis_title="Downforce (lbf)",
            height=1080,
            width=1920,
        )
        fig2.show()

    def plot_faxle_vs_raxle(self):
        fig = px.scatter(
            self.aero_df,
            x="Front Rideheight",
            # y=["Front Axle Downforce Mean", "Rear Axle Downforce Mean"],
            y="FA-RA Difference",
            size="Raw Downforce Mean",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig.update_layout(
            title="Front Axle vs Rear Axle Downforce",
            xaxis_title="Ride Height (in)",
            yaxis_title="Downforce (lbf)",
            height=1080,
            width=1920,
        )

        # fig.update_layout(
        #     title=f"Linear Potentiometer Data {title}",
        #     yaxis_title="mm",
        #     xaxis_title="Time",
        #     height=1080,
        #     width=1920,
        # )
        fig.show()

    def plot_aeromap(self, target_column: str = "Raw Downforce Mean",
                     save_plot: bool = False,
                     output_file_name: str = None) -> None:

        fig2 = go.Figure(go.Histogram2dContour(
            x=self.aero_df.get("Front Rideheight"),
            y=self.aero_df.get("Rear Rideheight"),
            z=self.aero_df.get(target_column),
            histfunc='avg',
            contours=dict(
                labelfont=dict(color='white'), start=110, end=150, size=5)))

        fig2.update_traces(contours_coloring="fill", contours_showlabels=False,
                           colorscale="balance",
                           colorbar=dict(title=f"{target_column}",
                                         titlefont=dict(size=20),
                                         titleside='right'),)
        fig2.update_layout(title=dict(text=f"Ride Height vs {target_column}",
                           font=dict(size=24), xref='paper', x=0.5),
                           # height=720, width=1024
                           )

        fig2.update_xaxes(
            title_text="Front Ride Height (in)", range=[4.5, 6.5])
        fig2.update_yaxes(title_text="Rear Ride Height (in)", range=[4.5, 8.0])
        fig2.show()

        if save_plot:
            fig2.write_image(output_file_name + ".png")
            fig2.write_html(output_file_name + ".html")
