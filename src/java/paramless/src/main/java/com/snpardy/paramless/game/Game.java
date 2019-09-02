package com.snpardy.paramless.game;

import com.snpardy.paramless.utility.UtilitySurface;


import java.util.HashSet;
import java.util.Arrays;
import java.util.Random;

import org.jblas.Solve;
import org.jblas.DoubleMatrix;



/**
 * A class the represents a two player game.
 */
public class Game {
  private double[][] rowPayoffMatrix;
  private double[][] columnPayoffMatrix;
  private Random random = new Random();
  
  public Game(double[][] rowPayoff, double[][] columnPayoff) {
    this.rowPayoffMatrix = rowPayoff;
    this.columnPayoffMatrix = columnPayoff;
  }
  
  public static Game randomTwoByTwoGame(int minPayoff, int maxPayoff){
    
    int range = maxPayoff - minPayoff;
    
    double[][] rowPayoff = new double[2][2];
    double[][] colPayoff = new double[2][2];
    for(int i = 0; i < rowPayoff.length; i++){
      for(int j = 0; j < rowPayoff[0].length; j++){
        double rand = minPayoff + Math.random()* range;
        rowPayoff[i][j] = rand;
        colPayoff[j][i] = rand;
      }
    }
    return new Game(rowPayoff, colPayoff);
  }
  
  /**
   *
   * @return double[][] representing a set of Nash equilibrium strategies. The array at
   * position 0 is the strategy of row player, position 1 is the strategy of column player.
   */
  public double[][] findRandomEquilibria(){
    boolean foundEquilibria = false;
    DoubleMatrix[] internalResult = null;
    HashSet<int[][]> supportsChecked = new HashSet<>();
    // Finding the maximum size of the support
    // only recording the smallest max as we'll only look at supports of the same size
    // @TODO extend to handle supports of multiple sizes
    int maxSize = this.rowPayoffMatrix[0].length;
    if(this.columnPayoffMatrix.length < maxSize){
      maxSize = this.columnPayoffMatrix.length;
    }
    
    
//  Initializing support
    /////////////////////////////////////////////////////////////////
    int size = random.nextInt(maxSize)+1;
    System.out.println("max: " + maxSize);
    System.out.println("size: " + size);
    // Randomly select support
    int[] I = new int[size];
    int[] J = new int[size];
    int[][] support = {I, J};
    // Randomly select support

    I[0] = random.nextInt(maxSize);
    J[0] = random.nextInt(maxSize);
    // randomly selecting indices of the support
    for (int index = 1; index < size; index++) {
      I[index] = random.nextInt(maxSize);
      // Making sure we don't select the same index twice
      // Making sure randomly selected indexes increase in size
      while(I[index] == I[index-1]){
        I[index] = random.nextInt(maxSize);
      }
      J[index] = random.nextInt(maxSize);
      while(J[index] == J[index-1]){
        J[index] = random.nextInt(maxSize);
      }
    }
    Arrays.sort(J);
    Arrays.sort(I);
    //////////////////////////////////////////////////////////////////
    while(!foundEquilibria) {

      // Checking support
      while (supportsChecked.contains(support)) {
        // Make sure that we're looking at a support that hasn't already been checked
        
        // Populating support
        size = random.nextInt(maxSize)+1;
        // Randomly select support
        I = new int[size];
        J = new int[size];
        support[0] = I;
        support[1] = J;
        I[0] = random.nextInt(maxSize);
        J[0] = random.nextInt(maxSize);
        // randomly selecting indices of the support
        for (int index = 1; index < size; index++) {
          I[index] = random.nextInt(maxSize);
          // Making sure we don't select the same index twice
          // Making sure randomly selected indexes increase in size
          while(I[index] == I[index-1]){
            I[index] = random.nextInt(maxSize);
          }
          J[index] = random.nextInt(size);
          while(J[index] == J[index-1]){
            J[index] = random.nextInt(maxSize);
          }
        }
        Arrays.sort(J);
        Arrays.sort(I);
        
      } // End while loop
      /////////////////////////////////////////////////////////
      
      
      
      internalResult = solveGame(size, support[0], support[1]);
      supportsChecked.add(support);
      
      if(coherentResponse(internalResult[0], internalResult[1]) &&
             bestResponse(support[0], support[1], internalResult[0], internalResult[1])) {
        foundEquilibria = true;
      }
    }
    
    return formatResult(support[0], support[1], internalResult[0], internalResult[1]);
  }
  
