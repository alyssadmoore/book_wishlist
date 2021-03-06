import os
from book import Book
import json #Save the book data as JSON
            #(instead of strings joined with a separator)

DATA_DIR = 'data'
BOOKS_FILE_NAME = os.path.join(DATA_DIR, 'wishlist.txt')
COUNTER_FILE_NAME = os.path.join(DATA_DIR, 'counter.txt')

separator = '^^^'  # a string probably not in any valid data relating to a book

book_list = []
counter = 0


def setup():
    ''' Read book info from file, if file exists. '''

    global counter

    try :
        with open(BOOKS_FILE_NAME) as f:
            data = f.read()
            # data = json.loads(f)
            make_book_list(data)
    except FileNotFoundError:
        # First time program has run. Assume no books.
        pass


    try:
        with open(COUNTER_FILE_NAME) as f:
            try:
                counter = int(f.read())
            except:
                counter = 0
    except:
        counter = len(book_list)


def shutdown():
    '''Save all data to a file - one for books, one for the current counter value, for persistent storage'''

    output_data = make_output_data()

    # Create data directory
    try:
        os.mkdir(DATA_DIR)
    except FileExistsError:
        pass # Ignore - if directory exists, don't need to do anything.

    with open(BOOKS_FILE_NAME, 'w') as f:
        f.write(output_data)
        # json.dumps(output_data)

    with open(COUNTER_FILE_NAME, 'w') as f:
        f.write(str(counter))
        # json.dumps(str(counter))


def get_books(**kwargs):
    ''' Return books from data store. With no arguments, returns everything. '''

    global book_list

    if len(kwargs) == 0:
        return book_list

    if 'read' in kwargs:
        read_books = [ book for book in book_list if book.read == kwargs['read'] ]
        return read_books


def add_book(book):
    ''' Add to db, set id value, return Book'''

    global book_list

    book.id = generate_id()
    book_list.append(book)


def generate_id():
    global counter
    counter += 1
    return counter


def set_read(book_id, date_read, rating):
    '''Update book with given book_id to read. Return True if book is found in DB and update is made, False otherwise.'''

    global book_list

    for book in book_list:

        if book.id == book_id:
            book.read = True
            book.date_read = date_read
            book.rating = rating
            return True

    return False # return False if book id is not found


def make_book_list(string_from_file):
    ''' turn the string from the file into a list of Book objects'''

    global book_list

    books_str = string_from_file.split('\n')

    try:
        for book_str in books_str:
            data = book_str.split(separator)
            book = Book(data[0], data[1], data[2] == 'True', int(data[3]), data[4])
            book_list.append(book)
            # json.dumps(book)
    except Exception as e:
        print("out of index", e)


def make_output_data():
    ''' create a string containing all data on books, for writing to output file'''

    global book_list

    output_data = []

    for book in book_list:
        output = [ book.title, book.author, str(book.read), str(book.id), str(book.date_read)]
        output_str = separator.join(output)
        output_data.append(output_str)
        # output_data.append(output)
        # json_str = json.dumps(output)

    all_books_string = '\n'.join(output_data)
    # all_books_string = json.loads(json_str)

    return all_books_string


def get_sorted_books_by_title(**kwargs):

    ''' Return books from data store. With no arguments, returns everything. '''

    global book_list

    if len(kwargs) == 0:
        return book_list

    if 'title' in kwargs:
        read_books = [ book for book in book_list if book.read == kwargs['title'] ]
        read_books
    return sorted(read_books, key=lambda book_list: book_list[1])

def get_sorted_books_by_author(**kwargs):
    ''' Return books from data store. With no arguments, returns everything. '''
    global book_list

    if len(kwargs) == 0:
        return book_list

        if 'author' in kwargs:
            read_books = [ book for book in book_list if book.read == kwargs['author'] ]
            read_books
    return sorted(read_books, key=lambda book_list: book_list[3])
