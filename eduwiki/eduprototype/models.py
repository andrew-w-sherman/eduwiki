from django.db import models

class User(models.Model):
    class Meta:
        verbose_name = ('User')
        verbose_name_plural = ('Users')

    def __unicode__(self):
        pass
    
    name = models.CharField(max_length=50)

class WikiPage(models.Model):
    class Meta:
        verbose_name = ('WikiPage')
        verbose_name_plural = ('WikiPages')

    def __unicode__(self):
        return title
    
    title = models.CharField(verbose_name="title of the page", max_length=255, primary_key=True)
    page_id = models.IntegerField(verbose_name="id of the page")
    url = models.URLField(verbose_name="the url of the page")
    mod_date = models.DateTimeField(verbose_name="last modified date", auto_now=True)
    links = models.ManyToManyField("self", through="Link", symmetrical=False, related_name="backlinks")
    wikitext = models.CharField(verbose_name="page wikitext", max_length=10000)
    description = models.CharField(verbose_name="a quick description for the page", max_length = 500)
    disambiguation = models.BooleanField(verbose_name="whether or not the page is a disambiguation")

class Link(models.Model):
    class Meta:
        verbose_name = ('Link')
        verbose_name_plural = ('Links')

    def __unicode__(self):
        return "Detail on link from" + source.title + "to" + target.title + "."
    
    source = models.ForeignKey(WikiPage, related_name="source")
    target = models.ForeignKey(WikiPage, related_name="target")
    position = models.IntegerField(verbose_name="relative position on the page", primary_key=True)

class Review(models.Model):
    class Meta:
        verbose_name = ('Review')
        verbose_name_plural = ('Reviews')

    def __unicode__(self):
        pass

    root = models.ForeignKey(WikiPage, verbose_name="the review the user started from", related_name="descendents")
    parent = models.ForeignKey('self', verbose_name="the review the user did above this one", related_name="children")
    page = models.ForeignKey(WikiPage, verbose_name="the page the user was branching from", related_name="reviews")
    presented_prereqs = models.ManyToManyField(WikiPage, verbose_name="the prereqs presented to the user", related_name="sessions_presented")
    chosen_prereqs = models.ManyToManyField(WikiPage, verbose_name="the prereqs the user chose from the list", related_name="sessions_chosen")
    suggested_prereq_name = models.CharField(verbose_name="the prereq the user suggested, in text form", max_length=200)
    suggested_prereq = models.ForeignKey(WikiPage, verbose_name="the prereq the user suggested, connected to a page if possible", related_name="suggested_parents")
    
    
class PrereqFeedback(models.Model):
    class Meta:
        verbose_name = ('PrereqFeedback')
        verbose_name_plural = ('PrereqFeedbacks')

    def __unicode__(self):
        pass
    
    prereq_page = models.ForeignKey(WikiPage, verbose_name="the page of the presented prereq")
    was_good = models.BooleanField(verbose_name="whether or not the prereq was good")
    suggested_distractor_name = models.CharField(verbose_name="the name of the distractor topic suggested", max_length=100)
    suggested_distractor_page = models.ForeignKey(WikiPage, verbose_name="if it can be connected, the page suggested by the user as a distractor", related_name="suggested_to_distract")
    suggested_distractor_snippet = models.CharField(verbose_name="the snippet suggested by the user", max_length=500)
    
class DistractorFeedback(models.Model):
    class Meta:
        verbose_name = ('DistractorFeedback')
        verbose_name_plural = ('DistractorFeedbacks')

    def __unicode__(self):
        pass
    
    user = models.ForeignKey(User, verbose_name="the user who gave the feedback")
    snippet = models.CharField(verbose_name="the snippet presented", max_length=400)
    was_good = models.BooleanField(verbose_name="whether or not the distractor was acceptable")
    distractor_page = models.ForeignKey(WikiPage, verbose_name="the page the distractor was from", related_name='feedback_as_distractor')
    distracted_page = models.ForeignKey(WikiPage, verbose_name="the page of the correct answer", related_name='feedback_of_distractors')
    review = models.ForeignKey(Review, verbose_name="the review this is from", related_name='distractor')
    

    
    