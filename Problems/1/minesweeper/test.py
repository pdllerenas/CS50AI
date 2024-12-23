import minesweeper
import runner

game = minesweeper.Minesweeper(height=8, width=8, mines=8)

runner.run(game)

