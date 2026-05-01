"""
Hardcoded Job Description for Resume Checking.
Modify this file to change the job role and requirements.
"""

COMPANY_NAME = "Nexora Technologies Pvt. Ltd."

JOB_TITLE = "Full Stack Developer"

JOB_DESCRIPTION = """
Position: Full Stack Developer
Company: Nexora Technologies Pvt. Ltd.
Location: Bangalore, India (Hybrid)
Experience: 2-5 years

About the role:
We are hiring a Full Stack Developer to join our product engineering team.
You will be responsible for building and maintaining internal and
client-facing web applications. The role requires someone who can work
independently across the frontend and backend, ship production-ready
code, and communicate clearly with the rest of the team.

Day-to-day responsibilities:
- Build and maintain web applications using React on the frontend
  and Node.js or Python on the backend.
- Design and implement RESTful APIs.
- Write and maintain unit and integration tests.
- Work with PostgreSQL or MongoDB for data storage.
- Deploy and manage applications using Docker and AWS (EC2, S3, Lambda).
- Participate in code reviews and sprint planning.
- Debug production issues and write post-mortems when needed.

Must-have requirements:
- Bachelors degree in Computer Science or equivalent practical experience.
- At least 2 years of professional experience building web applications.
- Strong working knowledge of JavaScript and TypeScript.
- Hands-on experience with React.js (hooks, context, routing).
- Backend experience with Node.js (Express) or Python (Django/Flask).
- Comfortable with SQL databases (PostgreSQL or MySQL) and at least
  one NoSQL database (MongoDB preferred).
- Experience with Git and pull-request-based workflows.
- Familiarity with Docker and basic AWS services.
- Understanding of REST API design and HTTP fundamentals.

Good-to-have:
- Experience with CI/CD pipelines (GitHub Actions, Jenkins).
- Familiarity with Redis, message queues, or caching strategies.
- Exposure to microservices or event-driven architecture.
- Knowledge of GraphQL.
- Experience with Agile/Scrum teams.
"""

# Skills the candidate MUST have (checked against resume text).
# These map directly to the "must-have" section above.
REQUIRED_SKILLS = [
    "javascript", "typescript",
    "react", "react.js", "reactjs",
    "node.js", "nodejs", "express",
    "python", "django", "flask",
    "sql", "postgresql", "mysql",
    "mongodb", "nosql",
    "git", "github",
    "docker",
    "aws", "ec2", "s3", "lambda",
    "rest", "restful", "api",
    "html", "css",
    "full stack", "fullstack", "full-stack",
]

# Skills that are nice to have but not required.
BONUS_SKILLS = [
    "ci/cd", "cicd", "github actions", "jenkins",
    "redis", "rabbitmq", "kafka",
    "microservices",
    "graphql",
    "agile", "scrum",
    "jest", "pytest", "testing", "unit test",
    "kubernetes", "k8s", "terraform",
    "next.js", "nextjs",
    "vue", "vuejs",
    "fastapi",
    "elasticsearch",
]

# Minimum percentage of REQUIRED_SKILLS the candidate must match to be shortlisted.
MINIMUM_REQUIRED_MATCH_PERCENT = 25
