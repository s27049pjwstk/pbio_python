#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Generator sekwencji nukleotydowych w formacie FASTA

Cel programu:
Program generuje losową sekwencję DNA składającą się z nukleotydów (A, C, G, T)
i zapisuje ją w formacie FASTA. Format FASTA jest standardowym formatem
używanym w bioinformatyce do przechowywania sekwencji nukleotydowych lub
aminokwasowych.

Kontekst zastosowania:
- Tworzenie danych testowych dla narzędzi bioinformatycznych
- Demonstracja obsługi plików FASTA w języku Python
- Analiza statystyczna losowych sekwencji DNA
- Nauka podstaw programowania w kontekście bioinformatyki

Wprowadzone ulepszenia:
- Podział na linie po 60 znaków zgodnie z FASTA
- Możliwość ustalenia wag dla nukleotydów
- Zapisywanie nowych sekwencji do istniejącego pliku
"""

import random
import os


def main():
    """
    Główna funkcja programu, która koordynuje zbieranie danych od użytkownika,
    generowanie sekwencji i zapis do pliku.
    """
    # Pobieranie danych wejściowych od użytkownika
    seq_length = get_sequence_length()  # Pobierz długość sekwencji
    seq_id = get_sequence_id()  # Pobierz ID sekwencji
    seq_description = get_sequence_description()  # Pobierz opis sekwencji
    user_name = get_user_name()  # Pobierz imię użytkownika

    # ORIGINAL:
    # # Generowanie losowej sekwencji DNA
    # dna_sequence = generate_dna_sequence(seq_length)
    # MODIFIED (Możliwość ustalenia wag dla nukleotydów):
    weights = get_nucleotide_weights()  # zapytaj i weź od użytkownika wagi
    dna_sequence = generate_dna_sequence(seq_length, weights)

    # Wstawienie imienia w losowe miejsce w sekwencji
    final_sequence = insert_name_into_sequence(dna_sequence, user_name)

    # Obliczanie statystyk sekwencji (tylko dla właściwej sekwencji DNA, bez imienia)
    stats = calculate_sequence_stats(dna_sequence)

    # ORIGINAL:
    # # Zapisanie sekwencji do pliku FASTA
    # filename = f"{seq_id}.fasta"
    # save_to_fasta(filename, seq_id, seq_description, final_sequence)
    # MODIFIED (Zapisywanie nowych sekwencji do istniejącego pliku):
    filename = f"{seq_id}.fasta"
    mode = 'w'  # default nadpisywanie

    if os.path.exists(filename):
        append_choice = input(f"Plik {filename} już istnieje. Czy chcesz dopisać sekwencję do istniejącego pliku? (t/n): ")
        if append_choice.lower() == 't':
            mode = 'a'  # tryb dopisywanie

    save_to_fasta(filename, seq_id, seq_description, final_sequence, mode)

    # Wyświetlenie statystyk sekwencji
    display_stats(stats, filename)


def get_sequence_length():
    """
    Pobiera od użytkownika długość sekwencji DNA.
    Weryfikuje, czy wprowadzona wartość jest liczbą całkowitą większą od 0.

    Returns:
        int: Długość sekwencji DNA
    """
    while True:
        try:
            length = int(input("Podaj długość sekwencji: "))
            if length <= 0:
                print("Długość sekwencji musi być liczbą większą od 0.")
                continue
            return length
        except ValueError:
            print("Wprowadź prawidłową liczbę całkowitą.")


def get_sequence_id():
    """
    Pobiera od użytkownika ID sekwencji.

    Returns:
        str: ID sekwencji
    """
    while True:
        seq_id = input("Podaj ID sekwencji: ").strip()
        if seq_id:  # Sprawdza, czy ID nie jest puste
            return seq_id
        print("ID sekwencji nie może być puste.")


def get_sequence_description():
    """
    Pobiera od użytkownika opis sekwencji.

    Returns:
        str: Opis sekwencji
    """
    return input("Podaj opis sekwencji: ")


def get_user_name():
    """
    Pobiera od użytkownika imię do wstawienia w sekwencji.

    Returns:
        str: Imię użytkownika
    """
    while True:
        name = input("Podaj imię: ").strip()
        if name:  # Sprawdza, czy imię nie jest puste
            return name
        print("Imię nie może być puste.")


# ORIGINAL:
# def generate_dna_sequence(length):
#     """
#     Generuje losową sekwencję DNA o podanej długości.
#
#     Args:
#         length (int): Długość sekwencji do wygenerowania
#
#     Returns:
#         str: Wygenerowana sekwencja DNA
#     """
#     # Lista nukleotydów w DNA
#     nucleotides = ['A', 'C', 'G', 'T']
#
#     # Generowanie losowej sekwencji przez wybieranie nukleotydów
#     sequence = ''.join(random.choice(nucleotides) for _ in range(length))
#
#     return sequence
# MODIFIED (Możliwość ustalenia wag dla nukleotydów):
def get_nucleotide_weights():
    """
    Pyta użytkownika czy chce ustalić wagi dla nukleotydów
    Jeśli tak, to pobiera te wagi od niego
    Zwraca albos wagi albo none
    """
    custom_weights = input("Czy chcesz ustalić wagi dla nukleotydów? (t/n): ").lower()

    if custom_weights == 't':
        weights = {}
        print("Podaj wagi dla poszczególnych nukleotydów (liczby większe od 0):")
        for nucleotide in ['A', 'C', 'G', 'T']:
            while True:
                try:
                    weight = float(input(f"Waga dla {nucleotide}: "))
                    if weight <= 0:
                        print("Waga musi być większa od 0.")
                        continue
                    weights[nucleotide] = weight
                    break
                except ValueError:
                    print("Wprowadź prawidłową liczbę.")
        return weights
    else:
        return None  # równe proporcje


