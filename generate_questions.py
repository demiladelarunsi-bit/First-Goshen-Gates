import os, django, random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'GOSHEN_GATES.settings')
django.setup()

from django.contrib.auth.models import User
from resultportal.models import ExamQuestion

user = User.objects.filter(is_superuser=True).first()
if not user:
    user, _ = User.objects.get_or_create(username='admin', defaults={'is_staff': True, 'is_superuser': True})
    user.set_password('admin123')
    user.save()

ExamQuestion.objects.all().delete()

classes = ['Nursery 1', 'Nursery 2', 'Primary 1', 'Primary 2', 'Primary 3', 'Primary 4', 'Primary 5', 'Primary 6']
terms = ['First Term', 'Second Term', 'Third Term']
years = ['2024', '2025', '2026']

def safe_opts(correct, wrong1, wrong2, wrong3):
    """Ensure no empty strings and no duplicates"""
    opts = [str(correct), str(wrong1), str(wrong2), str(wrong3)]
    opts = [o for o in opts if o.strip() != '']
    # Remove duplicates while preserving order
    seen = set()
    unique = []
    for o in opts:
        if o not in seen:
            seen.add(o)
            unique.append(o)
    # Fill missing options
    c = int(correct) if str(correct).isdigit() else 0
    filler = 0
    while len(unique) < 4:
        filler += 1
        candidate = str(c + filler * 3)
        if candidate not in seen:
            seen.add(candidate)
            unique.append(candidate)
    return unique[0], unique[1], unique[2], unique[3]

