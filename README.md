# nfl-predict-sophomore-seasons-2018  
An algorithm to predict the sophomore seasons of all second year running backs in 2018.  

## Training data  
Starting with a json dataset containing the single game statistics of every player for every nfl game since 1950, I eventually broke it down into datasets containing the rookie seasons and sophomore seasons of every running back in that timeframe who had at least 100 offensive touches in both their rookie and sophomore seasons, to ensure an accurate representation of their production for those seasons. The rookie seasons of these 238 running backs were compared to each running back to create neighbors, a certain number of most the most similar players. Then, these neighbors had their sophomore seasons analyzed to get their average fantasy points per game, which is used as the projection for the sophomore season of that running back. It is important to note that every running back was compared to every other running back, but never themselves.  

## Picking an algorithm  
Using the k nearest neighbors method, to pick the best way to get the neighbors, as well as the number of neighbors, I used a various combination of running back statistics to create several algorithms, and for each algorithm, I tested its performance with every possible amount of neighbors.  
max k7: The highest rate of players within 70% of their projected rating. {k number: rate}  
max k8: The highest rate of players within 80% of their	projected rating. {k number: rate}  
max k9: The highest rate of players within 90% of their	projected rating. {k number: rate}  
max kRating: The highest average prediction rating for all k values. {k number: rate}  
alt *: Looking at the rates for k numbers that maxed something.  

#### Possible stats. All stats weighted equally unless otherwise noted.  
![alt text](/images/Possible_Stats.png)  

#### This algorithm used every stat  
![alt text](/images/Algorithm_1.png)  

#### This algorithm used stats with yards  
![alt text](/images/Algorithm_2.png)  

#### This algorithm used stats with touchdowns  
![alt text](/images/Algorithm_3.png)  

#### This algorithm used per game stats  
![alt text](/images/Algorithm_4.png)  

#### This algorithm used per rushing attempt and per reception stats  
![alt text](/images/Algorithm_5.png)  

#### This algorithm used yards per rush and yards per reception  
![alt text](/images/Algorithm_6.png)  

#### This algorithm used rushing yards per game and receiving yards per game  
![alt text](/images/Algorithm_7.png)  

#### This algorithm used rushing yards per game  
![alt text](/images/Algorithm_8.png)  

#### This algorithm used receiving yards per game
![alt text](/images/Algorithm_9.png~)  

#### This algorithm used rushing yards per game weighted * .7 and receiving yards per game weighted * .3  
![alt text](/images/Algorithm_10.png)  

#### Selected algorithm  
Due to it having the best kRating, I selected algorithm 7 to use with 12 neighbors for each prediction.  This choice provides an average projection with 77.57% accuracy, with 72.15% of players being within 70% of thier projection, 51.48% of players being within 80% of their projection, and 27.84% of players being within 90% of their projection. From this, if a player's projection is 10 points per game, we can say their floor is 7.757 points per game and their ceiling is 12.89 points per game.  

## Algorithm 7 Projections  
Projections for every sophomore running back who touched the ball at least once on offense in their rookie season.  

#### Aaron Jones  
![alt text](/images/Aaron_Jones.png)  

#### Alvin Kamara    
![alt text](/images/Alvin_Kamara.png)  

#### Brian Hill  
![alt text](/images/Brian_Hill.png)  

#### Chris Carson  
![alt text](/images/Chris_Carson.png)  

#### Christian McCaffrey  
![alt text](/images/Christian_McCaffrey.png)  

#### D'Onta Foreman  
![alt text](/images/D'Onta_Foreman.png)  

#### Dalvin Cook  
![alt text](/images/Dalvin_Cook.png)  

#### De'Angelo Henderson  
![alt text](/images/De'Angelo_Henderson.png)  

#### Devante Mays  
![alt text](/images/Devante_Mays.png)  

#### Elijah McGuire  
![alt text](/images/Elijah_McGuire.png)  

#### Jamaal Williams  
![alt text](/images/Jamaal_Williams.png)  

#### James Conner  
![alt text](/images/James_Conner.png)  

#### Joe Mixon  
![alt text](/images/Joe_Mixon.png)  

#### Kareem Hunt  
![alt text](/images/Kareem_Hunt.png)  

#### Marlon Mack  
![alt text](/images/Marlon_Mack.png)  

#### Samaje Perine  
![alt text](/images/Samaje_Perine.png)  

#### Tarik Cohen  
![alt text](/images/Tarik_Cohen.png)  

#### Wayne Gallman  
![alt text](/images/Wayne_Gallman.png)  

## Projection Notes  
Due to the training data using running backs with at least 100 touches in both their rookie and sophomore seasons, running backs with a significant lack of touches may be misranked. Moreover, the projections seem to have a floor in the low 8's, so all players with projections from roughly 9.5 and below may actually perform much worse than projected.  

## Projection Rankings  
18.688304 - Dalvin Cook: 85/100 touches  
17.664375 - Kareem Hunt  
16.823333 - Alvin Kamara  
15.338788 - Chris Carson: 56/100 touches  
14.401863 - Christian McCaffrey  
11.381503 - Samaje Perine  
11.251977 - Jamaal Williams  
11.009945 - Aaron Jones: 90/100 touches  
10.542405 - Joe Mixon  
10.414620 - Tarik Cohen  
9.929193 - D'Onta Foreman: 84/100 touches  
9.607865 - Wayne Gallman  
9.600000 - Marlon Mack  
8.385556 - Elijah McGuire  

#### Unable to properly project due to a significant lack of touches  
8.942169 - De'Angelo Henderson: 9/100 touches  
8.825806 - Devante Mays: 7/100 touches  
8.825806 - James Conner: 32/100 touches  
8.668156 - Brian Hill: 13/100 touches  


## Final Notes  
These projections are strictly looking into the past in an attempt to predict the upcoming season. It is important, however, to factor current real world situations into these projections. If a running back is likely to get a significantly larger amount of touches than the previous season, such as Christian McCaffrey, then I'd suggest you look at their projection closer to their projected ceiling than their actual projection. Conversely, if a running back is likely to get a significantly lower workload than the previous season, such as Wayne Gallman, or if he is currently still a backup, such as D'Onta Foreman, then I would suggest you look at their projection closer to their projected floor than their actual projection. If these players were to get more touches however, they would certainly be worth an add off the waiver wire. 