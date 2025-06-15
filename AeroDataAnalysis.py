import os

import pandas as pd
import numpy as np
from typing import Final, Tuple, List
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
        merged_data = pd.DataFrame(
            pd.read_csv(f"{self.folder}1{self.base_file_name}", delimiter=",")
        )
        for i in range(2, 96):
            try:
                next_csv = pd.DataFrame(
                    pd.read_csv(f"{self.folder}{i}{self.base_file_name}")
                )
                merged_data = pd.concat([merged_data, next_csv])
            except FileNotFoundError:
                continue
        merged_data.to_csv(f"{self.folder}{output_file}", index=False)
        return merged_data

    def merge_airfoil_data(self, folders: [str], outputfile: str) -> pd.DataFrame:
        merged_data = pd.DataFrame(
            pd.read_csv(f"{self.folder}1/batch_1_{self.base_file_name}", delimiter=",")
        )
        for folder in folders:
            for i in range(2, 181):
                try:
                    next_csv = pd.DataFrame(
                        pd.read_csv(
                            f"{self.folder}{folder}batch_{i}_{self.base_file_name}"
                        )
                    )
                    merged_data = pd.concat([merged_data, next_csv])
                except FileNotFoundError:
                    continue
        merged_data.to_csv(f"{self.folder}{outputfile}", index=False)
        return merged_data

    def merge_moo_data(self, folder_range: Tuple, results_name: str, inputs_name: str):
        merged_data = pd.DataFrame()
        generation = 0
        for folder in range(folder_range[0], folder_range[1] + 1):
            if folder % 64 == 0:
                generation += 1
            folder_path = f"{self.folder}{folder}"
            print(folder_path)
            results = os.path.join(folder_path, results_name)
            print(results)
            inputs = os.path.join(folder_path, inputs_name)
            print(inputs)

            if os.path.exists(results) and os.path.exists(inputs):
                try:
                    results_df = pd.DataFrame(pd.read_csv(results))
                    inputs_df = pd.DataFrame(pd.read_csv(inputs))

                    combined_df = pd.concat([results_df, inputs_df], axis=1)

                    combined_df["Generation"] = generation
                    combined_df["Sim_Num"] = folder
                except:
                    continue
                combined_file = os.path.join(folder_path, f"{folder}_{results_name}")
                combined_df.to_csv(combined_file, index=False)
                print(f"combined file saved to {combined_file}")
                merged_data = pd.concat([merged_data, combined_df])
            else:
                print(f"Missing files in folder {folder}")
        merged_data.to_csv(f"{self.folder}Combined_{self.base_file_name}")

    def convert_rh_to_inches(self, columns: list[str]) -> None:
        for i, data in self.aero_data.iterrows():
            for column in columns:
                self.aero_data.at[i, column] = data[column] * 39.3701

    def convert_rh(self) -> None:
        for i, data in self.aero_data.iterrows():
            self.aero_data.at[i, "Rideheight"] = data["Chassis Heave"] + 1.69

    def create_aeromap_df(
        self,
        output_file: str,
        target_column: str = "Downforce",
        save_csv: bool = False,
    ) -> pd.DataFrame:
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
        self.aero_data[columns].to_csv(f"{self.folder}{output_file}", index=False)

    def normalize_columns(
        self, columns: list, save_csv: False, output_file: str = None
    ) -> None:
        # normalizer = Normalizer()
        # self.aero_data[columns] = normalizer.fit_transform(
        #     self.aero_data[columns])
        scaled = MinMaxScaler()
        self.aero_data[columns] = scaled.fit_transform(self.aero_data[columns])

        if save_csv:
            self.aero_data.to_csv(f"{self.folder}{output_file}", index=False)

    def calc_min_max_mean(self, column: str) -> None:
        print(f"{column}")
        print(f"Min: {self.aero_data[column].min()}")
        print(f"Max: {self.aero_data[column].max()}")
        print(f"Mean: {self.aero_data[column].mean()}\n")

    def print_corr(self) -> None:
        print(self.aero_data.corr()["Rear Axle Downforce"].sort_values(ascending=False))

    def calc_faxle_raxle_difference(self) -> None:
        self.aero_data["FA-RA Difference"] = (
            self.aero_data["Front Axle Downforce"]
            - self.aero_data["Rear Axle Downforce"]
        )

    def calc_aero_efficiency(self) -> None:
        self.aero_data["Aero Efficiency"] = (
            self.aero_data["ClA"] / self.aero_data["CdA"]
        )

    def clean_intersected_sims(self, column_name: str, threshold: float) -> None:
        for i, data in self.aero_data.iterrows():
            if data[column_name] < threshold:
                self.aero_data.drop(i, inplace=True)


