import random
import string
from medusa.learners import parse_ingenierias_markdown


def random_word(min_len=1, max_len=50):
    return "".join(random.choice(string.printable) for _ in range(random.randint(min_len, max_len)))


def test_parser_fuzz_no_crash_small_batch():
    for _ in range(200):
        n = random.randint(1, 5)
        md_parts = []
        for i in range(n):
            name = random_word(1, 20)
            # create random number of fields
            fields = []
            for _ in range(random.randint(0, 4)):
                k = random_word(1, 15)
                v = random_word(0, 200)
                fields.append(f"- {k}: {v}")
            md_parts.append("### " + name)
            md_parts.extend(fields)
        md = "\n".join(md_parts)
        res = parse_ingenierias_markdown(md)
        # number of parsed disciplines should equal number of headings
        assert len(res) == n
        for e in res:
            assert "name" in e
