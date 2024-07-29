
import star.base.report.Report;
import star.common.*;
import star.meshing.*;
import star.surfacewrapper.SurfaceWrapperAutoMeshOperation;
import star.vis.Scene;
import star.base.neo.*;
import star.cadmodeler.*;

import java.io.BufferedWriter;
import java.io.BufferedReader;
import java.io.File;
import java.io.FileWriter;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.concurrent.TimeUnit;

public class AeroMap extends StarMacro {

    Double chassisAngle = 0.0;
    Double chassisHeave = 1.0;
    static final int MAX_ITERATIONS = 10;
    @Override
    public void execute() {
        Simulation sim = getActiveSimulation();
        String baseDir = sim.getSessionDir();
        String simName = sim.getPresentationName();
        

        try {
            long startTotalTime = System.nanoTime();
            ReadCSVInputs(resolvePath("InputParams.csv"));
            updateSimParameters(sim);

            if (!updateMesh(sim)) {
                System.out.println("Fatal Mesh Error");
            }

            long iterationStartTime = System.nanoTime();
            sim.getSimulationIterator().run(MAX_ITERATIONS);

            long iterationEndTime = System.nanoTime();
            long iterationElapsedTime = iterationEndTime - iterationStartTime;
            System.out.println("Iteration Time Take: "
                    + TimeUnit.SECONDS.convert((iterationElapsedTime), TimeUnit.NANOSECONDS));
            saveScenes(sim, baseDir, simName);

            if (sim.getSimulationIterator().getCurrentIteration() != MAX_ITERATIONS) {
                System.out.println("Simulation did not reach max iterations");
                System.exit(4);
            }

            long endTotal = System.nanoTime();
            long totalElapsed = endTotal - startTotalTime;
            System.out.println("Total Time Taken: " + TimeUnit.SECONDS.convert(totalElapsed, TimeUnit.NANOSECONDS));
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("It is broken but probably not my fault");
            saveScenes(sim, baseDir, simName);
            System.exit(5);
        }
            
    

    }

    public void updateSimParameters(Simulation sim) {
        System.out.println("Updating sim parameters");
        System.out.println("Chassis Angle: " + chassisAngle);
        System.out.println("Chassis Heave: " + chassisHeave);
        
        ScalarGlobalParameter chassisAngleParam = ((ScalarGlobalParameter) sim.get(GlobalParameterManager.class)
                .getObject("Chassis Angle"));
        Units angleUnits = ((Units) sim.getUnitsManager().getObject("deg"));
        chassisAngleParam.getQuantity().setValueAndUnits(chassisAngle, angleUnits);

        ScalarGlobalParameter chassisHeaveScalar = ((ScalarGlobalParameter) sim.get(GlobalParameterManager.class)
                .getObject("chassisHeaveScalar"));
        Units chassisHeaveUnits = ((Units) sim.getUnitsManager().getObject("in"));
        chassisHeaveScalar.getQuantity().setValueAndUnits(chassisHeave, chassisHeaveUnits);

        System.out.println("Chassis Angle: " + chassisAngle);
        System.out.println("Heave: " + chassisHeave);
        

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
                    .println("Mesh pipeline time: " + TimeUnit.SECONDS.convert(meshElapsedTime, TimeUnit.NANOSECONDS));
        } catch (Exception e) { // catches fatal mesh errors
            e.printStackTrace();
            System.exit(2);
            return false;
        }
        return true;
    }

    public void saveScenes(Simulation sim, String baseDir, String simName) {

        String sep = System.getProperty("file.separator");
        String currentDir = baseDir + sep;
        BufferedWriter bwout;

        try {
            File currentSimDir = new File(currentDir);
            if (!currentSimDir.exists()) {
                currentSimDir.mkdirs();
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.exit(3);
        }

        try {

            bwout = new BufferedWriter(
                    new FileWriter(resolvePath(simName + "_Report.csv")));
            Collection<Report> reportCollection = sim.getReportManager().getObjects();

            for (Report thisReport : reportCollection) {
                bwout.write(thisReport.getPresentationName() + ",");
            }

            bwout.write("ChassisAngle,ChassisHeave");

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
            bwout.write(chassisAngle + "," +chassisHeave);

            bwout.close();

             for (Scene scn : sim.getSceneManager().getScenes()) {
                 sim.println("Saving Scene: " + scn.getPresentationName());
                 scn.printAndWait(resolvePath(currentDir + scn.getPresentationName() + ".jpg"), 1, 1920, 1080);
             }

             for (StarPlot plt : sim.getPlotManager().getObjects()) {
                 sim.println("Saving Plot: " + plt.getPresentationName());
                 plt.encode(resolvePath(currentDir + plt.getPresentationName() + ".jpg"), "jpg", 1920, 1080);
            }

        } catch (IOException iOException) {
            iOException.printStackTrace();
            System.exit(3);
        }

    }

    public void ReadCSVInputs(String fileName) {
        String line = "";
        try {
            BufferedReader br = new BufferedReader(new FileReader(fileName));
            br.readLine();
            while ((line = br.readLine()) != null) {
                String[] values = line.split(",");
                chassisAngle = Double.parseDouble(values[0]);
                chassisHeave = Double.parseDouble(values[1]);
                System.out.println(values[0]);
                System.out.println(values[1]);
            }
        } catch (IOException e) {
            e.printStackTrace();
            System.exit(1);
        }
    }
}
