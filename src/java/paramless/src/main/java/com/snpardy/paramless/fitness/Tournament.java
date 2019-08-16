package com.snpardy.paramless.fitness;

import com.snpardy.paramless.game.Game;
import com.snpardy.paramless.utility.UtilitySurface;

public class Tournament implements Fitness {
  
  private int rounds;
  private int min_payoff;
  private int max_payoff;
  private UtilitySurface resident;
  private UtilitySurface mutant;
  
  public Tournament(int rounds, int min_payoff, int max_payoff, UtilitySurface resident,
                    UtilitySurface mutant) {
    this.rounds = rounds;
    this.min_payoff = min_payoff;
    this.max_payoff = max_payoff;
    this.resident = resident;
    this.mutant = mutant;
  }
  
  @Override
  public double[] evaluate(UtilitySurface resident, UtilitySurface mutant, double epsilon){
  
    // Position zero is resident fitness
    // position one is mutant fitness
    double[] fitnessArray = new double[2];

    // Tournament loop
    for(int i=0; i < rounds; i++){
      // Generate a random game each time
      Game game = Game.randomTwoByTwoGame(min_payoff, max_payoff);
      
      
    }
  
   return fitnessArray;
  }
  
  
  
  public int getRounds() {
    return rounds;
  }
  
  public void setRounds(int rounds) {
    this.rounds = rounds;
  }
  
  public int getMin_payoff() {
    return min_payoff;
  }
  
  public void setMin_payoff(int min_payoff) {
    this.min_payoff = min_payoff;
  }
  
  public int getMax_payoff() {
    return max_payoff;
  }
  
  public void setMax_payoff(int max_payoff) {
    this.max_payoff = max_payoff;
  }
  
  public UtilitySurface getResident() {
    return resident;
  }
  
  public void setResident(UtilitySurface resident) {
    this.resident = resident;
  }
  
  public UtilitySurface getMutant() {
    return mutant;
  }
  
  public void setMutant(UtilitySurface mutant) {
    this.mutant = mutant;
  }
}
