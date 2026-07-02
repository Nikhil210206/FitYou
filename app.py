from flask import (
    Flask, render_template, request, jsonify, flash, redirect, url_for
)
import random
import pandas as pd
import os
import json
import logging

# STEP 1: ADDED NEW IMPORTS
import google.generativeai as genai
from dotenv import load_dotenv

# Authentication / database
from flask_sqlalchemy import SQLAlchemy
from flask_login import (
    LoginManager, UserMixin, login_user, logout_user,
    login_required, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash

# STEP 2: LOAD ENVIRONMENT VARIABLES FROM .env FILE
load_dotenv()

# Resolve data files relative to this file so the app works regardless of the
# current working directory (important on serverless hosts like Vercel).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EXERCISES_CSV = os.path.join(BASE_DIR, 'exercises.csv')
DIET_CSV = os.path.join(BASE_DIR, 'diet_data.csv')

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'fallback-secret-key-change-in-production')

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Database configuration ---------------------------------------------------
# Use DATABASE_URL when provided (e.g. Postgres in production). Fall back to a
# local SQLite file for development. Note: on read-only serverless filesystems
# (Vercel) you MUST set DATABASE_URL to a hosted database, since SQLite cannot
# be written to there.
database_url = os.getenv('DATABASE_URL', '').strip()
if database_url.startswith('postgres://'):
    # SQLAlchemy requires the 'postgresql://' scheme.
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
if not database_url:
    database_url = 'sqlite:///' + os.path.join(BASE_DIR, 'fityou.db')

app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'error'


