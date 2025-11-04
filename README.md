# [Modern Django Blog]

## 🌟 Modern Django Blog Platform

A fully functional, optimized, and extensible blog application built with Django. This platform provides essential blogging features including structured content, advanced filtering, and efficient content retrieval.

## ✨ Features

This blog application includes the following key features:

* **Optimized Querying:** Uses **`select_related()`** and **`prefetch_related()`** in list views to efficiently retrieve related data (Category, Author, Tags) and minimize database queries (solving the N+1 problem).
* **Search Functionality:** Implements fuzzy search via **`Q` objects** across post **Title** and **Content**.
* **Advanced Filtering:** Dedicated views and clean URLs for filtering posts by:
    * Category (using slugs)
    * Tag (using slugs)
    * Author (using usernames)
* **Pagination Persistence:** Implemented using Django's Paginator, ensuring the **search query or active filter** is preserved when navigating between pages.
* **Post Detail View:** Displays rich HTML content (using `|safe`), author information, a view counter, and dynamically retrieved **related posts**.
* **Account Setup:** Initial views and URLs for user account management (`accounts` app).
* **Clean URL Structure:** Uses slugs for posts, categories, and tags for SEO-friendly URLs.

## 🛠️ Technology Stack

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | Python, Django | The core web framework. |
| **Database** | SQLite (Default) / [**PostgreSQL**] | Handles data storage. |
| **Templating** | Django Template Language (DTL) | Used for dynamic HTML rendering. |

## 📦 Installation & Setup

### 1. Prerequisites

Ensure you have Python (3.8+) and Git installed.

### 2. Clone the Repository

```bash
git clone https://github.com/NimaZ05/Blogs.git
cd Blogs  
```
### 3. Setup Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  
# On Windows: venv\Scripts\activate
```
### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Database Setup

```bash
# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create a Superuser
python manage.py createsuperuser
```

### 6. Run the Application

```bash
python manage.py runserver
```

## 🎉 Contributing, Feedback, and Bugs

Thank you for exploring this project! Your input is incredibly valuable as we refine this application.

This project is a work in progress, and there are always better ways to implement functionality. If you have any suggestions, notice any bugs, or see potential for performance improvements, please don't hesitate to reach out.

**We appreciate your opinion on:**

* **Code Structure**
* **Query Performance** 
* **Template Logic**

### Reporting Bugs and Suggestions

1.  **Open an Issue:** Use the repository's **Issues** tab to report the problem or proposal.
2.  **Submit a Pull Request (PR):** Feel free to fork the repository and submit a PR with your fix or feature implementation.

We look forward to collaborating!


