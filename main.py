import sqlite3
import argparse

# parser = argparse.ArgumentParser()
# parser.add_argument("-k", "--keyword", type = str)
# parser.add_argument("-d", "--dbname", type = str)
# args = parser.parse_args()

# ich kann nicht argsParse konfiguirieren.

kw = '%Schwarz%'

con = sqlite3.connect("./imdb/imdb.db") 

# Teilaufgabe a, b1
print ("MOVIES")
cur_a = con.cursor()
cur_a.execute("SELECT DISTINCT m.title, m.year, g.genre FROM movie m JOIN genre g ON m.mid = g.movie_id WHERE m.title LIKE ?", (kw, ))
ans_a = []
for row in cur_a.fetchall():
    ans_a += row
print(*tuple(set(ans_a)), sep = ', ') 

# Teilaufgabe b2
cur_b = con.cursor()
cur_b.execute("SELECT DISTINCT sp.name FROM (SELECT * FROM actor UNION SELECT * FROM actress ) AS sp JOIN movie m ON sp.movie_id = (SELECT m.mid FROM movie m WHERE m.title LIKE ?) WHERE sp.movie_id = m.mid ORDER BY sp.name ASC LIMIT 5;", (kw,))
for ans_b in cur_b.fetchall():
    print(*ans_b, sep = ', ')

# Teilaufgabe c
print("\nACTORS")
cur_c = con.cursor()
cur_c.execute("SELECT DISTINCT sp.name  FROM ( SELECT * FROM actor UNION SELECT * FROM actress ) AS sp WHERE sp.name LIKE ? ORDER BY sp.name ASC;", (kw,))
for ans_c in cur_c.fetchall():
    print(*ans_c, sep = ', ')

# Teilaufgabe d
print("PLAYED IN")
cur_d1 = con.cursor()
cur_d1.execute("SELECT DISTINCT m.title FROM (SELECT * FROM actor UNION SELECT * FROM actress ) AS sp1 JOIN (SELECT * FROM actor UNION SELECT * FROM actress ) AS sp2 ON sp1.movie_id = sp2.movie_id JOIN movie m ON sp1.movie_id = m.mid WHERE sp1.name LIKE ? AND sp1. name <> sp2.name GROUP BY sp2.name ORDER BY COUNT(sp2.movie_id) DESC, sp2.name ASC;", (kw,))
for ans_d1 in cur_d1.fetchall():
    print(*ans_d1, sep = ', ')

print("CO-STARS")
cur_d2 = con.cursor()
cur_d2.execute("SELECT DISTINCT sp2.name, COUNT(sp2.movie_id) FROM (SELECT * FROM actor UNION SELECT * FROM actress ) AS sp1 JOIN (SELECT * FROM actor UNION SELECT * FROM actress ) AS sp2 ON sp1.movie_id = sp2.movie_id JOIN movie m ON sp1.movie_id = m.mid WHERE sp1.name LIKE ? AND sp1. name <> sp2.name GROUP BY sp2.name ORDER BY COUNT(sp2.movie_id) DESC, sp2.name ASC LIMIT 5;", (kw,))
for ans_d2 in cur_d2.fetchall():
    print(ans_d2[0], "(", ans_d2[1], ")")

# Aufgabe 5 fertig machen
con.commit()
con.close()