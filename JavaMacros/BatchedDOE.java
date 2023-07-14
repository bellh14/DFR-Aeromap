package macro;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.*;
import java.util.concurrent.TimeUnit;

import star.base.report.MinReport;
import star.base.report.Report;
import star.common.*;
import star.meshing.*;
import star.surfacewrapper.SurfaceWrapperAutoMeshOperation;
import star.vis.Scene;

public class BatchedDOE extends StarMacro{

    final double CHASSIS_ANGLE_MIN = -1.8131;
    final double CHASSIS_ANGLE_MAX = 0.8076;
    final int NUM_CHASSIS_ANGLES = 36;
    int currentSim = 2;
    int simNum = 1;
    int batchNum = 1;
    int currentBatch = 1; // used to skip already completed batches, start at 1
    int simsPerBatch = 6;
    double chassisHeave = -0.1429; // change for each new batch
//    ArrayList<Double> chassisAngles = new ArrayList<>(
//            Arrays.asList(0.8076, 0.4332, 0.0588, -0.3156, -0.6899, -1.0643, -1.4387));
    ArrayList<Double> chassisAngles = calculateChassisAngles();
    //-0.1429, 0.1429, 0.4286, 0.7143, 1.000


    @Override
    public void execute(){
        Simulation sim = getActiveSimulation();
        String baseDir = sim.getSessionDir();
        String simName = sim.getPresentationName();

        try {

            for(Double chassisAngle : chassisAngles){
                try {
                    if (currentBatch < (simsPerBatch * (batchNum - 1)) + 1) {
                        currentBatch += 1;
                        continue;
                    }
                    if(currentSim > simNum){
                        simNum += 1;
                        continue;
                    }
                    long startTotalTime = System.nanoTime(); // will measure the total time taken of the sim
                    System.out.println(chassisAngle);
                    updateSimParameters(sim, chassisAngle);
                    if (!checkKnownOutOfBounds(chassisAngle)) {
                        System.out.println(chassisAngle + "\n" + chassisHeave);
                        System.out.println("Previously known out of bounds so skipping");
                        saveScenes(sim, chassisAngle, chassisHeave, baseDir, simName);
                        currentSim += 1;
                        continue;
                    } else {

                        if (!updateMesh(sim)) { // runs meshing pipeline, catches errors
                            System.out.println("Fatal Mesh Error\nSkipping to next iteration");
                            continue;
                        }

                        long iterationStartTime = System.nanoTime();
                        sim.getSimulationIterator().run();
                        long iterationEndTime = System.nanoTime();
                        long iterationElapsedTime = iterationEndTime - iterationStartTime;
                        System.out.println("Iteration Time Take: " + TimeUnit.MINUTES.convert((iterationElapsedTime), TimeUnit.NANOSECONDS));
                        saveScenes(sim, chassisAngle, chassisHeave, baseDir, simName);
                        long endTotal = System.nanoTime();
                        long totalElapsed = endTotal - startTotalTime;
                        System.out.println("Total Time Taken: " + TimeUnit.MINUTES.convert(totalElapsed, TimeUnit.NANOSECONDS));
                        currentSim += 1;
                    }
                }catch (Exception e){
                    e.printStackTrace();
                    System.out.println("It is broken but probably not my fault");
                }
            }

        }catch (Exception e){
            e.printStackTrace();
            System.out.println("It is broken but probably not my fault");
        }
    }

    public ArrayList<Double> calculateChassisAngles(){
        //chassis_angle = np.round(self.CHASSIS_ANGLE_MIN + (j * angle_increment), 5)
        //angle_increment = (self.CHASSIS_ANGLE_MAX + abs(self.CHASSIS_ANGLE_MIN)) / (num_angles - 1)
        double angleIncrement = (CHASSIS_ANGLE_MAX + Math.abs(CHASSIS_ANGLE_MIN)) / (NUM_CHASSIS_ANGLES - 1);
        ArrayList<Double> angles = new ArrayList<>();
        double nextAngle = 0.0;
        for(int i = 0; i < NUM_CHASSIS_ANGLES; i++){
            nextAngle = (double) Math.round((CHASSIS_ANGLE_MIN + (i * angleIncrement)) * 10000) / 10000;
            //System.out.println(nextAngle); // for debugging insurance
            angles.add(nextAngle);
        }
        return angles;
    }

    public void updateSimParameters(Simulation sim, Double chassisAngle){

        ScalarGlobalParameter chassisAngleParam = ((ScalarGlobalParameter)
                sim.get(GlobalParameterManager.class).getObject("Chassis Angle"));
        Units angleUnits = ((Units) sim.getUnitsManager().getObject("deg"));
        chassisAngleParam.getQuantity().setValueAndUnits(chassisAngle, angleUnits);

        ScalarGlobalParameter chassisHeaveScalar = ((ScalarGlobalParameter)
                sim.get(GlobalParameterManager.class).getObject("chassisHeaveScalar"));
        Units chassisHeaveUnits = ((Units) sim.getUnitsManager().getObject("in"));
        chassisHeaveScalar.getQuantity().setValueAndUnits(chassisHeave, chassisHeaveUnits);

        System.out.println(chassisAngleParam.getQuantity().toString()); // validates inputs are correct
        System.out.println(chassisHeaveScalar.getQuantity().toString());
    }

