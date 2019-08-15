package com.snpardy.paramless.mutation;

import com.snpardy.paramless.utility.UtilitySurface;

/**
 * Interface for a mutation function object that will perform mutations on UtilitySurface object.
 */
public interface Mutation {
  UtilitySurface mutate(UtilitySurface grid);
  
}
