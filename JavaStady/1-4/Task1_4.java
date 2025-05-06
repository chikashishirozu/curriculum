/**
 * Task1-4: 課題内容
 *
 * ログイン機能をイメージして処理を書いてみましょう！
 * ・アカウント情報としてデータベースに登録されている情報
 * 　名前：alice
 * 　パスワード：alice123
 * 本課題では、すべての定数(合計６種類)を使いつつ、if文の使い方に慣れていきましょう！
 * 問① 〜 問⑤まで回答お願いします！
 *
 */
public class Task1_4 {

    // 定数（アカウント情報）
    // ① 登録されている名前（USER_NAME）とパスワード（USER_PASSWORD）を定数で定義してください。
    private static final String USER_NAME = "alice";
    private static final String USER_PASSWORD = "alice123";

    // 定数（メッセージ）
    private static final String CONST_MSG_SUCCESS = "ログイン成功です。";
    private static final String CONST_MSG_ERROR_NAME = "名前に誤りがあります。";
    private static final String CONST_MSG_ERROR_PASS = "パスワードに誤りがあります。";
    private static final String CONST_MSG_ERROR_INPUT = "入力情報に誤りがあります。";

    // 補足:
    //   定数は②〜⑤で使い回すために定義しておきます。
    //   final修飾子を付与すると、変数（動的に変わる値）ではなく、定数（変更不可な定まった値）となります。
    //   「ここへ記述」部分へ適当な値を記述しましょう。
    //   ※詳しくはJava2章にて紹介します。

    public static void main(String[] args) {
        // 以下の変数「name」「pass」を使用して、②〜⑤の条件を満たす処理を記述してください。
        // nameとpassはログイン画面からの入力値だと想定してみましょう。
         String name = "alice";
         String pass = "alice123";

        // ② 「name」の値が「USER_NAME」と等しく、「 pass 」の値が「USER_PASSWORD」と等しい場合。
        //      定数を使用して「 ログイン成功です 」と出力してください。
         if (name.equals(USER_NAME) && pass.equals(USER_PASSWORD)) {  
            System.out.println(CONST_MSG_SUCCESS);
		  	
        // ③ 「USER_NAME」の値のみ等しい場合。
        //     定数を使用して「 パスワードに誤りがあります。 」 と出力してください。
         } else if (name.equals(USER_NAME)) { 
            System.out.println(CONST_MSG_ERROR_PASS);
			
        // ④ 「USER_PASSWORD」の値のみ等しい場合。
        //定数を使用して「 名前に誤りがあります。 」と出力してください。
         } else if (pass.equals(USER_PASSWORD)) {
		    System.out.println(CONST_MSG_ERROR_NAME);
         
        // ⑤ 「USER_NAME」も「USER_PASSWORD」の値も間違っていた場合。 
        //定数を使用して「 入力情報に誤りがあります。 」と出力してください。
         } else {
		    System.out.println(CONST_MSG_ERROR_INPUT);
		 }
    }

}
