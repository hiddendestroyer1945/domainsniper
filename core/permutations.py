import idna

class Permutator:
    def __init__(self, domain_name):
        self.domain = domain_name.lower()
        self.variants = set()
        
        self.keyboard_map = {
            'q': 'wa', 'w': 'qesad', 'e': 'wrsdf', 'r': 'etfdg', 't': 'ryfgh', 'y': 'tughj', 'u': 'yihjk', 'i': 'uokjl', 'o': 'iplk', 'p': 'ol',
            'a': 'qwsz', 's': 'qwedxz', 'd': 'werfxc', 'f': 'ertgvc', 'g': 'rtyhvb', 'h': 'tyujnb', 'j': 'uikmn', 'k': 'iolm', 'l': 'op',
            'z': 'asx', 'x': 'zsdc', 'c': 'xdfv', 'v': 'cfgb', 'b': 'vghn', 'n': 'bhjm', 'm': 'njk'
        }
        
        self.homograph_map = {
            'a': ['а', 'à', 'á', 'â', 'ã', 'ä', 'å', 'ɑ', 'α'],
            'b': ['Ь', 'в', 'β', 'б'],
            'c': ['с', 'ç', 'ć', 'ĉ', 'ċ', 'č', '¢'],
            'd': ['ԁ', 'ď', 'đ'],
            'e': ['е', 'è', 'é', 'ê', 'ë', 'ē', 'ĕ', 'ė', 'ę', 'ě', 'ε'],
            'g': ['ɡ', 'ġ', 'ģ', 'ğ', 'ĝ'],
            'h': ['һ', 'ĥ', 'ħ'],
            'i': ['і', 'í', 'ì', 'ï', 'ı', 'ɩ', 'ι'],
            'j': ['ј', 'ĵ'],
            'k': ['ќ', 'ķ', 'ĸ', 'к', 'κ'],
            'l': ['ӏ', 'ĺ', 'ļ', 'ľ', 'ŀ', 'ł', 'ι'],
            'm': ['ⅿ', 'м'],
            'n': ['ո', 'ñ', 'ń', 'ņ', 'ň', 'η', 'π'],
            'o': ['о', 'ò', 'ó', 'ô', 'õ', 'ö', 'ø', 'ō', 'ŏ', 'ő', 'ο'],
            'p': ['р', 'þ', 'ρ'],
            'q': ['ԛ'],
            'r': ['г', 'ŕ', 'ŗ', 'ř'],
            's': ['ѕ', 'ś', 'ŝ', 'ş', 'š'],
            't': ['т', 'ť', 'ŧ', 'τ'],
            'u': ['υ', 'ù', 'ú', 'û', 'ü', 'ũ', 'ū', 'ŭ', 'ů', 'ű', 'ų'],
            'v': ['ν'],
            'w': ['ԝ', 'ŵ'],
            'x': ['х', 'χ'],
            'y': ['у', 'ý', 'ÿ', 'ŷ', 'υ'],
            'z': ['ᴢ', 'ź', 'ż', 'ž']
        }

    def generate_all(self):
        self.typosquatting()
        self.homographs()
        self.combosquatting()
        self.bitsquatting()
        self.sucks_domains()
        return sorted(list(self.variants))

    def typosquatting(self):
        # Omission
        for i in range(len(self.domain)):
            self.variants.add(self.domain[:i] + self.domain[i+1:])
        
        # Repetition
        for i in range(len(self.domain)):
            self.variants.add(self.domain[:i] + self.domain[i] + self.domain[i] + self.domain[i+1:])
            
        # Keyboard swap
        for i, char in enumerate(self.domain):
            if char in self.keyboard_map:
                for replacement in self.keyboard_map[char]:
                    self.variants.add(self.domain[:i] + replacement + self.domain[i+1:])

    def homographs(self):
        for i, char in enumerate(self.domain):
            if char in self.homograph_map:
                for homograph in self.homograph_map[char]:
                    # Generate simple single substitution
                    alt_domain = self.domain[:i] + homograph + self.domain[i+1:]
                    try:
                        # Ensure it's valid IDNA
                        self.variants.add(idna.encode(alt_domain).decode('ascii'))
                    except:
                        pass

    def combosquatting(self):
        keywords = ['login', 'secure', 'support', 'verify', 'account', 'update', 'portal', 'auth', 'mail']
        for kw in keywords:
            self.variants.add(f"{self.domain}-{kw}")
            self.variants.add(f"{self.domain}{kw}")

    def bitsquatting(self):
        for i in range(len(self.domain)):
            char_code = ord(self.domain[i])
            for b in range(8):
                new_code = char_code ^ (1 << b)
                new_char = chr(new_code)
                if new_char.isalnum() or new_char == '-':
                    self.variants.add(self.domain[:i] + new_char + self.domain[i+1:])

    def sucks_domains(self):
        suffixes = ['-sucks', 'sucks', 'reviews', '-reviews', 'audit', '-audit']
        for suffix in suffixes:
            self.variants.add(f"{self.domain}{suffix}")
