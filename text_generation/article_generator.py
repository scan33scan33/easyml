import sys
import re
import random

PUNCTUATORS = [',', ':', '.', ';']

class ArticleGenerator:
    def __init__(self):
        self.transition = {}
    
    def Learn(self, article):
        words = re.findall(r"[\w|']+|[^\s]", article)
        self.transition['^'] = [words[0]]
        self.transition[words[-1]] = ['$']
        for i in range(len(words) - 1):
            if words[i] not in self.transition:
                self.transition[words[i]] = []
            self.transition[words[i]].append(words[i + 1])

    def Generate(self):
        result = ''
        word = '^'
        while True:
            word = (self.transition[word][random.randint(
                        0, len(self.transition[word]) - 1)])
            if word is '$':
                break
            result += word in PUNCTUATORS and word or ' ' + word
        return result

if __name__ == '__main__':
    article_generator = ArticleGenerator()
    with open(sys.argv[1], 'r') as f:
        article_generator.Learn(f.read())
    print article_generator.Generate()