# ===================== MANUAL QUESTIONS =====================
manual = {
    'English Language': {
        'Nursery 1': [
            ('Which letter comes after A?', 'B', 'C', 'D', 'E', 'A'),
            ('Which is a vowel?', 'B', 'C', 'A', 'D', 'C'),
            ('What is the opposite of big?', 'Tall', 'Small', 'Long', 'Short', 'B'),
            ('Which word rhymes with cat?', 'Dog', 'Hat', 'Cup', 'Pen', 'B'),
            ('What starts with "B"?', 'Apple', 'Ball', 'Cat', 'Dog', 'B'),
            ('Which is a color?', 'Run', 'Blue', 'Jump', 'Fast', 'B'),
            ('What is the opposite of up?', 'Down', 'Left', 'Right', 'Far', 'A'),
            ('Which is an animal?', 'Table', 'Chair', 'Dog', 'Book', 'C'),
            ('Complete: C-A-__', 'T', 'K', 'P', 'B', 'A'),
            ('Choose the correct word: I am a ___.', 'Boy', 'Run', 'Happy', 'Big', 'A'),
            ('What letter comes before D?', 'A', 'B', 'C', 'E', 'B'),
            ('Which word starts with "M"?', 'Cat', 'Moon', 'Ball', 'Sun', 'B'),
            ('What is the opposite of hot?', 'Warm', 'Cold', 'Cool', 'Dry', 'B'),
            ('Complete: D-O-__', 'G', 'T', 'P', 'B', 'A'),
            ('Which is a fruit?', 'Car', 'Mango', 'Shoe', 'Pen', 'B'),
        ],
        'Nursery 2': [
            ('What letter comes after D?', 'E', 'F', 'G', 'C', 'A'),
            ('Which is a vowel?', 'D', 'E', 'F', 'G', 'B'),
            ('What rhymes with sun?', 'Moon', 'Fun', 'Cat', 'Dog', 'B'),
            ('Opposite of "open" is?', 'Close', 'Big', 'Small', 'Fast', 'A'),
            ('Which word starts with "Ch"?', 'Air', 'Chair', 'Ball', 'Dog', 'B'),
            ('What is the opposite of "sad"?', 'Cry', 'Happy', 'Angry', 'Sleep', 'B'),
            ('Which is a fruit?', 'Car', 'Mango', 'Shoe', 'Pen', 'B'),
            ('Complete: B-A-__', 'G', 'T', 'L', 'R', 'A'),
            ('Which animal says "meow"?', 'Dog', 'Cat', 'Cow', 'Bird', 'B'),
            ('What letter comes after G?', 'H', 'I', 'F', 'E', 'A'),
            ('Which word starts with "S"?', 'Cat', 'Sun', 'Ball', 'Dog', 'B'),
            ('Opposite of "wet" is?', 'Dry', 'Cold', 'Hot', 'Big', 'A'),
            ('Complete: F-I-__', 'X', 'G', 'V', 'N', 'B'),
            ('Which is a body part?', 'Pencil', 'Nose', 'Book', 'Chair', 'B'),
            ('What rhymes with "ball"?', 'Cat', 'Tall', 'Dog', 'Pen', 'B'),
        ],
        'Primary 1': [
            ('What is the plural of boy?', 'Boyes', 'Boys', 'Boyies', 'Boies', 'B'),
            ('Which word is a noun?', 'Run', 'Book', 'Fast', 'Beautiful', 'B'),
            ('What is the past tense of go?', 'Goed', 'Gone', 'Went', 'Going', 'C'),
            ('Complete: She ___ to school.', 'go', 'goes', 'going', 'gone', 'B'),
            ('Which is a verb?', 'Happy', 'Table', 'Sing', 'Big', 'C'),
            ('What is the opposite of hot?', 'Warm', 'Cold', 'Cool', 'Dry', 'B'),
            ('Choose the correct spelling:', 'Beautful', 'Beautiful', 'Beutiful', 'Beautifull', 'B'),
            ('Which word starts with "Sh"?', 'Cat', 'Ship', 'Bat', 'Dog', 'B'),
            ('What punctuation ends a question?', '.', ',', '?', '!', 'C'),
            ('Complete: A ___ has four legs.', 'Bird', 'Fish', 'Dog', 'Snake', 'C'),
            ('What is the plural of girl?', 'Girls', 'Girlies', 'Girles', 'Girl', 'A'),
            ('Which is an adjective?', 'Run', 'Big', 'Slowly', 'Under', 'B'),
            ('Past tense of "eat"?', 'Eated', 'Ate', 'Eaten', 'Eating', 'B'),
            ('Complete: They ___ playing.', 'is', 'are', 'am', 'was', 'B'),
            ('What is the opposite of "old"?', 'Ancient', 'New', 'Tall', 'Small', 'B'),
        ],
        'Primary 2': [
            ('What is the plural of child?', 'Childs', 'Children', 'Childes', 'Childies', 'B'),
            ('Which is an adjective?', 'Run', 'Quickly', 'Beautiful', 'Table', 'C'),
            ('What is the past tense of eat?', 'Eated', 'Ate', 'Eaten', 'Eating', 'B'),
            ('Complete: They ___ playing football.', 'is', 'are', 'was', 'am', 'B'),
            ('Find the noun: "The tall man ran fast."', 'tall', 'ran', 'man', 'fast', 'C'),
            ('What is the opposite of happy?', 'Joyful', 'Sad', 'Angry', 'Excited', 'B'),
            ('Which is a proper noun?', 'city', 'Lagos', 'river', 'mountain', 'B'),
            ('Complete: I have ___ apple.', 'a', 'an', 'the', 'some', 'B'),
            ('What is the plural of mouse?', 'Mouses', 'Mice', 'Mices', 'Mouse', 'B'),
            ('Which word is a pronoun?', 'Dog', 'He', 'Fast', 'Run', 'B'),
            ('What is the opposite of "rough"?', 'Hard', 'Smooth', 'Soft', 'Sharp', 'B'),
            ('Past tense of "come"?', 'Comed', 'Came', 'Come', 'Coming', 'B'),
            ('Which is a verb?', 'Car', 'House', 'Jump', 'Red', 'C'),
            ('Complete: The cat is ___ the table.', 'on', 'and', 'but', 'or', 'A'),
            ('What is the plural of "tooth"?', 'Tooths', 'Teeth', 'Toothes', 'Toothies', 'B'),
        ],
        'Primary 3': [
            ('What type of word is "quickly"?', 'Noun', 'Verb', 'Adverb', 'Adjective', 'C'),
            ('Give the past tense of "swim":', 'Swimmed', 'Swum', 'Swam', 'Swimming', 'C'),
            ('Which sentence is correct?', 'Him is running.', 'He is running.', 'His is running.', 'He running.', 'B'),
            ('What is a synonym for "big"?', 'Small', 'Tiny', 'Large', 'Short', 'C'),
            ('Identify the verb: "She sings beautifully."', 'She', 'sings', 'beautifully', 'None', 'B'),
            ('What is the plural of "foot"?', 'Foots', 'Footes', 'Feet', 'Footies', 'C'),
            ('Complete: If I ___ rich, I would travel.', 'am', 'was', 'were', 'be', 'C'),
            ('Which is a conjunction?', 'But', 'Quickly', 'Under', 'The', 'A'),
            ('What is an antonym of "brave"?', 'Bold', 'Cowardly', 'Strong', 'Fearless', 'B'),
            ('Choose the correct spelling:', 'Necesary', 'Necessary', 'Neccessary', 'Necesery', 'B'),
            ('What is the past tense of "buy"?', 'Buyed', 'Bought', 'Buied', 'Buying', 'B'),
            ('Which is a preposition?', 'Run', 'Under', 'Big', 'Fast', 'B'),
            ('Synonym of "happy"?', 'Sad', 'Joyful', 'Angry', 'Tired', 'B'),
            ('Complete: ___ you like tea?', 'Do', 'Does', 'Did', 'Are', 'A'),
            ('What is the plural of "leaf"?', 'Leafs', 'Leaves', 'Leafes', 'Leafies', 'B'),
        ],
        'Primary 4': [
            ('What type of sentence is this: "What time is it?"', 'Declarative', 'Interrogative', 'Imperative', 'Exclamatory', 'B'),
            ('Give the past perfect tense of "write":', 'Writed', 'Wrote', 'Had written', 'Has written', 'C'),
            ('Which is an abstract noun?', 'Table', 'Happiness', 'Water', 'Book', 'B'),
            ('What is the comparative form of "good"?', 'Gooder', 'More good', 'Better', 'Best', 'C'),
            ('Identify the preposition: "The cat is under the table."', 'cat', 'is', 'under', 'table', 'C'),
            ('What is the plural of "phenomenon"?', 'Phenomenons', 'Phenomena', 'Phenomenaes', 'Phenomeni', 'B'),
            ('Which word is a demonstrative pronoun?', 'He', 'This', 'Who', 'Which', 'B'),
            ('Complete: Neither John nor Mary ___ coming.', 'is', 'are', 'were', 'have', 'A'),
            ('What figure of speech is "The wind howled"?', 'Simile', 'Metaphor', 'Personification', 'Hyperbole', 'C'),
            ('Choose correctly: "Everyone has ___ book."', 'their', 'his or her', 'its', 'All of the above', 'D'),
            ('What is the superlative of "bad"?', 'Badder', 'More bad', 'Worst', 'Baddest', 'C'),
            ('Identify the adverb: "She ran quickly."', 'She', 'ran', 'quickly', 'None', 'C'),
            ('Which is a proper noun?', 'river', 'Nigeria', 'city', 'school', 'B'),
            ('Complete: I wish I ___ a bird.', 'am', 'was', 'were', 'is', 'C'),
            ('What is the past tense of "teach"?', 'Teached', 'Taught', 'Tought', 'Teaching', 'B'),
        ],
        'Primary 5': [
            ('What is the superlative form of "bad"?', 'Badder', 'More bad', 'Worst', 'Baddest', 'C'),
            ('What is the passive voice of "She wrote a letter"?', 'A letter was written by her.', 'A letter is written by her.', 'A letter has been written by her.', 'A letter were written by her.', 'A'),
            ('Which is a collective noun?', 'Flock', 'Sheep', 'Teacher', 'Pencil', 'A'),
            ('What is reported speech for: He said, "I am tired."', 'He said that he is tired.', 'He said that he was tired.', 'He said that I am tired.', 'He said that I was tired.', 'B'),
            ('Identify the gerund: "Swimming is fun."', 'is', 'fun', 'Swimming', 'None', 'C'),
            ('What is the synonym of "abundant"?', 'Scarce', 'Plentiful', 'Small', 'Weak', 'B'),
            ('Complete: Had I known, I ___ come.', 'will', 'would', 'should', 'could', 'B'),
            ('Which is an example of oxymoron?', 'As brave as a lion', 'Deafening silence', 'The wind whispered', 'Busy as a bee', 'B'),
            ('Choose the correct spelling:', 'Accomodation', 'Accommodation', 'Acomodation', 'Accommadation', 'B'),
            ('What is the plural of "criterion"?', 'Criterions', 'Criterias', 'Criteria', 'Criteriums', 'C'),
            ('Identify the clause: "When it rains, we stay inside"', 'Noun clause', 'Adverbial clause', 'Adjective clause', 'Main clause', 'B'),
            ('What is the antonym of "transparent"?', 'Clear', 'Opaque', 'Visible', 'Obvious', 'B'),
            ('Complete: She is ___ intelligent than her brother.', 'more', 'most', 'much', 'very', 'A'),
            ('Which is a compound sentence?', 'I ran.', 'I ran and she walked.', 'Because I ran.', 'Running fast.', 'B'),
            ('What is the past tense of "begin"?', 'Beginned', 'Begun', 'Began', 'Beginning', 'C'),
        ],
        'Primary 6': [
            ('What type of noun is "team"?', 'Common', 'Proper', 'Collective', 'Abstract', 'C'),
            ('Convert to indirect: "Where are you going?" she asked.', 'She asked where I was going.', 'She asked where are you going.', 'She asked where I am going.', 'She asked where was I going.', 'A'),
            ('What is the plural of "criterion"?', 'Criterions', 'Criterias', 'Criteria', 'Criteriums', 'C'),
            ('Identify the infinitive phrase: "He wants to study medicine."', 'He wants', 'to study medicine', 'study medicine', 'wants to study', 'B'),
            ('What literary device: "I have a million things to do"?', 'Simile', 'Metaphor', 'Hyperbole', 'Irony', 'C'),
            ('Which sentence uses the subjunctive mood?', 'I was there.', 'If I were you...', 'He is running.', 'She has gone.', 'B'),
            ('What is the antonym of "transparent"?', 'Clear', 'Opaque', 'Visible', 'Obvious', 'B'),
            ('Identify the main clause: "Although it was raining, we played football."', 'Although it was raining', 'we played football', 'it was raining', 'played football', 'B'),
            ('What is the correct form: "He acts as if he ___ the king."', 'is', 'was', 'were', 'are', 'C'),
            ('Choose: "The news ___ very surprising."', 'is', 'are', 'were', 'have been', 'A'),
            ('What is the plural of "syllabus"?', 'Syllabuses', 'Syllabi', 'Syllabus', 'Syllabusses', 'B'),
            ('Identify: "To err is human" - what is "to err"?', 'Noun clause', 'Infinitive phrase', 'Prepositional phrase', 'Adverbial clause', 'B'),
            ('What is the passive of "They build houses"?', 'Houses are built by them.', 'Houses is built by them.', 'Houses were build by them.', 'Houses built by them.', 'A'),
            ('Complete: Not only ___ intelligent, but also hardworking.', 'she is', 'is she', 'she was', 'was she', 'A'),
            ('What figure of speech: "The world is a stage"?', 'Simile', 'Metaphor', 'Personification', 'Hyperbole', 'B'),
        ],
    },
    'Basic Science': {
        'Nursery 1': [
            ('What do we use to see?', 'Ears', 'Eyes', 'Nose', 'Mouth', 'B'),
            ('What do we use to hear?', 'Eyes', 'Nose', 'Ears', 'Hands', 'C'),
            ('What is the color of the sky?', 'Green', 'Blue', 'Red', 'Yellow', 'B'),
            ('Which animal can fly?', 'Dog', 'Bird', 'Fish', 'Cat', 'B'),
            ('What do plants need to grow?', 'Ice', 'Water', 'Salt', 'Sand', 'B'),
            ('How many legs does a dog have?', '2', '3', '4', '6', 'C'),
            ('What do we breathe in?', 'Water', 'Food', 'Air', 'Milk', 'C'),
            ('What is the color of grass?', 'Blue', 'Red', 'Green', 'Yellow', 'C'),
            ('Which is a source of light?', 'Moon', 'Sun', 'Rock', 'Water', 'B'),
            ('What do we use to eat?', 'Hands', 'Fork', 'Mouth', 'Nose', 'C'),
            ('What animal says "moo"?', 'Dog', 'Cat', 'Cow', 'Bird', 'C'),
            ('Which is a living thing?', 'Stone', 'Tree', 'Water', 'Chair', 'B'),
            ('What do we drink?', 'Oil', 'Water', 'Juice', 'All drinks', 'D'),
            ('How many fingers do you have?', '5', '10', '8', '6', 'B'),
            ('What is the color of a banana?', 'Red', 'Yellow', 'Green', 'Blue', 'B'),
        ],
        'Nursery 2': [
            ('What color is a banana?', 'Red', 'Yellow', 'Green', 'Blue', 'B'),
            ('How many eyes do you have?', '1', '2', '3', '4', 'B'),
            ('What animal says "meow"?', 'Dog', 'Cat', 'Cow', 'Bird', 'B'),
            ('What do we drink when thirsty?', 'Juice', 'Water', 'Milk', 'All', 'D'),
            ('What comes from the sky as rain?', 'Water', 'Milk', 'Oil', 'Juice', 'A'),
            ('Which is bigger: elephant or ant?', 'Ant', 'Elephant', 'Same', 'None', 'B'),
            ('What do we wear on our feet?', 'Hat', 'Shoes', 'Gloves', 'Scarf', 'B'),
            ('What is the sun like during the day?', 'Dark', 'Bright', 'Cold', 'Blue', 'B'),
            ('Which food do we get from hens?', 'Milk', 'Eggs', 'Meat', 'Both B and C', 'D'),
            ('What part of the body do we use to write?', 'Foot', 'Hand', 'Head', 'Nose', 'B'),
            ('What animal lives in water?', 'Dog', 'Fish', 'Cat', 'Bird', 'B'),
            ('What season is hot in Nigeria?', 'Rainy', 'Dry', 'Harmattan', 'Winter', 'B'),
            ('Which is heavy: stone or feather?', 'Feather', 'Stone', 'Same', 'None', 'B'),
            ('What do we use to cut paper?', 'Ruler', 'Scissors', 'Pencil', 'Eraser', 'B'),
            ('How many legs does a chicken have?', '2', '4', '6', '8', 'A'),
        ],
        'Primary 1': [
            ('How many senses do we have?', '4', '5', '6', '7', 'B'),
            ('What part of the body do we use to smell?', 'Eyes', 'Ears', 'Nose', 'Tongue', 'C'),
            ('What do animals need to live?', 'Rocks', 'Food and water', 'Toys', 'Books', 'B'),
            ('Which is a living thing?', 'Stone', 'Water', 'Tree', 'Chair', 'C'),
            ('What is the largest planet?', 'Earth', 'Mars', 'Jupiter', 'Saturn', 'C'),
            ('How many legs does a spider have?', '4', '6', '8', '10', 'C'),
            ('What do fish breathe with?', 'Nose', 'Gills', 'Lungs', 'Mouth', 'B'),
            ('Which is a form of water?', 'Ice', 'Steam', 'Liquid water', 'All of the above', 'D'),
            ('What gives us heat and light?', 'Moon', 'Stars', 'Sun', 'Wind', 'C'),
            ('What season comes after rainy season?', 'Dry season', 'Harmattan', 'Rainy season', 'Winter', 'A'),
            ('What do we use to write?', 'Pen', 'Plate', 'Cup', 'Spoon', 'A'),
            ('Which is not a sense?', 'Sight', 'Hearing', 'Running', 'Touch', 'C'),
            ('What is the color of milk?', 'Blue', 'White', 'Green', 'Red', 'B'),
            ('What animal has a trunk?', 'Dog', 'Elephant', 'Cat', 'Bird', 'B'),
            ('What do plants produce that we breathe?', 'Carbon dioxide', 'Oxygen', 'Nitrogen', 'Helium', 'B'),
        ],
        'Primary 2': [
            ('What is the process by which plants make food?', 'Respiration', 'Photosynthesis', 'Digestion', 'Germination', 'B'),
            ('Which part of a plant absorbs water?', 'Leaf', 'Flower', 'Root', 'Stem', 'C'),
            ('What are the three states of matter?', 'Solid, Liquid, Gas', 'Hot, Cold, Warm', 'Big, Small, Medium', 'Hard, Soft, Rough', 'A'),
            ('What gas do we breathe out?', 'Oxygen', 'Nitrogen', 'Carbon dioxide', 'Hydrogen', 'C'),
            ('What is an example of a reptile?', 'Frog', 'Snake', 'Bird', 'Fish', 'B'),
            ('What causes day and night?', 'Moon', 'Stars', 'Earth rotation', 'Sun rotation', 'C'),
            ('Which nutrient gives us energy?', 'Vitamins', 'Carbohydrates', 'Minerals', 'Water', 'B'),
            ('What instrument measures temperature?', 'Ruler', 'Thermometer', 'Clock', 'Scale', 'B'),
            ('What is the largest ocean?', 'Atlantic', 'Indian', 'Arctic', 'Pacific', 'D'),
            ('What do we call baby frogs?', 'Cubs', 'Tadpoles', 'Larvae', 'Pups', 'B'),
            ('What is an example of a mammal?', 'Crocodile', 'Dog', 'Lizard', 'Snake', 'B'),
            ('Which gas do plants need for photosynthesis?', 'Oxygen', 'Carbon dioxide', 'Nitrogen', 'Hydrogen', 'B'),
            ('What is the function of the stem?', 'Absorb water', 'Support the plant', 'Make food', 'Store seeds', 'B'),
            ('What tool do we use to see small things?', 'Telescope', 'Microscope', 'Binoculars', 'Glasses', 'B'),
            ('What type of animal is a butterfly?', 'Mammal', 'Insect', 'Fish', 'Bird', 'B'),
        ],
        'Primary 3': [
            ('What is the boiling point of water?', '50 C', '75 C', '100 C', '120 C', 'C'),
            ('Which organ pumps blood?', 'Brain', 'Lungs', 'Heart', 'Kidney', 'C'),
            ('What is the largest organ of the body?', 'Heart', 'Liver', 'Skin', 'Brain', 'C'),
            ('What type of animal is a whale?', 'Fish', 'Mammal', 'Reptile', 'Amphibian', 'B'),
            ('What is force?', 'A push or pull', 'A color', 'A sound', 'A smell', 'A'),
            ('What is the function of the skeleton?', 'Digest food', 'Support the body', 'Pump blood', 'Breathe', 'B'),
            ('Which planet is known as the Red Planet?', 'Venus', 'Mars', 'Jupiter', 'Mercury', 'B'),
            ('What is habitat?', 'Animal food', 'Animal home', 'Animal color', 'Animal size', 'B'),
            ('What is friction?', 'A type of food', 'Force that opposes motion', 'A type of energy', 'A liquid', 'B'),
            ('What do roots do for a plant?', 'Make food', 'Absorb water', 'Produce flowers', 'Catch sunlight', 'B'),
            ('What is the melting point of ice?', '0 C', '100 C', '50 C', '25 C', 'A'),
            ('Which blood cells fight infection?', 'Red blood cells', 'White blood cells', 'Platelets', 'Plasma', 'B'),
            ('What is an omnivore?', 'Eats plants only', 'Eats meat only', 'Eats both plants and meat', 'Eats nothing', 'C'),
            ('What is the nearest star to Earth?', 'Mars', 'The Sun', 'The Moon', 'Venus', 'B'),
            ('What is magnetic force?', 'Push by muscles', 'Force from magnets', 'Force from water', 'Force from wind', 'B'),
        ],
        'Primary 4': [
            ('What is the chemical symbol for water?', 'O2', 'H2O', 'CO2', 'NaCl', 'B'),
            ('Which gas do plants absorb from the air?', 'Oxygen', 'Nitrogen', 'Carbon dioxide', 'Hydrogen', 'C'),
            ('What is the process of food breaking down called?', 'Circulation', 'Digestion', 'Respiration', 'Photosynthesis', 'B'),
            ('What type of energy does a moving car have?', 'Light energy', 'Kinetic energy', 'Potential energy', 'Heat energy', 'B'),
            ('What is the largest continent?', 'Africa', 'Asia', 'Europe', 'America', 'B'),
            ('What is the main function of white blood cells?', 'Carry oxygen', 'Fight infection', 'Clot blood', 'Digest food', 'B'),
            ('What instrument measures electric current?', 'Thermometer', 'Ammeter', 'Barometer', 'Seismograph', 'B'),
            ('What is soil erosion?', 'Making soil', 'Washing away of topsoil', 'Planting in soil', 'Watering soil', 'B'),
            ('What are the parts of a flower?', 'Root, stem, leaf', 'Petal, stamen, pistil', 'Skin, flesh, seed', 'None', 'B'),
            ('What is condensation?', 'Gas to liquid', 'Liquid to gas', 'Solid to liquid', 'Liquid to solid', 'A'),
            ('What is evaporation?', 'Gas to liquid', 'Liquid to gas', 'Solid to liquid', 'Liquid to solid', 'B'),
            ('What is the function of the lungs?', 'Pump blood', 'Digest food', 'Breathe', 'Think', 'C'),
            ('Which is a renewable resource?', 'Petroleum', 'Solar energy', 'Coal', 'Natural gas', 'B'),
            ('What is the SI unit of length?', 'Kilogram', 'Meter', 'Second', 'Liter', 'B'),
            ('What is an insulator?', 'Copper', 'Wood', 'Iron', 'Aluminum', 'B'),
        ],
        'Primary 5': [
            ('What is the pH of pure water?', '0', '5', '7', '14', 'C'),
            ('What is the chemical formula for carbon dioxide?', 'CO', 'CO2', 'C2O', 'O2C', 'B'),
            ('What is the unit of force?', 'Joule', 'Watt', 'Newton', 'Pascal', 'C'),
            ('What type of rock is formed from cooled lava?', 'Sedimentary', 'Igneous', 'Metamorphic', 'Fossil', 'B'),
            ('What is the function of the kidney?', 'Pump blood', 'Filter blood', 'Digest food', 'Control body', 'B'),
            ('What is a conductor of electricity?', 'Wood', 'Rubber', 'Copper', 'Glass', 'C'),
            ('What is the difference between speed and velocity?', 'No difference', 'Velocity has direction', 'Speed has direction', 'Velocity is slower', 'B'),
            ('What is pollination?', 'Making seeds', 'Transfer of pollen', 'Growing roots', 'Watering plants', 'B'),
            ('What causes rusting?', 'Water only', 'Air only', 'Water and oxygen', 'Heat only', 'C'),
            ('What is the boiling point of iron?', '100 C', '500 C', '1538 C', '2000 C', 'C'),
            ('What is an alloy?', 'Pure metal', 'Mixture of metals', 'A gas', 'A liquid', 'B'),
            ('What is the SI unit of energy?', 'Watt', 'Joule', 'Newton', 'Pascal', 'B'),
            ('What is osmosis?', 'Movement of water through membrane', 'Movement of air', 'Movement of light', 'Movement of sound', 'A'),
            ('What is the function of the liver?', 'Pump blood', 'Produce bile', 'Filter urine', 'Control muscles', 'B'),
            ('What is a solvent?', 'Something that dissolves', 'Something that gets dissolved', 'A solid', 'A gas', 'A'),
        ],
        'Primary 6': [
            ('What is the chemical symbol for oxygen?', 'Ox', 'O2', 'O', 'Og', 'C'),
            ('What is Newton first law about?', 'Gravity', 'Inertia', 'Acceleration', 'Action-reaction', 'B'),
            ('What is the function of the xylem in plants?', 'Make food', 'Transport water', 'Store food', 'Reproduce', 'B'),
            ('What is the difference between mixture and compound?', 'No difference', 'Mixture can be separated physically', 'Compound can be separated easily', 'Mixture is chemical', 'B'),
            ('What is ecological balance?', 'Equal number of plants', 'Balance between living and non-living', 'Equal temperature', 'No rain', 'B'),
            ('What is the SI unit of energy?', 'Watt', 'Joule', 'Newton', 'Pascal', 'B'),
            ('What is the importance of decomposers?', 'Make food', 'Break down dead matter', 'Produce oxygen', 'Provide shelter', 'B'),
            ('What is a satellite?', 'A star', 'A body orbiting another', 'A planet', 'A comet', 'B'),
            ('What is refraction of light?', 'Bouncing of light', 'Bending of light', 'Absorbing light', 'Blocking light', 'B'),
            ('What is the function of hormones?', 'Fight disease', 'Chemical messengers', 'Digest food', 'Carry oxygen', 'B'),
            ('What is chemical change?', 'Change in size only', 'Change producing new substances', 'Change in shape', 'Change in color only', 'B'),
            ('What is the law of conservation of mass?', 'Mass disappears', 'Mass is created', 'Mass cannot be created or destroyed', 'Mass doubles', 'C'),
            ('What is an ecosystem?', 'One animal', 'Community of living and non-living things', 'A garden', 'A zoo', 'B'),
            ('What is the function of the pancreas?', 'Pump blood', 'Produce insulin and enzymes', 'Filter blood', 'Store food', 'B'),
            ('What is a vacuum?', 'Full of air', 'Empty space with no matter', 'Full of water', 'Full of gas', 'B'),
        ],
    },
    'Social Studies': {
        'Nursery 1': [('What is your name called?', 'Nickname', 'Full name', 'Pet name', 'Title', 'B'), ('Who is the head of your family?', 'Brother', 'Father/Mother', 'Friend', 'Neighbor', 'B'), ('Where do you live?', 'School', 'House/Home', 'Market', 'Office', 'B'), ('What do we say when we wake up?', 'Good night', 'Good morning', 'Goodbye', 'Sorry', 'B'), ('Who teaches you in school?', 'Doctor', 'Teacher', 'Driver', 'Cook', 'B'), ('What do we wear to school?', 'Nightwear', 'Uniform', 'Swimsuit', 'Nothing', 'B'), ('Where do we buy food?', 'Hospital', 'Market', 'Church', 'Bank', 'B'), ('What do we use to brush our teeth?', 'Soap', 'Toothbrush', 'Comb', 'Towel', 'B'), ('Who is your friend?', 'Someone who helps you', 'Someone who fights you', 'A stranger', 'Nobody', 'A'), ('Where do we go to learn?', 'Hospital', 'School', 'Market', 'Bank', 'B')],
        'Nursery 2': [('What do you say when someone helps you?', 'Go away', 'Thank you', 'No', 'Stop', 'B'), ('Where do we buy things?', 'School', 'Market/Shop', 'Hospital', 'Church', 'B'), ('What do we call mother mother?', 'Aunt', 'Grandmother', 'Sister', 'Cousin', 'B'), ('What do we do at school?', 'Sleep', 'Learn', 'Cook', 'Drive', 'B'), ('Who drives a car?', 'Teacher', 'Doctor', 'Driver', 'Farmer', 'C'), ('What do we say when we hurt someone?', 'Thank you', 'Sorry', 'Hello', 'Goodbye', 'B'), ('Where does a doctor work?', 'School', 'Hospital', 'Market', 'Church', 'B'), ('What do we need to stay clean?', 'Dirt', 'Soap and water', 'Mud', 'Oil', 'B'), ('Who cooks at home?', 'Teacher', 'Driver', 'Parent/Cook', 'Doctor', 'C'), ('What is a good habit?', 'Fighting', 'Sharing', 'Lying', 'Stealing', 'B')],
        'Primary 1': [('What is a family?', 'Friends', 'Group of related people', 'Classmates', 'Neighbors', 'B'), ('What is the capital of Nigeria?', 'Lagos', 'Abuja', 'Kano', 'Ibadan', 'B'), ('Who is the leader of a country?', 'Governor', 'President', 'Chairman', 'Mayor', 'B'), ('What is a community?', 'One person', 'Group of people living together', 'A school', 'A market', 'B'), ('What do we use money for?', 'Playing', 'Buying and selling', 'Eating', 'Sleeping', 'B'), ('What is a good citizen?', 'Someone who breaks rules', 'Someone who obeys rules', 'Someone who fights', 'Someone who steals', 'B'), ('Where do we go when we are sick?', 'School', 'Hospital', 'Market', 'Church', 'B'), ('What is a friend?', 'Someone who hates you', 'Someone you like and play with', 'A stranger', 'An enemy', 'B'), ('What do we celebrate on October 1st?', 'Christmas', 'Independence Day', 'New Year', 'Easter', 'B'), ('What is respect?', 'Being rude', 'Showing regard for others', 'Fighting', 'Ignoring', 'B')],
        'Primary 2': [('What are the types of family?', 'Small only', 'Nuclear and Extended', 'Large only', 'Medium', 'B'), ('What is a national symbol?', 'A toy', 'An emblem representing a country', 'A game', 'A food', 'B'), ('What is the Nigerian flag color?', 'Red and Blue', 'Green and White', 'Black and Yellow', 'Purple and Orange', 'B'), ('What is a citizen?', 'A visitor', 'A legal member of a country', 'A tourist', 'A student', 'B'), ('What is cooperation?', 'Fighting', 'Working together', 'Cheating', 'Sleeping', 'B'), ('What is the Nigerian currency?', 'Dollar', 'Naira', 'Pound', 'Euro', 'B'), ('Who is the head of a state?', 'President', 'Governor', 'Chairman', 'Mayor', 'B'), ('What is a market?', 'A school', 'A place for buying and selling', 'A hospital', 'A church', 'B'), ('What is honesty?', 'Stealing', 'Telling the truth', 'Cheating', 'Fighting', 'B'), ('What are natural resources?', 'Man-made things', 'Gifts of nature', 'Imported goods', 'Buildings', 'B')],
        'Primary 3': [('What are the 6 geo-political zones in Nigeria?', 'States', 'NW, NE, NC, SW, SE, SS', 'Regions', 'Districts', 'B'), ('What is the role of local government?', 'Run the country', 'Provide services to local areas', 'Print money', 'Declare war', 'B'), ('What is culture?', 'Food only', 'Way of life of a people', 'Clothes only', 'Language only', 'B'), ('What is honesty?', 'Stealing', 'Telling the truth', 'Cheating', 'Fighting', 'B'), ('What are natural resources?', 'Man-made things', 'Gifts of nature', 'Imported goods', 'Buildings', 'B'), ('What is marriage?', 'A game', 'Union between a man and woman', 'A fight', 'A school', 'B'), ('What is a resource?', 'Nothing', 'Something useful', 'A problem', 'A disease', 'B'), ('What is shelter?', 'Food', 'A place to live', 'Clothing', 'Water', 'B'), ('Who is a leader?', 'A follower', 'Someone who guides others', 'A stranger', 'A child', 'B'), ('What is a tradition?', 'A new thing', 'Custom passed down', 'A food', 'A cloth', 'B')],
        'Primary 4': [('What is the Nigerian coat of arms?', 'A flag', 'An official emblem of Nigeria', 'A song', 'A dance', 'B'), ('What is democracy?', 'Rule by one person', 'Government by the people', 'Military rule', 'No government', 'B'), ('What is the arm of government that makes laws?', 'Executive', 'Legislature', 'Judiciary', 'Police', 'B'), ('What is transportation?', 'Eating food', 'Moving people and goods', 'Building houses', 'Growing crops', 'B'), ('What is the importance of the constitution?', 'Decoration', 'Supreme law of the land', 'A story book', 'A poem', 'B'), ('What is the national anthem?', 'A song about food', 'A patriotic song', 'A dance', 'A prayer', 'B'), ('Who heads the executive arm?', 'Chief Judge', 'President', 'Senate President', 'Speaker', 'B'), ('What are the arms of government?', 'Two', 'Three', 'Four', 'Five', 'B'), ('What is voting?', 'Sleeping', 'Choosing a leader by ballot', 'Fighting', 'Eating', 'B'), ('What is the national pledge?', 'A song', 'A promise of loyalty to Nigeria', 'A poem', 'A prayer', 'B')],
        'Primary 5': [('What is federalism?', 'Rule by states only', 'Division of power between central and state', 'Rule by one person', 'No government', 'B'), ('What is population?', 'Number of animals', 'Total number of people in a place', 'Number of cars', 'Number of houses', 'B'), ('What is the function of the judiciary?', 'Make laws', 'Execute laws', 'Interpret laws', 'Print money', 'C'), ('What is human rights?', 'Animal rights', 'Fundamental rights of all humans', 'School rules', 'Family rules', 'B'), ('What is the Nigerian Senate?', 'Lower house', 'Upper legislative chamber', 'Court', 'Executive office', 'B'), ('What is migration?', 'Staying in one place', 'Moving from one place to another', 'Sleeping', 'Eating', 'B'), ('What is urbanization?', 'Building farms', 'Growth of cities', 'Planting trees', 'Fishing', 'B'), ('What is a constitution?', 'A book of songs', 'Supreme law of a country', 'A story book', 'A dictionary', 'B'), ('What is corruption?', 'Honesty', 'Dishonest or illegal behavior', 'Kindness', 'Hard work', 'B'), ('What is the role of INEC?', 'Build roads', 'Conduct elections', 'Run hospitals', 'Teach students', 'B')],
        'Primary 6': [('What is GDP?', 'General Daily Plan', 'Gross Domestic Product', 'Government Development Program', 'Growth Data Percentage', 'B'), ('What is colonization?', 'Building ant colonies', 'A stronger country controlling a weaker one', 'Living alone', 'Trading fairly', 'B'), ('What is sustainable development?', 'Fast development', 'Development without harming the future', 'Old development', 'Slow development', 'B'), ('What is the Nigerian Senate?', 'Lower house', 'Upper legislative chamber', 'Court', 'Executive office', 'B'), ('What is the role of INEC?', 'Build roads', 'Conduct elections', 'Run hospitals', 'Teach students', 'B'), ('What is national integration?', 'Dividing a country', 'Uniting different ethnic groups', 'Fighting', 'Trading', 'B'), ('What is self-reliance?', 'Depending on others', 'Being able to do things yourself', 'Being lazy', 'Giving up', 'B'), ('What is the rule of law?', 'Rule by one person', 'Everyone is equal before the law', 'No laws', 'Military rule', 'B'), ('What is civic responsibility?', 'Being irresponsible', 'Duties of a citizen', 'Breaking laws', 'Ignoring others', 'B'), ('What is globalization?', 'Staying local', 'Connection between countries worldwide', 'Isolation', 'War', 'B')],
    },
    'Christian Religious Knowledge': {
        'Nursery 1': [('Who made the world?', 'Man', 'God', 'Angel', 'Animal', 'B'), ('Who was the first man?', 'Moses', 'Abraham', 'Adam', 'Noah', 'C'), ('Who was the first woman?', 'Mary', 'Eve', 'Sarah', 'Ruth', 'B'), ('What did God create on the first day?', 'Animals', 'Light', 'Man', 'Trees', 'B'), ('Who is the son of God?', 'Moses', 'Jesus', 'Peter', 'John', 'B'), ('Who is Jesus mother?', 'Martha', 'Mary', 'Elizabeth', 'Sarah', 'B'), ('Where do we pray?', 'In the bathroom', 'Anywhere', 'In the market only', 'Nowhere', 'B'), ('What is the Bible?', 'A story book', 'God word', 'A math book', 'A comic', 'B'), ('Who created you?', 'My parents', 'God', 'My teacher', 'Nobody', 'B'), ('What should we do to others?', 'Hurt them', 'Be kind', 'Ignore them', 'Fight them', 'B')],
        'Nursery 2': [('Who made you?', 'My parents', 'God', 'My teacher', 'Nobody', 'B'), ('What did God give us?', 'Nothing', 'Life', 'Toys only', 'Food only', 'B'), ('Who is Jesus?', 'A teacher only', 'The Son of God', 'A king only', 'A doctor', 'B'), ('Where do we go to worship God?', 'School', 'Church', 'Market', 'Hospital', 'B'), ('Who is a good friend?', 'Someone who is mean', 'Someone who shares', 'Someone who fights', 'Someone who lies', 'B'), ('What is prayer?', 'Talking to God', 'Talking to friends', 'Singing', 'Dancing', 'A'), ('Who looked after sheep?', 'A doctor', 'David', 'A teacher', 'A driver', 'B'), ('What did Jesus tell us to do?', 'Fight', 'Love one another', 'Steal', 'Lie', 'B'), ('Who baptized Jesus?', 'Peter', 'John', 'James', 'Andrew', 'B'), ('What is love?', 'Being mean', 'Caring for others', 'Fighting', 'Hating', 'B')],
        'Primary 1': [('How many days did God create the world?', '5', '6', '7', '10', 'B'), ('What did God rest on?', '6th day', '7th day', '1st day', '3rd day', 'B'), ('Who killed Goliath?', 'Saul', 'David', 'Jonathan', 'Samuel', 'B'), ('Who was thrown into the lion den?', 'David', 'Daniel', 'Jonah', 'Joseph', 'B'), ('What is the name of Jesus mother?', 'Martha', 'Mary', 'Elizabeth', 'Sarah', 'B'), ('Who built the ark?', 'Abraham', 'Noah', 'Moses', 'David', 'B'), ('What did Jesus feed to 5000 people?', 'Meat', 'Bread and fish', 'Rice', 'Fruits', 'B'), ('Who was the first king of Israel?', 'David', 'Saul', 'Solomon', 'Samuel', 'B'), ('What is a miracle?', 'Something normal', 'A wonderful act of God', 'A trick', 'A mistake', 'B'), ('Where was Jesus born?', 'Nazareth', 'Bethlehem', 'Jerusalem', 'Egypt', 'B')],
        'Primary 2': [('Where was Jesus born?', 'Nazareth', 'Bethlehem', 'Jerusalem', 'Egypt', 'B'), ('Who baptized Jesus?', 'Peter', 'John the Baptist', 'Moses', 'Paul', 'B'), ('How many disciples did Jesus choose?', '7', '10', '12', '15', 'C'), ('What miracle did Jesus perform at a wedding?', 'Walked on water', 'Turned water to wine', 'Fed 5000', 'Healed a blind man', 'B'), ('Who denied Jesus three times?', 'Judas', 'Peter', 'John', 'James', 'B'), ('Who betrayed Jesus?', 'Peter', 'John', 'Judas Iscariot', 'Thomas', 'C'), ('What is the Lord Prayer?', 'A song', 'The prayer Jesus taught', 'A psalm', 'A poem', 'B'), ('What happened on Good Friday?', 'Jesus was born', 'Jesus died on the cross', 'Jesus rose', 'Jesus ascended', 'B'), ('What is the Bible?', 'A story book', 'The word of God', 'A history book', 'A science book', 'B'), ('Who walked on water?', 'Peter only', 'Jesus', 'John', 'James', 'B')],
        'Primary 3': [('What is the greatest commandment?', 'Do not steal', 'Love God and neighbor', 'Do not kill', 'Go to church', 'B'), ('What is the Lord Prayer?', 'A song', 'The prayer Jesus taught', 'A psalm', 'A poem', 'B'), ('What happened on Good Friday?', 'Jesus was born', 'Jesus died on the cross', 'Jesus rose', 'Jesus ascended', 'B'), ('What is the Bible?', 'A story book', 'The word of God', 'A history book', 'A science book', 'B'), ('Who was swallowed by a big fish?', 'Daniel', 'Jonah', 'David', 'Solomon', 'B'), ('What is a parable?', 'A true story', 'An earthly story with heavenly meaning', 'A poem', 'A law', 'B'), ('What is the fruit of the Spirit?', 'Apple, banana', 'Love, joy, peace', 'Money, wealth', 'Food, water', 'B'), ('Who was the wisest king?', 'David', 'Solomon', 'Saul', 'Hezekiah', 'B'), ('What is the Ten Commandments?', '10 rules from God', '10 stories', '10 prayers', '10 songs', 'A'), ('Who appeared to Moses in a burning bush?', 'Angel', 'God', 'Jesus', 'Elijah', 'B')],
        'Primary 4': [('What is the Ten Commandments?', '10 rules given by God', '10 stories', '10 prayers', '10 songs', 'A'), ('Who was swallowed by a big fish?', 'Daniel', 'Jonah', 'David', 'Solomon', 'B'), ('What is a parable?', 'A true story', 'An earthly story with heavenly meaning', 'A poem', 'A law', 'B'), ('What is the fruit of the Spirit?', 'Apple, banana', 'Love, joy, peace', 'Money, wealth', 'Food, water', 'B'), ('Who was the wisest king?', 'David', 'Solomon', 'Saul', 'Hezekiah', 'B'), ('What is the greatest gift?', 'Money', 'Love', 'Food', 'House', 'B'), ('Who led the Israelites out of Egypt?', 'Abraham', 'Moses', 'David', 'Solomon', 'B'), ('What is the last book of the Bible?', 'Genesis', 'Revelation', 'Psalms', 'Matthew', 'B'), ('Who was Samuel mother?', 'Sarah', 'Hannah', 'Mary', 'Ruth', 'B'), ('What is faith?', 'Seeing is believing', 'Believing without seeing', 'Doubting', 'Fear', 'B')],
        'Primary 5': [('What is the Great Commission?', 'A tax', 'Jesus command to spread the gospel', 'A building project', 'A war', 'B'), ('What happened on the day of Pentecost?', 'Jesus was born', 'Holy Spirit came on disciples', 'Jesus died', 'Temple was built', 'B'), ('What is the church?', 'A building only', 'The body of Christ', 'A school', 'A hospital', 'B'), ('Who was Paul before conversion?', 'A fisherman', 'A persecutor of Christians', 'A tax collector', 'A king', 'B'), ('What is salvation?', 'Getting rich', 'Deliverance from sin through Jesus', 'Going to school', 'Being healthy', 'B'), ('What is baptism?', 'Swimming', 'A sacrament of initiation', 'A bath', 'A game', 'B'), ('Who wrote most of the New Testament?', 'Peter', 'Paul', 'John', 'James', 'B'), ('What is the book of Acts about?', 'Laws', 'Early church and apostles', 'Psalms', 'Prophets', 'B'), ('What is repentance?', 'No change', 'Turning away from sin', 'Being proud', 'Fighting', 'B'), ('What is the second coming?', 'Jesus returning to earth', 'Jesus birth', 'Jesus baptism', 'Nothing', 'A')],
        'Primary 6': [('What is justification?', 'Making excuses', 'Being made right with God', 'Being punished', 'Being ignored', 'B'), ('What are the Beatitudes?', 'Rules', 'Teachings of Jesus about blessedness', 'Stories', 'Laws of Moses', 'B'), ('What is sanctification?', 'Building a church', 'Process of being made holy', 'Getting baptized', 'Reading Bible', 'B'), ('What is the second coming of Christ?', 'Jesus coming back', 'Jesus birth', 'Jesus death', 'Jesus baptism', 'A'), ('What is the book of Revelation about?', 'History of Israel', 'End times and God victory', 'Psalms', 'Proverbs', 'B'), ('What is grace?', 'Money', 'Unmerited favor from God', 'Hard work', 'Luck', 'B'), ('Who was the first martyr?', 'Peter', 'Stephen', 'Paul', 'John', 'B'), ('What is the Trinity?', 'Three gods', 'God the Father, Son, Holy Spirit', 'Three angels', 'Three men', 'B'), ('What is discipleship?', 'Following Jesus', 'Following a teacher', 'Being a student', 'Reading books', 'A'), ('What is the Great Commandment?', 'Do not steal', 'Love God with all your heart', 'Go to church', 'Pray always', 'B')],
    },
}

