import pygame
import sys

# Inisialisasi Pygame
pygame.init()

# Ukuran layar
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 300

# Warna
VINTAGE_DARK_BLUE = (43, 52, 64)
VINTAGE_LIGHT_BLUE = (112, 146, 190)
VINTAGE_DARK_RED = (152, 58, 54)
VINTAGE_LIGHT_RED = (203, 153, 126)
VINTAGE_LINE = (174, 166, 143)

# Inisialisasi layar
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe (Made by Egg)")  # Ganti nama di sini

# Variabel permainan
board = [['', '', ''], ['', '', ''], ['', '', '']]
current_player = 'X'
game_over = False
winner = None

# Fungsi untuk menggambar garis pemisah
def draw_lines():
    pygame.draw.line(screen, VINTAGE_LINE, (SCREEN_WIDTH // 3, 0), (SCREEN_WIDTH // 3, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, VINTAGE_LINE, (2 * SCREEN_WIDTH // 3, 0), (2 * SCREEN_WIDTH // 3, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, VINTAGE_LINE, (0, SCREEN_HEIGHT // 3), (SCREEN_WIDTH, SCREEN_HEIGHT // 3), 5)
    pygame.draw.line(screen, VINTAGE_LINE, (0, 2 * SCREEN_HEIGHT // 3), (SCREEN_WIDTH, 2 * SCREEN_HEIGHT // 3), 5)

# Fungsi untuk menggambar tanda "X" atau "O"
def draw_mark(row, col):
    font = pygame.font.Font(None, 100)
    if board[row][col] == 'X':
        text = font.render('X', True, VINTAGE_LIGHT_BLUE)
    elif board[row][col] == 'O':
        text = font.render('O', True, VINTAGE_LIGHT_RED)
    else:
        return

    text_rect = text.get_rect(center=(col * SCREEN_WIDTH // 3 + SCREEN_WIDTH // 6, row * SCREEN_HEIGHT // 3 + SCREEN_HEIGHT // 6))
    pygame.draw.rect(screen, VINTAGE_LINE, (col * SCREEN_WIDTH // 3, row * SCREEN_HEIGHT // 3, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3), 5)
    screen.blit(text, text_rect)

# Fungsi untuk mengecek kondisi kemenangan
def check_winner():
    global game_over, winner
    # Cek baris dan kolom
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            game_over = True
            winner = board[i][0]
            return
        if board[0][i] == board[1][i] == board[2][i] != '':
            game_over = True
            winner = board[0][i]
            return
    # Cek diagonal
    if board[0][0] == board[1][1] == board[2][2] != '':
        game_over = True
        winner = board[0][0]
        return
    if board[0][2] == board[1][1] == board[2][0] != '':
        game_over = True
        winner = board[0][2]
        return
    # Cek apakah ada sel kosong
    if all(all(cell != '' for cell in row) for row in board):
        game_over = True
        winner = None
        return

# Fungsi untuk menampilkan pesan kemenangan atau seri dengan animasi fade in dan fade out
def show_message(message, color):
    font = pygame.font.Font(None, 36)
    alpha = 0
    message_surface = font.render(message, True, (255, 255, 255))  # Warna teks putih
    message_rect = message_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    while alpha < 255:
        pygame.time.delay(10)
        alpha += 5
        message_surface.set_alpha(alpha)
        screen.fill(VINTAGE_DARK_BLUE)
        draw_lines()
        for row in range(3):
            for col in range(3):
                draw_mark(row, col)
        screen.blit(message_surface, message_rect)
        pygame.display.flip()

    pygame.time.delay(1000)

    while alpha > 0:
        pygame.time.delay(10)
        alpha -= 5
        message_surface.set_alpha(alpha)
        screen.fill(VINTAGE_DARK_BLUE)
        draw_lines()
        for row in range(3):
            for col in range(3):
                draw_mark(row, col)
        screen.blit(message_surface, message_rect)
        pygame.display.flip()

# Fungsi untuk menampilkan menu
def show_menu():
    font = pygame.font.Font(None, 36)
    title_text = font.render("Tic Tac Toe (by Egg)", True, (255, 255, 255))  # Ganti nama di sini
    start_button = pygame.Rect(50, 150, 200, 50)
    start_text = font.render("Start", True, (255, 255, 255))  # Ganti nama di sini

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if start_button.collidepoint(mouse_x, mouse_y):
                    return True

        # Bersihkan layar
        screen.fill(VINTAGE_DARK_BLUE)

        # Animasi efek hover pada tombol "Start"
        is_hovered = start_button.collidepoint(pygame.mouse.get_pos())
        hover_color = VINTAGE_LIGHT_RED if is_hovered else VINTAGE_DARK_RED

        # Gambar tombol start
        pygame.draw.rect(screen, hover_color, start_button)
        pygame.draw.rect(screen, VINTAGE_LINE, start_button, 5)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))
        screen.blit(start_text, (start_button.x + start_button.width // 2 - start_text.get_width() // 2, start_button.y + start_button.height // 2 - start_text.get_height() // 2))

        # Update layar
        pygame.display.flip()

# Fungsi utama
def main():
    while True:
        if not show_menu():
            break

        # Reset permainan
        global board, current_player, game_over, winner
        board = [['', '', ''], ['', '', ''], ['', '', '']]
        current_player = 'X'
        game_over = False
        winner = None

        # Loop utama permainan
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                    mouse_x, mouse_y = pygame.mouse.get_pos()
                    clicked_row = mouse_y // (SCREEN_HEIGHT // 3)
                    clicked_col = mouse_x // (SCREEN_WIDTH // 3)
                    if board[clicked_row][clicked_col] == '':
                        board[clicked_row][clicked_col] = current_player
                        current_player = 'O' if current_player == 'X' else 'X'
                        check_winner()

            # Bersihkan layar
            screen.fill(VINTAGE_DARK_BLUE)

            # Gambar garis pemisah
            draw_lines()

            # Gambar tanda "X" atau "O"
            for row in range(3):
                for col in range(3):
                    draw_mark(row, col)

            # Tampilkan pesan kemenangan atau seri
            if game_over:
                if winner:
                    show_message(f'Player {winner} Wins!', VINTAGE_LINE)
                else:
                    show_message('It\'s a Draw!', VINTAGE_LINE)
                break

            # Update layar
            pygame.display.flip()

# Jalankan permainan
if __name__ == "__main__":
    main()
