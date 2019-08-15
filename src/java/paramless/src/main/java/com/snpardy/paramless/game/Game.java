package com.snpardy.paramless.game;

import com.snpardy.paramless.utility.UtilitySurface;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.Arrays;


public class Game {
  private BigDecimal[][] rowPayoff;
  private BigDecimal[][] columnPayoff;
  
  public Game(BigDecimal[][] rowPayoff, BigDecimal[][] columnPayoff) {
    this.rowPayoff = rowPayoff;
    this.columnPayoff = columnPayoff;
  }
  
  public static Game randomTwoByTwoGame(int minPayoff, int maxPayoff){
    BigDecimal[][] rowPayoff = new BigDecimal[2][2];
    BigDecimal[][] colPayoff = new BigDecimal[2][2];
    for(int i = 0; i < rowPayoff.length; i++){
      for(int j = 0; j < rowPayoff[0].length; j++){
        BigDecimal rand = BigDecimal.valueOf(minPayoff + Math.random()* maxPayoff);
        rowPayoff[i][j] = rand;
        colPayoff[j][i] = rand;
      }
    }
    return new Game(rowPayoff, colPayoff);
  }
  
  
  @Override
  public String toString(){
    return "Row player:\n" + Arrays.toString(rowPayoff) + "\n\n" + "Column player:\n" + Arrays.toString(columnPayoff);
  }
  
  public ArrayList<int[]> findRandomEquilibria(){
    ArrayList<int[]> equilibria = new ArrayList<>();
    
    // @TODO implement support enumeration => select random support, check if Nash, if yes return
    //  if no keep going => all games have a Nash so will terminate.
    
    return equilibria;
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
    
    BigDecimal[][] new_row_payoff = new BigDecimal[this.rowPayoff.length][this.rowPayoff[0].length];
    BigDecimal[][] new_col_payoff = new BigDecimal[this.columnPayoff.length][this.columnPayoff[0].length];
    
    
    for(int i = 0; i < new_row_payoff.length; i++){
      for(int j = 0; j < new_row_payoff[0].length; j++){
//        @TODO test this a lot - not sure if just swapping rol/col parameters is correct
        new_row_payoff[i][j] = rowSurface.getUtilityAtPayoff(this.rowPayoff[i][j],
            this.columnPayoff[i][j]);
        new_col_payoff[i][j] = columnSurface.getUtilityAtPayoff(this.columnPayoff[i][j],
            this.rowPayoff[i][j]);
      }
    }
    return new Game(new_row_payoff, new_col_payoff);
  }
  
}
