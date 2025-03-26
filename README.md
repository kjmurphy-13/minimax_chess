# Chess: User vs. Minimax
This program is a chess game in which the user plays against an AI agent utilizing a custom Minimax algorithm. 

### Strategy Recommendations
When it is the User's turn to move, each selected piece will display all of its possible moves across the board. Safe moves are highlighted in green, and moves that will lead to immediate capture are highlighted in red. The game also creates a "move recommendation" for the User using the same Minimax algorithm as the AI. 

### Adjustable AI Difficulty
To create a dynamic opponent, the User can change both the AI search depth and the maximum allotted time per move. Search depth translates to how many moves ahead the AI can think, and the maximum search time prevents the AI from thinking forever. These options can be set in the Main Menu before the game begins.

### Robust Evaluation Criteria
This game builds-in a variety of strategic indicators into the evaluation function, such as: raw material count, pawn structure, king safety, board development, central control, mobility, and positional score. 
