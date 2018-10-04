import random
from typing import List

from trepan.processor.command.base_submgr import capitalize


class NameGenerator:
    @staticmethod
    def generate() -> str:
        syllables = list(NameGenerator.HIGHLANDER_SYLLABLES)

        def get_num_components() -> int:
            pool = [2, 2, 2, 3]
            index = random.randint(0, len(pool) - 1)
            return pool[index]

        name = []
        for i in range(get_num_components()):
            index = random.randint(0, len(syllables) - 1)
            component = syllables.pop(index)
            name.append(component)
        return capitalize(''.join(name))

    FILTER = ['hair', 'naan', 'seinen', 'feilun', 'wonka', 'anal', 'shit', 'lol', 'tada', 'groan', 'shota',
              'futa', 'satan']

    GROUPS = {
        'Researcher': [],
        'Adventurer': [],
        'Archaeologist': [],
        'Paladin': [],
        'Enforcer': [],
        'Cultist': [],
        'Scholar': [],
        'Merchant': [],
        'Collector': [],
        'Magister': [],
        'Overseer': [],
        'Warrior': []
    }

    REDIN_SYLLABLES = ['mal', 'run', 'ae', 'kor', 'ith', 'tok', 'ro', 'sha', 'thro', 'storn', 'ja', 'bal',
                       'nha', 'han', 'on', 'no', 'os', 'or', 'im', 'la', 'wa', 'yal', 'fii', 'olb', 'arn', 'gan',
                       'ul', 'lok', 'krol', 'umn', 'sek', 'rha', 'rho', 'nu', 'kun', 'ber', 'nol', 'ish', 'an',
                       'rak', 'to', 'kro', 'aul', 'rae', 'li', 'y', 'sho']

    TIGRUN_SYLLABLES = ['ga', 'wa', 'yi', 'sho', 'ku', 'renn', 'ya', 'ka', 'ro', 'lun', 'fei', 'li', 'bai',
                        'hu', 'kan', 'yu', 'e', 'shi', 'wa', 'ir', 'ha', 'rai', 'rhi', 'al', 'won', 'ta',
                        'miu', 'ko', 'fun', 'tai', 'tan', 'zau', 'hom', 'ang', 'ri', 'hwa', 'jun', 'ban', 'ba',
                        'gunn', 'fu', 'dai', 'ji', 'toh', 'sei', 'o', 'yuu', 'su', 'sai', 'hii', 'yu',
                        'mao', 'jang', 'na']

    UMRIN_SYLLABLES = ['xir', 'sei', 'xia', 'nan', 'um', 'xis', 'rix', 'zen', 'ri', 'sa', 'in', 'te', 'za', 'zan',
                       'ix', 'im', 'en', 'iil', 'an', 'or', 'sun', 'ai', 'zue', 'ban', 'gi', 'ten', 'rat',
                       'ril', 'ez', 'nas', 'nen', 'ci', 'cia', 'tan', 'ke', 'ser', 'ti', 'set', 'zer', 'val',
                       'jin', 'xu', 'xen', 'lu', 'ma', 'el', 'ish', 'zel', 'zet', 'ys', 'cy']

    RIKELRIN_SYLLABLES = ['as', 'tha', 'ros', 'ta', 'yv', 'od', 'gro', 'mul', 'da', 'ga', 'ron', 'gor', 'nov',
                          'va', 'nos', 'nod', 'kor', 'an', 'um', 'dra', 'ath', 'born', 'kar', 'olb',
                          'veng', 'rik', 'rol', 'naz', 'ung', 'na', 'tev', 'vin', 'ul', 'tov', 'ata', 'tro',
                          'bor']

    RYAS_SYLLABLES = ['kax', 'zi', 'io', 'nyx', 'ky', 'var', 'fer', 'ze', 'den', 'nar', 'mar', 'rho', 'syl', 'zer',
                      'sol', 'set', 'yos', 'nia', 'ia', 'nae', 'a', 'xil', 'ind', 'va', 'ar', 'naz', 'ir', 'nem',
                      'rys', 'ari', 'an', 'em', 'en', 'kin', 'rhy', 'to', 'zet', 'gal', 'kand', 'nar', 'seo', 'ies',
                      'cass', 'zha', 'ius', 'stra', 'ian']

    HIGHLANDER_SYLLABLES = ['kur', 'rek', 'gen', 'ban', 'jan', 'lan', 'ul', 'ric', 'jorn', 'donn', 'nal', 'thar',
                            'orn', 'gor', 'kor', 'zan', 'sab', 'el', 'in', 'os', 'ro', 'reth', 'toh', 'rahl',
                            'roth', 'vol', 'rath', 'zen', 'ren', 'dol', 'aen', 'ind', 'rha', 'thor', 'jol',
                            'aul', 'ta', 'bar', 'ad', 'den', 'wen', 'ma', 'rod', 'dath', 'if', 'thek', 'dar',
                            'nos', 'dra', 'du', 'yn', 'ya', 'gar', 'ae', 'stro', 'rit', 'sor', 'jen', 'auk', 'ran',
                            'stom', 'rom']

for i in range(100):
    print(NameGenerator.generate())

