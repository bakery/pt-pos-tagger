# -*- coding: utf-8 -*-

import codecs
import nltk
from pickle import dump, load
from parse_rest.connection import register
from parse_rest.datatypes import Object

Verbs = Object.factory('verbs')

class Tagger:
  def __init__(self, options):
    register(options['parse_app_id'], options['parse_api_key'])
    self.load_tagger(options['tagger_filename'])
    self.load_sentence_tokenizer(options['sentence_tokenizer_filename'])

  def tag_text(self, text):
    sentences = self.__sent_detector.tokenize(text)
    return map(self.tag_sentence, sentences)

  def tag_sentence(self, sentence):
    tokens = sentence.split()
    tags = self.__tagger.tag(tokens)
    return ' '.join(map(self.process_tags, tags))

  def load_tagger(self, filename):
    input = open(filename, 'rb')
    self.__tagger = load(input)
    input.close()
  
  def load_sentence_tokenizer(self, filename):
    self.__sent_detector = nltk.data.load(filename)

  def lookup_verb(self, verb):
    verbs = Verbs.Query.filter(verb=verb)
    verbs = verbs._fetch()
    if len(verbs) > 0:
      infinitives = set(map(lambda v: v.infinitive, verbs))
      tenses = set(map(lambda v: v.tense, verbs))
      if len(infinitives) == 1 and len(tenses) == 1:
        return verbs[0]
    return None

  def process_tags(self, t):
    # 'v-fin', 'v-ger', 'v-inf', 'v-pcp'
    VERB_TAGS = ['v-fin', 'v-ger', 'v-pcp']
    if t[1] in VERB_TAGS:
      verb_data = self.lookup_verb(t[0])
      verb_data_str = ''
      if verb_data:
        verb_data_str = '<sup>{0} // {1}</sup>'.format(verb_data.infinitive,verb_data.tense)
      return u'<mark>{0}</mark>{1}'.format(t[0],verb_data_str)
    else:
      return t[0]