  /**
   * Given a set of strategies, returns the expected payoff of each player.
   *
   * @param strategies : a double[][] representing row player strategy and column player
   *                   strategies. Position 0 is thought of as the row player, position 1 is the
   *                   column player. The contents of the arrays at each place is the probability
   *                   that the player will play that strategy.
   * @return double[] : Position 0 is the expected payoff of the row player (or the player
   * with strategies at position 0 in the {@param strategies}, position 1 is expected payoff of
   * column player.
   */
  public double[] expectedPayoff(double[][] strategies){
    double[] rowStrategy = strategies[0];
    double[] colStrategy = strategies[1];
    
    double colExpectedPayoff = 0;
    double rowExpectedPayoff = 0;
    
    for(int i = 0; i < rowStrategy.length; i++){
      for(int j = 0; j < colStrategy.length; j++){
        rowExpectedPayoff =
            rowExpectedPayoff + (rowStrategy[i] * colStrategy[j] * rowPayoffMatrix[i][j]);
        colExpectedPayoff =
            colExpectedPayoff + (rowStrategy[i] * colStrategy[j] * columnPayoffMatrix[i][j]);
      }
    }
    return new double[]{rowExpectedPayoff, colExpectedPayoff};
  }
  
  /**
   * Returns a new game object with payoffs weighted by the players utility {@param surface}.
   *
   *
   * @param rowSurface : a UtilitySurface object representing the utility based preferences of the
   *                row player.
   * @param columnSurface : a UtilitySurface object representing the utility based preferences of the
   *    *                column player.
   * @return Game : a new game object.
   */
  public Game utilityConversion(UtilitySurface rowSurface, UtilitySurface columnSurface){
    
    double[][] new_row_payoff = new double[this.rowPayoffMatrix.length][this.rowPayoffMatrix[0].length];
    double[][] new_col_payoff = new double[this.columnPayoffMatrix.length][this.columnPayoffMatrix[0].length];
    
    
    for(int i = 0; i < new_row_payoff.length; i++){
      for(int j = 0; j < new_row_payoff[0].length; j++){
//        @TODO test this a lot - not sure if just swapping row/col parameters is correct
        new_row_payoff[i][j] = rowSurface.getUtilityAtPayoff(this.rowPayoffMatrix[i][j],
            this.columnPayoffMatrix[i][j]);
        new_col_payoff[i][j] = columnSurface.getUtilityAtPayoff(this.columnPayoffMatrix[i][j],
            this.rowPayoffMatrix[i][j]);
      }
    }
    return new Game(new_row_payoff, new_col_payoff);
  }
  
  
//  BASICS  //
  @Override
  public String toString(){
    return "Row player:\n" + Arrays.toString(rowPayoffMatrix) + "\n\n" + "Column player:\n" + Arrays.toString(columnPayoffMatrix);
  }
  
  public double[][] getRowPayoffMatrix() {
    return rowPayoffMatrix;
  }
  
  public double[][] getColumnPayoffMatrix() {
    return columnPayoffMatrix;
  }
  
  
  // HELPER METHODS //
  
  private boolean bestResponse(int[] rowSupport, int[] colSupport, DoubleMatrix rowStrategy,
                               DoubleMatrix colstrategy){
    if(rowSupport.length == this.rowPayoffMatrix.length && colSupport.length == this.columnPayoffMatrix[0].length){
      // support is the entire game
      return true;
    }
    
    double expectedPayoff;
    for(int j = 0; j < this.columnPayoffMatrix[0].length; j++){
      expectedPayoff = 0;
      for(int i=0; i < rowStrategy.columns -1; i++) {
        expectedPayoff += rowStrategy.get(i)*this.columnPayoffMatrix[i][j];
      }
      if(expectedPayoff >= rowStrategy.get(rowStrategy.length-1)){
        return false;
      }
    }
    
    for(int j = 0; j < this.rowPayoffMatrix.length; j++){
      expectedPayoff = 0;
      for(int i = 0; i < colstrategy.columns-1; i++){
        expectedPayoff += this.rowPayoffMatrix[j][i] * colstrategy.get(i);
      }
      if(expectedPayoff >= colstrategy.get(colstrategy.length-1));
    }
    
    return true;
  }
  
