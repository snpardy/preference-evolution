package com.snpardy.paramless.fitness;

import com.snpardy.paramless.utility.UtilitySurface;

import java.math.BigDecimal;
import java.util.ArrayList;

public interface Fitness {
  

  BigDecimal[] evaluate(UtilitySurface resident, UtilitySurface mutant, BigDecimal tolerance);
  
  ArrayList<Float> getFitnessArray();
  
}