# ===================== PROGRAMMATIC MATH QUESTIONS (FIXED) =====================
math_qs = {}

def add_q(cls, text, correct, wrong1, wrong2, wrong3, ans_letter):
    opts = safe_opts(correct, wrong1, wrong2, wrong3)
    letters = ['A', 'B', 'C', 'D']
    correct_idx = opts.index(str(correct))
    math_qs.setdefault(cls, []).append((text, opts[0], opts[1], opts[2], opts[3], letters[correct_idx]))

# Nursery 1: Addition/Subtraction within 5
for a in range(1, 5):
    for b in range(1, 6 - a):
        s = a + b
        add_q('Nursery 1', f'What is {a} + {b}?', s, s-1 if s-1>0 else s+1, s+1, s+2, 'C')
        if b <= a:
            d = a - b
            add_q('Nursery 1', f'What is {a} - {b}?', d, d+1, d-1 if d-1>0 else 1, d+2, 'B')

# Nursery 2: Addition/Subtraction within 10
for a in range(3, 9):
    for b in range(2, 11 - a):
        s = a + b
        add_q('Nursery 2', f'What is {a} + {b}?', s, s-1, s+1, s+2, 'B')
        if b <= a:
            d = a - b
            add_q('Nursery 2', f'What is {a} - {b}?', d, d+1, d-1 if d-1>0 else 1, d+2, 'B')

