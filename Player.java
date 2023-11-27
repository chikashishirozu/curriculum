public class Player {
    private int color;
    private String name;

    public Player(String name, int color) {
        this.name = name;
        this.color = color;
    }

    public int getColor() {
        return color;
    }

    public String getName() {
        return name;
    }

    public Piece play() {
        return new Piece(color);
    }
}
