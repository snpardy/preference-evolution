package com.snpardy.paramless;

import com.snpardy.paramless.fitness.Fitness;
import com.snpardy.paramless.mutation.Mutation;
import com.snpardy.paramless.utility.UtilitySurface;


import java.math.BigDecimal;
import java.util.ArrayList;

/**
 * A class to represent to configure and run evolution on UtilitySurface objects.
 * Will operate differently depending on what kind of Fitness and Mutation objects are passed as
 * parameters.
 */
public class Evolution {
  
  public static final BigDecimal DEFAULT_ATOL = BigDecimal.valueOf(1e-8);
  public static final int MAX_ITERATIONS = 1000000;
  
  private UtilitySurface initial;
  private Fitness fitnessFunction;
  private Mutation mutationFunction;
  private int iterations;
  private BigDecimal tolerance;
  
//  Constructors //
  public Evolution(UtilitySurface initial, Fitness fitnessFunction, Mutation mutationFunction, int iterations) {
    this.initial = initial;
    this.fitnessFunction = fitnessFunction;
    this.mutationFunction = mutationFunction;
    this.iterations = iterations;
    this.tolerance = DEFAULT_ATOL;
  }
  
  public Evolution(UtilitySurface initial, Fitness fitnessFunction, Mutation mutationFunction,
                   int iterations, BigDecimal tolerance) {
    this.initial = initial;
    this.fitnessFunction = fitnessFunction;
    this.mutationFunction = mutationFunction;
    this.iterations = iterations;
    this.tolerance = tolerance;
  }
  
  
//  Evolution functions //
  
  /**
   *
   * @return ArrayList<UtilitySurface> containing all UtilitySurfaces that were residents at some
   * point in the evolution run.
   * The last element in the array is the final resident. The first element is the initial.
   * Subtract 1 from the length of the array  for the number of successful invasions.
   */
  public ArrayList<UtilitySurface> run(){
    
    UtilitySurface resident = getInitial();
    
    ArrayList<UtilitySurface> timeSeriesData = new ArrayList<>();
    timeSeriesData.add(resident);
  
    UtilitySurface tmp;
    
    // main loop
    for(int i = 0; i < getIterations(); i++){
      tmp = evolutionStep(resident);
      if(tmp != null){
        resident = tmp;
        timeSeriesData.add(resident);
      }
    }
    
    return timeSeriesData;
  }
  
  /**
   * A single iteration of the evolution. Mutates the resident, compares the mutation to the
   * original and returns the mutant if fitness is greater, otherwise returns null.
   * @param resident; a UtilitySurface representing the current resident utility.
   * @return new resident if an invasion occurs, otherwise null
   */
  private UtilitySurface evolutionStep(UtilitySurface resident){
    // Mutating the resident
    UtilitySurface mutant = getMutationFunction().mutate(resident);
    
    // Comparing fitness
    BigDecimal[] fitness = getFitnessFunction().evaluate(resident, mutant, getTolerance());
    
    //compareTo is weird => returns -1, 0 or 1 to mean less than, equal to or greater than.
    if(fitness[0].compareTo(fitness[1]) < 0){
      return mutant;
    }
    return null;
  }
  
  
//  Getters //
  public UtilitySurface getInitial() {
    return initial;
  }
  
  public Fitness getFitnessFunction() {
    return fitnessFunction;
  }
  
  public Mutation getMutationFunction() {
    return mutationFunction;
  }
  
  public int getIterations() {
    return iterations;
  }
  
  public BigDecimal getTolerance() {
    return tolerance;
  }
}
