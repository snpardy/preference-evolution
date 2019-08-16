package com.snpardy.paramless.utility;

import org.junit.Assert;
import org.junit.Test;

import javax.rmi.CORBA.Util;


public class UtilitySurfaceTest {
  
  
  @Test
  public void selfishFactoryTest(){
    UtilitySurface selfish = UtilitySurface.selfish(0, 10, .5);
    
    // A selfish grid means that no matter the opponent payoff, the utility always equals the
    // payoff on offer to the agent.
    for(int i = 0; i<selfish.getUtilityGrid().length; i++){
      for(int j = 0; j<selfish.getUtilityGrid()[i].length; j++){
        Assert.assertEquals(selfish.getX()[i], selfish.getGridValueAt(i, j), 0);
      }
    }
  }
  
  @Test
  public void selflessFactoryTest(){
    UtilitySurface selfless = UtilitySurface.selfless(0, 10, .1);
    
    // A selfless grid means that no matter the payoff on offer to the x_player, the utility will
    // always equals be equal to the payoff of the y_player.
    
    for(int i = 0; i<selfless.getUtilityGrid().length; i++){
      for(int j = 0; j<selfless.getUtilityGrid()[i].length; j++){
        Assert.assertEquals(selfless.getY()[j], selfless.getGridValueAt(i, j), 0);
      }
    }
  }
  
  @Test
  public void replaceGridTest(){
    double[] x = new double[10];
    double[] y = new double[10];
    double[][] gridA = new double[10][10];
    double[][] gridB = new double[10][10];
    
    // Populating arrays
    for(int i = 0; i < 10; i ++){
      x[i] = (double)i;
      y[i] = (double)i;
      for(int j = 0; j < 10; j++){
        gridA[i][j] = (double)i;
        gridB[i][j] = (double)j;
      }
    }
    
    UtilitySurface A_SURFACE = new UtilitySurface(x, y, gridA, 1);
    // using the replace method
    UtilitySurface B_SURFACE = A_SURFACE.replaceGrid(gridB);
    
    double[][] newBGrid = B_SURFACE.getUtilityGrid();
    for(int index = 0; index < gridB.length; index++){
      Assert.assertArrayEquals(gridB[index], newBGrid[index], 0);
    }
    
  }

  @Test
  public void addToGridTest(){
    
    double step = 1;
    
    double[] x = new double[10];
    double[] y = new double[10];
    double[][] original = new double[10][10];
    double[][] addToOriginal = new double[10][10];
    double[][] expectedResult = new double[10][10];
    
    // Populating arrays
    for(int i=0; i<original.length; i++){
      x[i] = i;
      y[i] = i;
      for(int j=0; j<original[i].length; j++){
        original[i][j] = i;
        addToOriginal[i][j] = j;
        expectedResult[i][j] = i+j;
      }
    }
    
    UtilitySurface originalSurface = new UtilitySurface(x, y, original, step);
    // Using addToGrid method
    UtilitySurface resultSurface = originalSurface.addToGrid(addToOriginal);
    
    for(int i = 0; i < expectedResult.length; i++){
      Assert.assertArrayEquals(expectedResult[i], resultSurface.getUtilityGrid()[i], 0);
    }
    
    
    
  }
  
  @Test
  public void subFromGridTest(){
    
    double step = 1;
    
    double[] x = new double[10];
    double[] y = new double[10];
    double[][] original = new double[10][10];
    double[][] subFromOriginal = new double[10][10];
    double[][] expectedResult = new double[10][10];
    
    // Populating arrays
    for(int i=0; i<original.length; i++){
      x[i] = i;
      y[i] = i;
      for(int j=0; j<original[i].length; j++){
        original[i][j] = i;
        subFromOriginal[i][j] = j;
        expectedResult[i][j] = i-j;
      }
    }
    UtilitySurface originalSurface = new UtilitySurface(x, y, original, step);
    // Using addToGrid method
    UtilitySurface resultSurface = originalSurface.subFromGrid(subFromOriginal);
    
    for(int i = 0; i < expectedResult.length; i++){
      Assert.assertArrayEquals(expectedResult[i], resultSurface.getUtilityGrid()[i], 0);
    }
    
    
    
  }

  @Test
  public void getUtilityAtPayoffTest(){
  
    UtilitySurface stepOne = UtilitySurface.selfless(0, 10, 1);
    
    Assert.assertEquals(stepOne.getUtilityAtPayoff(3.32542, 7.222354),
                        stepOne.getGridValueAt(3,7),
                  0);
    Assert.assertEquals(stepOne.getUtilityAtPayoff(0.4, 7.52354),
        stepOne.getGridValueAt(0,8),
        0);
    
    UtilitySurface stepPointOne = UtilitySurface.random(0, 10, .1);
    
    Assert.assertEquals(stepPointOne.getUtilityAtPayoff(0.42541, 3.7952),
                        stepPointOne.getGridValueAt(4, 38),
                  0);
    
    
  }
  
}
