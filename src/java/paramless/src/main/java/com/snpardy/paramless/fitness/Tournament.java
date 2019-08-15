package com.snpardy.paramless.fitness;

import com.snpardy.paramless.utility.UtilitySurface;

public class Tournament {
  
  private int rounds;
  private int max_payoff;
  private UtilitySurface resident;
  private UtilitySurface mutant;
  
  public Tournament(int rounds, int max_payoff, UtilitySurface resident, UtilitySurface mutant) {
    this.rounds = rounds;
    this.max_payoff = max_payoff;
    this.resident = resident;
    this.mutant = mutant;
  }
  
  public int[] evaluate(){
    
    int[] fitnessArray = new int[2];
    // Position zero is resident fitness
    // position one is mutant fitness
    
    for(int i=0; i < rounds; i++){
    // Tournament loop
    }
  
    
  }
  
  
  
  public int getRounds() {
    return rounds;
  }
  
  public void setRounds(int rounds) {
    this.rounds = rounds;
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
