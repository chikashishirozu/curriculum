*>条件判断（２）
IDENTIFICATION DIVISION.
PROGRAM-ID. SAMPLE_10.

ENVIRONMENT DIVISION.

DATA DIVISION.
WORKING-STORAGE SECTION.
01 TEN PIC 9(3).

PROCEDURE DIVISION.
MAIN.
	DISPLAY "点数を入力"
	ACCEPT TEN
	IF TEN >= 70 THEN
		DISPLAY "合格"
	ELSE
		DISPLAY "不合格"
	END-IF
	STOP RUN.
