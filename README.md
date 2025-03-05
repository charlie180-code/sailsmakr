# Sailsmakr

**Sailsmakr** is a powerful, cloud-based platform designed to optimize and streamline business operations across various industries. The platform is built using cutting-edge technologies to ensure scalability, security, and flexibility. This README provides an overview of the technology stack, setup instructions, and key components behind Sailsmakr.

---

## Table of Contents
- [Technologies](#technologies)
- [Stack](#stack)
- [Getting Started](#getting-started)
- [Code Infrastructure](#code-infrastructure)
- [Database Management](#database-management)
- [Cloud and Containerization](#cloud-and-containerization)
- [Front-End Development](#front-end-development)
- [APIs and Integrations](#apis-and-integrations)
- [Testing and CI/CD](#testing-and-cicd)
- [License](#license)

---


## Technologies

Sailsmakr leverages a variety of modern technologies to deliver a seamless experience:

- **Python (Flask)**: Backend framework for handling requests and API logic.
- **Firestore**: Cloud-based NoSQL database for storing user-generated data such as files and media.
- **Neon DB (PostgreSQL)**: High-performance, secure PostgreSQL database for structured data management.
- **VanillaJS & ES6**: JavaScript standard used for building interactive front-end functionalities.
- **JQuery**: Simplifies HTML DOM manipulation and event handling.
- **TailwindCSS**: Utility-first CSS framework used for building responsive and modern UI components.
- **Bootstrap MD from Creative TIM**: Material design-based UI kit for building beautiful, functional user interfaces.
- **Docker**: Containerization platform for packaging the application and its dependencies to run consistently across environments.
- **Render Cloud**: Cloud platform for hosting and scaling the application.
- **OpenCage**: Geolocation API for converting coordinates into readable addresses.
- **FedEx & Freightos APIs**: Used for providing real-time shipping and freight suggestions.

---

## Stack

| ![Docker](https://img.icons8.com/color/48/000000/docker.png) Docker | ![Python](https://img.icons8.com/color/48/000000/python.png) Python | ![Firebase](https://img.icons8.com/color/48/000000/firebase.png) Firebase |
|---------------------------------------------|---------------------------------------------|---------------------------------------------|
| ![Node.js](https://img.icons8.com/color/48/000000/nodejs.png) Node.js | ![Bootstrap](https://img.icons8.com/color/48/000000/bootstrap.png) Bootstrap | ![TailwindCSS](https://img.icons8.com/color/48/000000/tailwindcss.png) TailwindCSS |
| ![FedEx](https://img.icons8.com/color/48/000000/fedex.png) FedEx | ![Render](https://img.icons8.com/external-tal-revivo-color-tal-revivo/48/000000/external-render-fast-secure-and-comprehensive-web-application-hosting-logo-color-tal-revivo.png) Render Cloud | ![VanillaJS](https://img.icons8.com/color/48/000000/javascript.png) VanillaJS |
| ![NeonDB](https://img.icons8.com/color/48/000000/database.png) NeonDB | ![jQuery](https://img.icons8.com/ios-filled/50/000000/jquery.png) jQuery | ![Jenkins](https://img.icons8.com/color/48/000000/jenkins.png) Jenkins |
| ![Flask](https://img.icons8.com/color/48/000000/flask.png) Flask | ![Terraform](https://img.icons8.com/color/48/000000/terraform.png) Terraform | ![PostgreSQL](https://img.icons8.com/color/48/000000/postgreesql.png) PostgreSQL |
| ![HTML5](https://img.icons8.com/color/48/000000/html-5.png) HTML5 | ![CSS3](https://img.icons8.com/color/48/000000/css3.png) CSS3 | ![Bash](https://img.icons8.com/color/48/000000/bash.png) Bash |

---

## Getting Started

### Prerequisites

To run Sailsmakr locally, ensure you have the following tools installed:

- **Docker**: For running the application in a containerized environment.
- **Python 3.x**: For the backend.
- **NPM**: For managing frontend dependencies and build tools.

### Installation

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/sailsmakr/sailsmakr.git
    cd sailsmakr
    ```

2. **Set Up the Backend**:
    - Create a Python virtual environment and install dependencies:
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      pip install -r requirements/common.txt
      ```

3. **Set Up the Frontend**:
    - Install npm dependencies:
      ```bash
      npm install
      ```

4. **Set Up Environment Variables**:
    - Create a `.env` file and add the necessary environment variables, such as API keys for OpenCage, FedEx, Freightos, and database credentials.

---

## Database Management

### Neon DB (PostgreSQL)

Sailsmakr uses Neon DB for managing structured data in a relational format:
- **ACID-compliant Database**: Ensures data reliability, integrity, and consistency.
- **Scalability**: Handles large-scale transactional queries and ensures data integrity.

### Firestore (NoSQL)

Firestore is used for handling unstructured data like files, media uploads, and logs:
- **Real-time Updates**: Facilitates instant data synchronization.
- **Scalability**: Easily scales with application demands.

---


## Cloud and Containerization

Sailsmakr runs on **Render Cloud**, providing seamless hosting and scaling capabilities. All components are containerized using **Docker**, ensuring consistency across development and production environments.

---

## Code Infrastructure

Sailsmakr's backend is  **mainly** powered by **Flask**, which handles API requests and core business logic. We're trying
to use the most of each framework and programming languages not just python and or flask.

```plaintext
📂 sailsmakr
├── 📁 apps
│   ├── 📁 accounting
│   ├── 📁 ads
│   ├── 📁 ai
│   ├── 📁 api
│   ├── 📁 archive
│   ├── 📁 auth
│   ├── 📁 blog
│   ├── 📁 career
│   ├── 📁 classroom
│   ├── 📁 calendar
│   ├── 📁 insights
│   ├── 📁 ordering
│   ├── 📁 promotion
│   ├── 📁 reseller
│   ├── 📁 sessions
│   ├── 📁 user
│   ├── 📁 wallet
│   ├── docker-compose.yml
│   ├── __init__.py(Main Entry Point)
│   ├── utils.py
│   ├── decorators.py
│   ├── filters.py
│   ├── task.py
│   ├── messages.pot
│   ├── babel.cfg
│   ├── tailwind.config.js
├── 📁 apps/templates
│   ├── 📁 api
│   ├── 📁 auth
│   ├── 📁 dashboard
│   ├── 📁 emails
│   ├── 📁 errors
│   ├── 📁 includes
│   ├── 📁 main
│   ├── 📁 reports
│   ├── 📁 views
│   ├── __init__.py
├── 📁 apps/templates/views
│   ├── 📁 empty
│   ├── 📁 engineering
│   ├── 📁 errors
│   ├── 📁 general
│   ├── 📁 hospital
│   ├── 📁 sailsmakr
│   ├── 📁 school
│   ├── 📁 shipping
│   ├── splash.html
│   ├── main.js
│   ├── preload.js
├── 📁 server
│   ├── nginx.conf (Web Server Config)
│   ├── package.json
│   ├── package-lock.json
│   ├── render.yaml
│   ├── sails.spec
├── 📁 build
├── 📁 dist
├── 📁 migrations
├── 📁 linux-venv
├── 📁 win-venv
├── CODE_OF_CONDUCT.md
├── contributing.md
├── config.py (Configuration Settings)
├── docker-compose.yml
├── Dockerfile (Container Config)
├── instance
├── run.py
├── setup.sh
├── build.sh
├── installer.nsh
├── README.md
├── documentation.txt
├── logo-desktop-splash.svg

```

---

## Database Management

### Neon DB (PostgreSQL)

Sailsmakr uses Neon DB for managing structured data in a relational format:
- **ACID-compliant Database**: Ensures data reliability, integrity, and consistency.
- **Scalability**: Handles large-scale transactional queries and ensures data integrity.

### Firestore (NoSQL)

Firestore is used for handling unstructured data like files, media uploads, and logs:
- **Real-time Updates**: Facilitates instant data synchronization.
- **Scalability**: Easily scales with application demands.

---

## Front-End Development

Sailsmakr's front-end is built using a combination of VanillaJS, ES6, and JQuery to deliver a dynamic and responsive user experience. The UI is styled using **TailwindCSS** and **Bootstrap MD from Creative TIM**.

### Front-End Libraries and Frameworks:
- **TailwindCSS**: Utility-first CSS framework for creating responsive designs quickly.
- **Bootstrap MD**: Material Design components from Creative TIM for modern UI.
- **VanillaJS (ES6)**: Core JavaScript standard for interactive components.
- **JQuery**: Simplifies DOM manipulation and event handling.

---

## Key Links

- [Main Dockerfile](https://github.com/charlie180-code/sailsmakr/blob/main/Dockerfile)
- [Docker Compose](https://github.com/charlie180-code/sailsmakr/blob/main/docker-compose.yml)
- [Nginx Configuration](https://github.com/charlie180-code/sailsmakr/tree/main/nginx)
- [Backend Code](https://github.com/charlie180-code/sailsmakr/tree/main/apps)
- [Main App Entry](https://github.com/charlie180-code/sailsmakr/blob/main/apps/__init__.py)
- [Models](https://github.com/charlie180-code/sailsmakr/tree/main/apps/models)
- [Configurations file](https://github.com/charlie180-code/sailsmakr/blob/main/config.py)
- [Frontend Code](https://github.com/charlie180-code/sailsmakr/tree/main/apps/static)
- [Basic Minimal Guide](https://github.com/charlie180-code/sailsmakr/blob/main/documentation.txt)
- [Contributions Guide](https://github.com/charlie180-code/sailsmakr/blob/main/contributing.md)

---

## Demo Videos

- [Demo 1: Inviting other company members](https://drive.google.com/file/d/1whSC-cLStOcRrl8bqqeKta9Nwpl_JEGT/view?usp=sharing)
- [Demo 2: Archiving system with error](https://drive.google.com/file/d/1p7SjoqDPwo8PyFm6fgy97L8hQu6PJ45q/view?usp=sharing)
- [Demo 3: Basic folder files search](https://drive.google.com/file/d/1UifxNJffOr-EriG4bDGdHsZaBjqJns1H/view?usp=sharing)
- [Demo 4: Employee infos updating](https://drive.google.com/file/d/1ziSB5M_mAo95Wxn_YsMYTZPweY2WmXhB/view?usp=sharing)
- [Demo 5: Invoice generation](https://drive.google.com/file/d/1vgKVsiO8zecIma0iYMzCk819vmyyCVC2/view?usp=sharing)
- [Demo 6: Student Enrollment Workflow](https://drive.google.com/file/d/1O7cl_BQuN1N6uLCEDy5dGeA-iUwaykTI/view?usp=sharing)

---

## APIs and Integrations

Sailsmakr integrates several third-party APIs to enhance functionality:

- **OpenCage**: Geolocation API that converts geographic coordinates into human-readable addresses, useful for location-based features.


---

## Testing and CI/CD

Sailsmakr plans to use **Jenkins** for continuous integration and automated testing. This ensures that code pushed to the repository is automatically tested, and builds are generated for deployment.

---

## Roadmap

- **Code as Infrastructure (IaC)**: Ensuring that infrastructure is defined and maintained programmatically using tools such as **Terraform** for provsionning infrastucture and **Ansible** for configuring this infrastructure.
- **Kubernetes (K8s)**: We have so many microservices that needs to be scaled with kubernetes.
- **Jenkins**: CI/CD tool used for automated testing and continuous integration.
- **NodeJS and Express**: for some features like task management we will add create a separate NodeJS microservice due to its asynchronous nature and easy integration.
- **MongoDB**: Document oriented database in order to deal with some type of data
- **AI & Machine Learning**: AI email writing assitant based on industry
- **Single User platform**: User can have a place to manage their works, sync their files, folders trough our Cloud and AI tools
- **Spotify & Netflix**: We will integrate major music and movies streaming providers to allow some user to relax while they're working
- **Audiobooks & tools**: we will add a suggestion system that can showcase products based on user job & responsabilities
- **Social Networking App**: Users from different companies can connect with each other
- **FedEx & Freightos**: APIs for providing real-time shipping rates, tracking information, and freight suggestions, ensuring that customers get the best shipping options.

---

**This README.md provides comprehensive documentation for the Sailsmakr project, detailing its technology stack, setup process, and contribution guidelines.*

**Bytesprint Robotics LLC**
> **Navigating complexities for the Advancement of Human Species.*

