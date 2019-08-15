package com.snpardy.paramless.utility;

import java.math.BigDecimal;


/**
 * An immutable class representing a two parameter utility surface and the array of parameter
 * values that correspond to each point in the surface. *
 * e.g The utility at point utilityGrid[i][j] is the result of some combination of x[i] and y[j]
 */
public class UtilitySurface {
  
  // step must be the difference between each element in the x & y arrays
  private BigDecimal step;
  private final BigDecimal[] x;
  private final BigDecimal[] y;
  private final BigDecimal[][] utilityGrid;
  
  public UtilitySurface(BigDecimal[] x, BigDecimal[] y, BigDecimal[][] utilityGrid, BigDecimal step) {
    this.x = x;
    this.y = y;
    this.utilityGrid = utilityGrid;
    this.step = step;
  }
  
  public static UtilitySurface selfless(int size, BigDecimal step) {
    
    BigDecimal[] x = new BigDecimal[size];
    BigDecimal[] y = new BigDecimal[size];
    BigDecimal[][] grid = new BigDecimal[size][size];
    
    for (int i = 0; i < size; i++) {
      x[i] = BigDecimal.valueOf(i);
      y[i] = BigDecimal.valueOf(i);
      for (int j = 0; j < size; j++) {
        grid[i][j] = BigDecimal.valueOf(i);
      }
    }
    return new UtilitySurface(x, y, grid, step);
  }
  
  public static UtilitySurface selfish(int size, BigDecimal step) {
    BigDecimal[] x = new BigDecimal[size];
    BigDecimal[] y = new BigDecimal[size];
    BigDecimal[][] grid = new BigDecimal[size][size];
    for (int i = 0; i < size; i++) {
      x[i] = BigDecimal.valueOf(i);
      y[i] = BigDecimal.valueOf(i);
      for (int j = 0; j < size; j++) {
        grid[i][j] = BigDecimal.valueOf(i);
      }
    }
    return new UtilitySurface(x, y, grid, step);
  }
  
  public static UtilitySurface random(int size, BigDecimal step){
    BigDecimal x[] = new BigDecimal[size];
    BigDecimal y[] = new BigDecimal[size];
    BigDecimal grid[][] = new BigDecimal[size][size];
  
    for (int i = 0; i < size; i++) {
      x[i] = BigDecimal.valueOf(i);
      y[i] = BigDecimal.valueOf(i);
      for (int j = 0; j < size; j++) {
        grid[i][j] = BigDecimal.valueOf(Math.random()*size);
      }
    }
    return new UtilitySurface(x, y, grid, step);
  }
  
  /**
   * Create a new UtilitySurface with a different utility grid.
   *
   * @param newGrid : a BigDecimal[][]
   * @return new UtilitySurface with {@param newGrid} in place of this.utilityGrid.
   */
  public UtilitySurface replaceGrid(BigDecimal[][] newGrid) {
    return new UtilitySurface(getX(), getY(), newGrid, getStep());
  }
  
  /**
   * Add two utilityGrids together, returns a new UtilitySurface without modifying the old one
   *
   * @param otherGrid : another BigDecimal[][] of the same dimensions as this.utilityGrid.
   * @return UtilitySurface : creates a new surface with a utility grid made of
   * {@param otherGrid} added {this.UtilityGrid}
   */
  public UtilitySurface addToGrid(BigDecimal[][] otherGrid) {
    BigDecimal[][] newGrid = new BigDecimal[x.length][y.length];
    for (int i = 0; i < getX().length; i++) {
      for (int j = 0; j < getY().length; j++) {
        newGrid[i][j] = getUtilityGrid()[i][j].add(otherGrid[i][j]);
      }
    }
    return new UtilitySurface(getX(), getY(), newGrid, getStep());
  }
  
  /**
   * Subtract {@param otherGrid} from this.utilityGrid.
   * Creates a new grid, does not alter original.
   *
   * @param otherGrid : another BigDecimal[][] of the same dimensions as this.utilityGrid.
   * @return UtilitySurface : creates a new surface with a utility grid made of
   * {@param otherGrid} subtracted from {this.UtilityGrid}.
   */
  public UtilitySurface subFromGrid(BigDecimal[][] otherGrid) {
    BigDecimal[][] newGrid = new BigDecimal[x.length][y.length];
    for (int i = 0; i < x.length; i++) {
      for (int j = 0; j < y.length; j++) {
        newGrid[i][j] = utilityGrid[i][j].subtract(otherGrid[i][j]);
      }
    }
    return new UtilitySurface(getX(), getY(), newGrid, getStep());
  }
  
  /**
   * Converts the given payoffs to the nearest grid index and returns the corresponding utility.
   *
   * @param x_i : the x payoff (usually the resident)
   * @param y_i : the y payoff (usually the mutant)
   * @return BigDecimal payoff at x_i, y_i.
   */
  public BigDecimal getUtilityAtPayoff(BigDecimal x_i, BigDecimal y_i){
    int x_index = x_i.divideToIntegralValue(step).intValue();
    int y_index = y_i.divideToIntegralValue(step).intValue();
    return getGridValueAt(x_index, y_index);
    
  }
  
  
  /** BASIC GETTERS**/
  
  
  // These three getters are a memory leak and so break the immutability of the class
  // but defensively copying will affect performance.
  public BigDecimal[] getX() {
    return x;
  }
  
  public BigDecimal[] getY() {
    return y;
  }
  
  public BigDecimal[][] getUtilityGrid() {
    return utilityGrid;
  }
  
  // This one is ok because it indexes the grid directly.
  public BigDecimal getGridValueAt(int x_i, int y_j) {
    return utilityGrid[x_i][y_j];
  }
  
  public BigDecimal getStep() {
    return this.step;
  }

  
  
}
