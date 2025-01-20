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

## Videos

### Agent Use Registration Process
![agent-use-registration-process](https://github.com/charlie180-code/sailsmakr/blob/main/screenshots/agent-use-registration-process.webm)
[View Code for Agent Use Registration Process](https://github.com/charlie180-code/sailsmakr/blob/main/apps/auth/controllers.py)

### Archiving System with Error Handling
![archiving-system-with-error](https://example.com/path-to-your-video/archiving-system-with-error.webm)
[View Code for Archiving System](https://github.com/your-repo/archiving-system-with-error)

### Basic Folder & Files Search
![basic-folder-files-search](https://example.com/path-to-your-video/basic-folder-files-search.webm)
[View Code for Basic Search](https://github.com/your-repo/basic-folder-files-search)

### Employee Infos Updating
![employee-infos-updating](https://example.com/path-to-your-video/employee-infos-updating.webm)
[View Code for Employee Infos Updating](https://github.com/your-repo/employee-infos-updating)

### Invoice File Generation
![invoice-file-generation](https://example.com/path-to-your-video/invoice-file-generation.webm)
[View Code for Invoice File Generation](https://github.com/your-repo/invoice-file-generation)

### Sailsmakr Integration - Login Page
![sailsmakr-integration-login-page](https://example.com/path-to-your-image/sailsmakr-integration-login-page.png)
[View Code for Login Page](https://github.com/your-repo/sailsmakr-integration-login-page)

### Sailsmakr Integration - Sales Statistics
![sailsmakr-integration-sales-statistics](https://example.com/path-to-your-image/sailsmakr-integration-sales-statistics.png)
[View Code for Sales Statistics](https://github.com/your-repo/sailsmakr-integration-sales-statistics)

### Student Enrollment Workflow (Sailsmakr)
![student-enrollment-workflow](https://example.com/path-to-your-video/student-enrollment-workflow.webm)
[View Code for Student Enrollment](https://github.com/your-repo/student-enrollment-workflow)

---

## Technologies

Sailsmakr leverages a variety of modern technologies to deliver a seamless experience:

- **Python (Flask)**: Backend framework for handling requests and API logic.
- **Code as Infrastructure**: Ensuring that infrastructure is defined and maintained programmatically using tools such as Terraform.
- **Firestore**: Cloud-based NoSQL database for storing user-generated data such as files and media.
- **Neon DB (PostgreSQL)**: High-performance, secure PostgreSQL database for structured data management.
- **VanillaJS & ES6**: JavaScript standard used for building interactive front-end functionalities.
- **JQuery**: Simplifies HTML DOM manipulation and event handling.
- **TailwindCSS**: Utility-first CSS framework used for building responsive and modern UI components.
- **Bootstrap MD from Creative TIM**: Material design-based UI kit for building beautiful, functional user interfaces.
- **Docker**: Containerization platform for packaging the application and its dependencies to run consistently across environments.
- **Jenkins**: CI/CD tool used for automated testing and continuous integration.
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
- **Node.js & npm**: For managing frontend dependencies and build tools.
- **Jenkins**: If you plan to set up continuous integration and testing locally.

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
      pip install -r requirements.txt
      ```

3. **Set Up the Frontend**:
    - Install npm dependencies:
      ```bash
      npm install
      ```

4. **Set Up Environment Variables**:
    - Create a `.env` file and add the necessary environment variables, such as API keys for OpenCage, FedEx, Freightos, and database credentials.

## Code Infrastructure

Sailsmakr's backend is powered by **Flask**, which handles API requests and core business logic. Infrastructure is managed programmatically with Terraform, ensuring consistency and scalability.

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

## Code Infrastructure

Sailsmakr's backend is powered by **Flask**, which handles API requests and core business logic. Infrastructure is managed programmatically with Terraform, ensuring consistency and scalability.

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

## APIs and Integrations

Sailsmakr integrates several third-party APIs to enhance functionality:

- **OpenCage**: Geolocation API that converts geographic coordinates into human-readable addresses, useful for location-based features.
- **FedEx & Freightos**: APIs for providing real-time shipping rates, tracking information, and freight suggestions, ensuring that customers get the best shipping options.

---

## Testing and CI/CD

Sailsmakr uses **Jenkins** for continuous integration and automated testing. This ensures that code pushed to the repository is automatically tested, and builds are generated for deployment.

---

## License

Sailsmakr Softwares is the sole owner of all source code. No code may be redistributed or reproduced without explicit permission from Sailsmakr Softwares.

---

**This README.md provides comprehensive documentation for the Sailsmakr project, detailing its technology stack, setup process, and contribution guidelines.*

