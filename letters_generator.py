import os, sys
from PIL import Image, ImageDraw, ImageFont

# im = Image.open("pillow-logo.webp")
# print(im.format, im.size, im.mode)
# im.show()

# Funkcja generująca obrazy liter greckich
# Funkcja generująca obrazy liter greckich
def generate_greek_letter_images(letters, output_dir, img_size=(32, 32), num_samples=100):
    # Sprawdzenie, czy istnieje folder wyjściowy
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Dla każdej litery generujemy odpowiednią liczbę przykładów
    for letter in letters:
        letter_dir = os.path.join(output_dir, letter)
        if not os.path.exists(letter_dir):
            os.makedirs(letter_dir)

        for i in range(num_samples):
            # Tworzenie pustego obrazu o podanym rozmiarze
            img = Image.new('L', img_size, color=255)  # 'L' oznacza skalę szarości, białe tło (255)
            draw = ImageDraw.Draw(img)

            # Ładowanie domyślnej czcionki systemowej
            font = ImageFont.load_default()


            # Obliczenie pozycji tekstu przy użyciu textbbox()
            bbox = draw.textbbox((0, 0), letter, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]  # Wyznaczanie szerokości i wysokości

            # Obliczenie pozycji, aby wycentrować literę na obrazie
            position = ((img_size[0] - text_width) // 2, (img_size[1] - text_height) // 2)

            # Rysowanie litery na obrazie
            draw.text(position, letter, fill=0, font=font)  # Czarny tekst (fill=0)

            # Zapisanie obrazu
            img.save(os.path.join(letter_dir, f'{letter}_{i}.png'))

    print(f"Wygenerowano obrazy dla liter {', '.join(letters)} w katalogu {output_dir}")

# Lista liter greckich do wygenerowania
greek_letters = ['Α', 'Β', 'Γ', 'Δ', 'Φ']  # Alpha, Beta, Gamma, Delta, Phi

# Ścieżka do czcionki (można zmienić na własną ścieżkę do czcionki)
font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"  # Na Linux, dla innych systemów ścieżka może być inna

# Ścieżka do folderu, w którym zapisane zostaną wygenerowane obrazy
output_dir = "greek_letters_images"

# Generowanie 100 przykładów dla każdej litery greckiej (rozmiar obrazów 32x32)
generate_greek_letter_images(greek_letters, output_dir, img_size=(32, 32), num_samples=100)