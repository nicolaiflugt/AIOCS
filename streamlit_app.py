import streamlit as st

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

# Reverse dictionary for decoding
REVERSE_MORSE_CODE_DICT = {value: key for key, value in MORSE_CODE_DICT.items()}

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

def rotX(text, shift):
    danish_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ'
    shifted_text = []
    for char in text.upper():
        if char in danish_alphabet:
            idx = danish_alphabet.index(char)
            shifted_idx = (idx + shift) % len(danish_alphabet)
            shifted_text.append(danish_alphabet[shifted_idx])
        else:
            shifted_text.append(char)
    return ''.join(shifted_text)

def decode_rotX(text, shift):
    danish_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ'
    shifted_text = []
    for char in text.upper():
        if char in danish_alphabet:
            idx = danish_alphabet.index(char)
            shifted_idx = (idx - shift) % len(danish_alphabet)
            shifted_text.append(danish_alphabet[shifted_idx])
        else:
            shifted_text.append(char)
    return ''.join(shifted_text)

st.title("Kodeskifter")

mode = st.selectbox("Vælg funktion:", ('Morsekode', 'ROT-X'))

if mode == 'Morsekode':
    action = st.radio("Vælg metode:", ('Kod', 'Afkod'))
    st.write("**Instruktion:** Brug '/' mellem bogstaver og '//' mellem ord i morsekode.")
elif mode == 'ROT-X':
    action = st.radio("Vælg metode:", ('Kod', 'Afkod'))
    st.write("**Instruktion:** Brug ROT-X til at rotere bogstaver i alfabetet. Angiv et bogstav (fx K) for at bestemme forskydningen.")

shift = None
danish_alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZÆØÅ'

if mode == 'ROT-X':
    letter_input = st.text_input("Indtast et bogstav for at bestemme rotationen (A=ingen forskydning):", "").upper().strip()
    if len(letter_input) == 1 and letter_input in danish_alphabet:
        shift = danish_alphabet.index(letter_input)
    else:
        shift = None

user_input = st.text_area("Indtast tekst:", "")

if st.button("Kør"):
    if mode == 'Morsekode':
        if action == 'Kod':
            result = encode_to_morse(user_input)
            st.text_area("Morsekode:", result)
        else:
            result = decode_from_morse(user_input)
            st.text_area("Tekst:", result)
    elif mode == 'ROT-X':
        if shift is None:
            st.warning("Indtast et gyldigt bogstav (A-Å) for at bestemme rotationen.")
        else:
            if action == 'Kod':
                result = rotX(user_input, shift)
            else:
                result = decode_rotX(user_input, shift)
            st.text_area(f"ROT-{shift} ({action}):", result)
