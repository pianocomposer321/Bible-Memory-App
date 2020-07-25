import re
import json


class Verse:
    def __init__(self, reference=None):
        self.kjv_bible = {}
        self.reference = ''
        self.book = ''
        self.chapter = ''
        self.verse = ''
        self.verse_ext = ''
        self.verses = []
        self.verse_text = ''
        self.passages = {}


        if reference is not None:
            self.reference = reference
            self.parse_verse(reference=reference)

        self.open_data_file()

    def open_data_file(self):
        with open("replace_I.json", 'r+') as file:
            self.kjv_bible = json.load(file)

    def parse_verse(self, reference=None):
        if reference is None:
            reference = self.reference
        
        BOOK_RE = re.compile(r"^\d*[a-zA-Z ]+")
        REF_RE = re.compile(r"\d{1,3}:\d{1,3}")
        VERSE_EXT_RE = re.compile(r"-(\d{1,3})")

        self.book = BOOK_RE.search(reference).group(0).strip()  # book = match of BOOK_RE minus trailing whitespace

        ref = REF_RE.search(reference).group(0)  # ref = match of REF_RE
        self.chapter, self.verse = ref.split(':')  # split chapter from verse
        self.chapter, self.verse = int(self.chapter.strip()), int(self.verse.strip())  # strip whitespace and convert to int
        self.verse_ext = VERSE_EXT_RE.search(reference)
        if self.verse_ext:
            self.verse_ext = self.verse_ext.group(1).strip()
            self.verse_ext = int(self.verse_ext)

    def get_verse_text(self):
        for book in self.kjv_bible['books']:
            if book["name"] == self.book:
                for chapter in book["chapters"]:
                    if chapter["chapter"] == self.chapter:
                        for verse in chapter["verses"]:
                            if not self.verse_ext:
                                if verse["verse"] == self.verse:
                                    # print(verse["text"])
                                    self.verses.append(verse['text'])
                                    return
                            else:
                                if verse["verse"] >= self.verse and verse["verse"] <= self.verse_ext:
                                    self.verses.append(verse["text"])
                                elif verse['verse'] > self.verse_ext:
                                    # for verse in self.verses:
                                    #     print(verse)
                                    # print()
                                    return


def main():
    ref = input("Enter a reference: ")
    print()
    # ref = "John 3:16-20"
    verse = Verse(ref)
    verse.get_verse_text()
    print('\n'.join(verse.verses))
    print()

if __name__ == '__main__':
    main()
