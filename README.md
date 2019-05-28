# That's Fantastic

A collection of information around my Fantastic Fest experiences.

## Installation Tips

`pyscopg2` may not compile/install correctly on macOS if certain libraries can't be found by the compiler. In particular, compiles were failing when openssl libraries were not found. I set `export LDFLAGS="-L/usr/local/opt/openssl/lib"; export CPPFLAGS="-I/usr/local/opt/openssl/include";` to tell the compiler where to find Homebrew-installed openssl and things worked after that.

# Getting started

First, *PostgreSQL* is the required database. This project uses PostgreSQL fields and features, such as Array fields and VIEWs. The *cinema* app's initial migration creates a GIN index on the country field of the Film model, and a *cinema_countries* PostgreSQL VIEW that presents distinct country names as populated from the film tables countries array column.

## Populating data

After you create the database, you can populate it with some included data:

If you run `python manage.py loaddata fantasticfest/fixtures/fantasticfests.json` to create event entries for Fantastic Fests, you'll be able to run the following to import film data for 2012-2015 and associate each film with the correct festival:

```shell
for i in {2012..2015}; do python manage.py importfilms --event fantastic-fest-$i data/films/$i; echo "Pant, pant, pant."; done;
```

## Scraping new films

You could run something like the following to scrape films from a website, but that may be cruel.

```
for i in {2012..2015}; do python manage.py scrapefilmsfromlist --savepath data/films/$i --url http://fantasticfest.com/films/category/festival-year-$i --max-pages 7; echo "Pant, pant, pant."; done;
```
