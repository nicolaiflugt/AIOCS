import streamlit as st
import math
import pandas as pd

# Morse code dictionary, including Danish letters
MORSE_CODE_DICT = {
    'A': '.-',    'B': '-...',  'C': '-.-.',  'D': '-..',   'E': '.',
    'F': '..-.',  'G': '--.',   'H': '....',  'I': '..',    'J': '.---',
    'K': '-.-',   'L': '.-..',  'M': '--',    'N': '-.',    'O': '---',
    'P': '.--.',  'Q': '--.-',  'R': '.-.',   'S': '...',   'T': '-',
    'U': '..-',   'V': '...-',  'W': '.--',   'X': '-..-',  'Y': '-.--',
    'Z': '--..',
    '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-',
    '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.',
    'Æ': '.-.-',  'Ø': '---.',  'Å': '.--.-'
}
REVERSE_MORSE_CODE_DICT = {v: k for k, v in MORSE_CODE_DICT.items()}

danish_alphabet = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'X', 'Y', 'Z', 'Æ', 'Ø', 'Å'
]

# Tastatur mapping til SMS-kode
SMS_KEYPAD = {
    'A': '2', 'B': '22', 'C': '222',
    'D': '3', 'E': '33', 'F': '333',
    'G': '4', 'H': '44', 'I': '444',
    'J': '5', 'K': '55', 'L': '555',
    'M': '6', 'N': '66', 'O': '666',
    'P': '7', 'Q': '77', 'R': '777', 'S': '7777',
    'T': '8', 'U': '88', 'V': '888',
    'W': '9', 'X': '99', 'Y': '999', 'Z': '9999',
    # Æ, Ø, Å håndteres før som AE, OE, AA
}

FRIMURER_BILLEDE_URL = "https://friluftsaktiviteter.dk/wp-content/uploads/2018/10/Frimurer-kode-Hjemmeside-e1541487806703.jpg"

# New alphabet specifically for 100P code (same letters, but separate variable)
danish_alphabet_2 = [
    'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
    'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
    'Æ', 'Ø', 'Å'
]

# Build the polybius table using danish_alphabet_2
rows_100p = ['P', 'O', 'I', 'N', 'T']
cols_100p = ['1', '2', '3', '4', '5', '6']

polybius_100p = {}
index = 0
for r in rows_100p:
    for c in cols_100p:
        if index < len(danish_alphabet_2):
            polybius_100p[danish_alphabet_2[index]] = r + c
            index += 1

reverse_polybius_100p = {v: k for k, v in polybius_100p.items()}

def encode_to_morse(text):
    encoded_words = []
    for word in text.upper().split():
        encoded_letters = []
        for char in word:
            if char in MORSE_CODE_DICT:
                encoded_letters.append(MORSE_CODE_DICT[char])
            else:
                encoded_letters.append('?')
        encoded_words.append('/'.join(encoded_letters))
    return '//'.join(encoded_words)
def decode_from_morse(morse_code):
    decoded_words = []
    words = morse_code.strip().split('//')
    for word in words:
        decoded_letters = []
        letters = word.strip().split('/')
        for letter in letters:
            decoded_letters.append(REVERSE_MORSE_CODE_DICT.get(letter.strip(), '?'))
        decoded_words.append(''.join(decoded_letters))
    return ' '.join(decoded_words)

def rot_x_encode(text, offset):
    result = ''
    for char in text.upper():
        if char in danish_alphabet:
            index = danish_alphabet.index(char)
            new_index = (index + offset) % len(danish_alphabet)
            result += danish_alphabet[new_index]
        else:
            result += char
    return result
def rot_x_decode(text, offset):
    result = ''
    for char in text.upper():
        if char in danish_alphabet:
            index = danish_alphabet.index(char)
            new_index = (index - offset) % len(danish_alphabet)
            result += danish_alphabet[new_index]
        else:
            result += char
    return result

def alpha_num_encode(text):
    encoded = []
    for char in text.upper():
        if char == ' ':
            encoded.append(' ')
        elif char in danish_alphabet:
            encoded.append(str(danish_alphabet.index(char) + 1))
        else:
            encoded.append('?')
    return ' '.join(encoded)
def alpha_num_decode(code):
    decoded = []
    for token in code.strip().split():
        if token.isdigit():
            idx = int(token) - 1
            if 0 <= idx < len(danish_alphabet):
                decoded.append(danish_alphabet[idx])
            else:
                decoded.append('?')
        else:
            decoded.append('?')
    return ''.join(decoded)

