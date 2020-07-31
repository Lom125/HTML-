
"""Создание html документа с помощью Python."""

class Tag:
    def __init__(self, tag, is_single=False, klass=None, **kwargs):
        """Задаем класс с возможностью ввода теста и атрибутов."""        
        self.tag = tag
        self.text = ""
        self.attributes = {}
        """self.body - это будущий список строк создаваемого html документа. Сюда мы будем добавлять все остальное содержимое."""
        self.body = []
        self.is_single = is_single

        if klass is not None:
            """Проверяем количество заданных классов (klass) у данного тега (если их больше одного, то соединяем их пробелами) и добавляем в словарь атрибутов."""             
            if "," in str(klass):
                self.attributes["class"] = " ".join(klass)
            else:
                self.attributes["class"] = klass
        """Добавляем в словарь другие атрибуты."""
        for attr, value in kwargs.items():
            if "_" in attr:
                attr = attr.replace("_", "-")
            self.attributes[attr] = value
        """Создаем полный список атрибутов, включая классы."""
        attrs = []
        for attribute, value in self.attributes.items():
            attrs.append('%s="%s"' % (attribute, value))
        attrs = " ".join(attrs)
        """Проверяем не пустой ли список атрибутов и записываем в список строк будущего html документа начальный тег с атрибутами или без них."""
        if attrs == [] or attrs == "":
            self.body.append("<%s>" % self.tag)
        else:
            self.body.append("<{tag} {attrs}>".format(tag=self.tag, attrs=attrs))
        

    def __enter__(self):
        return self

    def __exit__(self, mmm, type, value): 
        """Дописываем "текст" с отступом в список строк будущего html документа (с большой буквы и сразу после открывающего тега)."""
        if self.text != "":
            self.body.insert(1, "\t" + self.text.capitalize())
        """Добавляем или нет закрывающий тег."""
        if not self.is_single:
            self.body.append("</%s>" % self.tag)
        return self
 
    def __str__(self):
        return self
    
    """Определяем сложение между объектами. Строки из any.body добавляем с отступами в self.body. Здесь сроки из дочерних тегов добавляются в список текущего тега."""
    def __add__(self, any):
        for str_ in any.body:
            str_ = "\t" + str_
            self.body.append(str_)
        return self
   

class HTML(Tag):
    def __init__(self, output = None):
        """Формируем начальные записи списка строк html документа."""
        self.body = ["<!DOCTYPE html>", '<html lang="ru">']
        """Задаем возможность вывода в файл и формируем для этого строку, которую будем в него записывать."""        
        self.output = output
        self.stro = ""
   
    def __exit__(self, mmm, type, value): 
        """Добавляем закрывающий тег."""       
        self.body.append("</html>")
        """Выясняем, куда выводить текст: на экран или в файл."""
        if self.output == None:
            print(*self.body, sep = "\n")
        elif ".html" in self.output:
            for str_ in self.body:
                self.stro += str_ + "\n"
            file_ = open(self.output, "w", encoding="utf-8")
            file_.write(self.stro)
        else:
            print("Неправильное имя файла!")
   
    def __add__(self, any):
        """Добавляем все дочерние строки в html документ."""
        for str_ in any.body:
            self.body.append(str_)
        return self

class TopLevelTag(Tag):
    """Не вижу смысла задавать для тегов глобального уровня отдельный класс. А так им можно задавать атрибуты."""
    pass


if __name__ == "__main__":
    """Для вывода в файл надо задать имя файла с расширением html. Для вывода на экран никаких атрибутов для HTML задавать не надо - HTML()."""
    with HTML("html.html") as doc:
        with TopLevelTag("head") as head:
            with Tag("meta", is_single=True, charset=("UTF-8")) as meta:
                pass
            head += meta

            with Tag("title") as title:
                title.text = "hello"
            head += title
        doc += head

        with TopLevelTag("body") as body:
            
            with Tag("h1", klass=("main-text")) as h1:
                h1.text = "Test"
            body += h1

            with Tag("div", klass=("container", "container-fluid"), id="lead") as div:
                div.text = "Внутри содержатся два тега"
                with Tag("p") as paragraph:
                    paragraph.text = "Another test"
                
                div += paragraph

                with Tag("img", is_single=True, src="/icon.png") as img:
                    pass
               
                div += img

            body += div
        doc += body

