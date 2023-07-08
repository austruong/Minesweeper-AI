# Minesweeper-AI
A simple AI capable of learning from and playing Minesweeper via the concepts of machine learning and data mining.

# Overview
Through a command-line interface, the user is capable of generating Minesweeper maps of varying board sizes and difficulties -- Easy, Medium, and Hard -- and allowing the Minesweeper AI to solve the generated board.

# The AI Algorithm
The Minesweeper AI employs the following techniques to solve the board: 
1. Neighboring Cell Identification: The AI identifies and classifies all adjacent cells a probability to determine the probability that any of the unrevealed cells contain mines by examining any adjacent mines and the number of revealed cells.

2. Exploration Strategy: The AI explores cells by lowest probability of containing mines, this reduces the overall chance that the next cell the AI chooses to reveal will contain a mine
