python pacman.py -l tinyMaze -p SearchAgent -a fn=dfs --frameTime 0 > result.txt
echo >> result.txt
python pacman.py -l mediumMaze -p SearchAgent -a fn=dfs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l bigMaze -p SearchAgent -a fn=dfs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l tinyMaze -p SearchAgent -a fn=bfs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l mediumMaze -p SearchAgent -a fn=bfs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l bigMaze -p SearchAgent -a fn=bfs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l tinyMaze -p SearchAgent -a fn=ucs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l mediumMaze -p SearchAgent -a fn=ucs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l bigMaze -p SearchAgent -a fn=ucs --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l mediumDottedMaze -p StayEastSearchAgent --frameTime 0 >>result.txt
echo >> result.txt
REM python pacman.py -l mediumDottedMaze -p StayWestSearchAgent --frameTime 0 >>result.txt
python pacman.py -l mediumScaryMaze -p StayEastSearchAgent --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l mediumScaryMaze -p StayWestSearchAgent --frameTime 0 >>result.txt
echo >> result.txt
python pacman.py -l tinyCorners -p SearchAgent -a fn=bfs,prob=CornersProblem >>result.txt
echo >> result.txt
python pacman.py -l mediumCorners -p SearchAgent -a fn=bfs,prob=CornersProblem >>result.txt
echo >> result.txt
python pacman.py -l testSearch -p AStarFoodSearchAgent >>result.txt
echo >> result.txt
python pacman.py -l trickySearch -p AStarFoodSearchAgent >>result.txt
echo >> result.txt                                                                                                                                              