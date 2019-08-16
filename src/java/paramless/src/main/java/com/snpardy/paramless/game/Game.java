package com.snpardy.paramless.game;

import com.snpardy.paramless.utility.UtilitySurface;


import java.util.Arrays;

/**
 * A class the represents a two player game.
 */
public class Game {
  private double[][] rowPayoffMatrix;
  private double[][] columnPayoffMatrix;
  
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
    double[][] equilibria = new double[2][2];
    
    // @TODO implement support enumeration => select random support, check if Nash, if yes return
    //  if no keep going => all games have a Nash so will terminate.
    
    return equilibria;
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
  
}
