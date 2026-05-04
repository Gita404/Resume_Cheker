"""
Job Descriptions for Resume Checking.
Add or modify entries in JOB_LISTINGS to change available roles.
"""

JOB_LISTINGS = [

    # ── 1. Nexora Technologies ──────────────────────────────────────────────
    {
        "company": "Nexora Technologies Pvt. Ltd.",
        "title": "Full Stack Developer",
        "description": """Position: Full Stack Developer
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
- Experience with Agile/Scrum teams.""",
        "required_skills": [
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
        ],
        "bonus_skills": [
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
        ],
        "min_match_percent": 25,
    },

    # ── 2. Meridian Solutions ───────────────────────────────────────────────
    {
        "company": "Meridian Solutions",
        "title": "Data Analyst",
        "description": """Position: Data Analyst
Company: Meridian Solutions
Location: Hyderabad, India (On-site)
Experience: 1-3 years

About the role:
We are looking for a Data Analyst to support our business intelligence
team. You will work with large datasets, build reports and dashboards,
and help stakeholders make data-driven decisions. The ideal candidate
is comfortable with SQL, has experience with visualization tools, and
can communicate findings clearly.

Day-to-day responsibilities:
- Write and optimize SQL queries to extract and transform data.
- Build dashboards and reports using Tableau or Power BI.
- Clean, validate, and prepare data for analysis.
- Work with product and marketing teams to define KPIs and metrics.
- Conduct exploratory data analysis and present findings.
- Maintain documentation for data sources and report logic.

Must-have requirements:
- Bachelors degree in Statistics, Mathematics, Computer Science,
  or a related field.
- Strong SQL skills (joins, subqueries, window functions).
- Experience with at least one visualization tool (Tableau, Power BI,
  or Looker).
- Working knowledge of Excel and Google Sheets.
- Basic understanding of Python or R for data analysis.
- Good written and verbal communication skills.

Good-to-have:
- Experience with Python libraries (pandas, NumPy, matplotlib).
- Familiarity with ETL pipelines or data warehousing concepts.
- Knowledge of A/B testing and statistical methods.
- Experience with Google Analytics or similar tools.
- Exposure to cloud platforms (AWS, GCP, or Azure).""",
        "required_skills": [
            "sql", "mysql", "postgresql",
            "tableau", "power bi", "powerbi", "looker",
            "excel", "google sheets",
            "python", "r",
            "data analysis", "analytics",
            "statistics", "kpi", "metrics",
            "dashboard", "reporting",
        ],
        "bonus_skills": [
            "pandas", "numpy", "matplotlib", "seaborn",
            "etl", "data warehouse", "snowflake", "redshift",
            "a/b testing", "hypothesis testing",
            "google analytics",
            "aws", "gcp", "azure",
            "jupyter", "notebook",
            "dbt", "airflow",
        ],
        "min_match_percent": 25,
    },

    # ── 3. CloudVerse Inc. ──────────────────────────────────────────────────
    {
        "company": "CloudVerse Inc.",
        "title": "DevOps Engineer",
        "description": """Position: DevOps Engineer
Company: CloudVerse Inc.
Location: Pune, India (Remote)
Experience: 3-6 years

About the role:
We are hiring a DevOps Engineer to manage and improve our cloud
infrastructure and CI/CD pipelines. You will work closely with
development teams to automate deployments, monitor systems, and
ensure high availability of our services.

Day-to-day responsibilities:
- Design and maintain CI/CD pipelines using Jenkins, GitHub Actions,
  or GitLab CI.
- Manage cloud infrastructure on AWS (EC2, ECS, RDS, S3, Lambda).
- Write Infrastructure as Code using Terraform or CloudFormation.
- Set up monitoring and alerting using Prometheus, Grafana, or
  CloudWatch.
- Containerize applications using Docker and orchestrate with
  Kubernetes.
- Manage Linux servers and automate tasks with Bash/Python scripts.
- Implement security best practices and manage access controls.

Must-have requirements:
- Bachelors degree in Computer Science or equivalent experience.
- At least 3 years of experience in a DevOps or SRE role.
- Strong experience with AWS services.
- Hands-on experience with Docker and Kubernetes.
- Proficiency in at least one IaC tool (Terraform, CloudFormation).
- Experience with CI/CD tools (Jenkins, GitHub Actions, GitLab CI).
- Solid Linux administration skills.
- Scripting ability in Bash and Python.

Good-to-have:
- Experience with service mesh (Istio, Linkerd).
- Knowledge of HashiCorp tools (Vault, Consul).
- Familiarity with ELK stack or Datadog for logging.
- Experience with cost optimization on cloud platforms.
- AWS or Kubernetes certifications.""",
        "required_skills": [
            "aws", "ec2", "ecs", "rds", "s3", "lambda",
            "docker", "kubernetes", "k8s",
            "terraform", "cloudformation",
            "jenkins", "github actions", "gitlab ci",
            "ci/cd", "cicd",
            "linux", "bash", "python",
            "monitoring", "prometheus", "grafana", "cloudwatch",
            "devops", "sre",
            "git",
        ],
        "bonus_skills": [
            "istio", "linkerd", "service mesh",
            "vault", "consul", "hashicorp",
            "elk", "elasticsearch", "logstash", "kibana", "datadog",
            "ansible", "puppet", "chef",
            "nginx", "apache",
            "helm", "argocd",
        ],
        "min_match_percent": 25,
    },
]


# ── Helper to get a listing by index ─────────────────────────────────────────

def get_listing(index: int) -> dict:
    """Return a single job listing by index (clamped to valid range)."""
    index = max(0, min(index, len(JOB_LISTINGS) - 1))
    return JOB_LISTINGS[index]


def get_listing_labels() -> list[str]:
    """Return display labels for each listing (used in the selector)."""
    return [
        f"{jd['title']} -- {jd['company']}" for jd in JOB_LISTINGS
    ]
