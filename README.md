Dear Insight Team,

I wanted to write a Python code that was purely my own, so I tried not to adapt any solutions found on the web. Initially, I wanted to do a brute-force approach by just generating all possible board configurations and checking them one by one with the input until the right configuration is found. While browsing the web to look for the possible number of configurations, I stumbled over an article by Peter Norvig (http://norvig.com/sudoku.html). I learned that this would take a little too long. Just a little bit... (100 times the age of the universe, according to Norvig.)

After that, I implemented a version which would only work for very easy puzzles. Originally, I naively thought that all puzzles could be solved using just my "optimize()" method, but I quickly realized that this only works for simple puzzles where no guessing (i. e. randomly choose a valid option for a field and see whether it works) is required. I then had to switch to an objected-oriented design to better keep track of all board configurations and the number of guesses they contain. I thus ended up with a program that is a hybrid between analytically solving the puzzle (using the method "optimize()") and making guesses when that method fails (using "createguessedboards()"). The code very much proceeds in the way I would manually try to solve a Sudoku, and I am pretty sure it is not the most efficient strategy. 

However, I tested my latest solution with a variety of puzzles that I found online and that were classified as very difficult, and my code worked and seemed reasonably fast for all of these. If I could spend more time on this coding challenge, I would probably try to clean up ugly lines (e.g. line 152) by perhaps introducing another class for the fields, and introduce x-y-coordinates as attributes to get rid of my not-so-elegant 81-element list (the "fields" attribute in the class "Board"). Thanks for testing and I am looking forward to your feedback,

Sam