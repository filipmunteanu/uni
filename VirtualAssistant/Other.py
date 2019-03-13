import wikipedia
from Play import Play


class Other:
	
	player = Play()

	def stop_talking(self):
		self.player.respond("stop_talking_reply.mp3")

	def tell_iq(self):
		self.player.respond("reveal_iq.mp3")

	def tell_about_today(self):
		self.player.respond("about_today.mp3")

	def thank_you(self):
		self.player.respond("thank_you_compliment.mp3")

	def wikipedia_search(self, search_term):
		try:
			definition = wikipedia.summary(search_term, sentences = 2)
			# print definition
			self.player.play_this(definition)
		except Exception:
			self.player.respond("wikipedia_not_found.mp3")