def keyword_cipher_setup(keyword):
    reduced_alphabet = [c for c in danish_alphabet if c != 'W']
    keyword_unique = []
    seen = set()
    for char in keyword.upper():
        if char in reduced_alphabet and char not in seen:
            seen.add(char)
            keyword_unique.append(char)
    remaining_letters = [c for c in reduced_alphabet if c not in seen]
    full_sequence = keyword_unique + remaining_letters

    # Hvis ulige antal bogstaver, tilføj tom plads for at få lige rækker
    if len(full_sequence) % 2 != 0:
        full_sequence.append('')

    mid = math.ceil(len(full_sequence) / 2)  # øverste række får evt. ét bogstav ekstra
    top_row = full_sequence[:mid]
    bottom_row = full_sequence[mid:]
    return top_row, bottom_row

def kodeordskode_encode(text, keyword):
    top_row, bottom_row = keyword_cipher_setup(keyword)
    result = ''
    text = text.upper()
    for char in text:
        if char in top_row:
            idx = top_row.index(char)
            if idx < len(bottom_row):
                result += bottom_row[idx]
            else:
                result += char
        elif char in bottom_row:
            idx = bottom_row.index(char)
            if idx < len(top_row):
                result += top_row[idx]
            else:
                result += char
        else:
            # Bevar mellemrum og andre tegn som de er
            result += char
    return result.lower()
def kodeordskode_decode(text, keyword):
    # Kodning og afkodning er symmetrisk
    # Kan derfor bruge samme funktion
    # Brug uppercase for at finde bogstaverne, output med små bogstaver for læsbarhed
    return kodeordskode_encode(text, keyword)

def display_two_row_table(row1, row2):
    html = "<table style='border-collapse: collapse;'>"
    html += "<tr>"
    for cell in row1:
        html += f"<td style='border: 1px solid black; padding:5px; text-align:center;'>{cell}</td>"
    html += "</tr><tr>"
    for cell in row2:
        html += f"<td style='border: 1px solid black; padding:5px; text-align:center;'>{cell}</td>"
    html += "</tr></table>"
    st.markdown(html, unsafe_allow_html=True)

def sms_encode(text):
    text = text.upper()
    # Erstat Æ Ø Å med AE OE AA
    text = text.replace('Æ', 'AE').replace('Ø', 'OE').replace('Å', 'AA')
    encoded = []
    for char in text:
        if char == ' ':
            encoded.append(' ')  # mellemrum beholdes
        elif char in SMS_KEYPAD:
            encoded.append(SMS_KEYPAD[char])
        else:
            encoded.append('?')
    return ' '.join(encoded)
def sms_decode(code):
    # Afkoder SMS-kode - forenklet: antager mellemrum mellem bogstaver
    decoded = []
    for token in code.strip().split():
        # find bogstav ved at tælle længden af token og tallet
        if not token:
            decoded.append(' ')
            continue
        digit = token[0]
        length = len(token)
        # find bogstav der matcher tal og længde
        match = '?'
        for letter, seq in SMS_KEYPAD.items():
            if seq == digit * length:
                match = letter
                break
        decoded.append(match)
    decoded_text = ''.join(decoded)
    # Erstat AE OE AA tilbage til Æ Ø Å
    decoded_text = decoded_text.replace('AE', 'Æ').replace('OE', 'Ø').replace('AA', 'Å')
    return decoded_text

def encode_100p(text):
    text = text.upper()
    encoded = []
    for char in text:
        if char == ' ':
            encoded.append(' ')
        elif char in polybius_100p:
            encoded.append(polybius_100p[char])
        else:
            encoded.append('?')
    return ' '.join(encoded)
def decode_100p(code):
    code = code.upper().strip()
    decoded = []
    tokens = code.split()
    for token in tokens:
        if token == '':
            decoded.append(' ')
        elif token in reverse_polybius_100p:
            decoded.append(reverse_polybius_100p[token])
        else:
            decoded.append('?')
    return ''.join(decoded)

