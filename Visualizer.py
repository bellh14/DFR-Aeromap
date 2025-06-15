import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Tuple, List


class Visualizer:
    def __init__(self, data: pd.DataFrame):
        self.aero_df = data

    def scatter_plot(self) -> None:
        self.aero_df["ChassisAngle"] = self.aero_df["ChassisAngle"].astype(str)
        self.aero_df["ChassisHeave"] = self.aero_df["ChassisHeave"].astype(str)
        # self.aero_df["Cd"] = self.aero_df["Cd"].astype(str)
        # fig = px.scatter(self.aero_df, x="AOA", y="Cl", color="Cd", color_continuous_scale="balance")

        fig2 = px.scatter(
            self.aero_df, x="CdA", y="ClA", color="ChassisAngle", symbol="ChassisHeave"
        )

        fig2.update_traces(marker_size=20)
        fig2.update_layout(
            title=dict(text="ClA vs CdA", font=dict(size=40), xref="paper", x=0.5),
            height=1080,
            width=1920,
            showlegend=True,
            legend=dict(font=dict(size=20)),
        )
        fig2.update_xaxes(
            title_text="CdA", title_font=dict(size=32), tickfont=dict(size=20)
        )
        fig2.update_yaxes(
            title_text="ClA", title_font=dict(size=32), tickfont=dict(size=20)
        )
        fig2.show()
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
        fig = px.scatter(
            self.aero_df, x="FA-RA Difference", y="Aero Efficiency", trendline="ols"
        )
        fig.update_traces(marker_size=20, marker_color="green")
        fig.update_layout(
            title=dict(
                text="Aero Balance vs Aero Efficiency",
                font=dict(size=40),
                xref="paper",
                x=0.5,
            ),
            height=1080,
            width=1920,
            showlegend=True,
            legend=dict(font=dict(size=20)),
        )
        fig.update_xaxes(
            title_text="Front Axle - Rear Axle Downforce (lbs, lower is better)",
            title_font=dict(size=32),
            tickfont=dict(size=20),
        )
        fig.update_yaxes(
            title_text="Aero Efficiency (CLA/CDA)",
            title_font=dict(size=32),
            tickfont=dict(size=20),
        )
        fig.show()
        # fig2 = px.scatter(self.aero_df, x="Front Rideheight",
        #                   y="Rear Axle Downforce Mean", trendline='ols')
        # fig2.show()
        """ fig3 = px.scatter(self.aero_df, x="Chassis Angle",
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
        fig3.show() """
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

    def plot_df_vs_aero_efficiency(self):
        fig = px.scatter(
            self.aero_df,
            x="Downforce",
            y="Aero Efficiency",
            color_discrete_sequence=px.colors.qualitative.Vivid,
            trendline="ols",
        )
        fig.update_layout(
            title="Aero Efficiency vs Downforce",
            yaxis_title="Aero Efficiency",
            xaxis_title="Downforce (lbs)",
        )
        fig.show()

    def plot_25simA_moo_params(self):
        fig_fw1ez = px.scatter(
            self.aero_df,
            x="FW 1st Element Z",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_fw1ez.update_layout(
            title="Downforce vs FW 1st Element Z",
            xaxis_title="FW 1st Element Z",
            yaxis_title="Downforce (lbs)",
        )
        fig_fw1ez.show()
        fig_fw1ez.write_image("25simA3/fw1ezvsdf.png")

        fig_fw1eaoa = px.scatter(
            self.aero_df,
            x="FW 1st Element AOA",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_fw1eaoa.update_layout(
            title="Downforce vs FW 1st Element AOA",
            xaxis_title="FW 1st Element AOA (deg)",
            yaxis_title="Downforce (lbs)",
        )
        fig_fw1eaoa.show()
        fig_fw1eaoa.write_image("25simA3/fw1eaoavsdf.png")

        fig_fw4eaoa = px.scatter(
            self.aero_df,
            x="FW 4th Element AOA",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_fw4eaoa.update_layout(
            title="Downforce vs FW 4th Element AOA",
            xaxis_title="FW 4th Element AOA",
            yaxis_title="Downforce",
        )
        fig_fw4eaoa.show()
        fig_fw4eaoa.write_image("25simA3/fw4eaoavsdf.png")

        fig_fw4ez = px.scatter(
            self.aero_df,
            x="FW 4th Element Z",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_fw4ez.update_layout(
            title="Downforce vs FW 4th Element Z",
            xaxis_title="FW 4th Element Z",
            yaxis_title="Downforce",
        )
        fig_fw4ez.show()
        fig_fw4ez.write_image("25simA3/fw4ezvsdf.png")

        fig_fw4ex = px.scatter(
            self.aero_df,
            x="FW 4th Element X",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_fw4ex.update_layout(
            title="Downforce vs FW 4th Element X",
            xaxis_title="FW 4th Element X",
            yaxis_title="Downforce",
        )
        fig_fw4ex.show()
        fig_fw4ex.write_image("25simA3/fw4exvsdf.png")

        fig_rw1ez = px.scatter(
            self.aero_df,
            x="RW 1st Element Z",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_rw1ez.update_layout(
            title="Downforce vs RW 1st Element Z",
            xaxis_title="RW 1st Element Z",
            yaxis_title="Downforce",
        )
        fig_rw1ez.show()
        fig_rw1ez.write_image("25simA3/rw1ezvsdf.png")

        fig_rw1ex = px.scatter(
            self.aero_df,
            x="RW 1st Element X",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_rw1ex.update_layout(
            title="Downforce vs FW 1st Element X",
            xaxis_title="RW 1st Element X",
            yaxis_title="Downforce",
        )
        fig_rw1ex.show()
        fig_rw1ex.write_image("25simA3/rw1exvsdf.png")

        fig_rw1eaoa = px.scatter(
            self.aero_df,
            x="RW 1st Element AOA",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_rw1eaoa.update_layout(
            title="Downforce vs RW 1st Element AOA",
            xaxis_title="RW 1st Element AOA",
            yaxis_title="Downforce",
        )
        fig_rw1eaoa.show()
        fig_rw1eaoa.write_image("25simA3/rw1eaoavsdf.png")

        fig_bhaoa = px.scatter(
            self.aero_df,
            x="Bullhorn AOA",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_bhaoa.update_layout(
            title="Downforce vs Bullhorn AOA",
            xaxis_title="Bullhorn AOA",
            yaxis_title="Downforce",
        )
        fig_bhaoa.show()
        fig_bhaoa.write_image("25simA3/bhaoavsdf.png")

        fig_bhx = px.scatter(
            self.aero_df,
            x="Bullhorn X",
            y="Downforce",
            color_discrete_sequence=px.colors.qualitative.Vivid,
        )
        fig_bhx.update_layout(
            title="Downforce vs Bullhorn X",
            xaxis_title="Bullhorn X",
            yaxis_title="Downforce",
        )
        fig_bhx.show()
        fig_bhx.write_image("25simA3/bhxvsdf.png")

    def plot_25simA4_moo_params(
        self,
        params: List[Tuple[str, str]],
        objectives: List[Tuple[str, str]],
        show_plot: bool,
        save_plot: bool,
    ):
        for (
            i,
            param_pair,
        ) in enumerate(params):
            print(i)
            for j, objective_pair in enumerate(objectives):
                if param_pair[1] == "":
                    x_units = ""
                else:
                    x_units = f"({param_pair[1]})"
                if objective_pair[1] == "":
                    y_units = ""
                else:
                    y_units = f"({objective_pair[1]})"

                fig = px.scatter(
                    self.aero_df,
                    x=param_pair[0],
                    y=objective_pair[0],
                    color_discrete_sequence=px.colors.qualitative.Vivid,
                )
                fig.update_layout(
                    title=f"{objective_pair[0]} vs {param_pair[0]}",
                    xaxis_title=f"{param_pair[0]} {x_units}",
                    yaxis_title=f"{objective_pair[0]} {y_units}",
                    width=1920,
                    height=1080,
                )
                if show_plot:
                    fig.show()
                if save_plot:
                    fig.write_image(
                        f"25Final1/param_plots/{objective_pair[0]}vs{param_pair[0]}.png"
                    )

    def plot_aeromap(
        self,
        target_column: str = "Downforce",
        save_plot: bool = False,
        output_file_name: str = None,
    ) -> None:
        fig2 = go.Figure()
        fig2.add_trace(
            go.Scatter(
                x=[4.5, 5.2],
                y=[4.0, 7.5],
                mode="lines",
                line=dict(color="red", width=4, dash="dash"),
                name="Neutral Rideheight",
            )
        )

        fig2.add_trace(
            go.Histogram2dContour(
                x=self.aero_df.get("Front Rideheight"),
                y=self.aero_df.get("Rear Rideheight"),
                z=self.aero_df.get(target_column),
                histfunc="avg",
                contours=dict(labelfont=dict(color="white"), start=25, end=38, size=2),
            )
        )

        fig2.update_traces(
            selector=dict(type="histogram2dcontour"),
            contours_coloring="fill",
            contours_showlabels=False,
            colorscale="balance",
            colorbar=dict(
                title=f"{target_column} (lbf)",
                # titlefont=dict(size=32),
                ticklabelposition="outside right",
                tickfont=dict(size=20),
            ),
        )
        fig2.update_layout(
            title=dict(
                text=f"Ride Height vs {target_column}",
                font=dict(size=40),
                xref="paper",
                x=0.5,
            ),
            height=1080,
            width=1920,
            showlegend=True,
            legend=dict(xanchor="right", font=dict(size=20)),
            #    height=4320,
            #    width=7680,
        )

        fig2.update_xaxes(
            title_text="Front Ride Height (in)",
            range=[4.5, 5.2],
            title_font=dict(size=32),
            tickfont=dict(size=20),
        )
        fig2.update_yaxes(
            title_text="Rear Ride Height (in)",
            range=[4.0, 7.5],
            title_font=dict(size=32),
            tickfont=dict(size=20),
        )

        fig2.show()

        if save_plot:
            fig2.write_image(output_file_name + ".png")
            # fig2.write_html(output_file_name + ".html")

    def plot_df_aeromap(
        self,
        target_column: str = "Downforce",
        save_plot: bool = False,
        output_file_name: str = None,
    ) -> None:
        fig2 = go.Figure()

        fig2.add_trace(
            go.Histogram2dContour(
                x=self.aero_df.get("Front Axle Downforce"),
                y=self.aero_df.get("Rear Axle Downforce"),
                z=self.aero_df.get(target_column),
                histfunc="avg",
                contours=dict(labelfont=dict(color="white"), start=75, end=165, size=5),
            )
        )

        fig2.update_traces(
            selector=dict(type="histogram2dcontour"),
            contours_coloring="fill",
            contours_showlabels=False,
            colorscale="balance",
            colorbar=dict(
                title=f"{target_column} (lbf)",
                titlefont=dict(size=32),
                titleside="right",
                tickfont=dict(size=20),
            ),
        )
        fig2.update_layout(
            title=dict(
                text=f"FA, RA vs {target_column}",
                font=dict(size=40),
                xref="paper",
                x=0.5,
            ),
            height=1080,
            width=1920,
            showlegend=True,
            legend=dict(xanchor="right", font=dict(size=20)),
            #    height=4320,
            #    width=7680,
        )

        fig2.update_xaxes(
            title_text="Front Axle Downforce (lbs)",
            title_font=dict(size=32),
            tickfont=dict(size=20),
        )
        fig2.update_yaxes(
            title_text="Rear Axle Downforce (lbs)",
            title_font=dict(size=32),
            tickfont=dict(size=20),
        )

        fig2.show()

        if save_plot:
            fig2.write_image(output_file_name + ".png")
            # fig2.write_html(output_file_name + ".html")