# Primary 1: Two-digit within 20, times tables 2,3,5,10
for a in range(5, 16):
    for b in range(3, 21 - a):
        s = a + b
        add_q('Primary 1', f'What is {a} + {b}?', s, s-1, s+1, s+2, 'C')
for a in range(10, 20):
    for b in range(1, a):
        d = a - b
        add_q('Primary 1', f'What is {a} - {b}?', d, d+2, d-1 if d>1 else 1, d+1, 'D')
for t in [2, 3, 5, 10]:
    for n in range(1, 11):
        p = t * n
        add_q('Primary 1', f'What is {n} x {t}?', p, p-1 if p>1 else 1, p+1, p+2, 'B')

# Primary 2: More times tables, two-digit
for t in [4, 6, 7, 8, 9]:
    for n in range(2, 11):
        p = t * n
        add_q('Primary 2', f'What is {n} x {t}?', p, p-2 if p>2 else 1, p+1, p+2, 'C')
for a in range(10, 50, 7):
    for b in range(5, 30, 5):
        s = a + b
        if s > 80: continue
        add_q('Primary 2', f'What is {a} + {b}?', s, s-2, s+1, s+3, 'B')
for a in range(30, 80, 5):
    for b in range(5, a, 7):
        d = a - b
        if d < 5: continue
        add_q('Primary 2', f'What is {a} - {b}?', d, d+3, d-2 if d>2 else 1, d+1, 'D')

