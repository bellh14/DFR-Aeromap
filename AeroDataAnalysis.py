import pandas as pd
from typing import Final
from Visualizer import Visualizer


class AeroDataAnalysis:

    def __init__(self, base_file_name: str, folder_name: str):
        self.HEAVE_MIN: Final = -1.0
        self.HEAVE_MAX: Final = 1.0
        self.CHASSIS_ANGLE_MIN: Final = -1.8131
        self.CHASSIS_ANGLE_MAX: Final = 0.8076
        self.base_file_name = base_file_name
        self.folder = folder_name
        self.aero_data = pd.DataFrame()

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

    def create_aeromap_df(self, output_file: str,
                          save_csv: bool = False) -> pd.DataFrame:

        aeromap_df = pd.DataFrame()

        for i, data in self.aero_data.iterrows():
            data = data.to_frame().transpose()

            if i == 0:
                aeromap_df = pd.concat([aeromap_df, data])

            for j in range(round(data.loc[i, "Raw Downforce Mean"])):
                aeromap_df = pd.concat([aeromap_df, data])

        if save_csv:
            aeromap_df.to_csv(f"{self.folder}{output_file}", index=False)

        return aeromap_df


if __name__ == "__main__":
    file_name = "2024DesignStint4BaselineBullhornsBeamWingCleared_Report.csv"
    aeromap = AeroDataAnalysis(file_name, "2024V4/")
    aeromap.aero_data = aeromap.merge_csv_data("2024_aeromap_v4.csv")
    aeromap.create_aeromap_df("2024_aeromap_contour_v4.csv")
    visualizer = Visualizer(aeromap.aero_data)
    visualizer.plot_aeromap()
