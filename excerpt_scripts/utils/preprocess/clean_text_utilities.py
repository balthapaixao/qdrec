# preprocessing.py
import pandas as pd
import re
# from unidecode import unidecode
import logging
import datetime
# from copy import deepcopy
from .web_utilities import fix_spelling_in_answer


def remove_dash_n(text: str) -> str:
    """
    Remove quebras de linha

    Arguments:
        text {str} -- Texto a ser tratado

    Returns:
        str -- Texto tratado"""
    return text.replace('/n', ' ')


def remove_spaces(text: str) -> str:
    """
    Remove espaços que se repetem mais de 2 vezes

    Arguments:
        text {str} -- Texto a ser tratado

    Returns:
        str -- Texto tratado"""
    return re.sub(r"\s+", " ", text).strip()


def remove_lots_of_points(text: str) -> str:
    """
    Remove pontos que se repetem mais de 2 vezes

    Arguments:
        text {str} -- Texto a ser tratado

    Returns:
        str -- Texto tratado"""
    return re.sub('\.{2,}', ' ', text)


def remove_bad_chars(text: str) -> str:
    """
    Remove caracteres que não são letras, números ou espaços

    Arguments:
        text {str} -- Texto a ser tratado

    Returns:
        str -- Texto tratado"""
    return re.sub('[˜˚˝˙ˆˇ˚˘˘Œ˛œ_%ﬁﬂ‡š<>›„’]', ' ', text)


def spaced_letters(text: str) -> str:
    """
    Substitui palavras com espaços que puderam ser detectados anteriormente

    Arguments:
        text {str} -- Texto a ser tratado

    Returns:
        str -- Texto tratado
    """
    text = text.replace('A P O S E N T A R', ' aposentar ')
    text = text.replace('A N E X O I I I', 'ANEXO III')
    text = text.replace('A N E X O I I', 'ANEXO II')
    text = text.replace('A N E X O I V', 'ANEXO IV')
    text = text.replace('A N E X O I X', 'ANEXO IX')
    text = text.replace('A N E X O I', 'ANEXO I')
    text = text.replace('A N E X O V I', 'ANEXO VI')
    text = text.replace('A N E X O V I I', 'ANEXO VII')
    text = text.replace('A N E X O V I I I', 'ANEXO VIII')
    text = text.replace('A N E X O X I I I', 'ANEXO XIII')
    text = text.replace('A N E X O X I I', 'ANEXO XII')
    text = text.replace('A N E X O X I', 'ANEXO XI')
    text = text.replace('A N E X O X', 'ANEXO X')
    text = text.replace('A N E X O', 'ANEXO')

    text = text.replace("R E S O L V E", "RESOLVE")
    text = text.replace('J u s t i f i c a t i v a', 'Justificativa')
    text = text.replace("I P VA", "IPVA")
    text = text.replace(
        "S E C R E T A R I A D E E D U C A Ç Ã O", "SECRETARIA DE EDUCAÇÃO")
    text = text.replace("PRE FEIT O", "PREFEITO")
    text = text.replace("qui NTA-F Ei RA, 22 DE Ju LHO DE",
                        "quinta-feira, 22 de Julho de")
    text = text.replace("Ó R G Ã O RESPONSÁVE L SME", "ÓRGÃO RESPONSÁVEL SME")
    text = text.replace("I P VA", "IPVA")
    text = text.replace("R E C U R S O S : P r o g r a m a E s c o l a r A u t ô n o m a d e G e s t ã o",
                        "RECURSOS: Programa Escolar Autônoma de Gestão")
    # text = text.replace("I P VA", "IPVA")

    text = text.replace("cartei-rinha", "carteirinha")

    return text


def join_words(text: str) -> str:
    """
    Essa função é para juntar palavras que estão separadas

    Arguments:
        text {str} -- Texto

    Returns:
        str -- Texto com palavras juntas"""

    # Há muitas palavras assim: "res - ponsável"
    # Vou ter algum problema juntando coisa que não devia
    # Espero que nesses casos o tokenizer resolva
    return re.sub(' - ?', '', text)


def separate_words(text: str) -> str:
    """
    Essa função é para separar palavras que estão juntas

    Arguments:
        text {str} -- Texto

    Returns:
        str -- Texto com palavras separadas"""
    # Há muitas palavras assim: "FerrazPresidente" "FerrazAPresidente"
    # Vou supor que sempre que houver uma letra minúscula seguida de maiúscula é para separar
    text = re.sub('(?<=[a-záàâãéêíóôõú])(?=[A-ZÁÀÂÃÉÊÍÓÔÕÚ])', ' ', text)
    text = re.sub(
        '(?<=[ÓA-ZÁÀÂÃÉÊÍÓÔÕÚ])(?=[ÓA-ZÁÀÂÃÉÊÍÓÔÕÚ][a-záàâãéêíóôõú])', ' ', text)
    return text


