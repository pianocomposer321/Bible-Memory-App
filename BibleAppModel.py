import re
import json


class BibleAppModel:

    def __init__(self, reference=None):
        self.kjv_bible = {}
        self.reference = ''
        self.book = ''
        self.chapter = ''
        self.verse = ''
        self.verse_ext = ''
        self.passages = {}
        self.load_verses()
        self.open_data_file()
        if reference is not None:
            self.reference = reference
            self._get_verse(reference=reference)
            self.get_verse_text()
        self.verses = []

    def open_data_file(self):
        with open('kjv.json', 'r+') as (file):
            self.kjv_bible = json.load(file)

    def _get_verse(self, reference=None):
        if reference is None:
            reference = self.reference
        BOOK_RE = re.compile('^\\d*[a-zA-Z ]+')
        REF_RE = re.compile('\\d{1,3}:\\d{1,3}')
        VERSE_EXT_RE = re.compile('-(\\d{1,3})')
        self.book = BOOK_RE.search(reference).group(0).strip()
        ref = REF_RE.search(reference).group(0)
        self.chapter, self.verse = ref.split(':')
        self.chapter, self.verse = int(self.chapter.strip()), int(self.verse.strip())
        self.verse_ext = VERSE_EXT_RE.search(reference)
        if self.verse_ext:
            self.verse_ext = self.verse_ext.group(1).strip()
            self.verse_ext = int(self.verse_ext)

    def get_verse_text(self):
        self.passages[self.reference] = []

        for book in self.kjv_bible['books']:
            if book["name"] == self.book:
                for chapter in book["chapters"]:
                    if chapter["chapter"] == self.chapter:
                        for verse in chapter["verses"]:
                            if not self.verse_ext:
                                if verse["verse"] == self.verse:
                                    # print(verse["text"])
                                    # self.verses.append(verse['text'])
                                    vtext = verse['text']
                                    self.passages[self.reference].append(vtext)
                                    return
                            else:
                                if verse["verse"] >= self.verse and verse["verse"] <= self.verse_ext:
                                    # self.verses.append(verse["text"])
                                    vtext = verse['text']
                                    self.passages[self.reference].append(vtext)
                                elif verse['verse'] > self.verse_ext:
                                    return

    def load_verses(self, filename='verses.json'):
        with open(filename, 'r+') as (file):
            self.passages = json.load(file)

    def save_verses(self, filename='verses.json'):
        with open(filename, 'w') as (file):
            json.dump((self.passages), file, indent=4)

    def set_reference(self, reference):
        self.reference = reference
        self._get_verse(reference=reference)
        self.get_verse_text()


def main():
    ref = input('Enter a reference: ')
    print()
    verse = BibleAppModel(ref)
    print('\n'.join(verse.passages[ref]))


if __name__ == '__main__':
    main()
