"""
"""

import re

from markdown import Extension
from markdown.inlinepatterns import Pattern, IMAGE_REFERENCE_RE


class DanglingImageReferencePattern(Pattern):
    """ If a stored reference is not found assume this is a figure link and
        feed to the appropriate template. """
    #We use code copied from the python-markddown core for image links, but jump
    #  on dangling references before it gets a chance to complain.

    NEWLINE_CLEANUP_RE = re.compile(r'[ ]?\n', re.MULTILINE)

    def handleMatch(self, m):
        try:
            id = m.group(9).lower()
        except IndexError:
            id = None
        if not id:
            # if we got something like "[Google][]" or "[Google]"
            # we'll use "google" as the id
            id = m.group(2).lower()

        # Clean up linebreaks in id
        id = self.NEWLINE_CLEANUP_RE.sub(' ', id)
        if id in self.markdown.references:  # Pass on defined references.
            return None

        text = m.group(2)
        return self.makeTag(id, text)

    def makeTag(self, id, text):
        return '{{% figure {} "{}" %}}'.format(id, text)


class FigureExtension(Extension):
    def extendMarkdown(self, md, md_globals):
        md.inlinePatterns.add('dangling_image_reference',
                              DanglingImageReferencePattern(IMAGE_REFERENCE_RE, md),
                              '<image_reference')

def makeExtension(**kwargs):
    return FigureExtension(**kwargs)
