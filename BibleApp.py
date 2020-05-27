import re
import json

class Verse:
    def __init__(self, reference=None):
        if reference is not None:
            self.reference = reference
            self.get_verse(reference=reference)

        self.open_data_file()

    def open_data_file(self):
        with open("kjv.json", 'r+') as file:
            # for book in json.load(file)["books"]:
                                
            self.kjv_bible = json.load(file)

    def get_verse(self, reference=None):
        if reference is None:
            reference = self.reference
        
        BOOK_RE = re.compile(r"^\d*[a-zA-Z ]+")
        REF_RE = re.compile(r"\d{1,3}:\d{1,3}")
        VERSE_EXT_RE = re.compile(r"-(\d{1,3})")
        REPLACE_ROMAN_RE = re.compile(r"^[1-3]")

        self.book = BOOK_RE.search(reference).group(0).strip()  # book = match of BOOK_RE minus trailing whitespace
        # nr_of_Is = int(REPLACE_ROMAN_RE.search(self.book).group(0))
        nr_of_Is = REPLACE_ROMAN_RE.search(self.book)
        if nr_of_Is:
            nr_of_Is = int(nr_of_Is.group(0))
            self.book = REPLACE_ROMAN_RE.sub("I" * nr_of_Is, self.book)

        ref = REF_RE.search(reference).group(0)  # ref = match of REF_RE
        self.chapter, self.verse = ref.split(':')  # split chapter from verse
        self.chapter, self.verse = int(self.chapter.strip()), int(self.verse.strip())  # strip whitespace and convert to int
        self.verse_ext = VERSE_EXT_RE.search(reference)
        if self.verse_ext:
            self.verse_ext = self.verse_ext.group(1).strip()
            self.verse_ext = int(self.verse_ext)

        if self.verse_ext:
            print(f"The verse has an extension: {self.verse_ext}")
            print()


        # print(self.book)
        # print(self.chapter)
        # print(self.verse)

    def get_verse_text(self):
        verses = []
        for book in self.kjv_bible['books']:
            if book["name"] == self.book:
                for chapter in book["chapters"]:
                    if chapter["chapter"] == self.chapter:
                        for verse in chapter["verses"]:
                            if not self.verse_ext:
                                if verse["verse"] == self.verse:
                                    print(verse["text"])
                                    return
                            else:
                                if verse["verse"] >= self.verse and verse["verse"] <= self.verse_ext:
                                    verses.append(verse["text"])
        if self.verse_ext:
            for verse in verses:
                print(verse)
            print()
        

        # for book in self.kjv_bible['books']:
        #     if book["name"] == 'Genesis':
        #         print("Found: Genesis")
        #         return
        #     else:
        #         print("Not found: Genesis")
        #         return

def main():
    ref = input("Enter a reference: ")
    print()
    # ref = "John 3:16-20"
    verse = Verse(ref)
    verse.get_verse_text()

if __name__ == '__main__':
    main()
