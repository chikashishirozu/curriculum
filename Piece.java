public class Piece {
    public static final int BLACK = 0;
    public static final int WHITE = 1;
    private int color;

    public Piece(int color) {
        this.color = color;
    }

    public int getColor() {
        return color;
    }

    public void flip() {
        if (color == BLACK) {
            color = WHITE;
        } else {
            color = BLACK;
        }
    }
}
