from django.test import TestCase

from cinema.tests.factories import FilmFactory


class FilmDetailViewTest(TestCase):
    def setUp(self):
        self.film = FilmFactory()

    def test_view_film_detail(self):
        resp = self.client.get(self.film.get_absolute_url())

        self.assertEquals(resp.status_code, 200)
        self.assertContains(resp, self.film.title)
        self.assertContains(resp, self.film.synopsis)
        self.assertContains(resp, self.film.description)
        # self.assertContains(resp, self.film.related_urls)
