import os
try:
  from PIL import Image
except ImportError:
  import Image
import pytesseract
from pytesseract import TesseractNotFoundError
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator

# https://tesseract-ocr.github.io/tessdoc/ImproveQuality.html <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
# https://tesseract-ocr.github.io/tessdoc/Command-Line-Usage.html <<<<<<<<<<<<<

# https://pypi.org/project/pytesseract/

# https://github.com/tesseract-ocr/tesseract

# https://stackoverflow.com/questions/46184239/extract-a-page-from-a-pdf-as-a-jpeg

# https://www.datacamp.com/community/tutorials/wordcloud-python

# TODO: move all of the functional code to its own repo; add logic here to clone that repo into the res dir if it's not there

# Contains all methods called by readText() as well as interpreter-specific methods that
# must be overriden.
class TextInterpreterBase(object):
  def getRawOutput(self, imgfile, debug=False):
    output = self._get_raw_output(imgfile)
    if debug:
      self._log_raw_debug()
    return output
  
  def getGroupedOutput(self, imgfile, debug=False):
    output = self._get_grouped_output(imgfile)
    if debug:
      self._log_grouped_debug()
    return output

  def getJoinedOutput(self, imgfile, debug=False):
    output = self._get_joined_output(imgfile)
    if debug:
      self._log_joined_debug()
    return output

  def _get_raw_output(self, imgfile):
    pass
  def _log_raw_debug(self):
    pass
  def _get_grouped_output(self, imgfile):
    pass
  def _log_grouped_debug(self):
    pass
  def _get_joined_output(self, imgfile):
    pass
  def _log_joined_debug(self):
    pass

class TesseractTextInterpreter(TextInterpreterBase):
  def _get_raw_output(self, imgfile):
    pass # TODO
  def _log_raw_debug(self):
    pass # TODO

  def _get_grouped_output(self, imgfile):
    pass # TODO
  def _log_grouped_debug(self):
    pass # TODO

  def _get_joined_output(self, imgfile):
    output = dict()
    output['filename'] = imgfile
    try:
      parsing = pytesseract.image_to_string(Image.open(imgfile))
    except TesseractNotFoundError:
      print('pytesseract call failed. Is tesseract installed? [sudo apt install tesseract-ocr libtesseract-dev]')
      raise
    corrected_parsing = parsing.replace('|','I')
    lines = [line for line in corrected_parsing.split('\n') if not (line.replace(' ','').strip() == '')]
    output['lines'] = lines
    return output

  def _log_joined_debug(self):
    pass # TODO

# Parser choices
class Parser:
  JOIN = 0
  GROUP = 1
  RAW = 2

# Externally-callable function with all functionality.
def readText(image_filenames, parser=Parser.JOIN, verbose=False, debug=False, format_output=False, wordcloud_output=None, interpreter="tesseract"):
  # TODO: verbose
  # construct input image file name list
  fname_list = list()
  if type(image_filenames) == str:
    fname_list.append(image_filenames)
  else:
    fname_list = image_filenames

  # construct interpreter
  text_reader = None
  if interpreter == "tesseract":
    text_reader = TesseractTextInterpreter()
  else:
    text_reader = TesseractTextInterpreter()

  # interpret text for each image file
  text_interps = list()
  for fname in fname_list:
    if parser == Parser.JOIN:
      text_interps.append(text_reader.getJoinedOutput(fname, debug))
    elif parser == Parser.GROUP:
      text_interps.append(text_reader.getGroupedOutput(fname, debug))
    elif parser == Parser.RAW:
      text_interps.append(text_reader.getRawOutput(fname, debug)) 

  if format_output or not wordcloud_output is None:
    formatted_output = ''
    if parser == Parser.JOIN:
      for interp in text_interps:
        for line in interp['lines']:
          formatted_output += '%s\n' % line
    elif parser == Parser.GROUP:
      pass # TODO
    elif parser == Parser.RAW:
      pass # TODO

    # generate wordcloud and save figure
    if not wordcloud_output is None:
      if verbose:
        print('Generating word cloud...')
      wcfname = os.path.join(os.getcwd(), wordcloud_output.replace('.svg','') + '.svg')
      wordcloud = WordCloud(max_words=100, background_color="white").generate(formatted_output)
      wordcloud_svg = wordcloud.to_svg(embed_font=True)
      with open(wcfname, 'w+') as svgfile:
        svgfile.write(wordcloud_svg)
      if verbose:
        print('Done.\n')

    # if format option set, then return string. else, return python object
    if format_output:
      return formatted_output

  return text_interps