def dots_that_mess_segmentation(text: str) -> str:
    """
    Essa função é para corrigir alguns pontos que atrapalham a segmentação

    Arguments:
        text {str} -- Texto a ser corrigido

    Returns:
        str -- Texto corrigido"""
    text = re.sub('sec\.', 'Sec ', text, flags=re.IGNORECASE)
    text = re.sub('av\.', 'Avenida ', text, flags=re.IGNORECASE)
    text = re.sub('min\.', 'Ministro ', text, flags=re.IGNORECASE)
    text = re.sub('exmo\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('sr\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('dr\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('sra\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('proc\.', ' processo ', text, flags=re.IGNORECASE)
    text = re.sub('reg\.', ' registro ', text, flags=re.IGNORECASE)
    text = re.sub('func\.', ' funcionário ', text, flags=re.IGNORECASE)
    text = re.sub('art\.', ' artigo ', text, flags=re.IGNORECASE)
    text = re.sub('inc\.', ' inciso ', text, flags=re.IGNORECASE)
    text = re.sub('(?<=[ \.][A-Z])\.', ' ', text)
    text = re.sub('(?<=comp)\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('(?<=insc)\.', ' ', text, flags=re.IGNORECASE)
    text = re.sub('p[áa]g[\. ]', ' página ', text,
                  flags=re.IGNORECASE)  # Pág. N 5
    text = re.sub('\. *(n|n[uú]mero)[ \.°º]+',
                  ' número ', text, flags=re.IGNORECASE)  # . N°

    return text


def preprocess(text: str) -> str:
    """
    Função que faz o pré-processamento do texto

    Arguments:
        text {str} -- texto a ser processado

    Returns:
        str -- texto pré-processado"""
    text = remove_special_characters(text)
    text = remove_dash_n(text)
    text = remove_lots_of_points(text)
    text = remove_bad_chars(text)
    text = spaced_letters(text)
    text = dots_that_mess_segmentation(text)
    text = remove_spaces(text)
    text = join_words(text)
    text = separate_words(text)
    text = remove_page_breaker(text)
    text = remove_special_characters(text)

    return text


# my functions
def remove_special_characters(text: str) -> str:
    """
    Remove caracteres especiais do texto

    Arguments:
        text {str} -- texto a ser processado

    Returns:
        str -- texto sem caracteres especiais
    """
    text = text.replace("<__", "").replace("__>", "")
    text = text.replace("- -", "-")
    text = text.replace(" - ", "-")
    text = text.replace("  ", " ")
    text = text.replace("- ", "-")
    text = text.replace(" -", "-")

    return text


def remove_multiple_dashes(text: str) -> str:
    """
    Remove os traços que estão em excesso

    Arguments:
        text {str} -- texto a ser processado

    Returns:
        str -- texto sem traços em excesso
    """

    text = re.sub(r'-+', '-', text)

    return text


def remove_page_breaker(text: str) -> str:
    """
    Remove o texto que separa as páginas

    Arguments:
        text {str} -- texto a ser processado

    Returns:    
        str -- texto sem o separador de páginas
    """
    return text.replace("\n", " ").strip()


def find_occurrences(text: str,
                     character: str) -> list:
    """
    Encontra todas as ocorrências de um caracter em um texto

    Arguments:
        text {str} -- texto a ser processado
        character {str} -- caracter a ser procurado

    Returns:
        list -- lista com as posições das ocorrências"""
    return [i for i, letter in enumerate(text) if letter == character]


def get_whole_words(subtext: str) -> str:
    """
    Pega a palavra inteira, sem cortar pela metade

    Arguments:
        subtext {str} -- parte texto a ser processado

    Returns:
        str -- palavra inteira
        """
    spaces_indexes = find_occurrences(subtext, " ")
    first_pos = spaces_indexes[0]
    last_pos = spaces_indexes[-1]

    # pega entre o primeiro e o ultimo espaço
    # para não pegar palavras pela metade
    return (subtext[first_pos:
                    last_pos],
            first_pos,
            last_pos)


def contains_number(word: str):
    return bool(re.search(r'\d', word))


def find_dashes_and_replace_words(text: str,
                                  df_ptbr: pd.DataFrame) -> str:
    """
    Temos problemas onde há palavras com hífen
    Ex: "res - ponsável"

    Arguments:
        text {str} -- texto a ser processado
        df_ptbr {pd.DataFrame} -- dataframe com o dicionario das palavras em portugues pela funcao get_ptbr_dictionary()

    Returns:
        str -- texto processado
    """
    dashes_indexes = find_occurrences(text, "-")
    spaces_indexes = find_occurrences(text, " ")

    words = df_ptbr['Word'].map(lambda w: w.lower()).unique()  # unidecode

    for dash in dashes_indexes:
        try:
            space_before = max(
                [elem for elem in spaces_indexes if elem < dash])
        except:
            space_before = 0

        try:
            space_after = min([elem for elem in spaces_indexes if elem > dash])
        except:
            space_after = len(text)

        new_word = text[space_before:space_after]
        new_word = new_word.replace('-', '')

        new_word_cleaned = (new_word.
                            lower().
                            strip().
                            replace('.', '').
                            replace(',', '').
                            replace(':', '').
                            replace(';', '').
                            replace(')', '').
                            replace('(', '').
                            replace('[', '').
                            replace(']', ''))
        if not (contains_number(word=new_word)):
            if new_word_cleaned in words:
                text = ''.join([text[:space_before],
                                new_word,
                                text[space_after:]])

    return text


def clean_text(text: str,
               window_size: int = 50) -> str:
    """Remove caracteres especiais e espaços em branco

    Arguments:
        text {str} -- texto a ser limpo

        Keyword Arguments:
            window_size {int} -- tamanho da janela de contexto (default: {50})

    Returns:
        str -- texto limpo

    """
    inicio = datetime.datetime.now()  # .strftime("%Y%m%d%H:%M:%S")
    logging.info(
        f"TEXTO INICIAL {inicio.strftime('%Y%m%d%H:%M:%S')} -> {text}")
    dash_indexes = find_occurrences(text, "-")
    if dash_indexes:
        final_text = ''
        dash_indexes_size = len(dash_indexes)
        for i in range(0, dash_indexes_size):

            start_dash_position = dash_indexes[i]-window_size
            end_dash_position = dash_indexes[i]+window_size

            if start_dash_position < 0:
                # pegar inicio do texto caso o intervalo de contexto esteja antes da posição 0
                start_dash_position = 0

            if i == 0:
                last_position = 0
                start_dash_position = 0
            else:
                last_position = dash_indexes[i]
                if start_dash_position < (dash_indexes[i-1]+window_size):
                    # dash_indexes[i-1]+window_size
                    start_dash_position = last_space_position

            subtext = text[start_dash_position:
                           end_dash_position]

            subtext, first_space_position, last_space_position = get_whole_words(
                subtext=subtext)

            first_space_position += start_dash_position  # (last_position)
            last_space_position += start_dash_position  # last_position

            # aqui entra a validação no google
            _has_url = check_if_is_url(subtext)
            if _has_url:
                subtext = subtext
            else:
                subtext = fix_spelling_in_answer(subtext)[0]

            first_fragment = text[start_dash_position:
                                  first_space_position]

            if i == (dash_indexes_size-1):
                last_fragment = text[last_space_position:]
            else:
                next_dash_position = dash_indexes[i+1]-window_size

                last_fragment = text[last_space_position:
                                     next_dash_position]

            final_text += " ".join([first_fragment,
                                    subtext,
                                    last_fragment])
            final_text = final_text.replace("  ", " ")
    else:
        final_text = text

    final = datetime.datetime.now()
    logging.info(
        f"TEXTO FINAL {final.strftime('%Y%m%d%H:%M:%S')} -> {final_text}")
    logging.info(f"TEMPO DE PROCESSAMENTO -> {(final-inicio).total_seconds()}")

    return final_text


def read_dicionario_br() -> pd.DataFrame:
    """
    Lê o dicionário de palavras do português brasileiro

    Returns
    -------
    df_ptbr : pd.DataFrame
        Dataframe com as palavras do português brasileiro
    """
    # obtendo palavras do portugues brasileiro
    url = 'https://drive.google.com/file/d/1tUDeEyH6vonx-ctxeGVWG6gh4knP1Igi/view?usp=sharing'
    path = 'https://drive.google.com/uc?export=download&id='+url.split('/')[-2]
    header_list = ['Word']
    df_ptbr = pd.read_csv(path,
                          skiprows=0,
                          names=header_list,
                          header=None,
                          sep=',')
    return df_ptbr


def check_if_is_url(text: str) -> bool:
    """Check if a string is a URL.
    Args:
        text: a string
    Returns:
        a boolean
    """

    if (('http' in text) or
        ('www' in text) or
        ('.com' in text) or
            ('.br' in text)):
        return True
    else:
        return False


def clean(texts: pd.Series) -> pd.Series:
    """
    Limpa o texto

    Arguments:
        texts {pd.Series} -- texto a ser limpo

    Returns:
        pd.Series -- texto limpo
    """

    return texts.apply(lambda txt: clean_text(txt))


# new functions
