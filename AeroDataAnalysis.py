import pandas as pd
from typing import Final
from Visualizer import Visualizer
from sklearn.preprocessing import Normalizer, MinMaxScaler


class AeroDataAnalysis:

    def __init__(self, base_file_name: str, folder_name: str):
        self.HEAVE_MIN: Final = -1.0
        self.HEAVE_MAX: Final = 1.0
        self.CHASSIS_ANGLE_MIN: Final = -1.8131
        self.CHASSIS_ANGLE_MAX: Final = 0.8076
        self.base_file_name = base_file_name
        self.folder = folder_name
        self.aero_data = pd.DataFrame()

    def load_data(self, file_name: str):
        self.aero_data = pd.DataFrame(pd.read_csv(f"{self.folder}{file_name}"))

    def merge_csv_data(self, output_file: str) -> pd.DataFrame:

        merged_data = pd.DataFrame(pd.read_csv(
            f"{self.folder}batch_1_{self.base_file_name}", delimiter=','))
        for i in range(2, 9):
            try:
                next_csv = pd.DataFrame(pd.read_csv(
                    f"{self.folder}batch_{i}_{self.base_file_name}"))
                merged_data = pd.concat([merged_data, next_csv])
            except FileNotFoundError:
                continue
        merged_data.to_csv(f"{self.folder}{output_file}", index=False)
        return merged_data

    def convert_rh_to_inches(self, columns: list[str]) -> None:
        for i, data in self.aero_data.iterrows():
            for column in columns:
                self.aero_data.at[i, column] = data[column] * 39.3701

    def convert_rh(self) -> None:
        for i, data in self.aero_data.iterrows():
            self.aero_data.at[i,
                              "Rideheight"] = data["Chassis Heave"] + 1.69

    def create_aeromap_df(self, output_file: str,
                          target_column: str = "Raw Downforce Mean",
                          save_csv: bool = False) -> pd.DataFrame:

        aeromap_df = pd.DataFrame()

        for i, data in self.aero_data.iterrows():
            data = data.to_frame().transpose()

            if i == 0:
                aeromap_df = pd.concat([aeromap_df, data])

            for j in range(round(data.loc[i, target_column])):
                aeromap_df = pd.concat([aeromap_df, data])

        if save_csv:
            aeromap_df.to_csv(f"{self.folder}{output_file}", index=False)

        return aeromap_df

    def save_selected_columns(self, output_file: str, columns: list) -> None:
        self.aero_data[columns].to_csv(f"{self.folder}{output_file}",
                                       index=False)

    def normalize_columns(self, columns: list, save_csv: False,
                          output_file: str = None) -> None:
        # normalizer = Normalizer()
        # self.aero_data[columns] = normalizer.fit_transform(
        #     self.aero_data[columns])
        scaled = MinMaxScaler()
        self.aero_data[columns] = scaled.fit_transform(
            self.aero_data[columns])

        if save_csv:
            self.aero_data.to_csv(f"{self.folder}{output_file}",
                                  index=False)

    def calc_min_max_mean(self, column: str) -> None:
        print(f"{column}")
        print(f"Min: {self.aero_data[column].min()}")
        print(f"Max: {self.aero_data[column].max()}")
        print(f"Mean: {self.aero_data[column].mean()}")

    def calc_faxle_raxle_difference(self) -> None:
        self.aero_data["FA-RA Difference"] = self.aero_data["Front Axle Downforce Mean"] - \
            self.aero_data["Rear Axle Downforce Mean"]


if __name__ == "__main__":
    # file_name = "2024DesignStint4BaselineBullhornsBeamWingCleared_Report.csv"
    file_name = "24_Aeromap_Final.csv"
    aeromap = AeroDataAnalysis(file_name, "2024V4/")
    aeromap.load_data(file_name)
    # aeromap.convert_rh()
    # aeromap.convert_rh_to_inches(["Front Rideheight", "Rear Rideheight"])
    # aeromap.calc_faxle_raxle_difference()
    # aeromap.save_selected_columns(
    #     "24_Aeromap_Final.csv", aeromap.aero_data.columns)
    aeromap.create_aeromap_df("24_Aeromap_Final_Cleaned.csv",
                              save_csv=True)
    visualizer = Visualizer(aeromap.aero_data)
    visualizer.plot_aeromap(
        output_file_name="24AeroMapFinal_Report", save_plot=True)
    # visualizer.plot_faxle_vs_raxle()
    # visualizer.scatter_plot()
