import plotly.express as px
import plotly.graph_objects as go
import pandas as pd


class Visualizer:

    def __init__(self, data: pd.DataFrame):
        self.aero_df = data

    def scatter_plot(self) -> None:
        # self.aero_df["Chassis Angle"] = self.aero_df["Chassis Angle"].astype(
        #     str)
        # self.aero_df["Cd"] = self.aero_df["Cd"].astype(str)
        # fig = px.scatter(self.aero_df, x="AOA", y="Cl", color="Cd", color_continuous_scale="balance")

        # fig.update_layout(
        #     title=dict(text="S1223 Airfoil",
        #                font=dict(size=40), xref='paper', x=0.5),
        #     height=1080, width=1920, showlegend=True,
        #     legend=dict(font=dict(size=20)),
        # )
        # fig.update_xaxes(
        #     title_text="AOA (deg)", title_font=dict(size=32), tickfont=dict(size=20))
        # fig.update_yaxes(title_text="Cl",
        #                  title_font=dict(size=32), tickfont=dict(size=20))
        # fig.show()
        # fig.write_html("front_axle_vs_rear_axle.html")
        fig = px.scatter(self.aero_df, x="Chassis Angle", y="FA-RA Difference")
        fig.update_traces(marker_size=20)
        fig.update_layout(
            title=dict(text="FA - RA Difference",
                       font=dict(size=40), xref='paper', x=0.5),
            height=1080, width=1920, showlegend=True,
            legend=dict(font=dict(size=20)),
        )
        fig.update_xaxes(
            title_text="Chassis Angle (deg)", title_font=dict(size=32), tickfont=dict(size=20))
        fig.update_yaxes(title_text="Downforce (lbs)",
                         title_font=dict(size=32), tickfont=dict(size=20))
        fig.show()
        # fig2 = px.scatter(self.aero_df, x="Front Rideheight",
        #                   y="Rear Axle Downforce Mean", trendline='ols')
        # fig2.show()
        fig3 = px.scatter(self.aero_df, x="Chassis Angle",
                          y="Raw Downforce Mean")
        fig3.update_traces(marker_size=20)

        fig3.update_layout(
            title=dict(text="Chassis Angle vs Downforce",
                       font=dict(size=40), xref='paper', x=0.5),
            height=1080, width=1920, showlegend=True,
            legend=dict(font=dict(size=20)),
        )
        fig3.update_xaxes(
            title_text="Chassis Angle (deg)", title_font=dict(size=32), tickfont=dict(size=20))
        fig3.update_yaxes(title_text="Downforce (lbs)",
                          title_font=dict(size=32), tickfont=dict(size=20))
        fig3.show()
        # fig = px.scatter(self.aero_df, x="Rideheight", y="Raw Downforce Mean",
        #                  color="Chassis Angle", size="Raw Downforce Mean",
        #                  color_discrete_sequence=["red", "blue", "green", "yellow", "orange",
        #                                           "purple", "magenta", "goldenrod", "black", "cyan", "brown"],
        #                  hover_data=["Chassis Angle", "Chassis Heave", "FA-RA Difference", "Raw Downforce Mean"])
        # fig.update_layout(
        #     title=dict(text="2025 V1 Downforce vs Rideheight",
        #                font=dict(size=40), xref='paper', x=0.5),
        #     height=1080, width=1920, showlegend=True,
        #     legend=dict(font=dict(size=20)),
        # )

        # fig.update_xaxes(
        #     title_text="Ride Height (in)", title_font=dict(size=32), tickfont=dict(size=20))
        # fig.update_yaxes(title_text="Downforce (lbs)",
        #                  title_font=dict(size=32), tickfont=dict(size=20))
        # fig.show()
        # fig.write_html("25v1_03-10.html")

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
            xaxis_title="Ride Height",
            yaxis_title="Downforce",
            height=4320,
            width=7680,
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

        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=[4.85, 6.47], y=[
            4.12, 6.60], mode='lines', line=dict(color='red', width=4, dash="dash"), name="Neutral Rideheight"))

        fig2.add_trace(go.Histogram2dContour(
            x=self.aero_df.get("Front Rideheight"),
            y=self.aero_df.get("Rear Rideheight"),
            z=self.aero_df.get(target_column),
            histfunc='avg',
            contours=dict(
                labelfont=dict(color='white'), start=90, end=135, size=5)))

        fig2.update_traces(selector=dict(type='histogram2dcontour'), contours_coloring="fill", contours_showlabels=False,
                           colorscale="balance",
                           colorbar=dict(title=f"{target_column} (lbf)",
                                         titlefont=dict(size=32),
                                         titleside='right', tickfont=dict(size=20)),
                           )
        fig2.update_layout(title=dict(text=f"Ride Height vs {target_column}",
                           font=dict(size=40), xref='paper', x=0.5),
                           height=1080, width=1920, showlegend=True, legend=dict(xanchor="right", font=dict(size=20))
                           #    height=4320,
                           #    width=7680,
                           )

        fig2.update_xaxes(
            title_text="Front Ride Height (in)", range=[5.0, 5.8], title_font=dict(size=32), tickfont=dict(size=20))
        fig2.update_yaxes(title_text="Rear Ride Height (in)", range=[
                          4.5, 6.25],  title_font=dict(size=32), tickfont=dict(size=20))

        fig2.show()

        if save_plot:
            fig2.write_image(output_file_name + ".png")
            # fig2.write_html(output_file_name + ".html")
