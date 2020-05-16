Anti-Chess Term Project README- Manish Nagireddy (Section B)


Description:
* I will be implementing a variant of chess known as anti-chess or suicide chess. The goal of the game is to get rid of all of your pieces. The pieces move in the same manner as chess; in fact, the game is played like regular chess with the only caveat being that if there is a capture available, the player must capture the piece. Thus, the only time a player can choose a move is when there are zero or multiple captures available.
* The final version of the game will have three modes: player vs player, player vs AI, and AI vs AI where the player can pause the game at any time and/or make a move of his/her own at any point.


How to Run the Project:
* Load all the program files and image folders into one folder. Run the program titled ‘ChessGame.py”
* No libraries were used.


Shortcut Commands:
* Pressing the ‘a’ key in the game screen will get rid of the pawns (this is the demo board). Since it is white’s turn, there are three possible moves: capturing either of the black rooks or capturing the black queen. As the white player, click on either rook and make the corresponding capture. It is now black’s turn, and there are only two possible moves: capturing the remaining rook that is opposite the black rook or capturing the white queen. According to the strategy of antichess, a player wishes to prioritize capturing pieces of the minimum value. This is because pieces with larger values (i.e. rooks and queens) have more potential to capture and it is in the player’s best interest to preserve these kinds of pieces on his opponent’s side. Thus, the minimax AI should capture the opposing rook instead of the opposing queen. Now, press the ‘m’ key, which toggles the minimax AI. You should see that the black rook captures the white rook, thus demonstrating the way this algorithm works.