# Primary 3: Three-digit, division
for a in range(100, 400, 37):
    for b in range(50, 300, 43):
        s = a + b
        if s > 600: continue
        add_q('Primary 3', f'What is {a} + {b}?', s, s-10, s+5, s+8, 'B')
for a in range(200, 600, 41):
    for b in range(50, a, 37):
        d = a - b
        if d < 20: continue
        add_q('Primary 3', f'What is {a} - {b}?', d, d+7, d-5 if d>5 else 1, d+2, 'D')
for d in range(2, 13):
    for q in range(2, 13):
        p = d * q
        add_q('Primary 3', f'What is {p} divided by {d}?', q, q+1, q-1 if q>1 else 0, q+2, 'C')

# Primary 4: Larger operations, percentages
for a in range(1000, 5000, 317):
    for b in range(500, 3000, 211):
        s = a + b
        if s > 7000: continue
        add_q('Primary 4', f'What is {a} + {b}?', s, s-11, s+7, s+13, 'B')
for a in range(3000, 9000, 401):
    for b in range(500, a, 299):
        d = a - b
        if d < 200: continue
        add_q('Primary 4', f'What is {a} - {b}?', d, d+9, d-6, d+3, 'D')
for n in range(11, 20):
    for m in range(11, 20):
        p = n * m
        add_q('Primary 4', f'What is {n} x {m}?', p, p-n, p+m, p+5, 'B')
