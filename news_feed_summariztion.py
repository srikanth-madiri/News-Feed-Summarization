from nltk.tokenize import sent_tokenize,word_tokenize
from nltk.corpus import stopwords
from collections import defaultdict
from string import punctuation
from heapq import nlargest

import urllib
from bs4 import BeautifulSoup

class FrequencySummarizer:
	
	def __init__(self, min_cut=0.1, max_cut=0.9):
		
		self._min_cut = min_cut
		self._max_cut = max_cut 
		self._stopwords = set(stopwords.words('english') + list(punctuation))

	def _compute_frequencies(self, word_sent):
		
		freq = defaultdict(int)
		for s in word_sent:
			for word in s:
				if word not in self._stopwords:
					freq[word] += 1
		m = float(max(freq.values()))
		for w in list(freq):
		   freq[w] = freq[w]/m
		   if freq[w] >= self._max_cut or freq[w] <= self._min_cut:
		   	del freq[w]
		return freq

	def summarize(self, text, n):
		
		sents = sent_tokenize(text)
		assert n <= len(sents)
		word_sent = [word_tokenize(s.lower()) for s in sents]
		self._freq = self._compute_frequencies(word_sent)
		ranking = defaultdict(int)
		for i,sent in enumerate(word_sent):
		#	print(i);
		#	print(sent);
			for w in sent:
				if w in self._freq:
					ranking[i] += self._freq[w]
		sents_idx = self._rank(ranking, n)
		return [sents[j] for j in sents_idx]

	def _rank(self, ranking, n):
	
		return nlargest(n, ranking, key=ranking.get)





def get_only_text(url):
	page = urllib.request.urlopen(url).read().decode('utf8')
	soup = BeautifulSoup(page)
	text = ' '.join(map(lambda p: p.text, soup.find_all('p')))
	return soup.title.text, text

feed_xml = urllib.request.urlopen('http://feeds.bbci.co.uk/news/rss.xml').read()
feed = BeautifulSoup(feed_xml.decode('utf8'))
to_summarize = map(lambda p: p.text, feed.find_all('guid'))

fs = FrequencySummarizer()

for article_url in to_summarize:
	title, text = get_only_text(article_url)
	print('----------------------------------')
	print (title)
	print('----------------------------------')
	for s in fs.summarize(text, 2):
		print(s)
