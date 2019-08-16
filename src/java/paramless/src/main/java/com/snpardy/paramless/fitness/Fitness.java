package com.snpardy.paramless.fitness;

import com.snpardy.paramless.utility.UtilitySurface;

public interface Fitness {
  
  double[] evaluate(UtilitySurface resident, UtilitySurface mutant, double epsilon);
  
}
