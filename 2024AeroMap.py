import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from matplotlib import pyplot as plt
from plotly.subplots import make_subplots
from typing import Final


class AeroMapV1:

    """
        Will restructure this quite a bit for the next study, this was great for rapid testing, but is slow now
        This is quite messy right now, half did some restructuring, not much is typed right now
        Also need to learn how to align the axes better as still a little off due to rounding along the large range
        Note this does not include the merge for the 2023 baseline data, but the process is same as below
    """

    def __init__(self, file_name: str):
        self.HEAVE_MIN: Final = -1.0
        self.HEAVE_MAX: Final = 1.0
        self.CHASSIS_ANGLE_MIN: Final = -1.8131
        self.CHASSIS_ANGLE_MAX: Final = 0.8076
        self.file_name = file_name
        self.folder = "2024AeroMapV2\\"
        #self.merge_csv_data()
        self.aeromap_df = pd.DataFrame(pd.read_csv(self.file_name, delimiter=','))
        self.contour_df = self.create_df_for_contour()
        # self.z_2d = self.create_2d_z()
        # self.x = self.contour_df.get('FRH')
        # self.y = self.contour_df.get('RRH')
        #self.density_contour("density_contour_data_v1.csv")
        #self.density_contour("density_contour_data_v2.csv")


    @staticmethod
    def merge_csv_data(folder: str) -> pd.DataFrame:
        """ takes a file from a give folder to set as base,
         then appends each file after that and saves to new csv"""

        base_file_name = "_2024SensitivityStudy2_Straightline_finalv1cleared_Report.csv"
        aeromap_2024 = pd.DataFrame(pd.read_csv(folder + "batch_1_1" + base_file_name, delimiter=','))
        batches = [2, 3, 4, 5, 6]
        for batch in batches:
            for i in range(1, 9):
                if batch == 8 and i == 2:  # since 8_2 was used to initialize
                    continue
                try:
                    next_csv = pd.DataFrame(pd.read_csv(folder + "batch_" + str(batch) + "_" + str(i) + base_file_name, delimiter=','))
                    aeromap_2024 = pd.concat([aeromap_2024, next_csv])
                except FileNotFoundError:
                    continue
        aeromap_2024.to_csv("2024_aeromap_v2.csv", index=False)
        return aeromap_2024

    def merge_yaw_angle_data(self):
        base_file_name = "_2024Sensitivitytudy1_Yaw_Report.csv"
        folder = self.folder + "YawAngle\\"
        yaw_angle = pd.DataFrame(pd.read_csv(folder + "batch_1" + base_file_name, delimiter=','))
        for i in range(2, 8):
            try:
                next_csv = pd.DataFrame(pd.read_csv(folder + "batch_" + str(i) + base_file_name, delimiter=','))
                yaw_angle = pd.concat([yaw_angle, next_csv])
            except FileNotFoundError:
                print(folder + "batch_" + str(i) + "_" + base_file_name)
                continue
        yaw_angle.to_csv("2024_yaw_angle_v1.csv", index=False)

    def calculate_ride_height_combinations(self) -> None:
        ride_height_combinations = pd.DataFrame(columns=["Chassis Heave", "Chassis Angle", "Front Ride Height", "Rear Ride Height"])
        num_heaves = 36
        num_angles = 36
        heave_increment = (self.HEAVE_MAX + abs(self.HEAVE_MIN)) / (num_heaves - 1)
        angle_increment = (self.CHASSIS_ANGLE_MAX + abs(self.CHASSIS_ANGLE_MIN)) / (num_angles - 1)
        iteration = 0
        for i in range(0, 1):
            for j in range(0, num_angles):
                #chassis_heave = np.round(self.HEAVE_MIN + (i * heave_increment), 5)
                chassis_heave = np.round(-0.1429, 5)
                chassis_angle = np.round(self.CHASSIS_ANGLE_MIN + (j * angle_increment), 5)
                frh = 4.88 + (chassis_heave - 49.50) * np.sin(chassis_angle * (np.pi / 180))
                rrh = 5.55 + (chassis_heave + 46.04) * np.sin(chassis_angle * (np.pi / 180))
                ride_height_combinations.loc[iteration, "Chassis Heave"] = chassis_heave
                ride_height_combinations.loc[iteration, "Chassis Angle"] = chassis_angle

                ride_height_combinations.loc[iteration, "Front Ride Height"] = frh
                ride_height_combinations.loc[iteration, "Rear Ride Height"] = rrh
                iteration += 1
        # print(ride_height_combinations)
        fig = px.scatter(ride_height_combinations, x="Front Ride Height", y="Rear Ride Height")
        fig.show()
        ride_height_combinations.to_csv("Ride_Heights.csv", index=False)

    def create_2d_z(self) -> [[]]:  # converts 1D pd.series into 2D array for plotly contour, use if symmetric inputs
        z = []
        current_z = []
        current_angle = self.contour_df.loc[0, "ChassisAngle"]

        for i in range(len(self.contour_df.index)):
            new_angle = self.contour_df.loc[i, "ChassisAngle"]
            if new_angle == current_angle:
                current_z.append(self.contour_df.loc[i, "RDF"])
            else:
                z.append(current_z)
                current_z = []
                current_z.append(self.contour_df.loc[i, "RDF"])
                current_angle = new_angle

        z.append(current_z)
        return z

    def scatter_plot(self) -> None:  # plug and play scatter plots, can use size, symbol, or color to see more relations
        fig = px.scatter(self.aeromap_df, x="Front Rideheight", y="Front Axle Downforce", trendline='ols')
        fig.show()

        fig2 = px.scatter(self.aeromap_df, x="Front Rideheight", y="Rear Axle Downforce", trendline='ols')
        fig2.show()

    def create_df_for_contour(self) -> pd.DataFrame:
        plot_df = pd.DataFrame(pd.read_csv("2024_aeromap_plot_data.csv", delimiter=','))
        for i in range(len(self.aeromap_df.index)):
            current_angle = self.aeromap_df.loc[i, "Chassis Angle"]
            current_heave = self.aeromap_df.loc[i, "Chassis Heave"]
            for j in range(len(plot_df.index)):
                if i == 0:  # fills empty cells with None
                    plot_df.iloc[j, 0:3] = "None"

                if current_angle == plot_df.loc[j, "ChassisAngle"] and current_heave == plot_df.loc[j, "ChassisHeave"]:
                    #  if params match then copy values from the base df into the new df
                    plot_df.loc[j, "RDF"] = self.aeromap_df.loc[i, "Raw Downforce Mean"]
                    plot_df.loc[j, "FRH"] = self.aeromap_df.loc[i, "Front Rideheight"]
                    plot_df.loc[j, "RRH"] = self.aeromap_df.loc[i, "Rear Rideheight"]

        plot_df.to_csv("2024_aeromap_with_none.csv", index=False)
        return plot_df

    def aeromap_variations_v2(self) -> None:  # currently depreciated, will use if we have symmetric inputs
        fig = make_subplots(rows=2, cols=2, subplot_titles=('connectgaps = False', 'connectgaps = True'))

        fig.add_trace(go.Contour(z=self.z_2d, showscale=True, colorscale='jet',
                                 contours=dict(showlabels=True, labelfont=dict(size=12, color='white'))), 1, 1)
        fig.add_trace(go.Contour(z=self.z_2d, showscale=True, connectgaps=True, colorscale='jet',
                                 contours=dict(showlabels=True, labelfont=dict(size=12, color='white'))), 1, 2)
        fig.add_trace(go.Heatmap(z=self.z_2d, showscale=True, zsmooth='best', colorscale='jet'), 2, 1)
        fig.add_trace(go.Heatmap(z=self.z_2d, showscale=True, connectgaps=True, zsmooth='best', colorscale='jet'), 2, 2)

        fig.update_traces(row=1, col=1, x0=4, y0=4, dx=0.6, dy=0.4)
        fig.update_traces(row=1, col=2, x0=4, y0=4, dx=0.6, dy=0.4)
        fig.update_traces(row=2, col=1, x0=4, y0=4, dx=0.6, dy=0.4)
        fig.update_traces(row=2, col=2, x0=4, y0=4, dx=0.6, dy=0.4)
        fig.update_xaxes(title_text="Front Ride Height")
        fig.update_yaxes(title_text="Rear Ride Height")
        fig['layout']['yaxis1'].update(title='Contour map')
        fig['layout']['yaxis3'].update(title='Heatmap')
        #fig.update_traces(contours_coloring="fill", contours_showlabels=True)
        fig.show()

    def create_density_contour_df(self) -> pd.DataFrame:
        base_file_name = "_2024SensitivityStudy2_Straightline_finalv1cleared_Report.csv"
        density_contour_df = pd.DataFrame(pd.read_csv(self.folder + "batch_1_1" + base_file_name, delimiter=','))
        batches = [1, 2, 3, 4, 5, 6, 7, 8]
        for batch in batches:
            for i in range(1, 9):
                try:
                    next_csv = pd.DataFrame(
                        pd.read_csv(self.folder + "batch_" + str(batch) + "_" + str(i) + base_file_name, delimiter=','))
                    for j in range(1, int(next_csv.loc[0, "Raw Downforce Mean"])):
                        if batch == 2 and i == 3 and j == 1:  # since 2_3 was used to initialize
                            continue
                        density_contour_df = pd.concat([density_contour_df, next_csv])

                except FileNotFoundError:
                    continue
        print(density_contour_df)
        density_contour_df.to_csv("density_contour_data_v2.csv", index=False)
        return density_contour_df

    @staticmethod
    def density_contour(file_name: str) -> None:
        contour_data = pd.DataFrame(pd.read_csv(file_name, delimiter=','))

        fig2 = go.Figure(go.Histogram2dContour(
                                               x=contour_data.get("Front Rideheight"),
                                               y=contour_data.get("Rear Rideheight"),
                                               z=contour_data.get("Raw Downforce Mean"),
                                               histfunc='avg',
                                               contours=dict(labelfont=dict(color='white'), start=70, end=120, size=5)))
        fig2.update_traces(contours_coloring="fill", contours_showlabels=False, colorscale="balance",
                           colorbar=dict(title="Mean Downforce (lbs)", titlefont=dict(size=20), titleside='right'),
                           )
        fig2.update_layout(title=dict(text="Ride Height vs Downforce", font=dict(size=24), xref='paper', x=0.5),
                           font=dict(size=20),
                           #xaxis=dict(tick0=4.0, dtick=0.4),
                           #yaxis=dict(tick0=4.0, dtick=0.4),
                           #height=720, width=1024
                           )
        fig2.update_xaxes(title_text="Front Ride Height (in)", )
        fig2.update_yaxes(title_text="Rear Ride Height (in)")
        fig2.show()

        # can write static html file to export plot
        # fig2.write_html("2024Aeromap.html")

    def create_histogram(self) -> None:  # basic histogram plots
        baseline = pd.DataFrame(pd.read_csv("2023_aeromap_cleaned.csv", delimiter=','))
        #fig = px.histogram(self.aeromap_df, x="Raw Downforce Mean", nbins=10, range_x=(80, 125), text_auto=True)
        fig = go.Figure()
        fig.add_trace(go.Histogram(x=self.aeromap_df.get("Raw Downforce Mean"), name="New",
                                   xbins=dict(start=80, end=125, size=4), marker=dict(color="#007cff")))
        #fig.add_trace(go.Histogram(x=baseline.get("Raw Downforce Mean"), name="Baseline", xbins=dict(start=80, end=125, size=4)))
        fig.update_layout(title=dict(text="New", font=dict(size=24), xref='paper', x=0.5),
                          xaxis_title="Mean Downforce", yaxis_title="Count", bargap=0.2, bargroupgap=0.1,
                          xaxis=dict(tick0=80, dtick=4),
                          width=1024, height=720,
                          font=dict(size=18))
        #fig.update_traces(opacity=0.75)
        fig.show()

        fig2 = go.Figure()
        fig2.add_trace(go.Histogram(x=baseline.get("Raw Downforce Mean"), name="New",
                                   xbins=dict(start=80, end=125, size=4), marker=dict(color="#c7280e")))
        # fig.add_trace(go.Histogram(x=baseline.get("Raw Downforce Mean"), name="Baseline", xbins=dict(start=80, end=125, size=4)))
        fig2.update_layout(title=dict(text="Baseline", font=dict(size=24), xref='paper', x=0.5),
                          xaxis_title="Mean Downforce", yaxis_title="Count", bargap=0.2, bargroupgap=0.1,
                          xaxis=dict(tick0=80, dtick=4),
                          width=1024, height=720,
                          font=dict(size=18)),
        # fig.update_traces(opacity=0.75)
        fig2.show()


if __name__ == "__main__":
    aeromap = AeroMapV1("2024_aeromap_v2.csv")
    aeromap.density_contour("density_contour_data_v2.csv")
