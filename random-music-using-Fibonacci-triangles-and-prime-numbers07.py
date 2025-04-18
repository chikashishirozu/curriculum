import pygame.midi
import time
import random

# 数列を生成する関数
def generate_triangle(limit):
    return [n * (n + 1) // 2 for n in range(1, limit + 1)]

def generate_fibonacci(limit):
    sequence = [0, 1]
    while len(sequence) < limit:
        sequence.append(sequence[-1] + sequence[-2])
    return sequence

def generate_primes(limit):
    primes = []
    num = 2
    while len(primes) < limit:
        if all(num % p != 0 for p in primes):
            primes.append(num)
        num += 1
    return primes

# 数列をMIDIノートに変換
def sequence_to_midi(sequence, min_note=21, max_note=108, offset=0):
    return [min_note + (num % (max_note - min_note + 1)) + offset for num in sequence]

# 音楽を再生する関数
def play_triangle_focused_music(triangle, fibonacci, primes, device_id, duration=1500):
    pygame.midi.init()
    try:
        player = pygame.midi.Output(device_id)

        # トライアングル数列はピアノ、中間オクターブ
        player.set_instrument(0)  # ピアノ
        triangle_notes = sequence_to_midi(triangle, offset=24)

        # フィボナッチ数列は低音域
        fibonacci_notes = sequence_to_midi(fibonacci, offset=12)

        # 素数列は高音域
        prime_notes = sequence_to_midi(primes, offset=36)

        start_time = time.time()
        while time.time() - start_time < duration:
            # ランダムに休符を入れる
            if random.random() < 0.2:  # 20%の確率で休符
                time.sleep(random.uniform(0.5, 1.0))  # 休符の長さ
                continue

            # トライアングル数列を中心に再生
            triangle_note = random.choice(triangle_notes)
            velocity = random.randint(100, 127)
            player.note_on(triangle_note, velocity)
            time.sleep(random.uniform(0.2, 0.4))  # トライアングルは早めのテンポ
            player.note_off(triangle_note, velocity)

            # フィボナッチ数列で背景リズムを追加
            if random.random() < 0.5:  # 50%の確率でフィボナッチを再生
                fibonacci_note = random.choice(fibonacci_notes)
                velocity = random.randint(60, 90)
                player.note_on(fibonacci_note, velocity)
                time.sleep(random.uniform(0.3, 0.5))
                player.note_off(fibonacci_note, velocity)

            # 素数列でアクセントを追加
            if random.random() < 0.3:  # 30%の確率で素数を再生
                prime_note = random.choice(prime_notes)
                velocity = random.randint(80, 100)
                player.note_on(prime_note, velocity)
                time.sleep(random.uniform(0.2, 0.4))
                player.note_off(prime_note, velocity)

    finally:
        player.close()
        pygame.midi.quit()

# メイン処理
if __name__ == "__main__":
    output_device_id = 2  # 使用するMIDIデバイスID
    num_terms = 50        # 数列の項数

    # 数列を生成
    triangle = generate_triangle(num_terms)
    fibonacci = generate_fibonacci(num_terms)
    primes = generate_primes(num_terms)

    # 3分間音楽を再生
    play_triangle_focused_music(triangle, fibonacci, primes, output_device_id)




