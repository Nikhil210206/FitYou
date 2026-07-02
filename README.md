[![OSCI-Project-Banner.png](https://i.postimg.cc/76mJvBmF/OSCI-Project-Banner.png)](https://postimg.cc/8JfzMb84)

<p align="center">
  <img src="https://img.shields.io/badge/React-61DAFB?style=for-the-badge&logo=react&logoColor=white" alt="React.js">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-learn">
  <img src="https://img.shields.io/badge/MongoDB-47A248?style=for-the-badge&logo=mongodb&logoColor=white" alt="MongoDB">
  <img src="https://img.shields.io/badge/Google%20Generative%20AI-4285F4?style=for-the-badge&logo=google&logoColor=white" alt="Google Generative AI">
</p>

# FitYiu: Your AI Fitness Companion 🌟

FitYou redefines fitness with **AI-driven personalized plans** for workouts and diets. Empowering your fitness journey with cutting-edge technology and expert guidance, FitYou adapts to your unique goals and lifestyle.

**🌐 Live Deployment:** [Check it out here 👀](https://fityou-fit-ai.onrender.com/)

**Points for issues on leaderboard:** 
1 star - 5 points |
2 star - 10 points |
3 star - 15 points

## 📑 Table of Contents

- [🌟 Key Features](#-key-features)
- [💻 Technologies at Work](#-technologies-at-work)
- [🎯 Highlights](#-highlights)
- [📂 Project Structure](#-project-structure)
- [⚙️ How to Install](#️-how-to-install)
- [🛠️ Usage](#️-usage)
- [🚀 Future Enhancements](#-future-enhancements)
- [🤝 Contributions Welcome](#-contributions-welcome)
- [📞 Contact](#-contact)
- [🙏 Acknowledgments](#-acknowledgments)
- [📜 License](#-license)


## 🌟 Key Features

- 🏋️ **Personalized Workout Plans**
  Tailored routines based on your preferences, fitness goals, and available equipment, ensuring an effective and safe workout experience.

- 🥗 **Customized Diet Plans**
  Balanced meal recommendations with a special focus on Indian cuisine, offering 60% vegetarian and 40% non-vegetarian options.

- 🤖 **AI-Powered Insights**
  Smart algorithms deliver highly personalized fitness and diet suggestions, continuously learning and adapting to your progress.

- 🎨 **Dark-Themed, User-Friendly Interface**
  An intuitive and aesthetically pleasing dark-themed design provides a smooth and engaging user experience.

- 🛠️ **Professional Guidance**
  Access to experienced coaches and mentors for expert support and advice throughout your fitness journey.



## 💻 Technologies at Work

- **Frontend:** **React.js** for building a dynamic, responsive, and modern user interface.
- **Backend:** **Flask** for robust API management and seamless integration of AI models.
- **Machine Learning:** **Scikit-learn** powers the predictive modeling for personalized recommendations.
- **Database:** **MongoDB** for flexible and scalable storage of user profiles, fitness data, and personalized plans.
- **AI API:** **Google Generative AI** for advanced language understanding and enhanced interactive features.


## 🎯 Highlights

- **Stylish Dark Theme:** An elegant UI featuring subtle orange accents and modern typography for a premium feel.
- **Indian Cuisine Focus:** Thoughtfully curated meal plans that align with diverse cultural and dietary preferences specific to India.
- **AI-Driven Accuracy:** Leveraging data-powered intelligence to provide precise and effective personalized fitness recommendations.
- **Scalability:** Architected for growth, the platform is designed to efficiently accommodate an expanding user base and new features.


## 📂 Project Structure

The FitAi project follows a consolidated structure where both frontend (React) and backend (Flask) components reside primarily in the root directory, with dedicated folders for static assets, templates, and configurations.


```
📂 FitAi/  
├── .DS_Store                      # macOS folder metadata (can be ignored)  
├── .gitignore                     # Specifies untracked files to ignore  
├── .hintrc                        # Configuration for code linting/formatting  
├── .vercelignore                  # Files to ignore during Vercel deployment  
├── app.py                         # Main Flask application entry point  
├── DEPLOYMENT.md                  # Deployment instructions & guidelines  
├── diet_data.csv                  # Dataset containing diet-related data  
├── env_template.txt               # Template for environment variable setup  
├── exercises.csv                  # Dataset containing exercise-related data  
├── fitai.jpg                      # Project branding/logo image  
├── LICENSE                        # License file  
├── package-lock.json              # Exact versions of npm dependencies  
├── package.json                   # Frontend project metadata & npm scripts  
├── postcss.config.js              # PostCSS (CSS processor) configuration  
├── README.md                      # Main project documentation  
├── render.yaml                    # Deployment configuration for Render  
├── requirements.txt               # Python dependencies for Flask backend  
├── runtime.txt                    # Python runtime version specification  
├── SECURITY.md                    # Security policy for contributors/users  
├── tailwind.config.js             # Tailwind CSS configuration file  
└── vercel.json                    # Vercel deployment configuration  

├── .github/                       # GitHub repo configs  
│   ├── pull_request_template.md   # Template for PRs  
│   ├── ISSUE_TEMPLATE/            # Templates for bug reports, feature requests  
│   │   ├── bug_report.yml  
│   │   ├── config.yml  
│   │   └── feature_request.yml  
│   └── workflows/                 # CI/CD workflows (deploy, automation, etc.)  
│       ├── deploy.yml  
│       ├── issue-create-automate-message.yml  
│       └── pr-create-automate-message.yml  

├── .idea/                         # IDE configuration files (JetBrains IDEs)  
│   ├── .gitignore                 # IDE-specific gitignore  
│   ├── FitYou---Fit_Ai.iml        # IntelliJ project file  
│   ├── modules.xml                # IDE module settings  
│   ├── vcs.xml                    # Version control config for IDE  
│   └── inspectionProfiles/        # IDE inspection profile settings  
│       └── profiles_settings.xml  

├── static/                        # Static frontend assets  
│   ├── .DS_Store                  # macOS metadata (can be ignored)  
│   ├── css/                       # Theme & custom CSS  
│   │   └── theme.css              # Global theme styles  
│   ├── images/                    # Static images (logos, backgrounds, etc.)  
│   │   ├── faviconn.png  
│   │   ├── fitai.jpg  
│   │   ├── logo.jpg  
│   │   ├── med.jpg  
│   │   ├── nutrition.jpg  
│   │   ├── workoutplan.jpg  
│   │   └── yinyoga.jpg  
│   └── js/                        # JavaScript & React components  
│       ├── README_WorkoutPlanCard.md # Documentation for WorkoutPlanCard  
│       ├── theme.js               # Theme switcher logic  
│       ├── WorkoutPlanCard.jsx    # JSX component for workout plans  
│       ├── WorkoutPlanCard.tsx    # TypeScript variant of workout plan component  
│       ├── WorkoutPlanCardDemo.html # Demo HTML for workout plan card  
│       └── WorkoutPlanCardExample.jsx # Example usage of component  

├── templates/                     # Flask Jinja2 templates (HTML + assets)  
│   ├── chatbot.html               # Chatbot UI  
│   ├── coaches.html               # Coaches Marketplace  
│   ├── day1.html                  # Day 1 plan  
│   ├── day2.html                  # Day 2 plan  
│   ├── day3.html                  # Day 3 plan  
│   ├── day4.html                  # Day 4 plan  
│   ├── day5.html                  # Day 5 plan  
│   ├── day6.html                  # Day 6 plan  
│   ├── day7.html                  # Day 7 plan (Rest Day Importance & Routine)  
│   ├── diet.html                  # Diet plan page  
│   ├── diet_data.csv              # Diet data (duplicated for template use)  
│   ├── Home.html                  # Landing page  
│   ├── index.html                 # Main index/entry point  
│   ├── login.html                 # Login page  
│   ├── page5.html                 # Additional page (generic)  
│   ├── privacy.html               # Privacy policy page  
│   ├── registration.html          # User registration page  
│   ├── Sections.html              # Sections overview  
│   ├── sports.html                # Sports content page  
│   ├── terms.html                 # Terms & conditions page  
│   ├── Untitled-2.css             # CSS (unnamed, cleanup recommended)  
│   ├── workout_plan.html          # Workout plan overview  
│   ├── workout_routine.html       # Workout routine details page  
│   ├── Yoga.html                  # Yoga-related content  
│   ├── css/                       # CSS scoped for templates  
│   │   └── style.css  
│   └── images/                    # Images used in templates  
│       ├── fitai.jpg  
│       ├── FY.png  
│       ├── gym.jpg.png  
│       └── logo.jpg  

└── __pycache__/                   # Python compiled bytecode cache  
    └── app.cpython-313.pyc  

    ```


## ⚙️ How to Install

Follow these steps to set up and run FitAi locally for development:

1.  **Fork the repository.**
    * Click the "Fork" button on the top right of the GitHub repository page to create a copy in your account.
2.  **Clone your forked repository:**
    ```
    git clone https://github.com/Nikhil210206/FitYou---Fit_Ai.git
    ```
3.  **Navigate to the project directory:**
    ```
    cd FitYou---Fit_Ai
    ```
4.  **Install Python dependencies for the backend:**
    ```
    pip install -r requirements.txt
    ```
5.  **Install frontend dependencies:**
    ```
    npm install
    ```
6.  **Start the backend server:**
    ```
    flask run
    # Alternatively, if 'flask' command is not globally available:
    # python app.py
    ```
7.  **Start the frontend development server:**
    ```
    npm start
    ```
    * **Note:** Given the consolidated project structure, the `npm start` command runs the React development server. It serves the frontend assets (like your React components) which are then likely integrated or proxied by the Flask backend.
    * **Important:** Ensure both the Flask backend (Step 6) and the React development server (Step 7) are running concurrently for the full application functionality.
8.  **Open in browser:**
    * Access the application by navigating to: `http://localhost:5000`
    * **Explanation:** The Flask backend, which serves as the primary web server, typically runs on port `5000` by default. Your React frontend assets are likely served through this same port once the Flask application is running and configured to handle them.


## 🛠️ Usage

-   **Sign up or Log in:** Create an account or log in to access your personalized fitness dashboard.
-   **Enter your details:** Provide information about your fitness goals, current activity level, and available equipment.
-   **Receive Plans:** Get instant access to tailored workout routines and customized diet plans.
-   **Track Progress:** Monitor your achievements and adjust your preferences to evolve your plan as needed.
-   **Connect with Experts:** Engage with experienced coaches and mentors for additional guidance and motivation.



## 🚀 Future Enhancements

-   **Wearable Device Integration:** Seamless connectivity with popular wearable devices for real-time activity tracking and data synchronization.
-   **Multi-Language Support:** Expand accessibility by offering the application in multiple languages.
-   **Gamification Features:** Introduce engaging game-like elements and challenges to enhance user motivation and engagement.
-   **Advanced Analytics Dashboard:** A comprehensive dashboard providing deeper insights into user progress, performance metrics, and health trends.



## 🤝 Contributions Welcome

We welcome contributions from the community! To contribute to FitAi, please follow these steps to ensure a smooth and conflict-free process:

1.  **Fork the repository.**
    * Click the "Fork" button on the top right of the [FitAi GitHub repository](https://github.com/Nikhil210206/FitYou---Fit_Ai.git) 

2.  **Clone your forked repository locally:**
    ```
    git clone https://github.com/your-username/FitYou---Fit_Ai.git
    cd FitAi
    ```
    *Replace `your-username` with your actual GitHub username.*

3.  **Add the upstream remote:**
    * This step links your local repository to the original FitAi repository, allowing you to fetch updates.
    ```
    git remote add upstream https://github.com/Nikhil210206/FitYou---Fit_Ai.git
    ```

4.  **Fetch the latest changes from the upstream `main` branch:**
    * Before starting any work, always synchronize your local `main` branch with the upstream `main` to get the most recent updates and avoid merge conflicts.
    ```
    git fetch upstream
    ```

5.  **Merge upstream changes into your local `main` branch:**
    ```
    git checkout main
    git merge upstream/main
    ```
    * This ensures your local `main` is up-to-date.

6.  **Create a new branch for your feature or bug fix:**
    * Always work on a new branch, giving it a descriptive name (e.g., `feature/add-dark-mode`, `bugfix/fix-login-issue`).
    ```
    git checkout -b feature-name
    ```

7.  **Make your changes according to the issue assigned to you.**
    * Implement your feature or bug fix. Ensure your code follows the project's coding standards and includes necessary tests.

8.  **Commit your changes with a clear and concise message:**
    * Use a descriptive commit message that explains what changes were made.
    ```
    git commit -m 'feat: Add new feature'
    # Example for a bug fix:
    # git commit -m 'fix: Resolve login authentication issue'
    ```

9.  **Push your branch to your forked repository on GitHub (and set upstream):**
    * This command pushes your local `feature-name` branch to your `origin` remote (your forked repository) and sets it up to track that remote branch. This means that from now on, you can simply use `git push` and `git pull` without specifying the remote and branch name for this particular branch.
    ```
    git push -u origin feature-name
    ```
    * After this first push, subsequent pushes from this branch can simply be `git push`.

10. **Open a Pull Request (PR) for review:**
    * Go to your forked repository on GitHub.
    * You will see a "Compare & pull request" button next to your newly pushed branch. Click it.
    * Provide a clear title and detailed description of your changes, referencing the issue number it addresses (e.g., "Fixes #123").
    * Ensure your code adheres to our style guidelines and includes relevant tests.
   

## 💥 Resolving Merge Conflicts 

Merge conflicts happen when Git can't automatically reconcile changes between two branches. Here's how to resolve them concisely:

1.  **Sync with Latest `main`:**
    * Ensure your local `main` branch is up-to-date, then merge it into your feature branch.
    ```bash
    git checkout main
    git pull upstream main # Or git pull origin main
    git checkout feature-name
    git merge main
    ```
    *This step will likely trigger the conflict.*

2.  **Edit Conflicting Files:**
    * Open files flagged by Git. Manually edit sections marked by `<<<<<<<`, `=======`, and `>>>>>>>` to combine the desired changes.
    * **Remove all conflict markers** after resolution.

3.  **Stage Changes:**
    * After resolving each file, stage it:
    ```
    git add .
    ```

4.  **Commit Merge:**
    * Git will provide a default merge commit message. Review and save it.
    ```
    git commit
    ```

5.  **Push Resolved Branch:**
    * Push your updated, conflict-free feature branch:
    ```
    git push origin feature-name
    ```



## 📞 Contact

For any questions, suggestions, or collaborations, feel free to reach out to:

-   **Name:** Nikhil Balamurugan
-   **GitHub:** [Nikhil210206](https://github.com/Nikhil210206)
-   **Email:** nikhilbalamurugan@gmail.com


## 🙏 Acknowledgments

We extend our sincere gratitude to:

-   My incredible team and all dedicated contributors for their hard work and commitment.
-   The open-source community for providing invaluable tools and libraries that made this project possible.
-   The fitness community for their continuous inspiration and feedback.


## 📜 License

-   This project is licensed under the **MIT License** - see the [LICENSE](./LICENSE) file for more details.
-   This Project is under Open Source Connect India 2025
