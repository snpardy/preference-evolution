package com.snpardy.paramless.mutation;

import com.snpardy.paramless.utility.UtilitySurface;

import java.util.concurrent.ThreadLocalRandom;

public class GaussianMutation implements Mutation {
  
  private static final double e = Math.E;
  private static final double pointFive = 0.5;
  
  private double mutationEpsilon;
  private double radius;
  private int maxIterations=1000000;
  private double lowerBound;
  private double upperBound;
  private boolean boundsSet;
  
  // CONSTRUCTORS
  public GaussianMutation(double mutationEpsilon, double radius, int maxIterations,
                          int lowerBound, int upperBound){
    this.mutationEpsilon = mutationEpsilon;
    this.radius = radius;
    this.maxIterations = maxIterations;
    this.lowerBound = lowerBound;
    this.upperBound = upperBound;
    this.boundsSet = true;
  }
  
  public GaussianMutation(double mutationEpsilon, double radius,
                          int lowerBound, int upperBound){
    this.mutationEpsilon = mutationEpsilon;
    this.radius = radius;
    this.lowerBound = lowerBound;
    this.upperBound = upperBound;
    this.boundsSet = true;
  }
  
  public GaussianMutation(double mutationEpsilon, double radius) {
    this.mutationEpsilon = mutationEpsilon;
    this.radius = radius;
    this.boundsSet = false;
  }
  
  
//  MAIN MUTATION METHOD
  @Override
  public UtilitySurface mutate(UtilitySurface resident) {
    boolean successful;
    int attempt = 0;
    UtilitySurface mutant = attemptMutation(resident);
    if (boundsSet) {
      successful = withinBounds(mutant.getUtilityGrid());
      while (!successful) {
        mutant = attemptMutation(resident);
        successful = withinBounds(mutant.getUtilityGrid());
        attempt++;
        if (attempt > maxIterations) {
          throw new RuntimeException("Too many mutation attmepts without a successful attempt");
        }
      }
  
  
    }
    return mutant;
  }
  
// HELPER METHODS
  
  /**
   * Actually performs the gaussian mutation.
   * @param resident
   * @return a new UtilitySurface with the grid mutated a little.
   */
  private UtilitySurface attemptMutation(UtilitySurface resident){
    // @TODO implement mutation here
    // Randomly select x and y value
    // Create grid of perterbation
    // combine to grids (+ or -)
    // return new grid
  
    double[] x_array = resident.getX();
    double[] y_array = resident.getY();
    
    
    double x_mean = x_array[ThreadLocalRandom.current().nextInt(0,
        x_array.length)];
    double y_mean = y_array[ThreadLocalRandom.current().nextInt(0,
        y_array.length)];
    double variance = radius * Math.random();
    
    double[][] perturbation = bivariateNormalMutation(x_array, y_array, x_mean, y_mean,
        variance);
    
    if(Math.random() > 0.5){
      // Upwards
      return resident.addToGrid(perturbation);
    } else {
      // Downwards
      return resident.subFromGrid(perturbation);
    }
  }
  
  /**
   * Returns a grid with the same dimensions as resident.utilityGrid.
   * This new grid represents a bivariate normal distribution based on the given x_mean, y_mean and
   * variance.
   *
   * @param x_array : the values corresponding to 'x-axis' of the generated grid.
   * @param y_array : the values corresponding to 'y-axis' of the generated grid.
   * @param x_mean : a value (usually from the x_array) that represents the mean along that axis.
   * @param y_mean : a value (usually from the y_array) that represents the mean along that axis.
   * @param variance : the 'width' of the distribution.
   * @return double[][] : a grid that represents the z values of a bivariate normal distribution.
   */
  private double[][] bivariateNormalMutation(double[] x_array, double[] y_array, double x_mean,
                                                 double y_mean, double variance){
    
    double x_value;
    
    double[][] perturbation = new double[x_array.length][y_array.length];
    for(int i = 0; i< perturbation.length; i++){
      // calculating the x value out here as it only changes when i changes
      x_value = Math.pow((x_array[i] - (x_mean)),(2))/Math.pow(variance,2);
      for(int j = 0; j < perturbation[i].length; j++){
        // each element is set using the bivariate normal distribution formula
        perturbation[i][j] = mutationEpsilon *
            Math.pow(e, (
                (pointFive * (x_value + (Math.pow((y_array[j] - (y_mean)),2)/(Math.pow(variance,2)))*(-1)))
            ));
      }
    }
   return perturbation;
  }
  
  /**
   * Checks that the {@param grid} does not breach the objects lower and upper bounds.
   * If bounds have not been set, then returns true.
   *
   * @param grid : a grid of doubles
   * @return boolean : true if {@param grid} is within bounds, false otherwise.
   */
  private boolean withinBounds(double[][] grid){
    if(!boundsSet){
      return true;
    } else {
      for(double[] row : grid){
        for(double value : row){
          if(value < lowerBound || value > upperBound){
            // minimum is less than lowerBound || maximum is greater than upperBound
            return false;
          }
        }
      }
      return true;
    }
  }
  
}