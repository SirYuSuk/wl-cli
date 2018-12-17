#!usr/bin/env python3

import argparse
import requests
import sys
from terminaltables import SingleTable


def get_entries(word):
    par = {'m': "search", 'searchValue': word, 'tactical': "true"}
    head = {'Referer': "https://woordenlijst.org/"}
    url = "https://woordenlijst.org/api-proxy/"
    req = requests.get(url, headers=head, params=par)
    data = req.json()
    return data['_embedded']

def filter_entries(entries, mode, arg):
    if mode == "type":
        return [e for e in entries['exact'] if e['gram']['pos'] == arg]


def check_found(entries, word):
    if not entries:
        print(f"{word} is niet van de juiste soort, of het staat niet in de woordenlijst.")
        return False
    else:
        return True


def q_def_art(word):
    entries = filter_entries(get_entries(word), "type", 'NOU-C')
    if check_found(entries, word):
        return [(entries[0]['lemma'], entries[0]['gram']['art'])]


def q_gender(word):
    entries = filter_entries(get_entries(word), "type", 'NOU-C')
    if check_found(entries, word):
        if entries[0]['gram']['gender'] == "n":
            gend = "onzijdig"
        elif entries[0]['gram']['gender'] == "m":
            gend = "mannelijk"
        else:
            gend = "vrouwelijk"
        return [(entries[0]['lemma'], gend)]

def main(args):
    word = args.woord.lower()
    res = {}
    t_data = [["Woord"], [word]]

    if args.l:
        res['Bep. lidw.'] = q_def_art(word)
    if args.g:
        res['Geslacht'] = q_gender(word)
    
    for k in res.keys():
        t_data[0].append(k)
        if res[k]:
            t_data[1].append(res[k][0][1])
        else:
            t_data[1].append("---")
    table = SingleTable(t_data)
    print(table.table)



if __name__ == "__main__":
    pars = argparse.ArgumentParser(description='Terminal-client voor woordenlijst.org')
    pars.add_argument("woord", help="zoek dit woord op woordenlijst.org")
    pars.add_argument("-l", help="zoek het bepaald lidwoord dat bij het gegeven woord (znw) hoort",
                      action="store_true")
    pars.add_argument("-g", help="zoek het geslacht dat bij het gegeven woord (znw) hoort",
                      action="store_true")
    main(pars.parse_args())