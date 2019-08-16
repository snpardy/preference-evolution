package com.snpardy.paramless.utility;


/**
 * An immutable class representing a two parameter utility surface and the array of parameter
 * values that correspond to each point in the surface. *
 * e.g The utility at point utilityGrid[i][j] is the result of some combination of x[i] and y[j]
 */
public class UtilitySurface {
  
  // step must be the difference between each element in the x & y arrays
  private double step;
  private final double[] x;
  private final double[] y;
  private final double[][] utilityGrid;
  
  public UtilitySurface(double[] x, double[] y, double[][] utilityGrid, double step) {
    this.x = x;
    this.y = y;
    this.utilityGrid = utilityGrid;
    this.step = step;
  }
  
  /*  STATIC FACTORY METHODS  */
  public static UtilitySurface selfish(int min, int max, double step) {
    
    int len = (int)Math.floor((max-min)/step);
    
    double[] x = new double[len];
    double[] y = new double[len];
    double[][] grid = new double[len][len];
    
    double current = min;
    
    for (int i = 0; i < len; i++) {
      x[i] = current;
      y[i] = current;
      for (int j = 0; j < len; j++) {
        grid[i][j] = current;
      }
      current += step;
    }
    return new UtilitySurface(x, y, grid, step);
  }
  
  public static UtilitySurface selfless(int min, int max, double step) {
    
    int len = (int)Math.floor((max-min)/step);
    
    double[] x = new double[len];
    double[] y = new double[len];
    double[][] grid = new double[len][len];
    
    double current = min;
    
    for (int i = 0; i < len; i++) {
      x[i] = current;
      y[i] = current;
      for (int j = 0; j < len; j++) {
        grid[j][i] = current;
      }
      current += step;
    }
    return new UtilitySurface(x, y, grid, step);
  }
  
  public static UtilitySurface random(int min, int max, double step){
  
    int len = (int)Math.floor((max-min)/step);
    
    double[] x = new double[len];
    double[] y = new double[len];
    double[][] grid = new double[len][len];
    
    double current = min;
    for (int i = 0; i < len; i++) {
      x[i] = current;
      y[i] = current;
      for (int j = 0; j < len; j++) {
        grid[i][j] = Math.random()*len;
      }
      current += step;
    }
    return new UtilitySurface(x, y, grid, step);
  }
  
  
  /*  LOGIC METHODS  */
  
  /**
   * Create a new UtilitySurface with a different utility grid.
   *
   * @param newGrid : a BigDecimal[][]
   * @return new UtilitySurface with {@param newGrid} in place of this.utilityGrid.
   */
  public UtilitySurface replaceGrid(double[][] newGrid) {
    return new UtilitySurface(x, y, newGrid, step);
  }
  
  /**
   * Add two utilityGrids together, returns a new UtilitySurface without modifying the old one
   *
   * @param otherGrid : another BigDecimal[][] of the same dimensions as this.utilityGrid.
   * @return UtilitySurface : creates a new surface with a utility grid made of
   * {@param otherGrid} added {this.UtilityGrid}
   */
  public UtilitySurface addToGrid(double[][] otherGrid) {
    double[][] newGrid = new double[x.length][y.length];
    for (int i = 0; i < this.utilityGrid.length; i++) {
      for (int j = 0; j < this.utilityGrid[i].length; j++) {
        newGrid[i][j] = utilityGrid[i][j] + otherGrid[i][j];
      }
    }
    return new UtilitySurface(x, y, newGrid, step);
  }
  
  /**
   * Subtract {@param otherGrid} from this.utilityGrid.
   * Creates a new grid, does not alter original.
   *
   * @param otherGrid : another BigDecimal[][] of the same dimensions as this.utilityGrid.
   * @return UtilitySurface : creates a new surface with a utility grid made of
   * {@param otherGrid} subtracted from {this.UtilityGrid}.
   */
  public UtilitySurface subFromGrid(double[][] otherGrid) {
    double[][] newGrid = new double[x.length][y.length];
    for (int i = 0; i < x.length; i++) {
      for (int j = 0; j < y.length; j++) {
        newGrid[i][j] = utilityGrid[i][j] - otherGrid[i][j];
      }
    }
    return new UtilitySurface(x, y, newGrid, step);
  }
  
  /**
   * Converts the given payoffs to the nearest grid index and returns the corresponding utility.
   *
   * @param x_payoff : the x payoff (usually the resident)
   * @param y_payoff : the y payoff (usually the mutant)
   * @return BigDecimal payoff at x_i, y_i.
   */
  public double getUtilityAtPayoff(double x_payoff, double y_payoff){
    
    int x_index = (int)Math.round(x_payoff/step);
    int y_index = (int)Math.round(y_payoff/step);
    
    return getGridValueAt(x_index, y_index);
    
  }
  
  
  /*  BASIC GETTERS  */
  
  // These three getters are a memory leak and so break the immutability of the class
  // but defensively copying will affect performance.
  public double[] getX() {
    return x;
  }
  
  public double[] getY() {
    return y;
  }
  
  public double[][] getUtilityGrid() {
    return utilityGrid;
  }
  
  // This one is ok because it indexes the grid directly.
  public double getGridValueAt(int x_i, int y_j) {
    return utilityGrid[x_i][y_j];
  }
  
  public double getStep() {
    return this.step;
  }

  
  
}
