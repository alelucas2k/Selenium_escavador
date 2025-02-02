from scraper_facade import ScraperFacade
from database import Database

db = Database()
db.executar("CREATE TABLE IF NOT EXISTS professores (id INTEGER PRIMARY KEY, nome TEXT UNIQUE, status TEXT DEFAULT 'pendente')")

professores = ["Victor André Pinho de Oliveira", "Paulo Ribeiro Lins Junior", "Katyusco Santos", "Alexandre Sales Vasconcelos"]
for professor in professores:
    db.executar("INSERT OR IGNORE INTO professores (nome) VALUES (?)", (professor,))

scraper = ScraperFacade()

for professor in db.buscar("SELECT nome FROM professores WHERE status = 'pendente'"):
    scraper.buscar_professor(professor[0])

scraper.fechar()
db.fechar()