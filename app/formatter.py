from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

class Formatter(HtmlFormatter):
    coverage_classes = {
        1: "hit",
        0: "miss",
        None: "never",
    }
    
    def __init__(self, coverage, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.coverage = coverage
    
    def _format_lines(self, tokensource):
        line_number = 0
        for is_line, line in super()._format_lines(tokensource):
            if is_line:
                line_number += 1
            cov = self.coverage[line_number-1]
            covcls = self.coverage_classes[cov]
            line = f"<tr class=\"{covcls}\"><td><pre>{line_number}</pre></td><td><pre>{line}</pre></td></tr>\n"
            yield is_line, line

    def wrap(self, source, outfile):
        return self._wrap(source)

    def _wrap(self, inner):
        yield 0, "<table class=\"code\">\n"
        for line in inner:
            yield line
        yield 0, "</table>\n"
    
    def format_unencoded(self, tokensource, outfile):
        source = self._format_lines(tokensource)
        source = self.wrap(source, outfile)
        for t, piece in source:
            outfile.write(piece)

style = """
<style>
h1 {
    font-family: sans-serif;
    font-size: 18px;
}
.code tr {
}
.code td {
    padding: 4px;
    border: none;
    font-size: 12px;
}
.code {
    border-spacing: 0;
    border-collapse: separate;
    min-width: 700px;
}
.code pre {
    margin: 0;
    padding: 0;
}
.hit {
    background-color: rgba(208,233,153,0.5);
}
.miss {
    background-color: rgba(216,134,123,0.5);
}
.never {
    background-color: #fff;
}
</style>
"""

def run(filename, code, coverage):
    formatter = Formatter(coverage)
    highlighted = highlight(code, PythonLexer(), formatter)
    output = ""
    output += style
    output += "<style>"
    output += formatter.get_style_defs()
    output += "</style>"
    output += f"<h1>{filename}</h1>"
    output += highlighted
    return output
