from models import Base, engine, Categories, Teams, User
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

import sys
import codecs
engine = engine
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create default user to add to initial catalog
user_d = User(name='Meghan Riccardelli', email='bestx08@aol.com',
              picture='https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7cToFPGhSu5sLWo0MN-8F0OjC3i26jRFz-DFhty7NKv6hApcZ')
session.add(user_d)
session.commit()

cat0 = Categories(category_name='Basketball', user_id=1)
session.add(cat0)
session.commit()

cat1 = Categories(category_name='Soccer', user_id=1)
session.add(cat1)
session.commit()

cat2 = Categories(category_name='Baseball', user_id=1)
session.add(cat2)
session.commit()

cat3 = Categories(category_name='Hockey', user_id=1)
session.add(cat3)
session.commit()


team1 = Teams(team_name='Atlanta Hawks',
              team_details='American professional basketball team based in Atlanta, Georgia.',
              category=cat0, user_id=1)
session.add(team1)
session.commit()

team2 = Teams(team_name='Cleveland Cavaliers',
              team_details="often referred to as the Cavs, are an American professional basketball team based in Cleveland, Ohio. The Cavs compete in the National Basketball Association (NBA) as a member of the league's Eastern Conference Central Division.",
              category=cat0, user_id=1)
session.add(team2)
session.commit()

team3 = Teams(team_name='New York Knicks',
              team_details="more commonly referred to as the Knicks, are an American professional basketball team based in the borough of Manhattan, in New York City.",
              category=cat0, user_id=1)
session.add(team3)
session.commit()

team4 = Teams(team_name='Real Madrid CF',
              team_details="commonly known as Real Madrid, is a professional football club based in Madrid, Spain.",
              category=cat1, user_id=1)
session.add(team4)
session.commit()

team5 = Teams(team_name='FC Barcelona',
              team_details="known simply as Barcelona and colloquially as Barca, is a professional football club based in Barcelona, Catalonia, Spain.",
              category=cat1, user_id=1)
session.add(team5)
session.commit()

team6 = Teams(team_name='Club Atletico de Madrid',
              team_details="commonly known as Atletico Madrid, or simply as Atletico or Atleti, is a Spanish professional football club based in Madrid, that play in La Liga.",
              category=cat1, user_id=1)
session.add(team6)
session.commit()

team7 = Teams(team_name='New York Yankees',
              team_details="an American professional baseball team based in the New York City borough of the Bronx. The Yankees compete in Major League Baseball (MLB) as a member club of the American League (AL) East division.",
              category=cat2, user_id=1)
session.add(team7)
session.commit()

team8 = Teams(team_name='Boston Red Sox',
              team_details="an American professional baseball team based in Boston, Massachusetts. The Red Sox compete in Major League Baseball (MLB) as a member club of the American League (AL) East division.",
              category=cat2, user_id=1)
session.add(team8)
session.commit()

team9 = Teams(team_name='Los Angeles Dodgers',
              team_details="an American professional baseball team based in Los Angeles, California. The Dodgers compete in Major League Baseball (MLB) as a member club of the National League (NL) West division.",
              category=cat2, user_id=1)
session.add(team9)
session.commit()

team10 = Teams(team_name='Vegas Golden Knights',
               team_details="a professional ice hockey team based in the Las Vegas metropolitan area that began play in the 2017 NHL season.",
               category=cat3, user_id=1)
session.add(team10)
session.commit()

team11 = Teams(team_name='San Jose Sharks',
               team_details="a professional ice hockey team based in San Jose, California. They are members of the Pacific Division of the Western Conference of the National Hockey League (NHL).",
               category=cat3, user_id=1)
session.add(team11)
session.commit()

team12 = Teams(team_name='Toronto Maple Leags',
               team_details="are a professional ice hockey team based in Toronto, Ontario. They are members of the Atlantic Division of the Eastern Conference of the National Hockey League (NHL).",
               category=cat3, user_id=1)
session.add(team12)
session.commit()

print('Finished adding data!')