for pct in [10, 20, 25, 50, 75]:
    for base in [40, 60, 80, 100, 200, 400, 500, 800]:
        ans = int(base * pct / 100)
        add_q('Primary 4', f'What is {pct}% of {base}?', ans, ans-2 if ans>2 else 1, ans+3, ans+5, 'B')

# Primary 5: Area, perimeter, squares, cubes
for l in range(5, 20, 3):
    for w in range(3, 15, 2):
        area = l * w
        add_q('Primary 5', f'Area of a rectangle L={l}cm W={w}cm?', area, area-l, area+w, area+5, 'B')
        peri = 2 * (l + w)
        add_q('Primary 5', f'Perimeter of a rectangle L={l}cm W={w}cm?', peri, peri-4, peri+3, peri+6, 'B')
for n in range(11, 26):
    sq = n * n
    add_q('Primary 5', f'What is {n} squared?', sq, sq-n, sq+2, sq+4, 'B')
for s in range(4, 16):
    cube = s * s * s
    add_q('Primary 5', f'What is the cube of {s}?', cube, cube-s, cube+5, cube+3, 'B')

# Primary 6: Speed, volume, algebra
for speed in range(20, 100, 11):
    for time_h in [1, 2, 3, 4, 5]:
        dist = speed * time_h
        add_q('Primary 6', f'A car travels at {speed}km/h for {time_h}hrs. Distance?', dist, dist-speed, dist+5, dist+10, 'B')
