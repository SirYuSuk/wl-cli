#!usr/bin/env python3

import argparse
import requests
import sys
from terminaltables import AsciiTable


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


def def_art(word):
    entries = filter_entries(get_entries(word), "type", 'NOU-C')
    if not entries:
        print(f"{word} is geen zelfstandig naamwoord of het staat niet in de woordenlijst.")
        return
    else:
        t_data = [
            ["Zelfst. nm.", "Bep. lw."],
            [entries[0]['lemma'], entries[0]['gram']['art']]
        ]
        table = AsciiTable(t_data)
        print(table.table)


def main(args):
    word = args.woord.lower()
    if args.l:
        def_art(word)

if __name__ == "__main__":
    pars = argparse.ArgumentParser(description='Terminal-client voor woordenlijst.org')
    pars.add_argument("woord", help="zoek het gegeven woord op woordenlijst.org")
    pars.add_argument("-l", help="zoek het bepaald lidwoord dat bij het gegeven woord (znw) hoort",
                      action="store_true")
    main(pars.parse_args())