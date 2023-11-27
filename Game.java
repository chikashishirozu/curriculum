import java.util.Scanner;

public class Game {
    private Player player1;
    private Player player2;
    private Board board;
    private Player currentPlayer;

    public Game() {
        this.player1 = new Player("Player 1", Piece.BLACK);
        this.player2 = new Player("Player 2", Piece.WHITE);
        this.board = new Board();
        this.currentPlayer = player1;
    }

    public void start() {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            board.printBoard();
            System.out.println(currentPlayer.getName() + "'s turn. Enter your move in the format 'x y':");
            int x = scanner.nextInt();
            int y = scanner.nextInt();
            if (isValidMove(x, y)) {
                board.setPiece(x, y, currentPlayer.play());
                flipPieces(x, y);
                switchPlayer();
            } else {
                System.out.println("Invalid move. Try again.");
            }
        }
    }

    private boolean isValidMove(int x, int y) {
        // Add your own logic to check if the move is valid according to the rules of Othello
        return true;
    }

    private void flipPieces(int x, int y) {
        // Add your own logic to flip the pieces according to the rules of Othello
    }

    private void switchPlayer() {
        if (currentPlayer == player1) {
            currentPlayer = player2;
        } else {
            currentPlayer = player1;
        }
    }

    public static void main(String[] args) {
        Game game = new Game();
        game.start();
    }
}
