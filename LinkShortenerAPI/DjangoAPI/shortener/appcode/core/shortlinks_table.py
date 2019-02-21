class Shortlink:
    def __init__(self, shortlink, longlink, password):
        self.shortlink = shortlink
        self.longlink = longlink
        self.password = password

    def __str__(self):
        return '{"shortLink": "%s","longLink": "%s","password": "%s"}' % (self.shortlink, self.longlink, self.password)


class ShortlinksTable:
    def __init__(self):
        self.table_of_shortlinks = []

    def add_shortlink(self, shortlink, longlink, password):
        self.table_of_shortlinks.append(Shortlink(shortlink, longlink, password))

    def get_num_of_shortlinks(self):
        return len(self.table_of_shortlinks)

    def __str__(self):
        string = '['

        links = []
        for link in self.table_of_shortlinks:
            links.append(str(link))

        string += ','.join(links)

        string += ']'
        return string
