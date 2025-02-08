<?php
// データベースに接続する（接続情報は適切に設定すること）
$pdo = new PDO("mysql:host=localhost;dbname=bbsdatabase;charset=utf8mb4", "newuser", "J40AnzkvyrLA+H");

// エラーハンドリングとエラー表示を有効化
error_reporting(E_ALL);
ini_set('display_errors', 1);

// POSTリクエストを処理する
if ($_SERVER["REQUEST_METHOD"] === "POST") {
	if (isset($_POST["delete_id"])) {
		$delete_id = $_POST["delete_id"];
    
		// SQLインジェクション対策としてパラメータ化クエリを使用する
		$sql = "DELETE FROM bbs WHERE id = :delete_id";
		$stmt = $pdo->prepare($sql);
		$stmt->bindValue(":delete_id", $delete_id, PDO::PARAM_INT);
		$stmt->execute();
    
		// 削除が成功したら、同じページにリダイレクト
		header("Location: bbs.php");
		exit;
	}
    if (isset($_POST["content"]) && isset($_POST["user_name"])) {
        $content = $_POST["content"];
        $user_name = $_POST["user_name"];
        
        // SQLインジェクション対策としてパラメータ化クエリを使用する
        $sql = "INSERT INTO bbs (content, user_name, updated_at) VALUES (:content, :user_name, NOW())";
        $stmt = $pdo->prepare($sql);
        $stmt->bindValue(":content", $content, PDO::PARAM_STR);
        $stmt->bindValue(":user_name", $user_name, PDO::PARAM_STR);
        $stmt->execute();
        
		// データベースへの書き込みが成功したら、同じページにリダイレクト
		header("Location: bbs.php");
		exit;
    }
}

// データベースから投稿リストを取得する
$sql = "SELECT * FROM bbs ORDER BY updated_at DESC";
$stmt = $pdo->prepare($sql);
$stmt->execute();
$rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
?>

<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>ToDo掲示板</title>
    <!-- Bootstrap CDN -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-EVSTQN3/azprG1Anm3QDgpJLIm9Nao0Yz1ztcQTwFspd3yD65VohhpuuCOmLASjC" crossorigin="anonymous">
    <Link rel="shortcut icon" href="./favicon.ico/favicon.png" />
    <style type="text/css">
        /* 任意のスタイルを適用 */
        	div#main {
			padding: 30px;
			background-color: #efefef;
		}
		#a {
			margin: 5px 0 0 0;
		}
		#b {
			margin: 5px 0 10px 0;
			height: 300px;
		}
		#c {
			margin: 5px 0 0 0;		
		}
		#d {
			margin: 5px 0 10px 0;		
		}
		#e {
			margin: 10px 0 20px 0;			
		}
		#g {
			margin: 0;
		}
		#h {
			padding: 30px;
		}
		#i {
			width: 10%;
			box-sizing: border-box;
		}
		#j {
			width: 70%;
			box-sizing: border-box;
		}		
    </style>
</head>
<body>
    <div class="container">
        <div id="main">
            <h1>ToDo掲示板</h1>
            
            <!-- 投稿フォーム -->
            <div class="post-form">
                <h2>投稿フォーム</h2>
                <form class="form" action="bbs.php" method="post">
                    <div class="form-group">
                        <label class="control-label" id="a">投稿内容</label>
                        <textarea class="form-control" name="content" rows="5" id="b" required></textarea>
                    </div>
                    <div class="form-group">
                        <label class="control-label" id="c">投稿者</label>
                        <input class="form-control" type="text" name="user_name" id="d" required>
                    </div>
                    <button class="btn btn-primary" type="submit" id="e">送信</button>
                </form>
            </div>
            
            <!-- 発言リスト -->
            <div class="post-list">
                <h2>発言リスト</h2>
                <table class="table table-striped" id="h">
                    <thead>
                        <tr>
                            <th>id</th>
                            <th id="i">日時</th>
                            <th id="j">投稿内容</th>
                            <th>投稿者</th>
                            <th>削除</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($rows as $row): ?>
                            <tr>
                                <td><?= $row['id'] ?></td>
                                <td><?= $row['updated_at'] ?></td>
                                <td><?= htmlspecialchars($row['content']) ?></td>
                                <td><?= htmlspecialchars($row['user_name']) ?></td>
                                <td>
                                    <form action="bbs.php" method="post">
                                        <input type="hidden" name="delete_id" value="<?= $row["id"] ?>">
                                        <button class="btn btn-danger" type="submit">削除</button>
                                    </form>
                                </td>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js" integrity="sha384-IQsoLXl5PILFhosVNubq5LC7Qb9DXgDA9i+tQ8Zj3iwWAwPtgFTxbJ8NT4GN1R8p" crossorigin="anonymous"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/js/bootstrap.min.js" integrity="sha384-cVKIPhGWiC2Al4u+LWgxfKTRIcfu0JTxR+EQDz/bgldoEyl4H0zUF0QKbrJ0EcQF" crossorigin="anonymous"></script>
</body>
</html>


