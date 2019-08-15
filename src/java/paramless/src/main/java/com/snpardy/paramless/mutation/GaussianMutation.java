package com.snpardy.paramless.mutation;

import com.snpardy.paramless.utility.UtilitySurface;

import java.math.BigDecimal;
import java.util.concurrent.ThreadLocalRandom;

public class GaussianMutation implements Mutation {
  
  private static final double e = Math.E;
  private static final BigDecimal pointFive = BigDecimal.valueOf(.5);
  
  private double mutationEpsilon;
  private BigDecimal radius;
  private int maxIterations=1000000;
  private BigDecimal lowerBound;
  private BigDecimal upperBound;
  private boolean boundsSet;
  
  // CONSTRUCTORS
  public GaussianMutation(BigDecimal mutationEpsilon, BigDecimal radius, int maxIterations,
                          int lowerBound, int upperBound){
    this.mutationEpsilon = mutationEpsilon.doubleValue();
    this.radius = radius;
    this.maxIterations = maxIterations;
    this.lowerBound = BigDecimal.valueOf(lowerBound);
    this.upperBound = BigDecimal.valueOf(upperBound);
    this.boundsSet = true;
  }
  
  public GaussianMutation(BigDecimal mutationEpsilon, BigDecimal radius,
                          int lowerBound, int upperBound){
    this.mutationEpsilon = mutationEpsilon.doubleValue();
    this.radius = radius;
    this.lowerBound = BigDecimal.valueOf(lowerBound);
    this.upperBound = BigDecimal.valueOf(upperBound);
    this.boundsSet = true;
  }
  
  public GaussianMutation(BigDecimal mutationEpsilon, BigDecimal radius) {
    this.mutationEpsilon = mutationEpsilon.doubleValue();
    this.radius = radius;
    this.boundsSet = false;
  }
  
  
//  MAIN MUTATION METHOD
  @Override
  public UtilitySurface mutate(UtilitySurface resident) {
    boolean successful = false;
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
  private UtilitySurface attemptMutation(UtilitySurface resident){
    // @TODO implement mutation here
    // Randomly select x and y value
    // Create grid of perterbation
    // combine to grids (+ or -)
    // return new grid
  
    BigDecimal[] x_array = resident.getX();
    BigDecimal[] y_array = resident.getY();
    
    
    BigDecimal x_mean = x_array[ThreadLocalRandom.current().nextInt(0,
        x_array.length)];
    BigDecimal y_mean = y_array[ThreadLocalRandom.current().nextInt(0,
        y_array.length)];
    BigDecimal variance = radius.multiply(BigDecimal.valueOf(Math.random()));
    
    BigDecimal[][] perturbation = bivariateNormalMutation(x_array, y_array, x_mean, y_mean,
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
   * @param x_array
   * @param y_array
   * @param x_mean
   * @param y_mean
   * @param variance
   * @return
   */
  private BigDecimal[][] bivariateNormalMutation(BigDecimal[] x_array, BigDecimal[] y_array, BigDecimal x_mean,
                                                 BigDecimal y_mean, BigDecimal variance){
    
    BigDecimal x_value;
    
    BigDecimal[][] perturbation = new BigDecimal[x_array.length][y_array.length];
    for(int i = 0; i< perturbation.length; i++){
      // calculating the x value out here as it only changes when i changes
      x_value = (((x_array[i].subtract(x_mean)).pow(2)).divide(variance.pow(2)));
      for(int j = 0; j < perturbation[i].length; j++){
        // each element is set using the bivariate normal distribution formula
        perturbation[i][j] = BigDecimal.valueOf(mutationEpsilon * (
            Math.pow(e, (
                (pointFive.multiply(
                    x_value.add(
                            // y_value
                            (((y_array[j].subtract(y_mean)).pow(2)).divide(variance.pow(2)))
                        ))
          
                ).negate()).doubleValue()
            )));
      }
    }
   return perturbation;
  }
  
  /**
   * Checks that the {@param grid} does not breach the objects lower and upper bounds.
   * If bounds have not been set, then returns true.
   *
   * @param grid : a grid of BigDecimals
   * @return boolean : true if {@param grid} is within bounds, false otherwise.
   */
  private boolean withinBounds(BigDecimal[][] grid){
    if(!boundsSet){
      return true;
    } else {
      for(BigDecimal[] row : grid){
        for(BigDecimal value : row){
          if((value.compareTo(lowerBound) < 0) || (value.compareTo(upperBound) > 0 ) ) {
            // minimum is less than lowerBound || maximum is greater than upperBound
            return false;
          }
        }
      }
      return true;
    }
  }
}