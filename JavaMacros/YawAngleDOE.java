
import star.base.report.Report;
import star.common.*;
import star.meshing.*;
import star.surfacewrapper.SurfaceWrapperAutoMeshOperation;
import star.vis.Scene;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.concurrent.TimeUnit;

public class YawAngleDOE extends StarMacro {

    int currentSim = 1;
    ArrayList<Double> yawAngles = new ArrayList<>(
            Arrays.asList(15.0, 12.5, 10.0, 7.5, 5.0, 2.5, 0.0));

    @Override
    public void execute() {
        Simulation sim = getActiveSimulation();
        String baseDir = sim.getSessionDir();
        String simName = sim.getPresentationName();

        try {
            for (Double yawAngle : yawAngles) {
                try {
                    long startTotalTime = System.nanoTime(); // will measure the total time taken of the sim
                    updateSimParameters(sim, yawAngle);

                    if (!updateMesh(sim)) { // runs meshing pipeline, catches errors
                        System.out.println("Fatal Mesh Error\nSkipping to next iteration");
                        saveScenes(sim, yawAngle, baseDir, simName);
                        continue;
                    }

                    long iterationStartTime = System.nanoTime();
                    sim.getSimulationIterator().run();
                    long iterationEndTime = System.nanoTime();
                    long iterationElapsedTime = iterationEndTime - iterationStartTime;
                    System.out.println("Iteration Time Take: "
                            + TimeUnit.MINUTES.convert((iterationElapsedTime), TimeUnit.NANOSECONDS));
                    saveScenes(sim, yawAngle, baseDir, simName);
                    long endTotal = System.nanoTime();
                    long totalElapsed = endTotal - startTotalTime;
                    System.out.println(
                            "Total Time Taken: " + TimeUnit.MINUTES.convert(totalElapsed, TimeUnit.NANOSECONDS));
                    currentSim += 1;
                } catch (Exception e) {
                    e.printStackTrace();
                    System.out.println("It is broken but probably not my fault");
                    saveScenes(sim, yawAngle, baseDir, simName);
                    sim.saveState(simName + "_failed" + yawAngle);
                }

            }

        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("It is broken but probably not my fault");
        }
    }

    public void updateSimParameters(Simulation sim, Double yawAngle) {

        ScalarGlobalParameter chassisAngleParam = ((ScalarGlobalParameter) sim.get(GlobalParameterManager.class)
                .getObject("crosswindAngle"));
        Units angleUnits = ((Units) sim.getUnitsManager().getObject("deg"));
        chassisAngleParam.getQuantity().setValueAndUnits(yawAngle, angleUnits);

        System.out.println(chassisAngleParam.getQuantity().toString()); // validates inputs are correct
    }

    public boolean updateMesh(Simulation sim) {
        try {
            long meshStartTime = System.nanoTime();
            MeshPipelineController mesh = sim.get(MeshPipelineController.class);
            mesh.clearGeneratedMeshes();

            sim.get(MeshOperationManager.class).executeAll();

            long meshEndTime = System.nanoTime();
            long meshElapsedTime = meshEndTime - meshStartTime;
            System.out
                    .println("Mesh pipeline time: " + TimeUnit.MINUTES.convert(meshElapsedTime, TimeUnit.NANOSECONDS));
        } catch (Exception e) { // catches fatal mesh errors
            e.printStackTrace();
            return false;
        }
        return true;
    }

    public void saveScenes(Simulation sim, double yawAngle, String baseDir, String simName) {

        // String baseDir = sim.getSessionDir(); //get the name of the simulation's
        // directory
        String sep = System.getProperty("file.separator"); // get the right separator for your operative system
        String currentDir = baseDir + sep + currentSim + sep;
        BufferedWriter bwout;

        try {
            File currentSimDir = new File(currentDir);
            if (!currentSimDir.exists()) {
                currentSimDir.mkdirs();
            }
            sim.saveState(currentDir + currentSim + "_" + simName + ".sim");
        } catch (Exception e) {
            e.printStackTrace();
        }

        try {

            bwout = new BufferedWriter(
                    new FileWriter(resolvePath("batch_" + currentSim + "_" + simName + "_Report.csv")));
            Collection<Report> reportCollection = sim.getReportManager().getObjects();

            for (Report thisReport : reportCollection) {
                bwout.write(thisReport.getPresentationName() + ",");
            }

            bwout.write("Yaw Angle,");

            bwout.write("\n");

            for (Report thisReport : reportCollection) {

                String fieldLocationName = thisReport.getPresentationName();
                Double fieldValue = thisReport.getReportMonitorValue();
                String fieldUnits = thisReport.getUnits().toString();

                // Printing to chek in output window
                sim.println("Field Location :" + fieldLocationName);
                sim.println(" Field Value :" + fieldValue);
                sim.println(" Field Units :" + fieldUnits);
                sim.println("");

                // Write Output file as "sim file name"+report.csv
                bwout.write(fieldValue + ",");

            }
            bwout.write(yawAngle + ",");

            bwout.close();

        } catch (IOException iOException) {
            iOException.printStackTrace();
        }

        for (Scene scn : sim.getSceneManager().getScenes()) {
            sim.println("Saving Scene: " + scn.getPresentationName());
            scn.printAndWait(resolvePath(currentDir + scn.getPresentationName() + ".jpg"), 1, 1920, 1080);
        }

        for (StarPlot plt : sim.getPlotManager().getObjects()) {
            sim.println("Saving Plot: " + plt.getPresentationName());
            plt.encode(resolvePath(currentDir + plt.getPresentationName() + ".jpg"), "jpg", 1920, 1080);
        }

    }

    public static void main() { // can use for testing and validating input

    }
}