for side in range(3, 12):
    vol = side ** 3
    add_q('Primary 6', f'Volume of a cube with side {side}cm?', vol, vol-side, vol+4, vol+8, 'B')
for a in range(1, 10):
    for b in range(1, 10):
        x = a + b
        add_q('Primary 6', f'If x + {a} = {a+b+2}, find x.', x, x-1, x+2, x+1, 'B')
        ans = a * b + a * b
        add_q('Primary 6', f'If x = {b}, what is {a}x + {a*b}?', ans, a*b+a-1, a*b+1, a*b+a, 'D')

# ===================== COMBINE AND SAVE =====================
all_questions = {}
for subject in list(manual.keys()) + ['Mathematics']:
    all_questions[subject] = {}
    for cls in classes:
        all_questions[subject][cls] = []

for subject, class_data in manual.items():
    for cls, qs in class_data.items():
        all_questions[subject][cls] = qs

for cls, qs in math_qs.items():
    all_questions['Mathematics'][cls].extend(qs)

count = 0
for subject, class_data in all_questions.items():
    for cls, questions in class_data.items():
        if not questions:
            continue
        for q in questions:
            for term in terms:
                for year in years:
                    ExamQuestion.objects.create(
                        subject=subject,
                        student_class=cls,
                        term=term,
                        year=year,
                        question_text=q[0],
                        question_type='multiple_choice',
                        option_a=q[1],
                        option_b=q[2],
                        option_c=q[3],
                        option_d=q[4],
                        correct_answer=q[5],
                        marks=2,
                        created_by=user
                    )
                    count += 1

# VERIFY
empty = ExamQuestion.objects.filter(correct_answer='').count()
zero_marks = ExamQuestion.objects.filter(marks=0).count()
print(f'Created {count} questions')
print(f'Empty answers: {empty}')
print(f'Zero marks: {zero_marks}')
if empty > 0 or zero_marks > 0:
    print('WARNING: Deleting bad questions...')
    ExamQuestion.objects.filter(correct_answer='').delete()
    ExamQuestion.objects.filter(marks=0).delete()
    print(f'Cleaned. Total remaining: {ExamQuestion.objects.count()}')