    public boolean updateMesh(Simulation sim){
        try{
            long meshStartTime = System.nanoTime();
            MeshPipelineController mesh = sim.get(MeshPipelineController.class);
            mesh.clearGeneratedMeshes();

            TransformPartsOperation chassisAngle =
                    ((TransformPartsOperation) sim.get(MeshOperationManager.class).getObject("Chassis Angle"));
            chassisAngle.execute();

            TransformPartsOperation chassisHeave =
                    ((TransformPartsOperation) sim.get(MeshOperationManager.class).getObject("Chassis Heave"));
            chassisHeave.execute();

            SubtractPartsOperation subtractPartsOperation =
                    ((SubtractPartsOperation) sim.get(MeshOperationManager.class).getObject("Subtract"));
            subtractPartsOperation.execute();

            SurfaceWrapperAutoMeshOperation surfaceWrapper =
                    ((SurfaceWrapperAutoMeshOperation) sim.get(MeshOperationManager.class).getObject("Surface Wrapper"));
            surfaceWrapper.execute();

            if(!checkBounds(sim)){
                System.out.println("Signed Distance is negative");
                return false;
            }

            AutoMeshOperation fluidDomainMesh =
                    ((AutoMeshOperation) sim.get(MeshOperationManager.class).getObject("Fluid Domain Mesh"));
            fluidDomainMesh.execute();

            AutoMeshOperation radiatorMesh =
                    ((AutoMeshOperation) sim.get(MeshOperationManager.class).getObject("Radiator Mesh"));
            radiatorMesh.execute();

            long meshEndTime = System.nanoTime();
            long meshElapsedTime = meshEndTime - meshStartTime;
            System.out.println("Mesh pipeline time: " + TimeUnit.MINUTES.convert(meshElapsedTime, TimeUnit.NANOSECONDS));
        }catch (Exception e){ // catches fatal mesh errors
            e.printStackTrace();
            return false;
        }
        return true;
    }

    public boolean checkBounds(Simulation sim){
        MinReport minReport = ((MinReport) sim.getReportManager().getReport("signedDistance"));
        try{
            if(minReport.getValue() < 0){
                minReport.printReport();
                return false;
            }
        }catch (NullPointerException e){
            return false;
        }
        return true;
    }

    public boolean checkKnownOutOfBounds(Double chassisAngle){
        if(chassisAngle < -0.8 && chassisHeave == -1.0){
            System.out.println(chassisAngle + "\n" + chassisHeave);
            return false;
        }else if(chassisAngle < -1.4 && chassisHeave < -0.5){
            System.out.println(chassisAngle + "\n" + chassisHeave);
            return false;
        }

        return true;
    }

    public void saveScenes(Simulation sim, double chassisAngle, double chassisHeave, String baseDir, String simName){

        //String baseDir = sim.getSessionDir(); //get the name of the simulation's directory
        String sep = System.getProperty("file.separator"); //get the right separator for your operative system
        String currentDir = baseDir + sep + currentSim + sep;
        BufferedWriter bwout;

        try{
            File currentSimDir = new File(currentDir);
            if(!currentSimDir.exists()){
                currentSimDir.mkdirs();
            }
            sim.saveState(currentDir + "batch_" + batchNum + "_" + currentSim + "_" + simName + ".sim");
        }catch (Exception e){
            e.printStackTrace();
        }

        try{

            bwout = new BufferedWriter(new FileWriter
                    (resolvePath("batch_" + batchNum + "_" + currentSim + "_" + simName + "_Report.csv")));
            Collection<Report> reportCollection = sim.getReportManager().getObjects();

            for (Report thisReport : reportCollection){
                bwout.write(thisReport.getPresentationName() +",");
            }

            bwout.write("Chassis Angle,");
            bwout.write("Chassis Heave,");

            bwout.write("\n");

            for (Report thisReport : reportCollection){

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
            bwout.write(chassisAngle + ",");
            bwout.write(chassisHeave + ",");

            bwout.close();

        } catch (IOException iOException) {
            iOException.printStackTrace();
        }

        for (Scene scn: sim.getSceneManager().getScenes()) {
            sim.println("Saving Scene: " + scn.getPresentationName());
            scn.printAndWait(resolvePath(currentDir + scn.getPresentationName() + ".jpg"), 1, 1920, 1080);
        }


        for (StarPlot plt : sim.getPlotManager().getObjects()) {
            sim.println("Saving Plot: " + plt.getPresentationName());
            plt.encode(resolvePath(currentDir + plt.getPresentationName() + ".jpg"), "jpg", 1920, 1080);
        }

    }

    public static void main(){ // can use for testing and validating input

    }
}