if __name__ == "__main__":
    # file_name = "2024DesignStint4BaselineBullhornsBeamWingCleared_Report.csv"
    file_name = "25EV_MainDesign_v3_80kph_aeromap_Report.csv"
    aeromap = AeroDataAnalysis(file_name, "25EVAeromap/")
    # aeromap.merge_moo_data((0, 767), "25MainDesign_v3_Report.csv", "InputParams.csv")
    # aeromap.merge_csv_data("24Opti.csv")
    # aeromap.merge_airfoil_data(["1/", "2/", "3/", "4/"], "S1223Data.csv")
    aeromap.load_data(file_name)
    # aeromap.calc_hypervolume(["Downforce", "Front Axle Downforce"])
    # aeromap.convert_rh()
    # aeromap.convert_rh_to_inches(["Front Rideheight", "Rear Rideheight"])
    # aeromap.clean_intersected_sims("Front Axle Downforce", 25)
    # aeromap.calc_aero_efficiency()
    # aeromap.calc_faxle_raxle_difference()
    # aeromap.calc_min_max_mean("Downforce")
    # aeromap.calc_min_max_mean("Drag")
    # aeromap.calc_min_max_mean("Front Axle Downforce")
    # aeromap.calc_min_max_mean("Rear Axle Downforce")
    # aeromap.calc_min_max_mean("Aero Efficiency")
    # aeromap.print_corr()

    # aeromap.save_selected_columns("Cleaned_25SimB2.csv", aeromap.aero_data.columns)
    aeromap.create_aeromap_df(
        "25EVAeromap_Cleaned_v3.csv", target_column="Drag", save_csv=False
    )
    visualizer = Visualizer(aeromap.aero_data)
    # visualizer.plot_generation_performance()
    # visualizer.plot_df_vs_aero_efficiency()
    # params = [
    #     ("RW 3rd Element AOA", "deg"),
    #     ("RW 3rd Element X", "mm"),
    #     ("RW 3rd Element Z", "mm"),
    #     ("RW 2nd Element AOA", "deg"),
    #     ("RW 2nd Element X", "mm"),
    #     ("RW 2nd Element Z", "mm"),
    #     ("RW 1st Element AOA", "deg"),
    #     ("RW 1st Element X", "mm"),
    #     ("RW 1st Element Z", "mm"),
    #     ("RW Biplane1 Element AOA", "deg"),
    #     ("RW Biplane1 Element X", "mm"),
    #     ("RW Biplane1 Element Z", "mm"),
    #     ("RW Biplane2 Element AOA", "deg"),
    #     ("RW Biplane2 Element X", "mm"),
    #     ("RW Biplane2 Element Z", "mm"),
    #     ("FW 3rd Element AOA", "deg"),
    #     ("FW 3rd Element X", "mm"),
    #     ("FW 3rd Element Z", "mm"),
    #     ("FW 2nd Element AOA", "deg"),
    #     ("FW 2nd Element X", "mm"),
    #     ("FW 2nd Element Z", "mm"),
    #     ("FW 1st Element AOA", "deg"),
    #     ("FW 1st Element Z", "mm"),
    #     ("Bullhorn AOA", "deg"),
    #     ("Bullhorn X", "mm"),
    #     ("Bullhorn Z Angle", "mm"),
    #     ("FW Biplane Element AOA", "deg"),
    #     ("FW Biplane Element Z", "mm"),
    #     ("Generation", ""),
    #     ("Sim_Num", ""),
    #     ("Front Axle Downforce", "lbs"),
    #     ("Rear Axle Downforce", "lbs"),
    #     ("Downforce", "lbs"),
    #     ("Aero Efficiency", ""),
    #     ("FA-RA Difference", "lbs"),
    #     # ("Diffuser_Angle1", "deg"),
    #     # ("Expansion_Point1", "mm"),
    #     # ("Gurney_Height1", "mm"),
    #     # ("Intake_Length1", "mm"),
    #     # ("Outlet_Length1", "mm"),
    #     # ("Sidepod_Width1", "mm"),
    #     # ("Strake_Offset1", "mm"),
    # ]
    # objectives = [
    #     ("Front Axle Downforce", "lbs"),
    #     ("Rear Axle Downforce", "lbs"),
    #     ("Aero Efficiency", ""),
    #     ("Downforce", "lbs"),
    #     ("FA-RA Difference", "lbs"),
    # ]
    # visualizer.plot_25simA4_moo_params(params, objectives, False, True)
    visualizer.plot_aeromap(
        output_file_name="25EVAeromap", target_column="Drag", save_plot=True
    )
    # visualizer.plot_faxle_vs_raxle()
    # visualizer.scatter_plot()
