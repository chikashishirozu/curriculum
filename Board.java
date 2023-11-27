public class Board {
     public static final int SIZE = 8;
     private Piece[][] board;

     public Board() {
         board = new Piece[SIZE][SIZE];
         // Initialize the board with the initial Othello setup
         board[SIZE/2 - 1][SIZE/2 - 1] = new Piece(Piece.WHITE);
         board[SIZE/2][SIZE/2] = new Piece(Piece.WHITE);
         board[SIZE/2 - 1][SIZE/2] = new Piece(Piece.BLACK);
         board[SIZE/2][SIZE/2 - 1] = new Piece(Piece.BLACK);
     }

     public Piece getPiece(int x, int y) {
         return board[x][y];
     }

     public void setPiece(int x, int y, Piece piece) {
         board[x][y] = piece;
     }

     public void flipPiece(int x, int y) {
         Piece piece = getPiece(x, y);
         if (piece != null) {
             piece.flip();
         }
     }

     public void printBoard() {
         for (int i = 0; i < SIZE; i++) {
             for (int j = 0; j < SIZE; j++) {
                 Piece piece = getPiece(i, j);
                 if (piece == null) {
                     System.out.print("-");
                 } else if (piece.getColor() == Piece.BLACK) {
                     System.out.print("B");
                 } else {
                     System.out.print("W");
                 }
             }
             System.out.println();
         }
     }
}