def int_to_roman(num):
    val = [
        1000, 900, 500, 400,
        100, 90, 50, 40,
        10, 9, 5, 4,
        1
    ]
    syms = [
        "M", "CM", "D", "CD",
        "C", "XC", "L", "XL",
        "X", "IX", "V", "IV",
        "I"
    ]
    roman_num = ''
    i = 0
    while num > 0:
        for _ in range(num // val[i]):
            roman_num += syms[i]
            num -= val[i]
        i += 1
    return roman_num
def roman_to_int(s):
    roman_dict = {'I': 1, 'V': 5, 'X': 10, 'L': 50, 'C': 100, 'D': 500, 'M': 1000}
    i = 0
    num = 0
    while i < len(s):
        if i+1 < len(s) and roman_dict[s[i]] < roman_dict[s[i+1]]:
            num += roman_dict[s[i+1]] - roman_dict[s[i]]
            i += 2
        else:
            num += roman_dict[s[i]]
            i += 1
    return num

def encode_roversprog(text):
    vowels = "AEIOUYÆØÅaeiouyæøå"
    result = ""
    for char in text:
        if char.lower() not in vowels and char.isalpha():
            # konsonant: indsæt c + "o" + c (samme bogstav som konsonant)
            result += char + "o" + char.lower()
        else:
            # vokal eller andet: behold som det er
            result += char
    return result
def decode_roversprog(text):
    vowels = "AEIOUYÆØÅaeiouyæøå"
    result = ""
    i = 0
    while i < len(text):
        c = text[i]
        if c.lower() not in vowels and c.isalpha():
            # Forvent mønster: c o c
            if i + 2 < len(text) and text[i+1].lower() == "o" and text[i+2].lower() == c.lower():
                result += c
                i += 3
            else:
                # Hvis ikke mønsteret passer, behold bogstavet som det er
                result += c
                i += 1
        else:
            result += c
            i += 1
    return result

def binærkode_tabel(text, encode=True):
    # Tabel som dictionary
    tabel = {
        'A': '0000 0000', 'B': '0000 0001', 'C': '0000 0010', 'D': '0000 0011',
        'E': '0000 0100', 'F': '0000 0101', 'G': '0000 0110', 'H': '0000 0111',
        'I': '0000 1000', 'J': '0000 1001', 'K': '0000 1010', 'L': '0000 1011',
        'M': '0000 1100', 'N': '0000 1101', 'O': '0000 1110', 'P': '0000 1111',
        'Q': '0001 0000', 'R': '0001 0001', 'S': '0001 0010', 'T': '0001 0011',
        'U': '0001 0100', 'V': '0001 0101', 'W': '0001 0110', 'X': '0001 0111',
        'Y': '0001 1000', 'Z': '0001 1001', 'Æ': '0001 1010', 'Ø': '0001 1011', 'Å': '0001 1100'
    }

    if encode:
        # Encoder tekst til binær
        result = []
        for char in text.upper():
            if char in tabel:
                result.append(tabel[char])
            elif char == ' ':
                result.append(' ')  # adskiller ord
            else:
                result.append('?')  # Ukendt tegn
        return ' | '.join(result)
    else:
        # Decoder binær til tekst
        reverse_table = {v: k for k, v in tabel.items()}

        # Fjern evt. whitespaces og split ved både | og mellemrum
        blocks = []
        if '|' in text:
            # Hvis brugeren har brugt |, så brug det som separator
            blocks = [b.strip() for b in text.split('|') if b.strip()]
        else:
            # Ellers split på grupper af 9 tegn (8 bit + 1 space)
            raw = text.replace('\n', ' ').replace('\r', ' ')
            raw = raw.strip()
            while raw:
                block = raw[:9].strip()
                blocks.append(block)
                raw = raw[9:].strip()

        decoded_text = ""
        for block in blocks:
            if block == '':
                decoded_text += ' '
                continue
            if block in reverse_table:
                decoded_text += reverse_table[block]
            else:
                decoded_text += '?'
        return decoded_text

def vigenere_kode(text, nøgle, encode=True, alphabet=danish_alphabet_2):
    result = ""
    nøgle = nøgle.upper()
    n = len(nøgle)
    for i, char in enumerate(text.upper()):
        if char in alphabet:
            tekst_idx = alphabet.index(char)
            nøgle_idx = alphabet.index(nøgle[i % n])
            if encode:
                ny_idx = (tekst_idx + nøgle_idx) % len(alphabet)
            else:
                ny_idx = (tekst_idx - nøgle_idx) % len(alphabet)
            result += alphabet[ny_idx]
        else:
            result += char
    return result


    text = text.upper()
    square = create_polybius_square()
    sektorer = [text[i:i+5] for i in range(0, len(text), 5)]
    result = ""

    for sektor in sektorer:
        coords = [letter_to_coords(c, square) for c in sektor if c.isalpha()]
        coords = [c for c in coords if c is not None]

        # Opdel koordinaterne i to lige store dele: første halvdel = rækker, anden halvdel = kolonner
        half_len = len(coords) // 2

        rækker = coords[:half_len]
        kolonner = coords[half_len:]

        # Hvis ulige antal bogstaver, håndter sidste koordinat
        if len(coords) % 2 != 0:
            # Sidste koordinat er delt i to tal, så tilføj begge tal til rækker og kolonner
            sidste = coords[half_len]
            rækker.append((sidste[0],))
            kolonner.append((sidste[1],))

        # Flad rækker og kolonner ud til talrækkefølge som par
        # Nogle gange kan sidste element være tuple med 1 element - fix det:
        rækker_flat = []
        for r in rækker:
            if isinstance(r, tuple) and len(r) == 1:
                rækker_flat.append(r[0])
            else:
                rækker_flat.append(r[0])
        kolonner_flat = []
        for k in kolonner:
            if isinstance(k, tuple) and len(k) == 1:
                kolonner_flat.append(k[0])
            else:
                kolonner_flat.append(k[1])

        nye_coords = list(zip(rækker_flat, kolonner_flat))

        # Oversæt koordinater tilbage til bogstaver
        nye_bogstaver = [coords_to_letter(c, square) for c in nye_coords]

        result += "".join(nye_bogstaver)

    return result

def create_polybius_square():
    # 5x5 firkant uden Æ, Ø, Å - I/J på samme plads
    return [
        ['A','B','C','D','E'],
        ['F','G','H','I','K'],
        ['L','M','N','O','P'],
        ['Q','R','S','T','U'],
        ['V','W','X','Y','Z']
    ]
def letter_to_coords(letter, square):
    letter = letter.upper()
    if letter == 'J':  # I/J deler plads
        letter = 'I'
    for row_idx, row in enumerate(square):
        if letter in row:
            return (row_idx + 1, row.index(letter) + 1)
    return None
def coords_to_letter(coords, square):
    row, col = coords
    return square[row - 1][col - 1]
def bifid_encode(text):
    text = text.upper().replace('J', 'I')
    square = create_polybius_square()
    # Del teksten op i sektorer af max 5 bogstaver
    sektorer = [text[i:i+5] for i in range(0, len(text), 5)]
    result = ""

    for sektor in sektorer:
        # Find koordinater for hvert bogstav i sektoren
        coords = [letter_to_coords(c, square) for c in sektor if c.isalpha()]
        # Split koordinater i rækker og kolonner
        rækker = [r for r, c in coords]
        kolonner = [c for r, c in coords]
        # Kombiner rækker og kolonner i en ny række tal
        nye_tal = rækker + kolonner
        # Del op i nye koordinater (2 og 2 tal)
        nye_coords = [(nye_tal[i], nye_tal[i + 1]) for i in range(0, len(nye_tal), 2)]
        # Oversæt nye koordinater til bogstaver
        nye_bogstaver = [coords_to_letter(coord, square) for coord in nye_coords]
        result += "".join(nye_bogstaver)

    return result
def bifid_decode(text):
    text = text.upper().replace('J', 'I')
    square = create_polybius_square()
    sektorer = [text[i:i+5] for i in range(0, len(text), 5)]
    result = ""

    for sektor in sektorer:
        coords = [letter_to_coords(c, square) for c in sektor if c.isalpha()]
        # Alle koordinater som tal i rækkefølge
        tal = []
        for r, c in coords:
            tal.append(r)
            tal.append(c)

        # Halvér listen
        halv = len(tal) // 2
        # Første halvdel er rækker, anden halvdel er kolonner
        rækker = tal[:halv]
        kolonner = tal[halv:]

        # Hvis ulige antal bogstaver, kan der være ét ekstra tal til kolonner
        # Hvis det sker, fyldes rækker op tilsvarende
        if len(kolonner) < len(rækker):
            kolonner.append(tal[-1])

        # Saml nye koordinater parvis
        nye_coords = list(zip(rækker, kolonner))

        # Oversæt til bogstaver
        nye_bogstaver = [coords_to_letter(c, square) for c in nye_coords]
        result += "".join(nye_bogstaver)

    return result

def bacon_code_encode(plaintext, covertext):
    bacon_dict = {
        'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB',
        'E': 'AABAA', 'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB',
        'I': 'ABAAA', 'J': 'ABAAA',
        'K': 'ABAAB', 'L': 'ABABA', 'M': 'ABABB', 'N': 'ABBAA',
        'O': 'ABBAB', 'P': 'ABBBA', 'Q': 'ABBBB', 'R': 'BAAAA',
        'S': 'BAAAB', 'T': 'BAABA', 'U': 'BAABB', 'V': 'BAABB',
        'W': 'BABAA', 'X': 'BABAB', 'Y': 'BABBA', 'Z': 'BABBB'
    }
    plaintext = plaintext.upper().replace(" ", "")  # Fjern mellemrum i plaintext

    code = ""
    for char in plaintext:
        if char in bacon_dict:
            code += bacon_dict[char]
        else:
            code += 'AAAAA'  # ukendt tegn som AAAAA

    if len(covertext) < len(code):
        return "FEJL: Fyldteksten skal være mindst lige så lang som Bacon-koden (uden mellemrum)."

    # Skjul Bacon-koden i fyldteksten med små og store bogstaver:
    # 'A' i koden = små bogstaver i covertext, 'B' = store bogstaver
    result_chars = list(covertext)  # konverter til liste så vi kan ændre bogstaver

    # Brug kun de nødvendige antal bogstaver fra fyldteksten til kodning
    j = 0  # index i code
    for i in range(len(result_chars)):
        if j >= len(code):
            break
        if result_chars[i].isalpha():  # kun bogstaver tæller i fyldtekst
            if code[j] == 'A':
                result_chars[i] = result_chars[i].lower()
            else:
                result_chars[i] = result_chars[i].upper()
            j += 1
        else:
            # ikke-bogstav lader vi være som de er
            pass

    # resten af fyldteksten lader vi være uberørt
    return "".join(result_chars)
def bacon_code_decode(code_text):
    bacon_dict = {
        'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB',
        'E': 'AABAA', 'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB',
        'I': 'ABAAA', 'J': 'ABAAA',
        'K': 'ABAAB', 'L': 'ABABA', 'M': 'ABABB', 'N': 'ABBAA',
        'O': 'ABBAB', 'P': 'ABBBA', 'Q': 'ABBBB', 'R': 'BAAAA',
        'S': 'BAAAB', 'T': 'BAABA', 'U': 'BAABB', 'V': 'BAABB',
        'W': 'BABAA', 'X': 'BABAB', 'Y': 'BABBA', 'Z': 'BABBB'
    }
    reverse_dict = {v: k for k, v in bacon_dict.items()}

    # Oversæt input tekst til 'A' og 'B' baseret på små (a) og store (b) bogstaver
    code = ""
    for c in code_text:
        if c.isalpha():
            if c.islower():
                code += 'A'
            else:
                code += 'B'

    # Split i grupper af 5
    result = ""
    for i in range(0, len(code), 5):
        block = code[i:i+5]
        if len(block) < 5:
            break
        if block in reverse_dict:
            # I/J og U/V håndteres som I og U
            letter = reverse_dict[block]
            if letter == 'J':
                letter = 'I'
            if letter == 'V':
                letter = 'U'
            result += letter
        else:
            result += '?'
    return result
    bacon_dict = {
        'A': 'AAAAA', 'B': 'AAAAB', 'C': 'AAABA', 'D': 'AAABB',
        'E': 'AABAA', 'F': 'AABAB', 'G': 'AABBA', 'H': 'AABBB',
        'I': 'ABAAA', 'J': 'ABAAA',  # I/J deler kode
        'K': 'ABAAB', 'L': 'ABABA', 'M': 'ABABB', 'N': 'ABBAA',
        'O': 'ABBAB', 'P': 'ABBBA', 'Q': 'ABBBB', 'R': 'BAAAA',
        'S': 'BAAAB', 'T': 'BAABA', 'U': 'BAABB', 'V': 'BAABB',  # U/V deler kode
        'W': 'BABAA', 'X': 'BABAB', 'Y': 'BABBA', 'Z': 'BABBB'
    }
    if encode:
        text = text.upper()
        result = []
        for char in text:
            if char in bacon_dict:
                result.append(bacon_dict[char])
            elif char == ' ':
                result.append(' ')  # bevare mellemrum
            else:
                result.append('?')
        return ' '.join(result)
    else:
        # Decode - split i grupper af 5 tegn
        text = text.replace(' ', '')
        result = ""
        for i in range(0, len(text), 5):
            block = text[i:i+5]
            if len(block) < 5:
                break
            # Find bogstav med match i bacon_dict
            for k, v in bacon_dict.items():
                if v == block:
                    # Undgå dobbeltbogstaver (I/J og U/V) - altid brug I eller U
                    if k in ['J', 'V']:
                        result += k.replace('J', 'I').replace('V', 'U')
                    else:
                        result += k
                    break
            else:
                result += '?'
        return result


# Streamlit app
st.title("Kodesamling")

method = st.selectbox("Vælg metode:", ("Morsekode", "ROT-X", "Alfa-Nr.", "Kodeordskode", "Frimurerkode", "100P-koden", "Romertal", "Tastaturkode", "Bogkoden", "Kinesisk skrift", "Røversprog", "Punktskrift", "Semaforkode", "Binærkode", "Vigenère", "Bifid", "Baconkode"))



if method == "Morsekode":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    user_input = st.text_area("Indtast tekst eller morsekode:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = encode_to_morse(user_input)
            st.text_area("Kodet output:", result)
        else:
            result = decode_from_morse(user_input)
            st.text_area("Afkodet output:", result)

    # Vis morsekode-tabel billede nederst, skaleret til fuld bredde
    st.markdown("---")
    st.image("https://simplecode.dk/wp-content/uploads/2020/04/Morsen%C3%B8gle.png", use_container_width=True)

elif method == "ROT-X":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    key_letter = st.text_input("Indtast nøglebogstav (A-Å):").upper()
    offset = danish_alphabet.index(key_letter) if key_letter in danish_alphabet else 0
    user_input = st.text_area("Indtast tekst:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = rot_x_encode(user_input, offset)
            st.text_area("Kodet output:", result)
        else:
            result = rot_x_decode(user_input, offset)
            st.text_area("Afkodet output:", result)

elif method == "Alfa-Nr.":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    user_input = st.text_area("Indtast tekst eller kode:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = alpha_num_encode(user_input)
            st.text_area("Kodet output:", result)
        else:
            result = alpha_num_decode(user_input)
            st.text_area("Afkodet output:", result)

    # Divider alfabet i to med lige mange bogstaver, vis som to tabeller side om side
    split_index = math.ceil(len(danish_alphabet) / 2)
    first_half = danish_alphabet[:split_index]
    second_half = danish_alphabet[split_index:]

    # Første tabel
    header_row_1 = "| " + " | ".join(first_half) + " |"
    separator_row_1 = "|" + "|".join(["---"] * len(first_half)) + "|"
    number_row_1 = "| " + " | ".join([str(i+1) for i in range(len(first_half))]) + " |"
    st.markdown(f"{header_row_1}\n{separator_row_1}\n{number_row_1}")

    # Anden tabel
    header_row_2 = "| " + " | ".join(second_half) + " |"
    separator_row_2 = "|" + "|".join(["---"] * len(second_half)) + "|"
    number_row_2 = "| " + " | ".join([str(i+split_index+1) for i in range(len(second_half))]) + " |"
    st.markdown(f"{header_row_2}\n{separator_row_2}\n{number_row_2}")

elif method == "Kodeordskode":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    keyword = st.text_input("Indtast kodeord (brug A-Å, uden W):", value="SJAK").upper()
    user_input = st.text_area("Indtast tekst:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = kodeordskode_encode(user_input, keyword)
            st.text_area("Kodet output:", result)
        else:
            result = kodeordskode_decode(user_input, keyword)
            st.text_area("Afkodet output:", result)

    # Lav og vis tabel med to rækker: øverste og nederste række i kodeordskoden
    top_row, bottom_row = keyword_cipher_setup(keyword)

    # Juster længder for visning (fyld med tomme strenge hvis nødvendigt)
    max_len = max(len(top_row), len(bottom_row))
    top_row += [''] * (max_len - len(top_row))
    bottom_row += [''] * (max_len - len(bottom_row))

    df = pd.DataFrame([top_row, bottom_row])
    # Vis uden index og kolonne-headers
    display_two_row_table(top_row, bottom_row)

elif method == "SMS-kode":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    user_input = st.text_area("Indtast tekst eller kode:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = sms_encode(user_input)
            st.text_area("Kodet output:", result)
        else:
            result = sms_decode(user_input)
            st.text_area("Afkodet output:", result)

elif method == "Frimurerkode":
    st.header("Frimurerkode")

    st.image(FRIMURER_BILLEDE_URL, use_container_width=True)
    
    st.markdown("---")
    tekst = st.text_area("Skriv dine resultater her:", height=200)

elif method == "100P-koden":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    user_input = st.text_area("Indtast tekst eller kode:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = encode_100p(user_input)
            st.text_area("Kodet output:", result)
        else:
            result = decode_100p(user_input)
            st.text_area("Afkodet output:", result)

elif method == "Romertal":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    user_input = st.text_input("Indtast tal (for kod) eller romertal (for afkod):").upper()
    if st.button("Udfør"):
        if mode == "Kod":
            if user_input.isdigit():
                result = int_to_roman(int(user_input))
            else:
                result = "Indtast et gyldigt heltal."
            st.text_area("Kodet output:", result)
        else:  # Afkod
            try:
                result = str(roman_to_int(user_input))
            except KeyError:
                result = "Ugyldigt romertal."
            st.text_area("Afkodet output:", result)

elif method == "Tastaturkode":
    st.image(
        "https://cdn.shopify.com/s/files/1/0810/3669/files/danish-windows-keyboard-layout-keyshorts_1024x1024.png?3916",
        use_container_width=True
    )

    result_input = st.text_area("Skriv din kode eller tekst her:")

elif method == "Bogkoden":
    st.markdown("""
    Med bogkode kan man sende beskeder til
    andre, som har den samme bog/tekst, som du
    har. Det er vigtigt at have fat i den rigtige bog
    eller tekst, når man skal løse en bogkode.
    Der findes to variationer af koden. I den ene
    skal man finde hele ord, og i den anden skal
    man kun finde bogstaver. For begge variationer
    gælder, at man får en række tal, som man kan
    omdanne til bogstaver ved at tælle sig frem:

    **Bogkode med ord**  
    Her vil de tre talkombinationer betyde at du
    skal finde sidetal, linje, ord, i nævnte rækkefølge.  
    Således ville 24,12,3 være side 24 i en bog,  
    12. linje på siden og tredje ord på linjen.

    **Bogkode med bogstaver**  
    Her vil de tre talkombinationer betyde at du
    skal finde sidetal, linje, bogstav.  
    Med denne variation vil 24,12,3 være side 24,  
    12. linje på siden og 3. bogstav i denne linje.

    Det handler om at prøve sig frem. Hvis der er
    mange talkombinationer er det oftest
    bogstavvariationen, mens det ved færre
    talkombinationer oftest er ordvariationen.

    **Eksempler på bogkoden:**  
    _Kampklar i København_  
    i jagten på point,  
    VM-viljen i sving.  
    Flammen er tændt, gnisterne glimter,  
    patruljen er spændt, sejren vi skimter.  
    Til VM i glæde og gejst  
    Vi leger for livet  
    til VM i leg,  
    kæmper i vildskab og venskab.  
    Fri konkurrence i fri fantasi,  
    skaber verdensmestre i  
    Væbnermesterskaberi

    Bogkode med ord vil følgende:  
    1,5,1 1,4,2 2,5,2  
    blive til  
    “Patruljen er verdensmestre”

    Bogkode med bogstaver vil følgende:  
    2,5,1 1,1,1 1,4,3 2,1,3  
    1,6,10 1,5,5  
    1,1,3 1,1,13 1,4,13  
    1,2,8 1,2,9  
    2,2,4 2,2,5  
    blive til “skal du med på vm”
    """)

elif method == "Kinesisk skrift":
    st.markdown("""
    Kinesisk skrift er teksten skrevet bagfra. Altså
    hvor du staver ordet med det sidste bogstav
    først og så videre. Ordene står oftest stadig på
    deres normale plads i en tekst.  
                
    Man kan variere den ved at indsætte nye
    mellemrum eller helt slette mellemrummene. 
                 
    Man kan kende koden på, at der kan være store
    bogstaver sidst i sætninger, i stedet for først.  
    Desuden bruger den meget almindelige
    bogstaver, men det hele er volapyk.  
                
    Ordet ”Tophemmeligt” bliver fx til:  
    ”tgilemme hpoT”
    """)

elif method == "Røversprog":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    user_input = st.text_area("Indtast tekst:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = encode_roversprog(user_input)
            st.text_area("Kodet output:", result)
        else:
            result = decode_roversprog(user_input)
            st.text_area("Afkodet output:", result)
    
    st.markdown("""
    Røversprog er en simpel måde at lave sit eget
    kodesprog på, hvor man indsætter ekstra
    vokaler og konsonanter. Efter hver konsonant
    indsættes et O efterfulgt af den samme
    konsonant igen.  
                
    Med røversprog bliver ordet
    ”væbnermesterskabet” til  
    vovæbobnonerormomesostoterorsoskokabobetot  

    Her under kan du se, hvordan konsonanter og
    vokaler kobineres i røversproget  
    Røversprog kunne også sagtens laves med en
    anden vokal end O.
    """)

elif method == "Punktskrift":
    st.image("https://blind.dk/wp-content/uploads/2024/01/Punktskrift-alfabet-576x1024.png", use_container_width=True)
    user_input = st.text_area("Skriv dine observationer/resultater her løbende:")

elif method == "Semaforkode":
    st.image("https://friluftsaktiviteter.dk/wp-content/uploads/2019/03/Semafor.jpg", use_container_width=True)
    user_input = st.text_area("Skriv dine observationer/resultater her løbende:")
    st.markdown("""
    Semaforkode er et signaleringssystem, hvor to flag holdes i forskellige positioner for at angive bogstaver.  
    Billedet viser alfabetet med flagpositioner.  
                
    Brug tekstfeltet til at notere dine oversættelser eller observationer løbende.
    """)

elif method == "Binærkode":
    st.markdown("## Binærkode (fast tabel)")
    st.markdown("""
    Denne kode bruger et fast binært alfabet fra A til Å.
    """)
    choice = st.radio("Vælg handling:", ["Kod", "Afkod"])
    user_input = st.text_area("Indtast tekst eller binærkode:")
    
    # "Udfør"-knap
    if st.button("Udfør"):
        if user_input:
            if choice == "Kod":
                result = binærkode_tabel(user_input, encode=True)
            else:
                result = binærkode_tabel(user_input, encode=False)
            st.text_area("Resultat:", value=result, height=150)
        else:
            st.warning("Indtast venligst noget tekst eller kode først.")

    # Oversættelsestabel
    tabel = {
        'A': '0000 0000', 'B': '0000 0001', 'C': '0000 0010', 'D': '0000 0011',
        'E': '0000 0100', 'F': '0000 0101', 'G': '0000 0110', 'H': '0000 0111',
        'I': '0000 1000', 'J': '0000 1001', 'K': '0000 1010', 'L': '0000 1011',
        'M': '0000 1100', 'N': '0000 1101', 'O': '0000 1110', 'P': '0000 1111',
        'Q': '0001 0000', 'R': '0001 0001', 'S': '0001 0010', 'T': '0001 0011',
        'U': '0001 0100', 'V': '0001 0101', 'W': '0001 0110', 'X': '0001 0111',
        'Y': '0001 1000', 'Z': '0001 1001', 'Æ': '0001 1010', 'Ø': '0001 1011', 'Å': '0001 1100'
    }

    # Konverter til DataFrame
    df = pd.DataFrame(list(tabel.items()), columns=["Bogstav", "Binærkode"])

    # Fjern indekset helt
    df = df.reset_index(drop=True)

    st.dataframe(df, use_container_width=False)

elif method == "Vigenère":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    nøgleord = st.text_input("Indtast nøgleord (A-Å):").upper()
    user_input = st.text_area("Indtast tekst:")

    if st.button("Udfør"):
        if not nøgleord.isalpha() or len(nøgleord) == 0:
            st.error("Nøgleord skal kun indeholde bogstaver og må ikke være tomt.")
        else:
            if mode == "Kod":
                result = vigenere_kode(user_input, nøgleord, encode=True)
                st.text_area("Kodet output:", result)
            else:
                result = vigenere_kode(user_input, nøgleord, encode=False)
                st.text_area("Afkodet output:", result)

elif method == "Bifid":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))
    user_input = st.text_area("Indtast tekst:")
    if st.button("Udfør"):
        if mode == "Kod":
            result = bifid_encode(user_input)
            st.text_area("Kodet output:", result)
        else:
            result = bifid_decode(user_input)
            st.text_area("Afkodet output:", result)

elif method == "Baconkode":
    mode = st.radio("Vælg tilstand:", ("Kod", "Afkod"))

    if mode == "Kod":
        plaintext = st.text_input("Indtast hemmelig kode:")

        # Minimum fyldtekst længde (uden mellemrum)
        min_cover_length = len(plaintext.replace(" ", "")) * 5 if plaintext else 0

        if plaintext:
            st.info(f"Fyldteksten skal være mindst {min_cover_length} bogstaver lang (uden mellemrum).")

        covertext = st.text_area("Indtast fyldtekst (skal være mindst lige så lang som Bacon-koden):")

        # Længde uden mellemrum
        cover_length = len(covertext.replace(" ", ""))
        progress = min(cover_length / min_cover_length, 1.0) if min_cover_length > 0 else 1.0

        st.progress(progress)

        # Vis besked om længde med farve - opdateres live mens du skriver
        if min_cover_length > 0:
            if cover_length < min_cover_length:
                st.markdown(f"<p style='color: red;'>Fyldteksten er for kort med {min_cover_length - cover_length} bogstaver.</p>", unsafe_allow_html=True)
            elif cover_length > min_cover_length:
                st.markdown(f"<p style='color: red;'>Fyldteksten er for lang med {cover_length - min_cover_length} bogstaver.</p>", unsafe_allow_html=True)
            else:
                st.markdown(f"<p style='color: green;'>Fyldteksten har den korrekte længde.</p>", unsafe_allow_html=True)

        # Knap til at udføre kodning - kræver at både tekst og fyldtekst er udfyldt og korrekt længde
        if st.button("Udfør"):
            if plaintext and covertext:
                if cover_length < min_cover_length:
                    st.warning("Fyldteksten er for kort til at skjule hele den skjulte tekst.")
                else:
                    output = bacon_code_encode(plaintext, covertext)
                    st.text_area("Kodet tekst:", output, height=150)
            else:
                st.warning("Indtast både tekst og fyldtekst!")

    else:  # Afkod
        coded_text = st.text_area("Indtast kodet tekst (brug små og store bogstaver):")
        if st.button("Udfør"):
            if coded_text:
                output = bacon_code_decode(coded_text)
                st.text_area("Afkodet tekst:", output, height=150)
            else:
                st.warning("Indtast kodet tekst!")



