import os, pickle, re
from PySide2 import QtCore, QtWidgets


class LoadSave:
    def __init__(self):
        self.book = []  # book = [root, [pgs], {pg:file}, {pg: {obj: objfile}}]
        self.bookfiles = {}  # { page: file}  | book[2]
        self.pageobjs = {}  # {page: { obj name : obj img file, ...}}  | book[3]

        self.pgs = []  # [keys for book]  | book[1]
        self.index = 0  # iterator for pages
        self.title = ''
        self.savepath = ''

    def addobject(self, page, name, imgpath):
        if os.path.exists(imgpath):
            if page in self.pageobjs:
                self.pageobjs[page][name] = imgpath
            else:
                print(page)
                print('Not valid!\n')

    # if secondary coder, coded = 'Coded\Secondary'
    # returns book[] and title str
    def load_folder(self, coded='Coded'):
        folder = QtWidgets.QFileDialog.getExistingDirectory(options=QtWidgets.QFileDialog.ShowDirsOnly)
        # show dir bc only want them to select entire folders

        codedfolder = os.path.join(folder, coded).replace('\\', '/')

        newWork = True  # first time coding items
        issues = 0  # no issues

        if os.path.exists(codedfolder):
            files = os.listdir(codedfolder)
            if files:
                book, issues, title = self._load_folder_existing(codedfolder)
                if issues == 0:
                    if book:
                        self.book = book
                        self.title = title
                        self.savepath = codedfolder
                        return book, title

        book = []
        title = ''

        if newWork:
            book, title = self._load_folder(folder, [])
            if not book:
                return None, None

        # theres maybe coded work already
        if issues == 1:
            book[3] = self.codedfixer(book, codedfolder)
        else:
            if not os.path.exists(codedfolder):
                os.makedirs(codedfolder)
        os.chmod(codedfolder, 0o777)

        picklepath = os.path.join(codedfolder, title + '_base.pickle').replace('\\', '/')
        # book = [origin, [pgs], {pg:file}, {pg: {obj: objfile}}]
        try:
            self.index = 0
            self.title = title
            self.pgs = book[1]  # list of int
            self.imgfolder = book[2]
            self.pageobjs = book[3]
            self.book = book
        except KeyError:
            return None, None

        self.topickle(picklepath, book)
        self.savepath = codedfolder

        return book, title

    def _load_folder_existing(self, codedfolder):
        files = os.listdir(codedfolder)
        book = []
        title = ''
        issues = 0  # no issues

        for file in files:
            if file.endswith('_base.pickle'):
                path = os.path.join(codedfolder, file).replace('\\', '/')
                with open(path, 'rb') as f:
                    try:
                        book = pickle.load(f)
                        if len(book) >= 4:
                            title = file.split('_')[0]
                            break
                        if type(book) is not dict:
                            return None, 1, title
                    except EOFError:
                        # invalid savefile
                        return None, 1, ''
            elif file.endswith('.png') and issues > 0:
                return None, 1, None
        if len(book) < 4 or not book[3]:
            return None, 1, title
        elif book[3]:
            for item in book[3]:
                if len(book[3][item]) < 1:
                    return None, 1, title

        return book, 0, title

    def _load_folder(self, folder, book):
        fileext = (".jpg", ".jpeg", ".png")
        fileschema = ("Slide", "Page", "Pg", "P")
        foldercheck = ('Scans', 'Scans for Python')

        bookfiles = {}  # book[2]
        bookobjs = {}  # book[3]
        title = ''

        for path, _, files in os.walk(folder):
            book.append(path)

            if path.endswith(foldercheck):
                title = os.path.split(os.path.split(path)[0])[1]
            else:
                title = os.path.split(path)[1]

            # sort through pages
            for img in files:
                if img.endswith(fileext) and any(s in img for s in fileschema):
                    page = int(re.search(r'\d+', img).group())
                    f = os.path.join(path, img).replace('\\', '/')
                    bookfiles[page] = os.path.join(path, img).replace('\\', '/')
                    bookobjs[page] = {}
            break

        if len(bookfiles) < 1:
            return None, title

        book.append(list(bookfiles.keys()))
        book.append(bookfiles)
        book.append(bookobjs)

        return book, title

    def codedfixer(self, book, codedfolder):
        pgs = book[1]
        objects = book[3]  # dict { pg: {obj:file, obj2:file}}

        for path, _, files in os.walk(codedfolder):
            for obj in files:
                if obj.endswith('.png'):
                    page = int(re.search(r'\d+', obj).group())
                    name = os.path.splitext(obj)[0].split('_')[3]
                    file = os.path.join(path, obj).replace('\\', '/')

                    try:
                        if page in pgs:
                            objects[page][name] = file
                    except IndexError:
                        continue  # skip to next item
        return objects

    def topickle(self, filename, data):
        savefolder = self.savepath + os.sep + 'helperfiles'
        if not os.path.exists(savefolder):
            os.makedirs(savefolder)
        os.chmod(savefolder, 0o777)
        savepath = os.path.join(self.savepath, filename).replace('\\', '/')
        savepath2 = os.path.join(savefolder, filename).replace('\\','/')
        try:
            with open(savepath, 'wb') as f:
                pickle.dump(data, f)
            with open(savepath2, 'wb') as f:
                pickle.dump(data, f)
        except TypeError:
            print('Typeerror when pickling!')