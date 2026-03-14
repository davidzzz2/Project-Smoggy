### BS810 Final Project 
# SBP change Meta Analysis
data1 <- BS810_Final_Project2
# install.packages('metadat')
# install.packages('meta')
library(metadat)
library(meta)
library(metafor)
m.cont1 <- metacont(n.e = Ne,               
                    mean.e = Mean_e,              
                    sd.e = SD_e,              
                    n.c = Nc,                
                    mean.c = Mean_c,              
                    sd.c = SD_c,              
                    sm = "MD",              
                    common = TRUE,        
                    random = TRUE,      
                    studlab =`Study (SBP)`, 
                    data = data1)

print(m.cont1, digits = 2)

forest(m.cont1, 
       sortvar = m.cont1$w.fixed,
       label.e = "Treatment",
       label.right = "Favors Control",
       label.left = "Favors intervention",
       digits.mean = 1,
       digits.sd = 1,
       col.diamond = "blue") 

funnel(m.cont1, bg = "blue", xlab = "Mean Difference", ylab = "Standard Error")
col.contour = c("red", "darkorange", "gold")
funnel(m.cont1, bg="blue", backtransf = FALSE, contour.levels=c(0.90, 0.95, 0.99), 
       col.contour = col.contour)
legend(x = 6, y = 0.01, legend = c("p < 0.10", "p < 0.05", "p < 0.01"), 
       fill = col.contour)
title("Contour-Enhanced Funnel Plot")

metabias(m.cont1, method.bias = "Egger", plotit = TRUE)
metabias(m.cont1, method.bias = "Begg")

influence_results2 <- metainf(m.cont1, pooled = "random")
print(influence_results2)
forest(influence_results2)

meta_reg2 <- metareg(m.cont1, data1$Age)
summary(meta_reg2)




# DBP change meta analysis 
data2 <- BS810_Final_Project

m.cont2 <- metacont(n.e = Ne,               
                    mean.e = Mean_e,              
                    sd.e = SD_e,              
                    n.c = Nc,                
                    mean.c = Mean_c,              
                    sd.c = SD_c,              
                    sm = "MD",              
                    common = TRUE,        
                    random = TRUE,      
                    studlab =`Study (DBP)`, 
                    data = data2)

print(m.cont2, digits = 2)

forest(m.cont2, 
       sortvar = m.cont2$w.fixed,
       label.e = "Treatment",
       label.right = "Favors Control",
       label.left = "Favors intervention",
       digits.mean = 1,
       digits.sd = 1,
       col.diamond = "blue") 

funnel(m.cont2, bg = "blue", xlab = "Mean Difference", ylab = "Standard Error")
col.contour = c("red", "darkorange", "gold")
funnel(m.cont2, bg="blue", backtransf = FALSE, contour.levels=c(0.90, 0.95, 0.99), 
       col.contour = col.contour)
legend(x = 6, y = 0.01, legend = c("p < 0.10", "p < 0.05", "p < 0.01"), 
       fill = col.contour)
title("Contour-Enhanced Funnel Plot")

metabias(m.cont2, method.bias = "Egger", plotit = TRUE)
metabias(m.cont2, method.bias = "Begg")
 
influence_results <- metainf(m.cont2, pooled = "random")
print(influence_results)
forest(influence_results)

# meta-regression
meta_reg <- metareg(m.cont2, data2$Age)
summary(meta_reg)

