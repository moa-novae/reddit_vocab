import mtld
import spacy
import json
import timeit
from os import listdir, mkdir
from os.path import isfile, join, dirname


class literature_analysis(mtld.lexical_analysis):
    nlp = spacy.load('en_core_web_sm')
    nlp.max_length = 3500000

    def __init__(self, book):
        with open(book) as outfile:
            book_str = outfile.read()
            self.doc = literature_analysis.nlp(
                book_str, disable=['ner', 'tagger', 'textcat'])


def save_literature_analysis(books):
    output_json = {}
    output_dir = join(dirname(__file__), 'data')
    fileName = 'literature_data.txt'
    file_path = join(output_dir, fileName)
    for book in books:
        start = timeit.default_timer()
        result = literature_analysis(book)
        book_name = book[:book.find('.')]
        output_json[book_name] = {
            "mtld": result.mtld,
            "avg_sentence_length": result.avg_sentence_length
            }
        stop = timeit.default_timer()
        print(book_name, ' took ', stop - start)
    # Generate data subdirrector if it does not exist
    try:
        mkdir(output_dir)
    except Exception:
        pass
    # Save generated output JSON to ./data
    with open(file_path, 'w') as outfile:
        json.dump(output_json, outfile, indent=4)


books_path = join(dirname(__file__), 'books')
books = [join(books_path, f) for f in listdir(books_path)
         if isfile(join(books_path, f))
         ]
save_literature_analysis(books)