class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String(20), nullable=True)
    goal = db.Column(db.String(40), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def init_db():
    """Create database tables if they don't exist yet."""
    try:
        with app.app_context():
            db.create_all()
    except Exception as e:
        # Don't crash the whole app if the DB is unreachable; auth routes will
        # surface a clear error instead.
        logger.error(f"Could not initialize the database: {e}")


init_db()

# --- AI Chatbot Core Functionality ---

# Google retires older Gemini models over time. Keep the default on a current
# model and try a chain of fallbacks so the coach keeps working even after a
# model is deprecated. `gemini-flash-latest` always points at the newest Flash.
RETIRED_GEMINI_MODELS = {"gemini-pro", "gemini-1.0-pro", "gemini-1.5-flash", "gemini-1.5-pro"}
DEFAULT_GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_FALLBACK_MODELS = ["gemini-flash-latest", "gemini-2.0-flash", "gemini-2.5-flash"]

SYSTEM_PROMPT = (
    "You are FitAI, a professional, friendly, and encouraging AI fitness coach. "
    "Your expertise includes workout routines, nutrition, injury prevention, and motivation. "
    "Provide safe, clear, and actionable advice. If a question is outside the scope of "
    "fitness, health, or nutrition, you must politely state that you can only answer fitness-related questions. "
    "Keep your responses focused and easy to understand."
)


def _candidate_models():
    """Ordered, de-duplicated list of models to try (env override first)."""
    configured = os.getenv("GEMINI_MODEL", "").strip()
    candidates = []
    # Ignore a stale/retired value even if it's still set in the environment.
    if configured and configured not in RETIRED_GEMINI_MODELS:
        candidates.append(configured)
    candidates.append(DEFAULT_GEMINI_MODEL)
    candidates.extend(GEMINI_FALLBACK_MODELS)
    seen = set()
    return [m for m in candidates if not (m in seen or seen.add(m))]


def chat_with_fitness_ai(message):
    """
    Handles conversation with the Gemini API to provide fitness advice.
    """
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        logger.error("Gemini API key is not configured in the environment.")
        return "Error: The AI Coach is not configured correctly. Please contact the administrator."

    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        logger.error(f"Failed to configure Gemini client: {e}")
        return "Sorry, the AI Coach is temporarily unavailable. Please try again later."

    full_prompt = f"{SYSTEM_PROMPT}\n\nUser's question: {message}"

    last_error = None
    for model_name in _candidate_models():
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(full_prompt)
            text = (getattr(response, "text", "") or "").strip()
            if text:
                return text
            last_error = f"Empty response from {model_name}"
            logger.warning(last_error)
        except Exception as e:
            last_error = f"{model_name}: {e}"
            logger.warning(f"Gemini model '{model_name}' failed: {e}")
            continue

    logger.error(f"All Gemini models failed. Last error: {last_error}")
    return "Sorry, I'm having a little trouble connecting to my brain right now. Please try again in a moment."

# --- Workout Plan Generator ---

def load_exercises():
    """Load exercises with error handling"""
    try:
        if not os.path.exists(EXERCISES_CSV):
            logger.error("exercises.csv file not found")
            return pd.DataFrame()

        df = pd.read_csv(EXERCISES_CSV)
        required_columns = ['category', 'exercise_name', 'reps_min', 'reps_max']
        missing_columns = set(required_columns) - set(df.columns)
        
        if missing_columns:
            logger.error(f"Missing columns in exercises.csv: {missing_columns}")
            return pd.DataFrame()
        
        return df
    
    except Exception as e:
        logger.error(f"Error loading exercises.csv: {e}")
        return pd.DataFrame()

def output(intensity):
    """Generate a workout routine based on intensity."""
    df = load_exercises()
    
    if df.empty:
        logger.warning("No exercises data available, returning default routine")
        return ["Push-ups - 10 reps", "Squats - 15 reps", "Plank - 30 seconds"]
    
    routine_list = []
    
    def add_exercises(category, max_intensity_ratio):
        max_intensity = intensity * max_intensity_ratio
        current_sum = 0
        category_exercises = df[df['category'] == category]
        
        if category_exercises.empty:
            logger.warning(f"No exercises found for category: {category}")
            return
        
        for _, exercise in category_exercises.iterrows():
            current_sum += 1
            if current_sum < max_intensity:
                reps_min = exercise.get('reps_min')
                reps_max = exercise.get('reps_max')
                
                if pd.notnull(reps_min) and pd.notnull(reps_max):
                    reps = random.randint(int(reps_min), int(reps_max))
                    routine_list.append(f"{exercise['exercise_name']} - {reps} reps")
                else:
                    routine_list.append(f"{exercise['exercise_name']} - Duration-based")
            else:
                break
    
    add_exercises('warmup', 0.2)
    add_exercises('exercise', 0.6)
    add_exercises('cooldown', 0.2)
    
    return routine_list if routine_list else ["No exercises available"]

def calculate_intensity(weight, height):
    """Calculate BMI and determine workout intensity."""
    if height <= 0 or weight <= 0:
        return 50
        
    height_in_meters = height / 100
    bmi = weight / (height_in_meters ** 2)
    
    if bmi < 18.5:
        return 50
    elif 18.5 <= bmi < 24.9:
        return 70
    elif 25 <= bmi < 29.9:
        return 60
    else:
        return 40

# --- Sports / Level-based Routine Generator ---

# Keywords used to classify the exercises in exercises.csv into training styles,
# since the CSV only tags warmup/exercise/cooldown.
_CARDIO_KEYWORDS = (
    'jump', 'jack', 'burpee', 'mountain climber', 'high knee', 'butt kick',
    'sprint', 'skater', 'run', 'tuck', 'crab', 'bear crawl', 'sprawl',
    'knee tuck', 'plyometric', 'hill climber', 'frog', 'kick',
)
_FLEX_KEYWORDS = (
    'stretch', 'cobra', 'child', 'cat-cow', 'yoga', 'rotation', 'circle',
    'twist', 'mobility', 'forward bend', 'figure four', "cat", 'swing', 'bend',
)

# Per-level tuning: how many moves per block and how sets/reps scale.
_LEVEL_SETTINGS = {
    'beginner':     {'strength': 4, 'cardio': 3, 'flexibility': 3, 'sets': 2, 'rep_bias': 0.0},
    'intermediate': {'strength': 5, 'cardio': 4, 'flexibility': 3, 'sets': 3, 'rep_bias': 0.5},
    'advanced':     {'strength': 6, 'cardio': 4, 'flexibility': 4, 'sets': 4, 'rep_bias': 1.0},
}


def _classify_exercise(name):
    lname = str(name).lower()
    if any(k in lname for k in _FLEX_KEYWORDS):
        return 'flexibility'
    if any(k in lname for k in _CARDIO_KEYWORDS):
        return 'cardio'
    return 'strength'


def _reps_for(row, rep_bias):
    """Pick a rep count within the exercise's range, biased higher by level."""
    reps_min = row.get('reps_min')
    reps_max = row.get('reps_max')
    if pd.notnull(reps_min) and pd.notnull(reps_max) and int(reps_max) > 0:
        lo, hi = int(reps_min), int(reps_max)
        if hi < lo:
            lo, hi = hi, lo
        base = random.randint(lo, hi)
        # Nudge toward the top of the range for higher levels.
        return min(hi, int(round(base + (hi - base) * rep_bias)))
    return None


def _duration_for(row):
    dur_min = row.get('duration_min')
    dur_max = row.get('duration_max')
    if pd.notnull(dur_min) and pd.notnull(dur_max) and int(dur_max) > 0:
        return f"{random.randint(int(dur_min), int(dur_max))} seconds"
    return f"{random.choice([30, 40, 45, 60])} seconds"


def generate_sport_routine(level):
    """Build a varied, level-appropriate routine grouped into strength/cardio/flexibility."""
    level = (level or '').strip().lower()
    settings = _LEVEL_SETTINGS.get(level, _LEVEL_SETTINGS['beginner'])

    df = load_exercises()
    routine = {'strength': [], 'cardio': [], 'flexibility': []}

    if df.empty:
        routine['strength'] = [{'exercise': 'Push-ups', 'sets': settings['sets'], 'reps': 10}]
        routine['cardio'] = [{'exercise': 'Jumping Jacks', 'duration': '45 seconds'}]
        routine['flexibility'] = [{'exercise': 'Full-body stretch', 'duration': '60 seconds'}]
        return routine

    # Bucket every exercise by its inferred training style.
    buckets = {'strength': [], 'cardio': [], 'flexibility': []}
    for _, row in df.iterrows():
        buckets[_classify_exercise(row['exercise_name'])].append(row)

    for block in ('strength', 'cardio', 'flexibility'):
        pool = buckets[block]
        random.shuffle(pool)
        chosen = pool[:settings[block]]
        for row in chosen:
            name = row['exercise_name']
            if block == 'strength':
                reps = _reps_for(row, settings['rep_bias'])
                if reps:
                    routine['strength'].append({'exercise': name, 'sets': settings['sets'], 'reps': reps})
                else:
                    routine['strength'].append({'exercise': name, 'duration': _duration_for(row)})
            else:
                routine[block].append({'exercise': name, 'duration': _duration_for(row)})

    return routine

# --- Diet Plan Generator ---

# Normalize the goal/diet values coming from the form (or a user profile) to the
# canonical values used inside diet_data.csv.
GOAL_ALIASES = {
    'weight loss': 'weight_loss', 'weight_loss': 'weight_loss', 'lose weight': 'weight_loss',
    'fat loss': 'weight_loss', 'cutting': 'weight_loss',
    'weight gain': 'weight_gain', 'weight_gain': 'weight_gain', 'gain weight': 'weight_gain',
    'muscle gain': 'weight_gain', 'muscle_gain': 'weight_gain', 'bulking': 'weight_gain',
    'maintenance': 'maintenance', 'maintain': 'maintenance', 'maintain weight': 'maintenance',
    'general fitness': 'maintenance', 'general_fitness': 'maintenance',
    'strength training': 'maintenance', 'strength_training': 'maintenance',
}

DIET_CATEGORY_ALIASES = {
    'vegetarian': 'vegetarian', 'veg': 'vegetarian', 'vegan': 'vegetarian',
    'non-vegetarian': 'non-vegetarian', 'non vegetarian': 'non-vegetarian',
    'nonveg': 'non-vegetarian', 'non-veg': 'non-vegetarian', 'nonvegetarian': 'non-vegetarian',
}

PREFERRED_MEAL_TYPES = ['Breakfast', 'Mid-Morning', 'Lunch', 'Afternoon Snack', 'Dinner', 'Before Bed']


def normalize_goal(value):
    return GOAL_ALIASES.get((value or '').strip().lower(), 'maintenance')


def normalize_diet_category(value):
    return DIET_CATEGORY_ALIASES.get((value or '').strip().lower(), 'non-vegetarian')


def load_diet_data():
    """Load diet data with error handling"""
    try:
        if not os.path.exists(DIET_CSV):
            logger.error("diet_data.csv file not found")
            return pd.DataFrame()

        df = pd.read_csv(DIET_CSV)
        required_columns = ['food_item', 'meal_type', 'calories', 'goal', 'diet_category']
        missing_columns = set(required_columns) - set(df.columns)

        if missing_columns:
            logger.error(f"Missing columns in diet_data.csv: {missing_columns}")
            return pd.DataFrame()

        for col in ['meal_type', 'goal', 'diet_category', 'food_item']:
            df[col] = df[col].astype(str).str.strip()

        # Normalize to canonical lowercase values so filtering is reliable.
        df['goal'] = df['goal'].str.lower()
        df['diet_category'] = df['diet_category'].str.lower()

        return df

    except Exception as e:
        logger.error(f"Error loading diet_data.csv: {e}")
        return pd.DataFrame()

class WeeklyDietPlan:
    def __init__(self, age, height, weight, goal, duration, diet_type, gender, activity_level, health_conditions=None):
        self.age = age
        self.height = height
        self.weight = weight
        self.goal = goal
        self.goal_key = normalize_goal(goal)
        self.duration = duration
        self.diet_type = diet_type
        self.diet_category = normalize_diet_category(diet_type)
        self.gender = gender
        self.activity_level = activity_level
        self.health_conditions = health_conditions or []
        self.bmr = self.calculate_bmr()
        self.daily_calories = self.adjust_calories()
        self.diet_data = load_diet_data()

        if self.diet_data.empty:
            raise ValueError("Diet data could not be loaded. Please check diet_data.csv file.")

        # A non-vegetarian eats everything; a vegetarian only eats vegetarian food.
        if self.diet_category == 'vegetarian':
            self.food_pool = self.diet_data[self.diet_data['diet_category'] == 'vegetarian']
        else:
            self.food_pool = self.diet_data

        self.plan = self.create_diet_plan()

    def calculate_bmr(self):
        if self.gender == 'male':
            return 10 * self.weight + 6.25 * self.height - 5 * self.age + 5
        else:
            return 10 * self.weight + 6.25 * self.height - 5 * self.age - 161

    def adjust_calories(self):
        if self.goal_key == 'weight_gain':
            return self.bmr + 500
        elif self.goal_key == 'weight_loss':
            return self.bmr - 500
        else:
            return self.bmr

    def create_diet_plan(self):
        return {f'Day {i + 1}': self.get_meal_plan() for i in range(7)}

    def _meals_for_goal(self):
        """Meals matching the user's goal, falling back gracefully."""
        meals = self.food_pool[self.food_pool['goal'] == self.goal_key]
        if meals.empty:
            logger.warning(f"No meals for goal '{self.goal_key}', falling back to maintenance")
            meals = self.food_pool[self.food_pool['goal'] == 'maintenance']
        if meals.empty:
            meals = self.food_pool
        return meals

    def get_meal_plan(self):
        meals = self._meals_for_goal()

        if meals.empty:
            return self.get_default_meal_plan()

        available_meal_types = set(meals['meal_type'].unique())
        meal_types_to_use = [mt for mt in PREFERRED_MEAL_TYPES if mt in available_meal_types]
        if not meal_types_to_use:
            meal_types_to_use = list(available_meal_types)[:6]

        meal_plan = {}
        total_calories = 0
        for meal_type in meal_types_to_use:
            meal_options = meals[meals['meal_type'] == meal_type]
            if not meal_options.empty:
                selected_meal = meal_options.sample(1).iloc[0]
                calories = int(round(float(selected_meal['calories'])))
                total_calories += calories
                meal_plan[meal_type] = f"{selected_meal['food_item']} - {calories} calories"

        if total_calories:
            meal_plan['Daily Total'] = (
                f"~{total_calories} calories "
                f"(target ~{int(round(self.daily_calories))} kcal/day)"
            )

        health_note = self.get_health_specific_notes()
        if health_note:
            meal_plan['Health Notes'] = health_note

        return meal_plan

    def get_default_meal_plan(self):
        """Return a default meal plan when no data is available"""
        return {
            'Breakfast': 'Oatmeal with fruits - 300 calories',
            'Mid-Morning': 'Mixed nuts - 150 calories',
            'Lunch': 'Grilled chicken with vegetables - 500 calories',
            'Afternoon Snack': 'Greek yogurt - 120 calories',
            'Dinner': 'Fish with quinoa - 450 calories',
            'Before Bed': 'Herbal tea - 0 calories',
            'Health Notes': 'Default plan - Please consult a nutritionist for personalized recommendations'
        }

    def get_health_specific_notes(self):
        """Get specific dietary notes based on the user's health conditions."""
        notes = {
            'Diabetes': 'Focus on low glycemic index foods and monitor carbohydrate intake.',
            'High Blood Pressure': 'Limit salt, avoid processed foods, and season with herbs instead.',
            'Heart Disease': 'Emphasize omega-3 fatty acids and limit saturated fats.',
            'High Cholesterol': 'Reduce animal fats, increase fiber, and favor plant-based proteins.',
        }
        messages = [notes[c] for c in self.health_conditions if c in notes]
        return ' '.join(messages)

# --- File Upload and Health Condition Detection ---

def detect_health_conditions_from_text(text):
    """Detect health conditions from text content"""
    if not text:
        return []
    
    text_lower = text.lower()
    detected_conditions = []
    
    conditions = {
        "diabetes": "Diabetes", "diabetic": "Diabetes", "blood sugar": "Diabetes", "glucose": "Diabetes",
        "high blood pressure": "High Blood Pressure", "hypertension": "High Blood Pressure", "bp": "High Blood Pressure",
        "heart disease": "Heart Disease", "cardiac": "Heart Disease", "coronary": "Heart Disease",
        "asthma": "Asthma", "respiratory": "Respiratory Issues", "cancer": "Cancer", "tumor": "Cancer",
        "malignant": "Cancer", "kidney disease": "Kidney Disease", "renal": "Kidney Disease",
        "lung disease": "Lung Disease", "pulmonary": "Lung Disease", "arthritis": "Arthritis",
        "thyroid": "Thyroid Disorder", "cholesterol": "High Cholesterol", "migraine": "Migraine",
        "depression": "Depression", "anxiety": "Anxiety"
    }
    
    for keyword, condition in conditions.items():
        if keyword in text_lower and condition not in detected_conditions:
            detected_conditions.append(condition)
    
    return detected_conditions

# --- Flask Routes ---

@app.route("/")
def home():
    """Render the Home page."""
    return render_template("Home.html")

@app.route("/home")
def home_alt():
    """Alternative route for Home page."""
    return render_template("Home.html")

@app.route('/gen', methods=['GET', 'POST'])
@app.route('/generate', methods=['GET', 'POST'])
def generate():
    """Generate a workout routine based on user input."""
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash("Please log in to generate a personalized workout routine.", "error")
            return redirect(url_for('login', next=url_for('generate')))
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            
            if weight <= 0 or height <= 0:
                flash("Please enter valid positive weight and height values.", "error")
                return render_template('index.html')
            
            intensity = calculate_intensity(weight, height)
            routine = output(intensity)
            return render_template('index.html', routine=routine)
        
        except ValueError:
            flash("Please enter numeric values for weight and height.", "error")
            return render_template('index.html')
        except Exception as e:
            logger.error(f"Error generating routine: {e}")
            flash("An error occurred while generating your routine.", "error")
            return render_template('index.html')

    return render_template('index.html')

@app.route("/diet")
def diet():
    """Render the diet plan page."""
    return render_template("diet.html")

@app.route("/diet-plan", methods=["GET", "POST"])
def diet_plan():
    """Handle diet plan generation."""
    diet_plan = None
    if request.method == "POST":
        if not current_user.is_authenticated:
            flash("Please log in to generate a personalized meal plan.", "error")
            return redirect(url_for('login', next=url_for('diet_plan')))
        try:
            age = int(request.form["age"])
            height = float(request.form["height"])
            weight = float(request.form["weight"])
            goal = request.form["goal"]
            duration = int(request.form["duration"])
            diet_type = request.form["diet_type"]
            gender = request.form["gender"]
            activity_level = request.form["activity_level"]
            
            if age <= 0 or height <= 0 or weight <= 0 or duration <= 0:
                flash("Please enter valid positive values for all fields.", "error")
                return render_template("diet.html")
            
            health_conditions = json.loads(request.form.get("health_conditions", "[]"))
            
            user = WeeklyDietPlan(age, height, weight, goal, duration, diet_type, gender, activity_level, health_conditions)
            diet_plan = user.plan
            
        except ValueError as e:
            flash(f"Invalid input: {str(e)}", "error")
            logger.error(f"Diet plan generation failed: {e}")
        except Exception as e:
            flash("An error occurred while generating your meal plan. Please try again.", "error")
            logger.error(f"Diet plan generation failed: {e}")
            
    return render_template("diet.html", diet_plan=diet_plan)

@app.route('/sport', methods=['GET', 'POST'])
def sports():
    """Render the sports page, or generate a level-based routine on POST."""
    if request.method == 'POST':
        # Accept both form posts and JSON (the page fetches JSON).
        data = request.get_json(silent=True) or request.form
        fitness_level = (data.get('fitness_level') or '').strip()
        if not fitness_level:
            return jsonify({'status': 'error', 'error': 'Please choose a fitness level.'}), 400
        try:
            routine = generate_sport_routine(fitness_level)
            return jsonify({
                'status': 'success',
                'level': fitness_level,
                'routine': routine,
            })
        except Exception as e:
            logger.error(f"Error generating sport routine: {e}")
            return jsonify({'status': 'error', 'error': 'Could not generate a routine right now.'}), 500
    return render_template('sports.html')

@app.route("/workout")
def work():
    """Render the workout sections page."""
    return render_template("Sections.html")

@app.route("/GP")
def gp():
    """Render a general placeholder page (page5.html)."""
    return render_template("page5.html")

@app.route("/workout-plan")
def workout_plan():
    """Render the workout plan page."""
    return render_template("workout_plan.html")

# Day-specific workout plan pages
@app.route("/D1")
def d1(): return render_template("day1.html")
@app.route("/D2")
def d2(): return render_template("day2.html")
@app.route("/D3")
def d3(): return render_template("day3.html")
@app.route("/D4")
def d4(): return render_template("day4.html")
@app.route("/D5")
def d5(): return render_template("day5.html")
@app.route("/D6")
def d6(): return render_template("day6.html")
@app.route("/D7")
def d7(): return render_template("day7.html")

@app.route('/yoga')
def yoga():
    """Render the Yoga page."""
    return render_template('Yoga.html')

@app.route('/coaches')
def coaches():
    """Render the Coaches page."""
    return render_template('coaches.html')

# --- Authentication routes ---

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Create a new user account."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        age = request.form.get('age', '').strip()
        gender = request.form.get('gender', '').strip()
        goal = request.form.get('goal', '').strip()

        # Server-side validation
        if len(name) < 2:
            flash("Please enter your name (at least 2 characters).", "error")
        elif '@' not in email or '.' not in email:
            flash("Please enter a valid email address.", "error")
        elif len(password) < 6:
            flash("Password must be at least 6 characters.", "error")
        elif User.query.filter_by(email=email).first():
            flash("An account with that email already exists. Please log in.", "error")
        else:
            try:
                user = User(
                    name=name,
                    email=email,
                    age=int(age) if age.isdigit() else None,
                    gender=gender or None,
                    goal=goal or None,
                )
                user.set_password(password)
                db.session.add(user)
                db.session.commit()
                login_user(user)
                flash(f"Welcome, {user.name}! Your account has been created.", "success")
                return redirect(url_for('home'))
            except Exception as e:
                db.session.rollback()
                logger.error(f"Registration failed: {e}")
                flash("Could not create your account right now. Please try again later.", "error")

    return render_template('registration.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Log an existing user in."""
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f"Welcome back, {user.name}!", "success")
            next_page = request.args.get('next')
            # Only allow relative redirects to avoid open-redirect attacks.
            if next_page and next_page.startswith('/'):
                return redirect(next_page)
            return redirect(url_for('home'))

        flash("Invalid email or password.", "error")

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    """Log the current user out."""
    logout_user()
    flash("You have been logged out.", "success")
    return redirect(url_for('home'))


@app.route('/ai-coach')
@login_required
def ai_coach():
    """Display the AI fitness coach chatbot interface."""
    return render_template('chatbot.html')

@app.route('/api/chat', methods=['POST'])
@login_required
def chat_api():
    """API endpoint for chatbot conversations."""
    try:
        data = request.json or {}
        message = data.get('message', '').strip()

        if not message:
            return jsonify({'error': 'Message is required'}), 400
        
        ai_response = chat_with_fitness_ai(message)
        
        return jsonify({
            'response': ai_response,
            'status': 'success'
        })
    except Exception as e:
        logger.error(f"Server error in chat API: {str(e)}")
        return jsonify({
            'error': f'Server error: {str(e)}',
            'status': 'error'
        }), 500

@app.route('/upload_medical_certificate', methods=['POST'])
def upload_medical_certificate():
    """Handle medical certificate upload and extract health conditions."""
    try:
        if 'medical_certificate' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'}), 400
        
        file = request.files['medical_certificate']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'}), 400
        
        allowed_extensions = {'txt', 'pdf', 'docx'}
        file_extension = file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else ''
        
        if file_extension not in allowed_extensions:
            return jsonify({'success': False, 'error': 'File type not supported. Please upload PDF, DOCX, or TXT files.'}), 400
        
        text_content = ""
        if file_extension == 'txt':
            try:
                text_content = file.read().decode('utf-8')
            except UnicodeDecodeError:
                text_content = file.read().decode('latin-1')
        else:
            # Inform user that we don't process complex file types directly
            return jsonify({
                'success': False,
                'error': f'Processing {file_extension.upper()} files requires specific libraries. Please copy-paste the text content or convert to TXT format.'
            }), 400
        
        health_conditions = detect_health_conditions_from_text(text_content)
        conditions_text = ', '.join(health_conditions) if health_conditions else 'None'
        
        return jsonify({
            'success': True,
            'health_conditions': health_conditions,
            'conditions_text': conditions_text
        })
    except Exception as e:
        logger.error(f"Error processing file: {e}")
        return jsonify({'success': False, 'error': f'Error processing file: {str(e)}'}), 500

# Additional routes for legal pages
@app.route('/privacy')
def privacy_policy():
    """Render the Privacy Policy page."""
    return render_template('privacy.html')

@app.route('/terms')
def terms_of_service():
    """Render the Terms of Service page."""
    return render_template('terms.html')

@app.route('/about')
def about():
    """Render the About page."""
    return render_template('about.html')

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    """Render a custom 404 error page."""
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    """Render a custom 500 error page."""
    logger.error(f"Internal server error: {e}")
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)