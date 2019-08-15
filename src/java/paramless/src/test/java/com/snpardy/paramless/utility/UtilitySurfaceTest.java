package com.snpardy.paramless.utility;
import com.snpardy.paramless.utility.UtilitySurface;
import org.junit.Test;

import static org.junit.Assert.assertArrayEquals;
import static org.junit.Assert.assertEquals;

import java.math.BigDecimal;

public class UtilitySurfaceTest {
  
  @Test
  public void replaceGridTest(){
    BigDecimal[] x = new BigDecimal[10];
    BigDecimal[] y = new BigDecimal[10];
    BigDecimal[][] gridA = new BigDecimal[10][10];
    BigDecimal[][] gridB = new BigDecimal[10][10];
    
    // Populating arrays
    for(int i = 0; i < 10; i ++){
      x[i] = BigDecimal.valueOf(i);
      y[i] = BigDecimal.valueOf(i);
      for(int j = 0; j < 10; j++){
        gridA[i][j] = BigDecimal.valueOf(i);
        gridB[i][j] = BigDecimal.valueOf(j);
      }
    }
    
    UtilitySurface A_SURFACE = new UtilitySurface(x, y, gridA, BigDecimal.valueOf(1));
    // using the replace method
    UtilitySurface B_SURFACE = A_SURFACE.replaceGrid(gridB);
    
    assertArrayEquals(B_SURFACE.getUtilityGrid(), gridB);
    
    
    
  }

  


}
