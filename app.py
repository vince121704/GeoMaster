from flask import Flask, render_template, request, redirect, session, flash
import random
import sqlite3

app = Flask(__name__)
app.secret_key = 'stem212'
DATABASE = 'game_data.db'

def init_db():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS leaderboard (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            score INTEGER,
            difficulty TEXT
        )
    ''')
    conn.commit()
    conn.close()

def update_leaderboard(username, score, difficulty):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('INSERT INTO leaderboard (username, score, difficulty) VALUES (?, ?, ?)',
              (username, score, difficulty))
    conn.commit()
    conn.close()

def get_leaderboard_scores():
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()
    c.execute('SELECT username, score, difficulty FROM leaderboard ORDER BY score DESC')
    scores = c.fetchall()
    conn.close()
    return scores

questions = [
       {
        'question': 'What is the hardest natural substance on Earth?',
        'choices': ['Diamond', 'Quartz', 'Topaz', 'Corundum'],
        'correct_answer': 'Diamond',
        'difficulty': 'Easy'
    },
    {
        'question': 'Which type of rock is formed from cooling magma or lava?',
        'choices': ['Sedimentary rock', 'Igneous rock', 'Metamorphic rock', 'Granite'],
        'correct_answer': 'Igneous rock',
        'difficulty': 'Easy'
    },
    {
        'question': 'What causes an earthquake?',
        'choices': ['Volcanic eruption', 'Tectonic plate movement', 'Hurricane', 'Tsunami'],
        'correct_answer': 'Tectonic plate movement',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the process by which rock is broken down into smaller particles?',
        'choices': ['Erosion', 'Deposition', 'Weathering', 'Compaction'],
        'correct_answer': 'Weathering',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the study of fossils called?',
        'choices': ['Seismology', 'Paleontology', 'Mineralogy', 'Geomorphology'],
        'correct_answer': 'Paleontology',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the primary gas that makes up the Earth\'s atmosphere?',
        'choices': ['Oxygen', 'Nitrogen', 'Carbon dioxide', 'Argon'],
        'correct_answer': 'Nitrogen',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which layer of the Earth\'s atmosphere is closest to the surface?',
        'choices': ['Troposphere', 'Stratosphere', 'Mesosphere', 'Thermosphere'],
        'correct_answer': 'Troposphere',
        'difficulty': 'Hard'
    },
    {
        'question': 'What is the process of changing a liquid into a gas called?',
        'choices': ['Evaporation', 'Condensation', 'Sublimation', 'Precipitation'],
        'correct_answer': 'Evaporation',
        'difficulty': 'Hard'
    },
    {
        'question': 'What type of rock is formed by the compaction and cementation of sediments?',
        'choices': ['Igneous rock', 'Metamorphic rock', 'Granite', 'Sedimentary rock'],
        'correct_answer': 'Sedimentary rock',
        'difficulty': 'Hard'
    },
    {
        'question': 'What is the softest mineral on the Mohs scale?',
        'choices': ['Talc', 'Gypsum', 'Calcite', 'Feldspar'],
        'correct_answer': 'Talc',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the process of changing a solid directly into a gas called?',
        'choices': ['Melting', 'Evaporation', 'Sublimation', 'Condensation'],
        'correct_answer': 'Sublimation',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which type of rock is formed by the alteration of existing rock under heat and pressure?',
        'choices': ['Igneous rock', 'Metamorphic rock', 'Granite', 'Sedimentary rock'],
        'correct_answer': 'Metamorphic rock',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the process of particles being dropped and deposited by wind, water, or ice called?',
        'choices': ['Weathering', 'Erosion', 'Deposition', 'Compaction'],
        'correct_answer': 'Deposition',
        'difficulty': 'Hard'
    },
    {
        'question': 'What is the name for a naturally occurring solid chemical substance composed of one or more minerals?',
        'choices': ['Rock', 'Mineral', 'Sediment', 'Deposit'],
        'correct_answer': 'Rock',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the study of the Earth\'s physical features, climate, and weather patterns called?',
        'choices': ['Meteorology', 'Geology', 'Climatology', 'Oceanography'],
        'correct_answer': 'Geology',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which type of rock is formed from the accumulation of organic remains?',
        'choices': ['Igneous rock', 'Metamorphic rock', 'Granite', 'Sedimentary rock'],
        'correct_answer': 'Sedimentary rock',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the process by which rocks, minerals, or organic matter are added to a landform or landmass?',
        'choices': ['Deposition', 'Erosion', 'Weathering', 'Compaction'],
        'correct_answer': 'Deposition',
        'difficulty': 'Hard'
    },
    {
        'question': 'What is the study of the Earth\'s oceans and seas called?',
        'choices': ['Oceanography', 'Marine biology', 'Limnology', 'Climatology'],
        'correct_answer': 'Oceanography',
        'difficulty': 'Hard'
    },
 {
        'question': 'What is the largest planet in our solar system?',
        'choices': ['Mars', 'Jupiter', 'Saturn', 'Earth'],
        'correct_answer': 'Jupiter',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the chemical symbol for gold?',
        'choices': ['Ag', 'Au', 'Fe', 'Cu'],
        'correct_answer': 'Au',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the process of converting sunlight into chemical energy in plants called?',
        'choices': ['Photosynthesis', 'Respiration', 'Fermentation', 'Oxidation'],
        'correct_answer': 'Photosynthesis',
        'difficulty': 'Easy'
    },
    {
        'question': 'Which planet is known as the "Red Planet"?',
        'choices': ['Mercury', 'Venus', 'Mars', 'Neptune'],
        'correct_answer': 'Mars',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the largest ocean on Earth?',
        'choices': ['Atlantic Ocean', 'Arctic Ocean', 'Indian Ocean', 'Pacific Ocean'],
        'correct_answer': 'Pacific Ocean',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the study of the Earth\'s physical features, climate, and weather patterns called?',
        'choices': ['Meteorology', 'Geology', 'Climatology', 'Oceanography'],
        'correct_answer': 'Geology',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the process of converting a gas into a liquid called?',
        'choices': ['Condensation', 'Evaporation', 'Sublimation', 'Precipitation'],
        'correct_answer': 'Condensation',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the main component of Earth\'s atmosphere?',
        'choices': ['Oxygen', 'Carbon dioxide', 'Nitrogen', 'Argon'],
        'correct_answer': 'Nitrogen',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the process of changing a liquid directly into a gas called?',
        'choices': ['Sublimation', 'Melting', 'Evaporation', 'Condensation'],
        'correct_answer': 'Evaporation',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the study of fossils called?',
        'choices': ['Seismology', 'Paleontology', 'Mineralogy', 'Geomorphology'],
        'correct_answer': 'Paleontology',
        'difficulty': 'Medium'
    },
    {
        'question': 'What is the process of particles being dropped and deposited by wind, water, or ice called?',
        'choices': ['Weathering', 'Erosion', 'Deposition', 'Compaction'],
        'correct_answer': 'Deposition',
        'difficulty': 'Hard'
    },
    {
        'question': 'Which layer of the Earth\'s atmosphere is closest to the surface?',
        'choices': ['Troposphere', 'Stratosphere', 'Mesosphere', 'Thermosphere'],
        'correct_answer': 'Troposphere',
        'difficulty': 'Hard'
    },
    {
        'question': 'What is the process of changing a solid directly into a gas called?',
        'choices': ['Melting', 'Evaporation', 'Sublimation', 'Condensation'],
        'correct_answer': 'Sublimation',
        'difficulty': 'Hard'
    },
    {
        'question': 'What type of rock is formed by the compaction and cementation of sediments?',
        'choices': ['Igneous rock', 'Metamorphic rock', 'Granite', 'Sedimentary rock'],
        'correct_answer': 'Sedimentary rock',
        'difficulty': 'Hard'
    },
    {
        'question': 'What is the process by which rocks, minerals, or organic matter are added to a landform or landmass?',
        'choices': ['Deposition', 'Erosion', 'Weathering', 'Compaction'],
        'correct_answer': 'Deposition',
        'difficulty': 'Hard'
    },
    {
        'question': 'What is the study of the Earth\'s oceans and seas called?',
        'choices': ['Oceanography', 'Marine biology', 'Limnology', 'Climatology'],
        'correct_answer': 'Oceanography',
        'difficulty': 'Hard'
    },
     {
        'question': 'Which city is known as the "Eternal City"?',
        'choices': ['Rome', 'Athens', 'Paris', 'Cairo'],
        'correct_answer': 'Rome',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the largest desert in the world?',
        'choices': ['Sahara Desert', 'Gobi Desert', 'Arabian Desert', 'Kalahari Desert'],
        'correct_answer': 'Sahara Desert',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which country is known as the "Land of the Midnight Sun"?',
        'choices': ['Norway', 'Sweden', 'Finland', 'Iceland'],
        'correct_answer': 'Norway',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the national animal of Canada?',
        'choices': ['Moose', 'Beaver', 'Polar Bear', 'Bald Eagle'],
        'correct_answer': 'Beaver',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which famous landmark is located in India and known as a symbol of love?',
        'choices': ['Eiffel Tower', 'Great Wall of China', 'Machu Picchu', 'Taj Mahal'],
        'correct_answer': 'Taj Mahal',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the largest lake in Africa?',
        'choices': ['Lake Victoria', 'Lake Tanganyika', 'Lake Malawi', 'Lake Chad'],
        'correct_answer': 'Lake Victoria',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which country is known for its fjords?',
        'choices': ['New Zealand', 'Canada', 'Norway', 'Chile'],
        'correct_answer': 'Norway',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the official language of Brazil?',
        'choices': ['Spanish', 'English', 'Portuguese', 'French'],
        'correct_answer': 'Portuguese',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which continent is known as the "Dark Continent"?',
        'choices': ['Africa', 'Asia', 'Europe', 'South America'],
        'correct_answer': 'Africa',
        'difficulty': 'Easy'
    },
    {
        'question': 'What is the currency of Japan?',
        'choices': ['Yuan', 'Yen', 'Rupee', 'Won'],
        'correct_answer': 'Yen',
        'difficulty': 'Medium'
    },
    {
        'question': 'Which country is known for the Pyramids of Giza?',
        'choices': ['Egypt', 'Mexico', 'Greece', 'India'],
        'correct_answer': 'Egypt',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the capital city of Australia?',
        'choices': ['Sydney', 'Melbourne', 'Canberra', 'Brisbane'],
        'correct_answer': 'Canberra',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the longest river in the world?',
        'choices': ['Nile', 'Amazon', 'Mississippi', 'Yangtze'],
        'correct_answer': 'Nile',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which country is home to the Taj Mahal?',
        'choices': ['India', 'China', 'Turkey', 'Egypt'],
        'correct_answer': 'India',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which continent is known for the Great Barrier Reef?',
        'choices': ['North America', 'Asia', 'Australia', 'Africa'],
        'correct_answer': 'Australia',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the largest desert in the world?',
        'choices': ['Sahara Desert', 'Gobi Desert', 'Atacama Desert', 'Antarctic Desert'],
        'correct_answer': 'Sahara Desert',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which country is known for its tulips and windmills?',
        'choices': ['Netherlands', 'Belgium', 'Denmark', 'Switzerland'],
        'correct_answer': 'Netherlands',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the official language of China?',
        'choices': ['Mandarin', 'Cantonese', 'Shanghainese', 'Tibetan'],
        'correct_answer': 'Mandarin',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which country is known for the Colosseum?',
        'choices': ['Italy', 'Spain', 'Greece', 'France'],
        'correct_answer': 'Italy',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which continent is known for the Amazon Rainforest?',
        'choices': ['Africa', 'South America', 'Asia', 'North America'],
        'correct_answer': 'South America',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the capital city of Canada?',
        'choices': ['Toronto', 'Montreal', 'Ottawa', 'Vancouver'],
        'correct_answer': 'Ottawa',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which country is known for its canals and gondolas?',
        'choices': ['Italy', 'Spain', 'Greece', 'France'],
        'correct_answer': 'Italy',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the official language of Germany?',
        'choices': ['German', 'English', 'French', 'Spanish'],
        'correct_answer': 'German',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which country is known for the Acropolis?',
        'choices': ['Greece', 'Italy', 'Turkey', 'Egypt'],
        'correct_answer': 'Greece',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which continent is known for the Sahara Desert?',
        'choices': ['Africa', 'Asia', 'Europe', 'South America'],
        'correct_answer': 'Africa',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the official language of Russia?',
        'choices': ['Russian', 'English', 'French', 'German'],
        'correct_answer': 'Russian',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which country is known for the Stonehenge?',
        'choices': ['England', 'Scotland', 'Ireland', 'Wales'],
        'correct_answer': 'England',
        'difficulty': 'Easy'
    },

    {
        'question': 'What is the currency of Brazil?',
        'choices': ['Peso', 'Euro', 'Real', 'Dollar'],
        'correct_answer': 'Real',
        'difficulty': 'Easy'
    },

    {
        'question': 'Which country is known for the Great Wall?',
        'choices': ['China', 'India', 'Mexico', 'Egypt'],
        'correct_answer': 'China',
        'difficulty': 'Easy'
    },

        {
        'question': 'Which continent is known for the Eiffel Tower?',
        'choices': ['Europe', 'North America', 'Asia', 'South America'],
        'correct_answer': 'Europe',
        'difficulty': 'Easy'
        },


        {
        'question': 'What is the capital city of Japan?',
        'choices': ['Tokyo', 'Kyoto', 'Osaka', 'Hiroshima'],
        'correct_answer': 'Tokyo',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Statue of Liberty?',
        'choices': ['United States', 'France', 'England', 'Italy'],
        'correct_answer': 'United States',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of Mexico?',
        'choices': ['Spanish', 'English', 'Portuguese', 'French'],
        'correct_answer': 'Spanish',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Angkor Wat?',
        'choices': ['Cambodia', 'Vietnam', 'Thailand', 'Laos'],
        'correct_answer': 'Cambodia',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Serengeti National Park?',
        'choices': ['Africa', 'Asia', 'Europe', 'North America'],
        'correct_answer': 'Africa',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the largest city in South Africa?',
        'choices': ['Cape Town', 'Johannesburg', 'Durban', 'Pretoria'],
        'correct_answer': 'Johannesburg',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Machu Picchu?',
        'choices': ['Peru', 'Bolivia', 'Ecuador', 'Colombia'],
        'correct_answer': 'Peru',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of Egypt?',
        'choices': ['Arabic', 'English', 'French', 'Swahili'],
        'correct_answer': 'Arabic',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Hagia Sophia?',
        'choices': ['Turkey', 'Greece', 'Egypt', 'Italy'],
        'correct_answer': 'Turkey',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Great Wall of China?',
        'choices': ['Asia', 'North America', 'Europe', 'South America'],
        'correct_answer': 'Asia',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the capital city of Spain?',
        'choices': ['Madrid', 'Barcelona', 'Valencia', 'Seville'],
        'correct_answer': 'Madrid',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Christ the Redeemer statue?',
        'choices': ['Brazil', 'Argentina', 'Chile', 'Uruguay'],
        'correct_answer': 'Brazil',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of South Korea?',
        'choices': ['Korean', 'English', 'Mandarin', 'Japanese'],
        'correct_answer': 'Korean',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Petra archaeological site?',
        'choices': ['Jordan', 'Israel', 'Lebanon', 'Saudi Arabia'],
        'correct_answer': 'Jordan',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Matterhorn mountain?',
        'choices': ['Europe', 'Asia', 'Africa', 'South America'],
        'correct_answer': 'Europe',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of Argentina?',
        'choices': ['Spanish', 'English', 'Portuguese', 'French'],
        'correct_answer': 'Spanish',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Blue Mosque?',
        'choices': ['Turkey', 'Greece', 'Egypt', 'Italy'],
        'correct_answer': 'Turkey',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the currency of South Africa?',
        'choices': ['Rand', 'Dollar', 'Peso', 'Euro'],
        'correct_answer': 'Rand',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Alhambra palace?',
        'choices': ['Spain', 'Portugal', 'Italy', 'Morocco'],
        'correct_answer': 'Spain',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Victoria Falls?',
        'choices': ['Africa', 'Asia', 'Europe', 'South America'],
        'correct_answer': 'Africa',
        'difficulty': 'Medium'
        },   
     
        {
        'question': 'Which continent is known for the Eiffel Tower?',
        'choices': ['Europe', 'North America', 'Asia', 'South America'],
        'correct_answer': 'Europe',
        'difficulty': 'Easy'
        },


        {
        'question': 'What is the capital city of Japan?',
        'choices': ['Tokyo', 'Kyoto', 'Osaka', 'Hiroshima'],
        'correct_answer': 'Tokyo',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Statue of Liberty?',
        'choices': ['United States', 'France', 'England', 'Italy'],
        'correct_answer': 'United States',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of Mexico?',
        'choices': ['Spanish', 'English', 'Portuguese', 'French'],
        'correct_answer': 'Spanish',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Angkor Wat?',
        'choices': ['Cambodia', 'Vietnam', 'Thailand', 'Laos'],
        'correct_answer': 'Cambodia',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Serengeti National Park?',
        'choices': ['Africa', 'Asia', 'Europe', 'North America'],
        'correct_answer': 'Africa',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the largest city in South Africa?',
        'choices': ['Cape Town', 'Johannesburg', 'Durban', 'Pretoria'],
        'correct_answer': 'Johannesburg',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Machu Picchu?',
        'choices': ['Peru', 'Bolivia', 'Ecuador', 'Colombia'],
        'correct_answer': 'Peru',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of Egypt?',
        'choices': ['Arabic', 'English', 'French', 'Swahili'],
        'correct_answer': 'Arabic',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Hagia Sophia?',
        'choices': ['Turkey', 'Greece', 'Egypt', 'Italy'],
        'correct_answer': 'Turkey',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Great Wall of China?',
        'choices': ['Asia', 'North America', 'Europe', 'South America'],
        'correct_answer': 'Asia',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the capital city of Spain?',
        'choices': ['Madrid', 'Barcelona', 'Valencia', 'Seville'],
        'correct_answer': 'Madrid',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Christ the Redeemer statue?',
        'choices': ['Brazil', 'Argentina', 'Chile', 'Uruguay'],
        'correct_answer': 'Brazil',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of South Korea?',
        'choices': ['Korean', 'English', 'Mandarin', 'Japanese'],
        'correct_answer': 'Korean',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Petra archaeological site?',
        'choices': ['Jordan', 'Israel', 'Lebanon', 'Saudi Arabia'],
        'correct_answer': 'Jordan',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Matterhorn mountain?',
        'choices': ['Europe', 'Asia', 'Africa', 'South America'],
        'correct_answer': 'Europe',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the official language of Argentina?',
        'choices': ['Spanish', 'English', 'Portuguese', 'French'],
        'correct_answer': 'Spanish',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Blue Mosque?',
        'choices': ['Turkey', 'Greece', 'Egypt', 'Italy'],
        'correct_answer': 'Turkey',
        'difficulty': 'Medium'
        },

        {
        'question': 'What is the currency of South Africa?',
        'choices': ['Rand', 'Dollar', 'Peso', 'Euro'],
        'correct_answer': 'Rand',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which country is known for the Alhambra palace?',
        'choices': ['Spain', 'Portugal', 'Italy', 'Morocco'],
        'correct_answer': 'Spain',
        'difficulty': 'Medium'
        },

        {
        'question': 'Which continent is known for the Victoria Falls?',
        'choices': ['Africa', 'Asia', 'Europe', 'South America'],
        'correct_answer': 'Africa',
        'difficulty': 'Medium'
        },
        {
    'question': 'Which continent is the largest by land area?',
    'choices': ['Asia', 'Antarctica', 'Australia', 'Europe'],
    'correct_answer': 'Asia',
    'difficulty': 'Easy'
},
{
    'question': 'What is the longest river in the world?',
    'choices': ['Amazon River', 'Nile River', 'Mississippi River', 'Yangtze River'],
    'correct_answer': 'Nile River',
    'difficulty': 'Easy'
},
{
    'question': 'Which country is known as the "Land of the Rising Sun"?',
    'choices': ['China', 'Japan', 'India', 'Thailand'],
    'correct_answer': 'Japan',
    'difficulty': 'Easy'
},
{
    'question': 'Which is the largest desert in the world?',
    'choices': ['Sahara Desert', 'Gobi Desert', 'Arabian Desert', 'Kalahari Desert'],
    'correct_answer': 'Sahara Desert',
    'difficulty': 'Medium'
},
{
    'question': 'What is the highest mountain in Africa?',
    'choices': ['Mount Kilimanjaro', 'Mount Everest', 'Mount McKinley', 'Mount Fuji'],
    'correct_answer': 'Mount Kilimanjaro',
    'difficulty': 'Medium'
},
{
    'question': 'Which city is located on two continents?',
    'choices': ['Istanbul', 'Moscow', 'Cairo', 'Athens'],
    'correct_answer': 'Istanbul',
    'difficulty': 'Medium'
},
{
    'question': 'What is the smallest country in the world?',
    'choices': ['Monaco', 'Maldives', 'Vatican City', 'San Marino'],
    'correct_answer': 'Vatican City',
    'difficulty': 'Medium'
},
{
    'question': 'Which country is known as the "Land of a Thousand Lakes"?',
    'choices': ['Sweden', 'Finland', 'Canada', 'Norway'],
    'correct_answer': 'Finland',
    'difficulty': 'Hard'
},
{
    'question': 'What is the largest coral reef system in the world?',
    'choices': ['Great Barrier Reef', 'Belize Barrier Reef', 'Maldives Coral Reef', 'Red Sea Coral Reef'],
    'correct_answer': 'Great Barrier Reef',
    'difficulty': 'Hard'
},
{
    'question': 'Which country is the most populous in the world?',
    'choices': ['India', 'United States', 'China', 'Brazil'],
    'correct_answer': 'China',
    'difficulty': 'Hard'
},
{
    'question': 'What is the driest inhabited continent on Earth?',
    'choices': ['Africa', 'Europe', 'Australia', 'Antarctica'],
    'correct_answer': 'Australia',
    'difficulty': 'Hard'
},
]

@app.route('/start')
def home():
    if 'username' in session:
        return render_template('start.html', username=session['username'])
    return redirect('/start')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/homepage')
def homepage():
    if 'username' in session:
        return render_template('homepage.html', logged_in=True)
    return render_template('homepage.html', logged_in=False)

@app.route('/start')
def start():
    return render_template('start.html')

@app.route('/guest_start')
def guest_start():
    return render_template('guest_start.html')

@app.route('/guest_result')
def guest_result():
    return render_template('guest_result.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    init_db()
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()

        c.execute('SELECT * FROM users WHERE username = ?', (username,))
        existing_user = c.fetchone()
        if existing_user:
            flash('Username already exists. Please choose a different username.')
            return redirect('/register')

        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        conn.close()

        flash('Registration successful. Please login.')
        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        conn = sqlite3.connect(DATABASE)
        c = conn.cursor()
        c.execute('SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
        user = c.fetchone()
        conn.close()
        if user:
            session['username'] = user[1]
            return redirect('/homepage')
        else:
            flash('Invalid username or password.')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect('/homepage')

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        session['difficulty'] = difficulty  
        filtered_questions = random.sample([q for q in questions if q['difficulty'] == difficulty], 5)
        random.shuffle(filtered_questions)
        return render_template('quiz.html', questions=filtered_questions, difficulty=difficulty)
    leaderboard_scores = get_leaderboard_scores()
    return render_template('homepage.html', username=session.get('username'), scores=leaderboard_scores)

@app.route('/guest_index', methods=['GET', 'POST'])
def guest_index():
    if request.method == 'POST':
        difficulty = request.form.get('difficulty')
        filtered_questions = random.sample([q for q in questions if q['difficulty'] == difficulty], 5)
        random.shuffle(filtered_questions)
        return render_template('guest_quiz.html', questions=filtered_questions)

@app.route('/howto')
def howto():
    return render_template('howto.html')

@app.route('/submit', methods=['POST'])
def submit():
    difficulty = session.get('difficulty')  
    score = 0
    for question in questions:
        selected_choice = request.form.get(question['question'])
        if selected_choice == question['correct_answer']:
            score += 1

    if 'username' in session:
        username = session['username']
        update_leaderboard(username, score, difficulty)

    return render_template('result.html', score=score)

@app.route('/guest_submit', methods=['POST'])
def guest_submit():
    score = 0
    for question in questions:
        selected_choice = request.form.get(question['question'])
        if selected_choice == question['correct_answer']:
            score += 1
    return render_template('guest_result.html', score=score)

@app.route('/leaderboard')
def leaderboard():
    leaderboard_scores = get_leaderboard_scores()
    return render_template('leaderboard.html', scores=leaderboard_scores)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