  /**
   * Checks that the strategies calulated for both players contain probabilities (i.e. between 0
   * and 1).
   *
   * @param rowStrategy : an representing the strategy of the row player, the final element being
   *                   the expected payoff.
   * @param colStrategy : an representing the strategy of the column player, the final element being
   *                   the expected payoff.
   * @return boolean : true if the probabilities in both strategies are between 0 and 1, false
   *                   otherwise.
   */
  private boolean coherentResponse(DoubleMatrix rowStrategy, DoubleMatrix colStrategy){
    for(int i = 0; i < rowStrategy.length-1; i++){
      if(rowStrategy.get(i) < 0 || rowStrategy.get(i) > 1){
        return false;
      }
    }
    for(int i =0; i <colStrategy.length-1; i++){
      if(colStrategy.get(i) < 0 || colStrategy.get(i) > 1){
        return false;
      }
    }
    return true;
  }
  
  public DoubleMatrix[] solveGame(int size, int[] rowSupport, int[] columnSupport) {
    // Solve linear equations
    //@TODO remove print statements
    System.out.println("Row: ");
    System.out.println(Arrays.toString(rowSupport));
    System.out.println("Col: ");
    System.out.println(Arrays.toString(columnSupport));
    // Constructing linear equations
  
    //The row player must play in a way that makes the column player indifferent
    //The column player must play in a way that makes the column player indifferent
    DoubleMatrix rowEqMatrix = new DoubleMatrix(size + 1, size + 1);
    DoubleMatrix colEqMatrix = new DoubleMatrix(size + 1, size + 1);
    for (int r : rowSupport) {
      for (int c : columnSupport) {
        rowEqMatrix.put(r, c, this.columnPayoffMatrix[c][r]);
        colEqMatrix.put(r, c, this.rowPayoffMatrix[r][c]);
      }
    }
  
    for (int i = 0; i < size; i++) {
      // filling the last column here (it's always -1!)
      rowEqMatrix.put(i, size, -1);
      colEqMatrix.put(i, size, -1);
      // filling the last row here (it's always 1)
      rowEqMatrix.put(size, i, 1);
      colEqMatrix.put(size, i, 1);
    
      // filling the bottom right
      rowEqMatrix.put(size, size, 0);
      colEqMatrix.put(size, size, 0);
    }
  
    // The 'B' in A*X=B
    // E.g. First two elems represent the payoff in each case being
    // equal, the third elem represents the fact that the probabililty must sum to 1
    DoubleMatrix B = DoubleMatrix.zeros(size + 1);
    B.put(size, 1);
  
    DoubleMatrix rowResult = Solve.solve(rowEqMatrix, B);
    DoubleMatrix colResult = Solve.solve(colEqMatrix, B);
    
    return new DoubleMatrix[] {rowResult, colResult};
  }
  
  private double[][] formatResult(int[] rowSupport, int[] columnSupport, DoubleMatrix rowResult,
                                      DoubleMatrix colResult){
    
    double[] rowStrategy = new double[this.rowPayoffMatrix.length];
    // i indexes the result array (results will be ordered the same as in r but not at the same
    // index e.g. support of {0, 2} will have indices of [0,1]
    int i = 0;
    for(int r : rowSupport){
      rowStrategy[r] = rowResult.get(i);
      i++;
    }
  
    double[] colStrategy = new double[this.columnPayoffMatrix[0].length];
    // i indexes the result array (results will be ordered the same as in r but not at the same
    // index e.g. support of {0, 2} will have indices of [0,1]
    i = 0;
    for(int c : columnSupport){
      colStrategy[c] = colResult.get(i);
      i++;
    }
    return new double[][] {rowStrategy, colStrategy};
  }
  
}
