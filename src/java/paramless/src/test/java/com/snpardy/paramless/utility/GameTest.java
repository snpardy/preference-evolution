package com.snpardy.paramless.utility;

import com.snpardy.paramless.game.Game;
import org.junit.Assert;
import org.junit.Test;

import org.jblas.DoubleMatrix;

import java.util.Arrays;

public class GameTest {
  
  @Test
  public void getRowPayoffTest(){
    double[][] row = {{1.0,2.0},{7.0, 2.0}};
    double[][] col = {{8.0,2.0},{5.0, 1.0}};
  
    Game testGame = new Game(row, col);
    
    Assert.assertArrayEquals(row, testGame.getRowPayoffMatrix());
    
    
  }
  
  @Test
  public void supportEnumerationTest(){
  
//    Game testGame = new Game(new double[][]{{7.0, 1.0}, {4.0, 9.0}}, new double[][]{{3, 3}, {1,
//        4}});
    Game testGame = new Game(new double[][]{{2.0, 2.0}, {6.0, 1.0}}, new double[][]{{3.0, 7.0},
        {4.0,
        3.0}});
    double[][] equilibrium = testGame.findRandomEquilibria();
    
    if(equilibrium == null){
      System.out.println("Null!");
    } else {
      System.out.println("Length: "+ equilibrium.length);
      for (double[] e : equilibrium) {
        System.out.println(Arrays.toString(e));
      }
    }
    
    
  }
  
  @Test
  public void solveGameTest() {
  
    Game testGame = new Game(new double[][]{{6.0, 2.0}, {8.0, 2.0}}, new double[][]{{8, 3}, {5, 4}});
  
    DoubleMatrix[] results = testGame.solveGame(2, new int[]{0, 1}, new int[]{0, 1});
  
    if (results == null) {
      System.out.println("No equilibria!");
    } else {
      for (DoubleMatrix r : results) {
        System.out.println(r);
      }
    }
  
  }
  
  
  
  
}