def generate_dna_sequence(length, weights=None):
    """
    Generuje losową sekwencję DNA o podanej długości z możliwością kontrolowania wag nukleotydów.

    Args:
        length (int): Długość sekwencji do wygenerowania
        weights (dict, optional): wagi dla poszczególnych nukleotydów, jak none to równe

    Returns:
        str: Wygenerowana sekwencja DNA
    """
    # Lista nukleotydów w DNA
    nucleotides = ['A', 'C', 'G', 'T']

    if weights:
        # Generowanie losowej sekwencji z uwzględnieniem wag
        weights_list = [weights[n] for n in nucleotides]
        sequence = ''.join(random.choices(nucleotides, weights=weights_list, k=length))
    else:
        # Generowanie losowej sekwencji z równymi proporcjami
        sequence = ''.join(random.choice(nucleotides) for _ in range(length))

    return sequence

def insert_name_into_sequence(sequence, name):
    """
    Wstawia imię w losowe miejsce w sekwencji DNA.

    Args:
        sequence (str): Oryginalna sekwencja DNA
        name (str): Imię do wstawienia

    Returns:
        str: Sekwencja DNA z wstawionym imieniem
    """
    # Wybierz losową pozycję do wstawienia imienia
    position = random.randint(0, len(sequence))

    # Wstaw imię w wybrane miejsce
    final_sequence = sequence[:position] + name + sequence[position:]

    return final_sequence


def calculate_sequence_stats(sequence):
    """
    Oblicza statystyki sekwencji DNA.

    Args:
        sequence (str): Sekwencja DNA do analizy

    Returns:
        dict: Słownik zawierający statystyki sekwencji
    """
    # Inicjalizacja liczników dla poszczególnych nukleotydów
    counts = {'A': 0, 'C': 0, 'G': 0, 'T': 0}

    # Zliczanie wystąpień każdego nukleotydu
    for nucleotide in sequence:
        counts[nucleotide] += 1

    total_length = len(sequence)

    # Obliczanie procentowej zawartości każdego nukleotydu
    percentages = {
        nucleotide: (count / total_length) * 100
        for nucleotide, count in counts.items()
    }

    # Obliczanie stosunku CG do AT
    cg_content = (counts['C'] + counts['G']) / total_length * 100

    return {
        'percentages': percentages,
        'cg_content': cg_content
    }


# ORIGINAL:
# def save_to_fasta(filename, seq_id, description, sequence):
#     """
#     Zapisuje sekwencję DNA do pliku w formacie FASTA.
#
#     Args:
#         filename (str): Nazwa pliku do zapisu
#         seq_id (str): ID sekwencji
#         description (str): Opis sekwencji
#         sequence (str): Sekwencja DNA do zapisu
#     """
#     with open(filename, 'w') as f:
#         # Zapisz nagłówek FASTA
#         header = f">{seq_id}"
#         if description:
#             header += f" {description}"
#         f.write(header + "\n")
#
#         # Zapisz sekwencję, można również dodać łamanie linii co 80 znaków
#         f.write(sequence + "\n")
# MODIFIED (Podział na linie po 60 znaków zgodnie z FASTA oraz Zapisywanie nowych sekwencji do istniejącego pliku):
def save_to_fasta(filename, seq_id, description, sequence, mode='w'):
    """
    Zapisuje sekwencję DNA do pliku w formacie FASTA.

    Args:
        filename (str): Nazwa pliku do zapisu
        seq_id (str): ID sekwencji
        description (str): Opis sekwencji
        sequence (str): Sekwencja DNA do zapisu
        mode (str): Tryb zapisywania ('w' - nadpisywanie, 'a' - dopisywanie)
    """
    with open(filename, mode) as f:
        # Zapisz nagłówek FASTA
        header = f">{seq_id}"
        if description:
            header += f" {description}"
        f.write(header + "\n")

        # Podział sekwencji na linie po 60 znaków
        line_length = 60
        for i in range(0, len(sequence), line_length):
            line = sequence[i:i + line_length]
            f.write(line + "\n")


def display_stats(stats, filename):
    """
    Wyświetla statystyki sekwencji DNA.

    Args:
        stats (dict): Słownik zawierający statystyki sekwencji
        filename (str): Nazwa pliku, do którego zapisano sekwencję
    """
    percentages = stats['percentages']
    cg_content = stats['cg_content']

    print(f"\nSekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")

    # Wyświetlanie procentowej zawartości każdego nukleotydu
    for nucleotide, percentage in percentages.items():
        print(f"{nucleotide}: {percentage:.1f}%")

    # Wyświetlanie zawartości par CG
    print(f"%CG: {cg_content:.1f}")


if __name__ == "__main__":
    main()
